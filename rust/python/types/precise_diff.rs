use pyo3::prelude::*;

#[pyclass(module = "_pendulum")]
pub struct PreciseDiff {
    #[pyo3(get, set)]
    pub years: i32,
    #[pyo3(get, set)]
    pub months: i32,
    #[pyo3(get, set)]
    pub days: i32,
    #[pyo3(get, set)]
    pub hours: i32,
    #[pyo3(get, set)]
    pub minutes: i32,
    #[pyo3(get, set)]
    pub seconds: i32,
    #[pyo3(get, set)]
    pub microseconds: i32,
    #[pyo3(get, set)]
    pub total_days: i32,
}

#[pymethods]
impl PreciseDiff {
    #[new]
    #[pyo3(signature = (years=0, months=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0, total_days=0))]
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        years: Option<i32>,
        months: Option<i32>,
        days: Option<i32>,
        hours: Option<i32>,
        minutes: Option<i32>,
        seconds: Option<i32>,
        microseconds: Option<i32>,
        total_days: Option<i32>,
    ) -> Self {
        Self {
            years: years.unwrap_or(0),
            months: months.unwrap_or(0),
            days: days.unwrap_or(0),
            hours: hours.unwrap_or(0),
            minutes: minutes.unwrap_or(0),
            seconds: seconds.unwrap_or(0),
            microseconds: microseconds.unwrap_or(0),
            total_days: total_days.unwrap_or(0),
        }
    }

    fn __repr__(&self) -> String {
        format!("PreciseDiff(years={}, months={}, days={}, hours={}, minutes={}, seconds={}, microseconds={}, total_days={})", self.years, self.months, self.days, self.hours, self.minutes, self.seconds, self.microseconds, self.total_days)
    }
}
