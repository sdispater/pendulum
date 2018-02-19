import os
import pytzdata

from collections import namedtuple
from struct import unpack
from typing import List, Dict

from pytzdata.exceptions import TimezoneNotFound

from .exceptions import InvalidZoneinfoFile, InvalidTimezone
from .timezone import Timezone
from .transition import Transition
from .posix_timezone import posix_spec, PosixTimezone
from .transition_type import TransitionType


_offset = namedtuple('offset', 'utc_total_offset is_dst abbr_idx')

header = namedtuple(
    'header',
    'version '
    'utclocals '
    'stdwalls '
    'leaps '
    'transitions '
    'types '
    'abbr_size'
)


class Reader:
    """
    Reads compiled zoneinfo TZif (\0, 2 or 3) files.
    """

    def read_for(self, timezone: str) -> Timezone:
        """
        Read the zoneinfo structure for a given timezone name.

        :param timezone: The timezone.
        """
        try:
            file_path = pytzdata.tz_path(timezone)
        except TimezoneNotFound:
            raise InvalidTimezone(timezone)

        return self.read(file_path)

    def read(self, file_path: str) -> Timezone:
        """
        Read a zoneinfo structure from the given path.

        :param file_path: The path of a zoneinfo file.
        """
        if not os.path.exists(file_path):
            raise InvalidZoneinfoFile('The tzinfo file does not exist')

        with open(file_path, 'rb') as fd:
            return self._parse(fd)

    def _check_read(self, fd, nbytes) -> bytes:
        """
        Reads the given number of bytes from the given file
        and checks that the correct number of bytes could be read.
        """
        result = fd.read(nbytes)

        if not result or len(result) != nbytes:
            raise InvalidZoneinfoFile(
                f'Expected {nbytes} bytes reading {fd.name}, '
                f'but got {len(result) if result else 0}'
            )

        return result

    def _parse(self, fd) -> Timezone:
        """
        Parse a zoneinfo file.
        """
        hdr = self._parse_header(fd)

        if hdr.version in (2, 3):
            # We're skipping the entire v1 file since
            # at least the same data will be found in TZFile 2.
            fd.seek(
                hdr.transitions * 5
                + hdr.types * 6
                + hdr.abbr_size
                + hdr.leaps * 4
                + hdr.stdwalls
                + hdr.utclocals,
                1
            )

            # Parse the second header
            hdr = self._parse_header(fd)

            if hdr.version != 2 and hdr.version != 3:
                raise InvalidZoneinfoFile(
                    f'Header versions mismatch for file {fd.name}'
                )

            # Parse the v2 data
            trans = self._parse_trans_64(fd, hdr.transitions)
            type_idx = self._parse_type_idx(fd, hdr.transitions)
            types = self._parse_types(fd, hdr.types)
            abbrs = self._parse_abbrs(fd, hdr.abbr_size, types)

            fd.seek(
                hdr.leaps * 8
                + hdr.stdwalls
                + hdr.utclocals,
                1
            )

            # TODO: posix tz
            trule = self._parse_posix_tz(fd)
        else:
            # TZFile v1
            trans = self._parse_trans_32(fd, hdr.transitions)
            type_idx = self._parse_type_idx(fd, hdr.transitions)
            types = self._parse_types(fd, hdr.types)
            abbrs = self._parse_abbrs(fd, hdr.abbr_size, types)
            trule = None

        types = [
            TransitionType(off, is_dst, abbrs[abbr])
            for off, is_dst, abbr in types
        ]

        transitions = []
        previous = None
        for trans, idx in zip(trans, type_idx):
            transition = Transition(trans, types[idx], previous)
            transitions.append(transition)

            previous = transition

        if not transitions:
            transitions.append(
                Transition(0, types[0], None)
            )

        return Timezone(transitions, posix_rule=trule)

    def _parse_header(self, fd) -> header:
        buff = self._check_read(fd, 44)

        if buff[:4] != b'TZif':
            raise InvalidZoneinfoFile(
                f'The file "{fd.name}" has an invalid header.'
            )

        version = {
            0x00: 1,
            0x32: 2,
            0x33: 3
        }.get(buff[4])

        if version is None:
            raise InvalidZoneinfoFile(
                f'The file "{fd.name}" has an invalid version.'
            )

        hdr = header(
            version,
            *unpack('>6l', buff[20:44])
        )

        return hdr

    def _parse_trans_64(self, fd, n: int) -> List[int]:
        trans = []
        for _ in range(n):
            buff = self._check_read(fd, 8)
            trans.append(unpack('>q', buff)[0])

        return trans

    def _parse_trans_32(self, fd, n: int) -> List[int]:
        trans = []
        for _ in range(n):
            buff = self._check_read(fd, 4)
            trans.append(unpack('>i', buff)[0])

        return trans

    def _parse_type_idx(self, fd, n: int) -> List[int]:
        buff = self._check_read(fd, n)

        return list(unpack(f'{n}B', buff))

    def _parse_types(self, fd, n: int) -> List[tuple]:
        types = []

        for _ in range(n):
            buff = self._check_read(fd, 6)
            offset = unpack('>l', buff[:4])[0]
            is_dst = buff[4] == 1
            types.append((offset, is_dst, buff[5]))

        return types

    def _parse_abbrs(self, fd, n: int, types: List[tuple]) -> Dict[int, str]:
        abbrs = {}
        buff = self._check_read(fd, n)

        for *_, idx in types:
            if idx not in abbrs:
                abbr = buff[idx:buff.find(b'\0', idx)].decode('utf-8')
                abbrs[idx] = abbr

        return abbrs

    def _parse_posix_tz(self, fd) -> PosixTimezone:
        s = fd.read().decode('utf-8')

        if not s.startswith('\n') or not s.endswith('\n'):
            raise InvalidZoneinfoFile(
                f'Invalid posix rule in file "{fd.name}"'
            )

        s = s.strip()

        return posix_spec(s)


