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

    let mut in_ranges: bool = true;
    let mut ranges: Vec<(i64, i64)> = Vec::new();

    for line in &data {
        if line == "" {
            in_ranges = !in_ranges;
            continue;
        }
        if in_ranges {
            let mut split = line.split("-");
            let start = split.next().unwrap().parse::<i64>().unwrap();
            let end = split.next().unwrap().parse::<i64>().unwrap();
            ranges.push((start, end));
            continue;
        }

        let ingredient = line.parse::<i64>().unwrap();

        for (start, end) in ranges.iter() {
            if *start <= ingredient && *end >= ingredient {
                answer += 1;
                break;
            }
        }
    }

    println!("PART 1: {:?}", answer);
    answer = 0;
    ranges = Vec::new();

    // collect all the intervals
    for line in &data {
        if line == "" {
            break;
        }
        let mut split = line.split("-");
        let start = split.next().unwrap().parse::<i64>().unwrap();
        let end = split.next().unwrap().parse::<i64>().unwrap();
        ranges.push((start, end));
    }

    // sort them by start
    ranges.sort_by_key(|(start, _)| *start);

    // merge them
    let mut merged: Vec<(i64, i64)> = vec![ranges[0]];
    for (start, end) in ranges.into_iter().skip(1) {
        let last = merged.last_mut().unwrap();
        if start <= last.1 {
            // overlap or touch -> extend (replace)
            last.1 = last.1.max(end);
        } else {
            // no overlap -> add
            merged.push((start, end));
        }
    }

    for (start, end) in merged {
        answer += end - start + 1;
    }

    println!("PART 2: {:?}", answer);
}
