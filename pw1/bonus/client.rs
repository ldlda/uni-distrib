use std::{
    error::Error,
    io::{BufRead, BufReader, Write},
    net::TcpStream,
};
mod fib;

const IPAHHDRESS: &str = "[2603:c024:4512:af42::5:32]:7844";

fn main() -> Result<(), Box<dyn Error>> {
    let this = TcpStream::connect(IPAHHDRESS)?;
    let mut thisbuf = BufReader::new(this);

    let mut num = String::new();
    let n = thisbuf.read_line(&mut num)?;
    println!("n = {n}, num = {num}");

    let num: u64 = num.trim().parse()?;
    println!("number got {num}");

    writeln!(thisbuf.get_mut(), "this is a sentence of {ahh}", ahh = fib::fib(num))?;

    Ok(())
} 