use core::str;
use std::{fmt, str::CharIndices};

use crate::{
    constants::{DAYS_PER_MONTHS, MONTHS_OFFSETS},
    helpers::{days_in_year, is_leap, is_long_year, week_day},
};

pub struct Duration {
    years: i32,
}

#[derive(Debug, Clone)]
pub struct ParseError {
    index: usize,
    c: char,
    message: String,
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} (Position: {})", self.message, self.index.to_string())
    }
}

pub struct ParsedDateTime {
    pub year: u32,
    pub month: u32,
    pub day: u32,
    pub hour: u32,
    pub minute: u32,
    pub second: u32,
    pub microsecond: u32,
    pub offset: Option<i32>,
    pub has_offset: bool,
    pub time_is_midnight: bool,
}

impl<'a> ParsedDateTime {
    pub fn new() -> ParsedDateTime {
        ParsedDateTime {
            year: 0,
            month: 1,
            day: 1,
            hour: 0,
            minute: 0,
            second: 0,
            microsecond: 0,
            offset: None,
            has_offset: false,
            time_is_midnight: false,
        }
    }
}

pub struct ParsedDuration {
    pub years: i32,
    pub months: i32,
    pub days: i32,
    pub hours: i32,
    pub minutes: i32,
    pub seconds: i32,
    pub microseconds: i32,
}

impl<'a> ParsedDuration {
    pub fn new() -> ParsedDuration {
        ParsedDuration {
            years: 0,
            months: 0,
            days: 0,
            hours: 0,
            minutes: 0,
            seconds: 0,
            microseconds: 0,
        }
    }
}

pub struct Parsed {
    pub datetime: Option<ParsedDateTime>,
    pub duration: Option<ParsedDuration>,
    pub second_datetime: Option<ParsedDateTime>,
}

impl<'a> Parsed {
    pub fn new() -> Parsed {
        Parsed {
            datetime: None,
            duration: None,
            second_datetime: None,
        }
    }
}

pub struct Parser<'a> {
    /// Input to parse.
    src: &'a str,
    /// Iterator used for getting characters from `src`.
    chars: CharIndices<'a>,
    /// Current byte offset into `src`.
    idx: usize,
    /// Current character
    current: char,
}

impl<'a> Parser<'a> {
    /// Creates a new parser from a &str.
    pub fn new(input: &'a str) -> Parser<'a> {
        let mut p = Parser {
            src: input,
            chars: input.char_indices(),
            idx: 0,
            current: '\0',
        };
        p.inc();
        p
    }

    /// Increments the parser if the end of the input has not been reached.
    /// Returns whether or not it was able to advance.
    fn inc(&mut self) -> bool {
        match self.chars.next() {
            Some((i, ch)) => {
                self.idx = i;
                self.current = ch;
                true
            }
            None => {
                self.idx = self.src.len();
                self.current = '\0';
                false
            }
        }
    }

    fn parse_error(&mut self, message: String) -> ParseError {
        ParseError {
            index: self.idx,
            c: self.current,
            message: message,
        }
    }

    fn unexpected_character_error(
        &mut self,
        field_name: &str,
        expected_character_count: usize,
    ) -> ParseError {
        if self.end() {
            return self.parse_error(format!(
                "Unexpected end of string while parsing {}. Expected {} more character{}.",
                field_name,
                expected_character_count,
                if expected_character_count != 1 {
                    "s"
                } else {
                    ""
                }
            ));
        }

        self.parse_error(format!(
            "Invalid character while parsing {}: {}.",
            field_name, self.current,
        ))
    }

    /// Returns true if the parser has reached the end of the input.
    fn end(&self) -> bool {
        self.idx >= self.src.len()
    }

    fn parse_integer(&mut self, length: usize, field_name: &str) -> Result<u32, ParseError> {
        let mut value: u32 = 0;

        for i in 0..length {
            if self.end() {
                return Err(self.parse_error(format!(
                    "Unexpected end of string while parsing \"{}\". Expected {} more character{}",
                    field_name,
                    length - i,
                    if (length - i) != 1 { "s" } else { "" }
                )));
            }

            if self.current >= '0' && self.current <= '9' {
                value = 10 * value + self.current.to_digit(10).unwrap() as u32;
                self.inc();
            } else {
                return Err(self.unexpected_character_error(field_name, length - i));
            }
        }

        Ok(value)
    }

    pub fn parse(&mut self) -> Result<Parsed, ParseError> {
        let mut parsed = Parsed::new();

        if self.current == 'P' {
            // Duration (and possibly time interval)
        } else {
            self.parse_datetime(&mut parsed);
        }

        Ok(parsed)
    }

    fn parse_datetime(&mut self, parsed: &mut Parsed) -> Result<(), ParseError> {
        let mut datetime = ParsedDateTime::new();
        let mut extended_date_format: bool = false;

        datetime.year = self.parse_integer(4, "year")?;

        if self.current == '-' {
            self.inc();
            extended_date_format = true;

            if self.current == 'W' {
                // ISO week and day in extended format (i.e. Www-D)
                self.inc();

                let iso_week = self.parse_integer(2, "iso week")?;
                let mut iso_day: u32 = 1;

                if !self.end() && self.current != ' ' && self.current != 'T' {
                    // Optional day
                    if self.current != '-' {
                        return Err(self.parse_error(format!(
                            "Invalid character \"{}\" while parsing {}",
                            self.current, "date separator"
                        )));
                    }

                    self.inc();

                    iso_day = self.parse_integer(1, "iso day")?;
                }

                match self.iso_to_ymd(datetime.year, iso_week, iso_day) {
                    Ok((year, month, day)) => {
                        datetime.year = year;
                        datetime.month = month;
                        datetime.day = day;
                    }
                    Err(error) => return Err(error),
                }
            } else {
                /*
                Month and day in extended format (MM-DD) or ordinal date (DDD)
                We'll assume first that the next part is a month and adjust if not.
                */
                datetime.month = self.parse_integer(2, "month")?;

                if !self.end() && self.current != ' ' && self.current != 'T' {
                    if self.current == '-' {
                        // Optional day
                        self.inc();
                        datetime.day = self.parse_integer(2, "day")?;
                    } else {
                        // Ordinal day
                        let ordinal_day =
                            (datetime.month * 10 + self.parse_integer(1, "ordinal day")?) as i32;

                        match self.ordinal_to_ymd(datetime.year, ordinal_day, false) {
                            Ok((year, month, day)) => {
                                datetime.year = year;
                                datetime.month = month;
                                datetime.day = day;
                            }
                            Err(error) => return Err(error),
                        }
                    }
                } else {
                    datetime.day = 1;
                }
            }
        } else {
            if self.current == 'W' {
                // Compact ISO week and day (WwwD)
                self.inc();

                let iso_week = self.parse_integer(2, "iso week")?;
                let mut iso_day: u32 = 1;

                if !self.end() && self.current != ' ' && self.current != 'T' {
                    iso_day = self.parse_integer(1, "iso day")?;
                }

                match self.iso_to_ymd(datetime.year, iso_week, iso_day) {
                    Ok((year, month, day)) => {
                        datetime.year = year;
                        datetime.month = month;
                        datetime.day = day;
                    }
                    Err(error) => return Err(error),
                }
            } else {
                /*
                Month and day in compact format (MMDD) or ordinal date (DDD)
                We'll assume first that the next part is a month and adjust if not.
                */
                datetime.month = self.parse_integer(2, "month")?;
                let mut ordinal_day = self.parse_integer(1, "ordinal day")? as i32;

                if self.end() || self.current == ' ' || self.current == 'T' {
                    // Ordinal day
                    ordinal_day = datetime.month as i32 * 10 + ordinal_day;

                    match self.ordinal_to_ymd(datetime.year, ordinal_day, false) {
                        Ok((year, month, day)) => {
                            datetime.year = year;
                            datetime.month = month;
                            datetime.day = day;
                        }
                        Err(error) => return Err(error),
                    }
                } else {
                    // Day
                    datetime.day = ordinal_day as u32 * 10 + self.parse_integer(1, "day")?;
                }
            }
        }

        if !self.end() {
            // Date/Time separator
            if self.current != 'T' && self.current != ' ' {
                return Err(self.parse_error(format!(
                    "Invalid character \"{}\" while parsing {}",
                    self.current, "date and time separator (\"T\" or \" \")"
                )));
            }

            self.inc();

            // Hour
            datetime.hour = self.parse_integer(2, "hour")?;

            if !self.end() && self.current != 'Z' && self.current != '+' && self.current != '-' {
                // Optional minute and second
                if self.current == ':' {
                    // Minute and second in extended format (mm:ss)
                    self.inc();

                    // Minute
                    datetime.minute = self.parse_integer(2, "minute")?;

                    if !self.end()
                        && self.current != 'Z'
                        && self.current != '+'
                        && self.current != '-'
                    {
                        // Optional second
                        if self.current != ':' {
                            return Err(self.parse_error(format!(
                                "Invalid character \"{}\" while parsing {}",
                                self.current, "time separator (\":\")"
                            )));
                        }

                        self.inc();

                        // Second
                        datetime.second = self.parse_integer(2, "second")?;

                        if self.current == '.' || self.current == ',' {
                            // Optional fractional second
                            self.inc();

                            datetime.microsecond = 0;
                            let mut i: u8 = 0;

                            while i < 6 {
                                if self.current >= '0' && self.current <= '9' {
                                    datetime.microsecond = datetime.microsecond * 10
                                        + self.current.to_digit(10).unwrap();
                                } else if i == 0 {
                                    // One digit minimum is required
                                    return Err(self.unexpected_character_error("subsecond", 1));
                                } else {
                                    break;
                                }

                                self.inc();
                                i += 1;
                            }

                            // Drop extraneous digits
                            while self.current >= '0' && self.current <= '9' {
                                self.inc();
                            }

                            // Expand missing microsecond
                            while i < 6 {
                                datetime.microsecond *= 10;
                                i += 1;
                            }
                        }

                        if !extended_date_format {
                            return Err(self.parse_error(format!("Cannot combine \"basic\" date format with \"extended\" time format (Should be either `YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).")));
                        }
                    }
                } else {
                    // Minute and second in compact format (mmss)

                    // Minute
                    datetime.minute = self.parse_integer(2, "minute")?;

                    if !self.end()
                        && self.current != 'Z'
                        && self.current != '+'
                        && self.current != '-'
                    {
                        // Optional second

                        datetime.second = self.parse_integer(2, "second")?;

                        if self.current == '.' || self.current == ',' {
                            // Optional fractional second
                            self.inc();

                            datetime.microsecond = 0;
                            let mut i: u8 = 0;

                            while i < 6 {
                                if self.current >= '0' && self.current <= '9' {
                                    datetime.microsecond = datetime.microsecond * 10
                                        + self.current.to_digit(10).unwrap();
                                } else if i == 0 {
                                    // One digit minimum is required
                                    return Err(self.unexpected_character_error("subsecond", 1));
                                } else {
                                    break;
                                }

                                self.inc();
                                i += 1;
                            }

                            // Drop extraneous digits
                            while self.current >= '0' && self.current <= '9' {
                                self.inc();
                            }

                            // Expand missing microsecond
                            while i < 6 {
                                datetime.microsecond *= 10;
                                i += 1;
                            }
                        }
                    }

                    if extended_date_format {
                        return Err(self.parse_error(format!("Cannot combine \"extended\" date format with \"basic\" time format (Should be either `YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).")));
                    }
                }
            }
        }

        if datetime.hour == 24
            && datetime.minute == 0
            && datetime.second == 0
            && datetime.microsecond == 0
        {
            // Special case for 24:00:00, which is valid for ISO 8601.
            // This is equivalent to 00:00:00 the next day.
            // We will store the information for now.
            datetime.time_is_midnight = true
        }

        if self.current == 'Z' || self.current == '+' || self.current == '-' {
            // Optional timezone offset
            let mut tzsign = 0;

            if self.current == '+' {
                tzsign = 1;
            } else if self.current == '-' {
                tzsign = -1;
            }

            self.inc();

            let mut tzhour: i32 = 0;
            let mut tzminute: i32 = 0;

            if tzsign != 0 {
                // Offset hour
                tzhour = self.parse_integer(2, "timezone hour")? as i32;
                if self.current == ':' {
                    // Optional separator
                    self.inc();

                    tzminute = self.parse_integer(2, "timezone minute")? as i32;
                } else {
                    tzminute = self.parse_integer(2, "timezone minute")? as i32;
                }
            }

            if tzminute > 59 {
                return Err(self.parse_error(format!("timezone minute must be in 0..59")));
            }

            tzminute += tzhour * 60;
            tzminute *= tzsign;

            if tzminute.abs() > 1440 {
                return Err(self.parse_error(format!("The absolute offset is to large")));
            }

            datetime.offset = Some(tzminute * 60);
        }

        if !self.end() {
            return Err(self.parse_error(format!("Unconverted data remains")));
        }

        match &parsed.datetime {
            Some(_) => {
                parsed.second_datetime = Some(datetime);
            }
            None => match &parsed.duration {
                Some(_) => {
                    parsed.second_datetime = Some(datetime);
                }
                None => {
                    parsed.datetime = Some(datetime);
                }
            },
        }

        Ok(())
    }

    fn iso_to_ymd(
        &mut self,
        iso_year: u32,
        iso_week: u32,
        iso_day: u32,
    ) -> Result<(u32, u32, u32), ParseError> {
        if iso_week > 53 || iso_week > 52 && !is_long_year(iso_year) {
            return Err(ParseError {
                index: self.idx,
                c: self.current,
                message: format!(
                    "Invalid ISO date: week {} out of range for year {}",
                    iso_week, iso_year
                ),
            });
        }

        if iso_day > 7 {
            return Err(ParseError {
                index: self.idx,
                c: self.current,
                message: format!("Invalid ISO date: week day is invalid"),
            });
        }

        let ordinal: i32 =
            iso_week as i32 * 7 + iso_day as i32 - (week_day(iso_year, 1, 4) as i32 + 3);

        self.ordinal_to_ymd(iso_year, ordinal, true)
    }

    fn ordinal_to_ymd(
        &mut self,
        year: u32,
        ordinal: i32,
        allow_out_of_bounds: bool,
    ) -> Result<(u32, u32, u32), ParseError> {
        let mut ord: i32 = ordinal;
        let mut y: u32 = year;
        let mut leap: usize = is_leap(y) as usize;
        let mut month: u32 = 1;
        let mut day: u32 = 1;

        if ord < 1 {
            if !allow_out_of_bounds {
                return Err(self.parse_error(format!(
                    "Invalid ordinal day: {} is too small for year {}",
                    ordinal.to_string(),
                    year.to_string()
                )));
            }
            // Previous year
            ord += days_in_year(year - 1) as i32;
            y -= 1;
            leap = is_leap(y) as usize;
        }

        if ord > days_in_year(y) as i32 {
            if !allow_out_of_bounds {
                return Err(self.parse_error(format!(
                    "Invalid ordinal day: {} is too large for year {}",
                    ordinal.to_string(),
                    year.to_string()
                )));
            }

            // Next year
            ord -= days_in_year(y) as i32;
            y += 1;
            leap = is_leap(y) as usize;
        }

        for i in 1..14 {
            if ord < MONTHS_OFFSETS[leap][i] {
                day = ord as u32 - MONTHS_OFFSETS[leap][i - 1] as u32;
                month = (i - 1) as u32;

                return Ok((y as u32, month, day));
            }
        }

        Err(self.parse_error(format!(
            "Invalid ordinal day: {} is too large for year {}",
            ordinal.to_string(),
            year.to_string()
        )))
    }
}
