# -*- coding: utf-8 -*-

from pendulum import Period

from .. import (AbstractTestCase, eleventh, fifth, first, fourteenth, fourth,
                ninth, second, seventh, sixth, tenth, third, thirteenth,
                twelfth)


class ExcludeTestcase(AbstractTestCase):

    def test_exclude_from(self):
        first_period = Period(
            start=third,
            end=sixth
        )
        second_period = Period(
            start=ninth,
            end=twelfth
        )

        def assertExcluded(start, end, expected=None):
            if expected is None:
                expected = [
                    first_period,
                    second_period
                ]

            excluded = Period(
                start=start,
                end=end
            ).exclude_from(
                first_period,
                second_period
            )
            self.assertEqual(
                expected,
                excluded
            )

        starts = [
            first,
            first_period.start
        ]

        for start in starts:

            if start == first:
                # Before/start first period - before first period
                assertExcluded(
                    expected=[
                        first_period,
                        second_period
                    ],
                    start=start,
                    end=second
                )

                # Before/start first period - start first period
                assertExcluded(
                    expected=[
                        first_period,
                        second_period
                    ],
                    start=start,
                    end=first_period.start
                )

            # Before/start first period - in first period
            assertExcluded(
                expected=[
                    # 4 - 6
                    Period(
                        start=fourth,
                        end=sixth
                    ),
                    # 9 - 12
                    second_period
                ],
                start=start,
                end=fourth
            )

            # Before/start first period - end first period
            assertExcluded(
                expected=[
                    second_period
                ],
                start=start,
                end=first_period.end
            )

            # Before/start first period - after first period
            assertExcluded(
                expected=[
                    second_period
                ],
                start=start,
                end=seventh
            )

            # Before/start first period - start second period
            assertExcluded(
                expected=[
                    second_period
                ],
                start=start,
                end=second_period.start
            )

            # Before/start first period - in second period
            assertExcluded(
                expected=[
                    Period(
                        start=tenth,
                        end=second_period.end
                    )
                ],
                start=start,
                end=tenth
            )

            # Before/start first period - end second period
            assertExcluded(
                expected=[],
                start=start,
                end=second_period.end
            )

            # Before/start first period - after second period
            assertExcluded(
                expected=[],
                start=start,
                end=thirteenth
            )

        # In first period - in first period
        assertExcluded(
            expected=[
                # 3 - 4
                Period(
                    start=first_period.start,
                    end=fourth
                ),
                # 5 - 6
                Period(
                    start=fifth,
                    end=first_period.end
                ),
                # 9 - 12
                second_period
            ],
            start=fourth,
            end=fifth
        )

        # In first period - end first period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                ),
                second_period
            ],
            start=fourth,
            end=first_period.end
        )

        # In first period - after first period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                ),
                second_period
            ],
            start=fourth,
            end=seventh
        )

        # In first period - start second period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                ),
                second_period
            ],
            start=fourth,
            end=second_period.start
        )

        # In first period - in second period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                ),
                Period(
                    start=tenth,
                    end=second_period.end
                )
            ],
            start=fourth,
            end=tenth
        )

        # In first period - end second period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                )
            ],
            start=fourth,
            end=second_period.end
        )

        # In first period - after second period
        assertExcluded(
            expected=[
                Period(
                    start=first_period.start,
                    end=fourth
                )
            ],
            start=fourth,
            end=thirteenth
        )

        # End first period - after first period
        assertExcluded(
            expected=[
                first_period,
                second_period
            ],
            start=first_period.end,
            end=seventh
        )

        # End first period - start second period
        assertExcluded(
            expected=[
                first_period,
                second_period
            ],
            start=first_period.end,
            end=second_period.start
        )

        # After first period - start second period
        assertExcluded(
            expected=[
                first_period,
                second_period
            ],
            start=seventh,
            end=second_period.start
        )

        mids = [
            first_period.end, seventh,
            second_period.start
        ]

        for mid in mids:
            # End/after first periods or start second period - in second period
            assertExcluded(
                expected=[
                    first_period,
                    Period(
                        start=tenth,
                        end=second_period.end
                    )
                ],
                start=mid,
                end=tenth
            )

            # End/after first periods or start second period - end second period
            assertExcluded(
                expected=[
                    first_period
                ],
                start=mid,
                end=second_period.end
            )

            # End/after first periods or start second period - after second period
            assertExcluded(
                expected=[
                    first_period
                ],
                start=mid,
                end=thirteenth
            )

        # In second period - in second period
        assertExcluded(
            expected=[
                first_period,
                Period(
                    start=second_period.start,
                    end=tenth
                ),
                Period(
                    start=eleventh,
                    end=second_period.end
                )
            ],
            start=tenth,
            end=eleventh
        )

        # In second period - end second period
        assertExcluded(
            expected=[
                first_period,
                Period(
                    start=second_period.start,
                    end=tenth
                )
            ],
            start=tenth,
            end=second_period.end
        )

        # In second period - after second period
        assertExcluded(
            expected=[
                first_period,
                Period(
                    start=second_period.start,
                    end=tenth
                )
            ],
            start=tenth,
            end=thirteenth
        )

        ends = [
            second_period.end,
            thirteenth
        ]

        for end in ends:
            # End second period - after second period
            assertExcluded(
                expected=[
                    first_period,
                    second_period
                ],
                start=end,
                end=fourteenth
            )
