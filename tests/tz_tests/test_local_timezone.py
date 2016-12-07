# -*- coding: utf-8 -*-

import os
from .. import AbstractTestCase
from pendulum.tz import LocalTimezone


class LocalTimezoneTest(AbstractTestCase):

    def test_unix_symlink(self):
        self.skip_if_windows()

        # A ZONE setting in the target path of a symbolic linked localtime, f ex systemd distributions
        local_path = os.path.join(os.path.split(__file__)[0], '..')
        tz = LocalTimezone.get_tz_name_for_unix(
            _root=os.path.join(local_path, 'fixtures', 'tz', 'symlink')
        )

        self.assertEqual(tz.name, 'Europe/Paris')
