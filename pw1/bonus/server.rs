// use std::thread;

use std::{
    error::Error,
    io::{BufRead, BufReader, Write},
    net::TcpListener,
};

const AHHDRESS: &str = "[2603:c024:4512:af42::5:32]:7844";

fn main() -> Result<(), Box<dyn Error>> {
    let bro = TcpListener::bind(AHHDRESS)?;
    let (one, sos) = bro.accept()?;
    println!("we got a {sos}");
    let mut onebuf = BufReader::new(one);
    // so a concern is that this one gets dropped AFTER one which well doesnt happen here but what if

    let num: u8 = rand::random();
    let num = num % 93;
    println!("number is {num}");
    writeln!(onebuf.get_mut(), "{num}")?;

    let mut answer = String::new();
    let n = onebuf.read_line(&mut answer)?;
    println!("rsz {n}");
    println!("so fib is like uhhhhhh {answer}");

    Ok(())
}
//     println!("Hello, world!");
//     println!("first program written in console!");
//     let bro = 3 - 5;
//     let other = bro.max({
//         let other = 5 - 3;
//         use std::ops::Neg;
//         other.neg()
//     });
//     println!("that is {other}")
