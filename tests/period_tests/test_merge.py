# -*- coding: utf-8 -*-

from pendulum import Period

from .. import (AbstractTestCase, eighth, fifth, first, fourteenth, fourth,
                ninth, second, seventh, sixth, tenth, third, thirteenth,
                twelfth)


class MergeTestcase(AbstractTestCase):

    def test_merge(self):
        first_period = Period(
            start=third,
            end=sixth
        )
        second_period = Period(
            start=ninth,
            end=twelfth
        )

        def assertMerged(start, end, expected=None):
            if expected is None:
                expected = [
                    first_period,
                    second_period
                ]

            merged = Period(
                start=start,
                end=end
            ).merge(
                first_period,
                second_period
            )

            self.assertEqual(
                expected,
                merged
            )

        # If merged period is before other ones, nothing should be changed.
        assertMerged(
            expected=[
                Period(
                    first,
                    second
                ),
                first_period,
                second_period
            ],
            start=first,
            end=second
        )

        # Assert that edging periods are merged into one
        assertMerged(
            expected=[
                Period(
                    first,
                    first_period.end
                ),
                second_period
            ],
            start=first,
            end=first_period.start
        )

        starts = [
            first,
            first_period.start
        ]

        for start in starts:
            # Before/start first period - in first period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=first_period.end
                    ),
                    second_period
                ],
                start=start,
                end=fourth
            )

            # Before/start first period - end first period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=first_period.end
                    ),
                    second_period
                ],
                start=start,
                end=first_period.end
            )

            # Before/start first period - after first period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=seventh),
                    second_period
                ],
                start=start,
                end=seventh
            )
            # Before/start first period - start second period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=second_period.end
                    )
                ],
                start=start,
                end=second_period.start
            )

            # Before/start first period - in second period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=second_period.end
                    )
                ],
                start=start,
                end=tenth
            )

            # Before/start first period - end second period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=second_period.end
                    )
                ],
                start=start,
                end=second_period.end
            )

            # Before/start first period - after second period
            assertMerged(
                expected=[
                    Period(
                        start=start,
                        end=thirteenth
                    )
                ],
                start=start,
                end=thirteenth
            )

        # In first period - in first period
        assertMerged(
            expected=None,
            start=fourth,
            end=fifth
        )

        # In first period - end first period
        assertMerged(
            expected=None,
            start=fourth,
            end=first_period.end
        )

        # In first period - after first period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=seventh
                ),
                second_period
            ],
            start=fourth,
            end=seventh
        )

        # In first period - start second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=fourth,
            end=second_period.start
        )

        # In first period - in second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=fourth,
            end=tenth
        )

        # In first period - end second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=fourth,
            end=second_period.end
        )

        # In first period - after second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=thirteenth
                )
            ],
            start=fourth,
            end=thirteenth
        )

        # End first period - after first period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=seventh
                ),
                second_period
            ],
            start=first_period.end,
            end=seventh
        )

        # End first period - start second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=first_period.end,
            end=second_period.start
        )

        # End first period - in second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=first_period.end,
            end=tenth
        )

        # End first period - end second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=second_period.end
                )
            ],
            start=first_period.end,
            end=second_period.end
        )

        # End first period - after second period
        assertMerged(
            expected=[
                Period(
                    start=first_period.start,
                    end=thirteenth
                )
            ],
            start=first_period.end,
            end=thirteenth
        )

        # After first period - after first period
        assertMerged(
            expected=[
                first_period,
                Period(
                    start=seventh,
                    end=eighth
                ),
                second_period
            ],
            start=seventh,
            end=eighth
        )

        # After first period - start second period
        assertMerged(
            expected=[
                first_period,
                Period(
                    start=seventh,
                    end=second_period.end
                )
            ],
            start=seventh,
            end=second_period.start
        )

        # After first period - in second period
        assertMerged(
            expected=[
                first_period,
                Period(
                    start=seventh,
                    end=second_period.end
                )
            ],
            start=seventh,
            end=tenth
        )

        # After first period - end second period
        assertMerged(
            expected=[
                first_period,
                Period(
                    start=seventh,
                    end=second_period.end
                )
            ],
            start=seventh,
            end=second_period.end
        )

        # After first period - after second period
        assertMerged(
            expected=[
                first_period,
                Period(
                    start=seventh,
                    end=thirteenth
                )
            ],
            start=seventh,
            end=thirteenth
        )

        second_period_mergings = [
            second_period.start,
            tenth,
            second_period.end
        ]
        for merge in second_period_mergings:
            if merge != second_period.start:
                assertMerged(
                    expected=None,
                    start=merge,
                    end=tenth
                )
            else:
                assertMerged(
                    expected=None,
                    start=merge,
                    end=second_period.end
                )

            assertMerged(
                expected=[
                    first_period,
                    Period(
                        start=second_period.start,
                        end=thirteenth
                    )
                ],
                start=merge,
                end=thirteenth
            )

        assertMerged(
            expected=[
                first_period,
                second_period,
                Period(
                    thirteenth,
                    fourteenth
                )
            ],
            start=thirteenth,
            end=fourteenth
        )
