use std::env;
use std::fs::read_to_string;

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

    let mut args: Vec<Vec<i64>> = Vec::new();
    for i in 0..data.len() - 1 {
        args.push(
            data[i]
                .split_whitespace()
                .map(|x| x.parse().unwrap())
                .collect(),
        );
    }
    let ops: Vec<char> = data[data.len() - 1]
        .split_whitespace()
        .map(|c| c.chars().next().unwrap())
        .collect();

    for i in 0..ops.len() {
        match ops[i] {
            '+' => answer += args.iter().fold(0, |acc, x| acc + x[i]),
            '*' => answer += args.iter().fold(1, |acc, x| acc * x[i]),
            _ => println!("ERROR: unknown operator {}", ops[i]),
        }
    }

    println!("PART 1: {:?}", answer);
    answer = 0;

    let mut args: Vec<Vec<Option<i64>>> = Vec::new();
    for i in 0..data.len() - 1 {
        args.push(
            data[i]
                .chars()
                .map(|c| c.to_digit(10).map(|d| d as i64))
                .collect(),
        );
    }

    let ops: Vec<Option<char>> = data[data.len() - 1]
        .chars()
        .map(|c| {
            if c == '+' {
                Some('+')
            } else if c == '*' {
                Some('*')
            } else {
                None
            }
        })
        .collect();

    let numbers: Vec<Option<i64>> = (0..args[0].len())
        .map(|i| {
            let digits: Vec<i64> = args.iter().filter_map(|row| row[i]).collect();
            if digits.is_empty() {
                None
            } else {
                Some(digits.into_iter().fold(0, |acc, x| acc * 10 + x))
            }
        })
        .collect();

    let mut need_op: bool = true;
    let mut op: char = '?';
    let mut subtotal: i64 = 0;
    for i in 0..numbers.len() {
        if need_op {
            op = ops[i].unwrap();
            subtotal = if op == '+' { 0 } else { 1 };
            need_op = false;
        }
        if numbers[i].is_none() {
            need_op = true;
            answer += subtotal;
            continue;
        }
        match op {
            '+' => subtotal += numbers[i].unwrap(),
            '*' => subtotal *= numbers[i].unwrap(),
            _ => println!("ERROR: unknown operator {}", op),
        }
    }
    answer += subtotal;

    println!("PART 2: {:?}", answer);
}
