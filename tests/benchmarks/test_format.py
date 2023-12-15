from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pytest_benchmark.fixture import (  # type: ignore[import-untyped]
        BenchmarkFixture,
    )

import pendulum

from pendulum.formatting.formatter import Formatter


def test_format(benchmark: BenchmarkFixture) -> None:
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)

    @benchmark  # type: ignore[misc]
    def benchmark_() -> None:
        f.format(d, "S")
        f.format(d, "SS")
        f.format(d, "SSS")
        f.format(d, "SSSS")
        f.format(d, "SSSSS")
        f.format(d, "SSSSSS")

        f.format(d, "zz")
        f.format(d, "z")
        f.format(d, "ZZ")
        f.format(d, "Z")

        f.format(d, "LT")
        f.format(d, "LTS")
        f.format(d, "L")
        f.format(d, "LL")
        f.format(d, "LLL")
        f.format(d, "LLLL")
