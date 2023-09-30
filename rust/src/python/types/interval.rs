use pyo3::prelude::*;

use pyo3::types::PyDelta;

#[pyclass(extends=PyDelta)]
#[derive(Default)]
pub struct Interval {
    pub days: i32,
    pub seconds: i32,
    pub microseconds: i32,
}

#[pymethods]
impl Interval {
    #[new]
    #[pyo3(signature = (days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))]
    pub fn new(
        py: Python,
        days: Option<i32>,
        seconds: Option<i32>,
        microseconds: Option<i32>,
        milliseconds: Option<i32>,
        minutes: Option<i32>,
        hours: Option<i32>,
        weeks: Option<i32>,
    ) -> PyResult<Self> {
        println!("{} days", 31);
        PyDelta::new(
            py,
            days.unwrap_or(0),
            seconds.unwrap_or(0),
            microseconds.unwrap_or(0),
            true,
        )?;

        let f = Ok(Self {
            days: days.unwrap_or(0),
            seconds: seconds.unwrap_or(0),
            microseconds: microseconds.unwrap_or(0),
        });

        println!("{} days", 31);

        f
    }
}
