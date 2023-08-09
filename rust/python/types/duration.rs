use pyo3::prelude::*;

#[pyclass(module = "_pendulum")]
pub struct Duration {
    #[pyo3(get, set)]
    pub years: u32,
    #[pyo3(get, set)]
    pub months: u32,
    #[pyo3(get, set)]
    pub weeks: u32,
    #[pyo3(get, set)]
    pub days: u32,
    #[pyo3(get, set)]
    pub hours: u32,
    #[pyo3(get, set)]
    pub minutes: u32,
    #[pyo3(get, set)]
    pub seconds: u32,
    #[pyo3(get, set)]
    pub microseconds: u32,
}

#[pymethods]
impl Duration {
    #[new]
    #[pyo3(signature = (years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0))]
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        years: Option<u32>,
        months: Option<u32>,
        weeks: Option<u32>,
        days: Option<u32>,
        hours: Option<u32>,
        minutes: Option<u32>,
        seconds: Option<u32>,
        microseconds: Option<u32>,
    ) -> Self {
        Self {
            years: years.unwrap_or(0),
            months: months.unwrap_or(0),
            weeks: weeks.unwrap_or(0),
            days: days.unwrap_or(0),
            hours: hours.unwrap_or(0),
            minutes: minutes.unwrap_or(0),
            seconds: seconds.unwrap_or(0),
            microseconds: microseconds.unwrap_or(0),
        }
    }

    #[getter]
    fn remaining_days(&self) -> PyResult<u32> {
        Ok(self.days)
    }

    #[getter]
    fn remaining_seconds(&self) -> PyResult<u32> {
        Ok(self.seconds)
    }
}
