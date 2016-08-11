# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import re

from .timezone import Timezone
from .parser import Parser


class LocalTimezone(object):

    _cache = None

    @classmethod
    def get(cls, force=False):
        if cls._cache is None or force:
            name = cls.get_local_tz_name()
            if isinstance(name, Timezone):
                cls._cache = name
            else:
                cls._cache = Timezone.load(cls.get_local_tz_name())

        return cls._cache

    @classmethod
    def get_local_tz_name(cls):
        if sys.platform == 'win32':
            os = 'windows'
        elif 'darwin' in sys.platform:
            os = 'darwin'
        else:
            os = 'unix'

        return getattr(cls, 'get_tz_name_for_{}'.format(os))()

    @classmethod
    def get_tz_name_for_darwin(cls):
        tzname = None
        try:
            output = subprocess.check_output(
                "systemsetup -gettimezone",
                stderr=subprocess.STDOUT
            )

            tzname = output.replace(b'Time Zone: ', b'').strip()
        except OSError:
            pass

        if not tzname:
            # link will be something like /usr/share/zoneinfo/America/Los_Angeles.
            link = os.readlink("/etc/localtime")
            tzname = link[link.rfind("zoneinfo/") + 9:]

        return tzname

    @classmethod
    def get_tz_name_for_windows(cls):
        from tzlocal.win32 import get_localzone_name

        return get_localzone_name()

    @classmethod
    def get_tz_name_for_unix(cls):
        tzenv = os.environ.get('TZ')
        if tzenv:
            try:
                return _tz_from_env(tzenv)
            except ValueError:
                pass

        _root = '/'

        # Now look for distribution specific configuration files
        # that contain the timezone name.
        tzpath = os.path.join(_root, 'etc/timezone')
        if os.path.exists(tzpath):
            with open(tzpath, 'rb') as tzfile:
                data = tzfile.read()

                # Issue #3 was that /etc/timezone was a zoneinfo file.
                # That's a misconfiguration, but we need to handle it gracefully:
                if data[:5] != 'TZif2':
                    etctz = data.strip().decode()
                    # Get rid of host definitions and comments:
                    if ' ' in etctz:
                        etctz, dummy = etctz.split(' ', 1)
                    if '#' in etctz:
                        etctz, dummy = etctz.split('#', 1)

                    return etctz.replace(' ', '_')

        # CentOS has a ZONE setting in /etc/sysconfig/clock,
        # OpenSUSE has a TIMEZONE setting in /etc/sysconfig/clock and
        # Gentoo has a TIMEZONE setting in /etc/conf.d/clock
        # We look through these files for a timezone:

        zone_re = re.compile('\s*ZONE\s*=\s*\"')
        timezone_re = re.compile('\s*TIMEZONE\s*=\s*\"')
        end_re = re.compile('\"')

        for filename in ('etc/sysconfig/clock', 'etc/conf.d/clock'):
            tzpath = os.path.join(_root, filename)
            if not os.path.exists(tzpath):
                continue
            with open(tzpath, 'rt') as tzfile:
                data = tzfile.readlines()

            for line in data:
                # Look for the ZONE= setting.
                match = zone_re.match(line)
                if match is None:
                    # No ZONE= setting. Look for the TIMEZONE= setting.
                    match = timezone_re.match(line)
                if match is not None:
                    # Some setting existed
                    line = line[match.end():]
                    etctz = line[:end_re.search(line).start()]

                    # We found a timezone
                    return etctz.replace(' ', '_')

        # systemd distributions use symlinks that include the zone name,
        # see manpage of localtime(5) and timedatectl(1)
        tzpath = os.path.join(_root, 'etc/localtime')
        if os.path.exists(tzpath) and os.path.islink(tzpath):
            tzpath = os.path.realpath(tzpath)
            start = tzpath.find("/") + 1
            while start is not 0:
                tzpath = tzpath[start:]
                try:
                    return Timezone.load(tzpath)
                except ValueError:
                    pass
                start = tzpath.find("/") + 1

        # No explicit setting existed. Use localtime
        for filename in ('etc/localtime', 'usr/local/etc/localtime'):
            tzpath = os.path.join(_root, filename)

            if not os.path.exists(tzpath):
                continue
            with open(tzpath, 'rb') as tzfile:
                return Timezone('', *Parser.parse(tzfile))

        raise RuntimeError('Can not find any timezone configuration')

def _tz_from_env(tzenv):
    if tzenv[0] == ':':
        tzenv = tzenv[1:]

    # TZ specifies a file
    if os.path.exists(tzenv):
        return Timezone('', *Parser.parse(tzenv))

    # TZ specifies a zoneinfo zone.
    try:
        tz = Timezone.load(tzenv)

        return tz
    except ValueError:
        raise
