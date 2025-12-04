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

    for range in data[0].split(',') {
        let minmax: Vec<i64> = range.split('-').map(|s| s.parse().unwrap()).collect();
        for id in minmax[0]..minmax[1] + 1 {
            let ids: Vec<char> = id.to_string().chars().collect();
            let splitidx = ids.len() / 2;
            if ids[0..splitidx] == ids[splitidx..ids.len()] {
                answer += id;
            }
        }
    }

    println!("PART 1: {}", answer);

    answer = 0;
    for range in data[0].split(',') {
        let minmax: Vec<i64> = range.split('-').map(|s| s.parse().unwrap()).collect();
        for id in minmax[0]..minmax[1] + 1 {
            let num_digits: i64 = (id.checked_ilog10().unwrap_or(0) + 1) as i64;
            for div in (1..).take_while(|d| 2 * d <= num_digits) {
                if num_digits % div == 0 {
                    let pattern: i64 = id % 10_i64.checked_pow(div as u32).unwrap();
                    let mut multiplier: i64 = 1;
                    for exp in 1..num_digits / div {
                        multiplier += 10_i64.checked_pow((exp * div) as u32).unwrap();
                    }
                    if multiplier == 1 {
                        continue;
                    }
                    if id == pattern * multiplier {
                        answer += id;
                        break;
                    }
                }
            }
        }
    }

    println!("PART 2: {:?}", answer);
}
