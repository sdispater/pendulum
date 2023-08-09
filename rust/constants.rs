pub const EPOCH_YEAR: u32 = 1970;

pub const DAYS_PER_N_YEAR: u32 = 365;
pub const DAYS_PER_L_YEAR: u32 = 366;

pub const SECS_PER_MIN: u32 = 60;
pub const SECS_PER_HOUR: u32 = SECS_PER_MIN * 60;
pub const SECS_PER_DAY: u32 = SECS_PER_HOUR * 24;

// 400-year chunks always have 146097 days (20871 weeks).
pub const DAYS_PER_400_YEARS: u32 = 146_097;
pub const SECS_PER_400_YEARS: u64 = DAYS_PER_400_YEARS as u64 * SECS_PER_DAY as u64;

// The number of seconds in an aligned 100-year chunk, for those that
// do not begin with a leap year and those that do respectively.
pub const SECS_PER_100_YEARS: [u64; 2] = [
    (76 * DAYS_PER_N_YEAR as u64 + 24 * DAYS_PER_L_YEAR as u64) * SECS_PER_DAY as u64,
    (75 * DAYS_PER_N_YEAR as u64 + 25 * DAYS_PER_L_YEAR as u64) * SECS_PER_DAY as u64,
];

// The number of seconds in an aligned 4-year chunk, for those that
// do not begin with a leap year and those that do respectively.
#[allow(clippy::erasing_op)]
pub const SECS_PER_4_YEARS: [u32; 2] = [
    (4 * DAYS_PER_N_YEAR + 0 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
    (3 * DAYS_PER_N_YEAR + DAYS_PER_L_YEAR) * SECS_PER_DAY,
];

// The number of seconds in non-leap and leap years respectively.
pub const SECS_PER_YEAR: [u32; 2] = [
    DAYS_PER_N_YEAR * SECS_PER_DAY,
    DAYS_PER_L_YEAR * SECS_PER_DAY,
];

// The month lengths in non-leap and leap years respectively.
pub const DAYS_PER_MONTHS: [[i32; 13]; 2] = [
    [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
];

// The day offsets of the beginning of each (1-based) month in non-leap
// and leap years respectively.
// For example, in a leap year there are 335 days before December.
pub const MONTHS_OFFSETS: [[i32; 14]; 2] = [
    [
        -1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365,
    ],
    [
        -1, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366,
    ],
];

pub const DAY_OF_WEEK_TABLE: [u32; 12] = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4];

pub const TM_JANUARY: usize = 0;
pub const TM_DECEMBER: usize = 11;
