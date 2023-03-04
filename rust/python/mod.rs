use pyo3::prelude::*;

mod helpers;
mod parsing;
mod types;

use helpers::{is_leap, is_long_year, local_time, week_day};
use parsing::parse_iso8601;

#[pymodule]
pub fn _pendulum(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_leap, m)?)?;
    m.add_function(wrap_pyfunction!(is_long_year, m)?)?;
    m.add_function(wrap_pyfunction!(local_time, m)?)?;
    m.add_function(wrap_pyfunction!(week_day, m)?)?;
    m.add_function(wrap_pyfunction!(parse_iso8601, m)?)?;

    Ok(())
}
