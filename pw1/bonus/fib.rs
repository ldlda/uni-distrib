//! where you think ts is from lmao
#![allow(unused)]

/// give me a fibonacci number NOW
pub const fn fast2(n: u32) -> u64 {
    let (mut a, mut b) = (0, 1);
    let m = n;
    let bit_len = u32::BITS - m.leading_zeros(); // copilot
    let mut mask = if bit_len == 0 { 0 } else { 1 << (bit_len - 1) };
    while mask > 0 {
        let c = a * (2 * b - a);
        let d = a * a + b * b;
        if m & mask == 0 {
            (a, b) = (c, d);
        } else {
            (a, b) = (d, c + d);
        }
        mask >>= 1;
    }
    a
}
// 0, 1, 3, 7
// -> -1 /2 -1 /2 -1 /2
// ->
pub const fn iterfib(mut n: u32) -> u64 {
    let (mut a, mut b) = (0, 1);
    while n > 0 {
        (a, b) = (b, a + b);
        n -= 1; // do this to be const
    }
    a
}
/// ai code, more reliable =)))
pub const fn fib(n: u32) -> u64 {
    const fn fib_pair(n: u32) -> (u64, u64) {
        if (n) == 0 {
            (0, 1)
        } else {
            let (a, b) = fib_pair(n / 2);
            let c = a * (2 * b - a);
            let d = a * a + b * b;

            if n % 2 == 0 {
                (c, d)
            } else {
                (d, c + d)
            }
        }
    }

    fib_pair(n).0
}

#[cfg(test)]
mod tests {
    use super::fast2;

    use super::iterfib;

    use super::fib;

    #[test]
    pub(crate) fn it_works() {
        for _ in 0..100 {
            let n = crate::rand_lda::randfib();
            let a = fib(n);
            let b = iterfib(n);
            let c = fast2(n);
            assert_eq!(a, b, "a does not equal b; n = {n}");
            assert_eq!(c, b, "c does not equal b; n = {n}")
        }
    }
}
