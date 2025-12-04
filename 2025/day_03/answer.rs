use std::env;
use std::fs::read_to_string;
use std::iter::FromIterator;

fn read_input(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string());
    }

    result
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let data = read_input(&args[1]);
    let mut answer: i64 = 0;

    for bank in &data {
        let units: &i16;
        let tens: &i16;

        let batteries: Vec<i16> =
            Vec::from_iter(bank.chars().map(|c| c.to_digit(10).unwrap() as i16));
        let size = batteries.len();
        let max_bat = batteries.iter().max().unwrap();
        let max_bat_at = batteries.iter().position(|&x| x == *max_bat).unwrap();
        if max_bat_at == size - 1 {
            units = max_bat;
            tens = batteries[..batteries.len() - 1].iter().max().unwrap();
        } else {
            tens = max_bat;
            units = batteries[max_bat_at + 1..].iter().max().unwrap();
        }
        let max_power = (10 * tens + units) as i64;
        answer += max_power;
    }
    println!("PART 1: {}", answer);
    answer = 0;

    for bank in &data {
        let batteries: Vec<i16> =
            Vec::from_iter(bank.chars().map(|c| c.to_digit(10).unwrap() as i16));
        let bank_size = batteries.len();

        let mut max_bat_at: Option<usize> = None;
        let mut max_bat: &i16;
        let mut max_bats: Vec<i16> = Vec::new();

        for i in (0..12).rev() {
            let start = max_bat_at.map_or(0, |i| i+1);
            let end = bank_size - i;
            (max_bat_at, max_bat) = batteries[start..end]
                .iter()
                .enumerate()
                .rev()
                .max_by_key(|(_, val)| *val)
                .map(|(x, y)| (Some(x + start), y))
                .unwrap();
            max_bats.push(*max_bat);
        }
        let joltage:i64 = max_bats.iter().fold(0, |acc, &b| acc * 10 + b as i64);
        answer += joltage;

    }

    println!("PART 2: {:?}", answer);
}
