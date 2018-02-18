import sys
import os
import re

from contextlib import contextmanager
from typing import Union

from .timezone import Timezone, TimezoneFile


_mock_local_timezone = None
_local_timezone = None


def get_local_timezone() -> Timezone:
    global _local_timezone

    if _mock_local_timezone is not None:
        return _mock_local_timezone

    if _local_timezone is None:
        tz = _get_system_timezone()

        _local_timezone = tz

    return _local_timezone


def set_local_timezone(mock: Union[str, Timezone, None] = None) -> None:
    global _mock_local_timezone

    _mock_local_timezone = mock


@contextmanager
def test_local_timezone(mock: Timezone) -> None:
    set_local_timezone(mock)

    yield

    set_local_timezone()


def _get_system_timezone() -> Timezone:
    if sys.platform == 'win32':
        return _get_windows_timezone()
    elif 'darwin' in sys.platform:
        return _get_darwin_timezone()

    return _get_unix_timezone()


def _get_windows_timezone() -> Timezone:
    from tzlocal.win32 import get_localzone_name

    return Timezone(get_localzone_name())


def _get_darwin_timezone() -> Timezone:
    # link will be something like /usr/share/zoneinfo/America/Los_Angeles.
    link = os.readlink("/etc/localtime")
    tzname = link[link.rfind("zoneinfo/") + 9:]

    return Timezone(tzname)


def _get_unix_timezone(_root='/') -> Timezone:
    tzenv = os.environ.get('TZ')
    if tzenv:
        try:
            return _tz_from_env(tzenv)
        except ValueError:
            pass

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

                return Timezone(etctz.replace(' ', '_'))

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
                return Timezone(etctz.replace(' ', '_'))

    # systemd distributions use symlinks that include the zone name,
    # see manpage of localtime(5) and timedatectl(1)
    tzpath = os.path.join(_root, 'etc/localtime')
    if os.path.exists(tzpath) and os.path.islink(tzpath):
        tzpath = os.path.realpath(tzpath)
        parts = tzpath.split('/')[-2:]
        while parts:
            tzpath = '/'.join(parts)
            try:
                return Timezone(tzpath)
            except (ValueError, IOError, OSError):
                pass

            parts.pop(0)

    # No explicit setting existed. Use localtime
    for filename in ('etc/localtime', 'usr/local/etc/localtime'):
        tzpath = os.path.join(_root, filename)

        if not os.path.exists(tzpath):
            continue

        return TimezoneFile(tzpath)

    raise RuntimeError('Unable to find any timezone configuration')


def _tz_from_env(tzenv: str) -> Timezone:
    if tzenv[0] == ':':
        tzenv = tzenv[1:]

    # TZ specifies a file
    if os.path.exists(tzenv):
        return TimezoneFile(tzenv)

    # TZ specifies a zoneinfo zone.
    try:
        return Timezone(tzenv)
    except ValueError:
        raise
