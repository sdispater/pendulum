# -*- coding: utf-8 -*-

import inspect
import os
import pytz

from datetime import datetime
from struct import unpack, calcsize

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

    path = os.path.join(os.path.dirname(inspect.getfile(pytz)), 'zoneinfo')

    @classmethod
    def load(cls, name):
        name = _compat.decode(name)
        try:
            with pytz.open_resource(name) as f:
                return cls._load(f)
        except _compat.FileNotFoundError:
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
        if len(transition_times) == 0:
            transitions = tuple()
        else:
            # calculate transition info
            transitions = tuple()
            for i in range(len(transition_times)):
                transition_type_index = lindexes[i]

                if i == 0:
                    pre_transition_type_index = lindexes[i]
                else:
                    pre_transition_type_index = lindexes[i - 1]

                pre_time = datetime(
                    *local_time(transition_times[i],
                                transition_types[pre_transition_type_index].utc_offset)
                )
                time = datetime(
                    *local_time(transition_times[i],
                                transition_types[transition_type_index].utc_offset)
                )
                tr = Transition(
                    transition_times[i],
                    transition_type_index,
                    pre_time,
                    time,
                    pre_transition_type_index
                )

                transitions += (tr,)

        # Determine the before-first-transition type
        default_transition_type_index = 0
        if transitions:
            index = 0
            if transition_types[0].is_dst:
                index = transition_types.index(transitions[0].transition_type)
                while index != 0 and transition_types[index].is_dst:
                    index -= 1

            while index != len(transition_types) and transition_types[index].is_dst:
                index += 1

            if index != len(transitions):
                default_transition_type_index = index

        return (
            transitions,
            transition_types,
            default_transition_type_index,
            tuple(map(lambda tr: tr.utc_time, transitions))
        )
