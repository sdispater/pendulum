# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from struct import unpack, calcsize
from pytzdata import tz_file
from pytzdata.exceptions import TimezoneNotFound

from .. import _compat
from ..helpers import local_time
from .transition import Transition
from .transition_type import TransitionType


def _byte_string(s):
    """Cast a string or byte string to an ASCII byte string."""
    return s.encode('US-ASCII')

_NULL = _byte_string('\0')


def _std_string(s):
    """Cast a string or byte string to an ASCII string."""
    return str(s.decode('US-ASCII'))


class Loader(object):

    @classmethod
    def load(cls, name):
        name = _compat.decode(name)
        try:
            with tz_file(name) as f:
                return cls._load(f)
        except TimezoneNotFound:
            raise ValueError('Unknown timezone [{}]'.format(name))

    @classmethod
    def load_from_file(cls, filepath):
        try:
            with open(filepath, 'rb') as f:
                return cls._load(f)
        except _compat.FileNotFoundError:
            raise ValueError('Unable to load file [{}]'.format(filepath))

    @classmethod
    def _load(cls, fp):
        head_fmt = '>4s c 15x 6l'
        head_size = calcsize(head_fmt)
        (magic, fmt, ttisgmtcnt, ttisstdcnt, leapcnt, timecnt,
         typecnt, charcnt) = unpack(head_fmt, fp.read(head_size))

        # Make sure it is a tzfile(5) file
        assert magic == _byte_string('TZif'), 'Got magic %s' % repr(magic)

        # Read out the transition times,
        # localtime indices and ttinfo structures.
        data_fmt = '>%(timecnt)dl %(timecnt)dB %(ttinfo)s %(charcnt)ds' % dict(
            timecnt=timecnt, ttinfo='lBB' * typecnt, charcnt=charcnt)
        data_size = calcsize(data_fmt)
        data = unpack(data_fmt, fp.read(data_size))

        # make sure we unpacked the right number of values
        assert len(data) == 2 * timecnt + 3 * typecnt + 1
        transition_times = tuple(trans for trans in data[:timecnt])
        lindexes = tuple(data[timecnt:2 * timecnt])
        ttinfo_raw = data[2 * timecnt:-1]
        tznames_raw = data[-1]
        del data

        # Process ttinfo into separate structs
        transition_types = tuple()
        tznames = {}
        i = 0
        while i < len(ttinfo_raw):
            # have we looked up this timezone name yet?
            tzname_offset = ttinfo_raw[i + 2]
            if tzname_offset not in tznames:
                nul = tznames_raw.find(_NULL, tzname_offset)
                if nul < 0:
                    nul = len(tznames_raw)
                tznames[tzname_offset] = _std_string(
                    tznames_raw[tzname_offset:nul])
            transition_types += (
                TransitionType(
                    ttinfo_raw[i], bool(ttinfo_raw[i + 1]),
                    tznames[tzname_offset]
                ),
            )
            i += 3

        # Now build the timezone object
        transitions = tuple()
        tzinfos = tuple()

        if not transition_times:
            if transition_types:
                transitions += (Transition(0, 0, datetime(1970, 1, 1), datetime(1970, 1, 1), 0),)
                tzinfos += ((
                    transition_types[0].utc_offset,
                    transition_types[0].is_dst,
                    None,
                    transition_types[0].abbrev
                ),)
        else:
            # calculate transition info
            tr = None
            for i in range(len(transition_times)):
                # We retrieve transition types indexes
                transition_type_index = lindexes[i]

                if i == 0:
                    pre_transition_type_index = lindexes[i]
                else:
                    pre_transition_type_index = lindexes[i - 1]

                pre_transition_type = transition_types[pre_transition_type_index]
                transition_type = transition_types[transition_type_index]

                # We calculate local times based on the transition types
                # we retrieved
                pre_time = datetime(
                    *local_time(transition_times[i],
                                pre_transition_type.utc_offset,
                                0)
                )
                time = datetime(
                    *local_time(transition_times[i],
                                transition_type.utc_offset,
                                0)
                )

                # We build the tzinfo information as tuples
                # and retrieve their index to store them
                # in the transition.
                # If they do not already exist we add them
                # to the tzinfos tuple to look them up later
                # if necessary.
                dst = tr.time - tr.pre_time if tr else None
                pre_tzinfo = (
                    pre_transition_type.utc_offset,
                    pre_transition_type.is_dst,
                    dst if dst != timedelta() else None,
                    pre_transition_type.abbrev
                )

                try:
                    pre_tzinfo_index = tzinfos.index(pre_tzinfo)
                except ValueError:
                    tzinfos += (pre_tzinfo,)

                    pre_tzinfo_index = len(tzinfos) - 1

                dst = time - pre_time
                tzinfo = (
                    transition_type.utc_offset,
                    transition_type.is_dst,
                    dst if dst != timedelta() else None,
                    transition_type.abbrev
                )

                try:
                    tzinfo_index = tzinfos.index(tzinfo)
                except ValueError:
                    tzinfos += (tzinfo,)

                    tzinfo_index = len(tzinfos) - 1

                # Finally, we build the transition instance.
                tr = Transition(
                    transition_times[i],
                    tzinfo_index,
                    pre_time,
                    time,
                    pre_tzinfo_index
                )

                transitions += (tr,)

        # Determine the before-first-transition type
        default_tzinfo_index = 0
        if transitions:
            index = 0
            if tzinfos[0][2]:
                index = transitions[0].tzinfo_index
                while index != 0 and tzinfos[index][2]:
                    index -= 1

            while index != len(tzinfos) and tzinfos[index][2]:
                index += 1

            if index != len(transitions):
                default_tzinfo_index = index

        return (
            transitions,
            tzinfos,
            default_tzinfo_index,
            tuple(map(lambda tr: tr.utc_time, transitions))
        )
