use std::collections::HashMap;
use std::collections::HashSet;
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

    let mut beams: HashSet<usize> = vec![data[0].find("S").unwrap()].into_iter().collect();
    let mut splitters: HashSet<usize>;
    for line in &data[1..] {
        splitters = line.match_indices('^').map(|(i, _)| i).collect();
        for beam in &beams & &splitters {
            answer += 1;
            beams.insert(beam + 1);
            beams.insert(beam - 1);
            beams.remove(&beam);
        }
    }

    println!("PART 1: {:?}", answer);

    let mut beams: HashMap<usize, i64> = HashMap::new();
    beams.insert(data[0].find("S").unwrap(), 1);

    for line in data[1..].iter() {
        let splitters_at: HashSet<usize> = line.match_indices('^').map(|(i, _)| i).collect();
        if splitters_at.is_empty() {
            continue;
        }

        for splitter in &splitters_at {
            if !beams.contains_key(splitter) {
                continue;
            }
            *beams.entry(splitter - 1).or_insert(0) += beams[splitter];
            *beams.entry(splitter + 1).or_insert(0) += beams[splitter];
            beams.remove(&splitter);
        }
    }

    answer = beams.values().sum();
    println!("PART 2: {:#?}", answer);
}
