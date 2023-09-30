extern crate core;

#[cfg(feature = "mimalloc")]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

mod constants;
mod helpers;
mod parsing;
mod python;

pub use python::_pendulum;
