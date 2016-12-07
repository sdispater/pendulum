# -*- coding: utf-8 -*-


class TransitionType(object):

    def __init__(self, utc_offset, is_dst, abbrev):
        self.utc_offset = utc_offset
        self.is_dst = is_dst
        self.abbrev = abbrev

    def __repr__(self):
        return '<TransitionType [{}, {}, {}]>'.format(
            self.utc_offset,
            self.is_dst,
            self.abbrev
        )
