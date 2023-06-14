use pyo3::exceptions;
use pyo3::{prelude::*, types::PyDateTime};

use crate::parsing::Parser;
use crate::python::types::{Duration, FixedTimezone};

#[pyfunction]
pub fn parse_iso8601(py: Python, input: &str) -> PyResult<PyObject> {
    let parsed = Parser::new(input).parse();

    match parsed {
        Ok(parsed) => match (parsed.datetime, parsed.duration, parsed.second_datetime) {
            (Some(datetime), None, None) => match datetime.offset {
                Some(offset) => {
                    let dt = PyDateTime::new(
                        py,
                        datetime.year as i32,
                        datetime.month as u8,
                        datetime.day as u8,
                        datetime.hour as u8,
                        datetime.minute as u8,
                        datetime.second as u8,
                        datetime.microsecond as u32,
                        Some(
                            Py::new(py, FixedTimezone::new(offset, None))?
                                .to_object(py)
                                .extract(py)?,
                        ),
                    )?;

                    return Ok(dt.to_object(py));
                }
                None => {
                    let dt = PyDateTime::new(
                        py,
                        datetime.year as i32,
                        datetime.month as u8,
                        datetime.day as u8,
                        datetime.hour as u8,
                        datetime.minute as u8,
                        datetime.second as u8,
                        datetime.microsecond as u32,
                        None,
                    )?;

                    return Ok(dt.to_object(py));
                }
            },
            (None, Some(duration), None) => {
                return Ok(Py::new(
                    py,
                    Duration::new(
                        Some(duration.years),
                        Some(duration.months),
                        Some(duration.weeks),
                        Some(duration.days),
                        Some(duration.hours),
                        Some(duration.minutes),
                        Some(duration.seconds),
                        Some(duration.microseconds),
                    ),
                )?
                .to_object(py));
            }
            (_, _, _) => todo!(),
        },
        Err(error) => Err(exceptions::PyValueError::new_err(format!("{}", error))),
    }
}
