use pyo3::{prelude::*, types::PyDateTime};

use crate::parsing::Parser;
use crate::python::types::FixedTimezone;

#[pyfunction]
pub fn parse_iso8601<'p>(py: Python<'p>, input: &str) -> PyResult<&'p PyDateTime> {
    let parsed = Parser::new(input).parse();

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
                Py::new(py, FixedTimezone::new(offset, None))?
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
