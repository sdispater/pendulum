extern crate core;

use pyo3::{prelude::*, types::PyDateTime};

mod constants;
mod helpers;
mod parsing;
mod types;

use types::TzInfo;

#[pyfunction]
fn is_leap(year: u32) -> PyResult<bool> {
    Ok(helpers::is_leap(year))
}

#[pyfunction]
fn is_long_year(year: u32) -> PyResult<bool> {
    Ok(helpers::is_long_year(year))
}

#[pyfunction]
fn week_day(year: u32, month: u32, day: u32) -> PyResult<u32> {
    Ok(helpers::week_day(year, month, day))
}

#[pyfunction]
fn local_time(
    unix_time: isize,
    utc_offset: isize,
    microsecond: usize,
) -> PyResult<(usize, usize, usize, usize, usize, usize, usize)> {
    Ok(helpers::local_time(unix_time, utc_offset, microsecond))
}

#[pyfunction]
fn parse<'p>(py: Python<'p>, input: &str) -> PyResult<&'p PyDateTime> {
    let parsed = parsing::Parser::new(input).parse();

    match parsed.offset {
        Some(offset) => PyDateTime::new(
            py,
            parsed.year as i32,
            parsed.month as u8,
            parsed.day as u8,
            parsed.hour as u8,
            parsed.minute as u8,
            parsed.second as u8,
            parsed.microsecond as u32,
            Some(
                Py::new(py, TzInfo::new(offset))?
                    .to_object(py)
                    .extract(py)?,
            ),
        ),
        None => PyDateTime::new(
            py,
            parsed.year as i32,
            parsed.month as u8,
            parsed.day as u8,
            parsed.hour as u8,
            parsed.minute as u8,
            parsed.second as u8,
            parsed.microsecond as u32,
            None,
        ),
    }
}

#[pymodule]
fn _pendulum(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_leap, m)?)?;
    m.add_function(wrap_pyfunction!(is_long_year, m)?)?;
    m.add_function(wrap_pyfunction!(local_time, m)?)?;
    m.add_function(wrap_pyfunction!(week_day, m)?)?;
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    Ok(())
}
