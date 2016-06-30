# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class FoTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'fo'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('1 sekund síðan', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('2 sekundir síðan', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('1 minutt síðan', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('2 minuttir síðan', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('1 tími síðan', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('2 tímar síðan', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('1 dag síðan', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('2 dagar síðan', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('1 vika síðan', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('2 vikur síðan', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('1 mánaður síðan', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('2 mánaðir síðan', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('1 ár síðan', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('2 ár síðan', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('um 1 sekund', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 sekund aftaná', d.diff_for_humans(d2))
            self.assertEqual('1 sekund áðrenn', d2.diff_for_humans(d))

            self.assertEqual('1 sekund', d.diff_for_humans(d2, True))
            self.assertEqual('2 sekundir', d2.diff_for_humans(d.add_second(), True))
