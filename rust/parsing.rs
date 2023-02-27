use core::str;
use std::str::CharIndices;

use crate::{
    constants::{DAYS_PER_MONTHS, MONTHS_OFFSETS},
    helpers::{days_in_year, is_leap, is_long_year, week_day},
};

pub struct Duration {
    years: i32,
}

pub struct Parsed {
    pub is_date: bool,
    pub is_time: bool,
    pub is_datetime: bool,
    pub is_duration: bool,
    pub is_period: bool,

    ambiguous: bool,
    pub year: u32,
    pub month: u32,
    pub day: u32,
    pub hour: u32,
    pub minute: u32,
    pub second: u32,
    pub microsecond: u32,
    pub offset: Option<i32>,
    pub has_offset: bool,
}

impl<'a> Parsed {
    pub fn new() -> Parsed {
        Parsed {
            is_date: false,
            is_time: false,
            is_datetime: false,
            is_duration: false,
            is_period: false,

            ambiguous: false,
            year: 0,
            month: 1,
            day: 1,
            hour: 0,
            minute: 0,
            second: 0,
            microsecond: 0,
            offset: None,
            has_offset: false,
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

    /// Increments the parser by `n` characters if the end of the input
    /// has not been reached. Eliminates the need for repeated 'self.inc();'
    /// in code.
    fn inc_n(&mut self, n: usize) -> bool {
        for _ in 0..n {
            if !self.inc() {
                return false;
            }
        }
        true
    }

    /// Returns true if the parser has reached the end of the input.
    fn end(&self) -> bool {
        self.idx >= self.src.len()
    }

    pub fn parse(&mut self) -> Parsed {
        let mut parsed = Parsed::new();
        parsed.is_date = true;

        for _ in 0..4 {
            if self.end() {
                // TODO: Error
            }

            if self.current >= '0' && self.current <= '9' {
                parsed.year = 10 * parsed.year + self.current.to_digit(10).unwrap() as u32;
                self.inc();
            } else {
                // TODO: Error
                return parsed;
            }
        }

        let mut leap = is_leap(parsed.year);
        let mut separators: u32 = 0;
        let mut week: u32 = 0;
        let mut monthday: u32 = 0;
        let mut i = 0;

        // Optional separator
        if self.current == '-' {
            separators += 1;
            self.inc();
        }

        // Checking for week dates
        if self.current == 'W' {
            self.inc();

            let mut weekday: u32 = 1;

            while !self.end() && self.current != ' ' && self.current != 'T' {
                if self.current == '-' {
                    separators += 1;
                    self.inc();
                    continue;
                }

                week = 10 * week + self.current.to_digit(10).unwrap() as u32;

                i += 1;
                self.inc();
            }

            match i {
                2 => (), // Only week number
                3 => {
                    // Week with week day
                    if !(separators == 0 || separators == 2) {
                        // We should have to or no separators
                        // TODO: Invalid week date
                        return parsed;
                    }

                    weekday = week % 10;
                    week /= 10;
                }
                _ => {
                    // TODO: Invalid week date
                    return parsed;
                }
            }

            // Checks
            if week > 53 || week > 52 && !is_long_year(parsed.year) {
                // TODO: Invalid week number
                return parsed;
            }

            if weekday > 7 {
                // TODO: Invalid week day
                return parsed;
            }

            // Calculating ordinal day
            let mut ordinal: u32 = week * 7 + weekday - (week_day(parsed.year, 1, 4) + 3);

            if ordinal < 1 {
                // Previous year
                ordinal += days_in_year(parsed.year - 1);
                parsed.year -= 1;
                leap = is_leap(parsed.year);
            }

            if ordinal > days_in_year(parsed.year) {
                // Next year
                ordinal -= days_in_year(parsed.year);
                parsed.year += 1;
                leap = is_leap(parsed.year);
            }

            for j in 1..14 {
                if ordinal <= MONTHS_OFFSETS[leap as usize][j] as u32 {
                    parsed.day = ordinal - MONTHS_OFFSETS[leap as usize][j - 1] as u32;
                    parsed.month = (j - 1) as u32;

                    break;
                }
            }
        } else {
            // At this point we need to check the number
            // of characters until the end of the date part
            // (or the end of the string).
            //
            // If two, we have only a month if there is a separator, it may be a time otherwise.
            // If three, we have an ordinal date.
            // If four, we have a complete date
            while !self.end() && self.current != ' ' && self.current != 'T' {
                if self.current == '-' {
                    separators += 1;
                    self.inc();
                    continue;
                }

                if !(self.current >= '0' && self.current <= '9') {
                    // TODO: Error
                    return parsed;
                }

                monthday = 10 * monthday + self.current.to_digit(10).unwrap() as u32;
                self.inc();

                i += 1;
            }

            match i {
                0 => (),
                2 => {
                    if separators == 0 {
                        // TODO: ambiguous
                        parsed.ambiguous = true;
                        ();
                    }

                    parsed.month = monthday;
                }
                3 => {
                    // Ordinal day
                    if separators > 1 {
                        // TODO: Invalid ordinal date
                        return parsed;
                    }

                    if monthday < 1 || monthday > MONTHS_OFFSETS[leap as usize][13] as u32 {
                        // TODO: Invalid ordinal day for year
                        return parsed;
                    }

                    for j in 1..14 {
                        if monthday < MONTHS_OFFSETS[leap as usize][j] as u32 {
                            parsed.day = monthday - MONTHS_OFFSETS[leap as usize][j - 1] as u32;
                            parsed.month = (j - 1) as u32;

                            break;
                        }
                    }
                }
                4 => {
                    // Month and day
                    parsed.month = monthday as u32 / 100;
                    parsed.day = monthday as u32 % 100;
                }
                _ => {
                    // TODO: Error
                    return parsed;
                }
            }
        }

        if separators > 0 && monthday == 0 && week == 0 {
            // TODO: Invalid date

            return parsed;
        }

        if parsed.month > 12 {
            // TODO: Invalid month
            return parsed;
        }

        if parsed.day > DAYS_PER_MONTHS[leap as usize][parsed.month as usize] as u32 {
            // TODO: Invalid day for month
            return parsed;
        }

        separators = 0;

        if self.current == 'T' || self.current == ' ' {
            if parsed.ambiguous {
                // TODO: Invalid date
                return parsed;
            }

            // We have time so we have a datetime
            parsed.is_date = false;
            parsed.is_datetime = true;

            if !self.inc() {
                // TODO: invalid date
                return parsed;
            }

            // Grabbing time information
            i = 0;
            let mut time = 0;
            while !self.end()
                && self.current != '.'
                && self.current != ','
                && self.current != 'Z'
                && self.current != '+'
                && self.current != '-'
            {
                if self.current == ':' {
                    separators += 1;
                    self.inc();
                    continue;
                }

                if !(self.current >= '0' && self.current <= '9') {
                    // TODO: Invalid time
                    return parsed;
                }

                time = 10 * time + self.current.to_digit(10).unwrap();
                i += 1;
                self.inc();
            }

            match i {
                2 => {
                    // Hours only
                    if separators > 0 {
                        // Extraneous separators
                        // TODO: Invalid time
                        return parsed;
                    }

                    parsed.hour = time;
                }
                4 => {
                    // Hours and minutes
                    if separators > 1 {
                        // Extraneous separators
                        // TODO: Invalid time
                        return parsed;
                    }

                    parsed.hour = time / 100;
                    parsed.minute = time % 100;
                }
                6 => {
                    // Hours, minutes and seconds
                    if separators > 2 {
                        // Extraneous separators
                        // TODO: Invalid time
                        return parsed;
                    }

                    parsed.hour = time / 10000;
                    parsed.minute = time / 100 % 100;
                    parsed.second = time % 100;
                }
                _ => {
                    // TODO: Invalid time
                    return parsed;
                }
            }

            // Checks
            if parsed.hour > 23 {
                // TODO: Invalid hour
                return parsed;
            }

            if parsed.minute > 59 {
                // TODO: Invalid minute
                return parsed;
            }

            if parsed.second > 59 {
                // TODO: Invalid second
                return parsed;
            }

            // Subsecond
            if self.current == '.' || self.current == ',' {
                self.inc();

                time = 0;
                i = 0;
                while !self.end()
                    && self.current != 'Z'
                    && self.current != '+'
                    && self.current != '-'
                {
                    if !(self.current >= '0' && self.current <= '9') {
                        // TODO: Invalid time
                        return parsed;
                    }

                    time = 10 * time + self.current.to_digit(10).unwrap();
                    i += 1;
                    self.inc();
                }

                // Adjust to microseconds
                if i > 6 {
                    parsed.microsecond = time / 10u32.pow(i - 6);
                } else if i <= 6 {
                    parsed.microsecond = time * 10u32.pow(6 - i);
                }
            }
        }

        // Timezone
        if self.current == 'Z' {
            parsed.has_offset = true;
            self.inc();
        } else if self.current == '+' || self.current == '-' {
            let tz_sign: i32 = if self.current == '+' { 1 } else { -1 };

            parsed.has_offset = true;
            self.inc();

            i = 0;
            separators = 0;
            let mut offset: i32 = 0;

            while !self.end() {
                if self.current == ':' {
                    separators += 1;
                    self.inc();
                    continue;
                }

                if !(self.current >= '0' && self.current <= '9') {
                    // TODO: Invalid offset
                    return parsed;
                }

                offset = 10 * offset + self.current.to_digit(10).unwrap() as i32;
                self.inc();
                i += 1;
            }

            match i {
                2 => {
                    // hh format
                    if separators > 0 {
                        // Extraneous separators
                        // TODO: Invalid offset
                        return parsed;
                    }

                    parsed.offset = Some(tz_sign * offset * 3600);
                }
                4 => {
                    // hhmm format
                    if separators > 1 {
                        // Extraneous separators
                        // TODO: Invalid offset
                        return parsed;
                    }

                    parsed.offset = Some(tz_sign * ((offset / 100 * 3600) + (offset % 100 * 60)));
                }
                _ => {
                    // Wrong format
                    // TODO: Invalid format
                    return parsed;
                }
            }
        }

        return parsed;
    }
}
