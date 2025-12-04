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
    let mut pos = 50;
    let mut zerocounter = 0;

    for mut instruction in data {
        let direction = instruction.remove(0);
        let distance: i32 = instruction.parse().unwrap();

        if direction == 'L' {
            pos = (pos - distance + 100) % 100;
        } else if direction == 'R' {
            pos = (pos + distance + 100) % 100;
        }

        if pos == 0 {
            zerocounter += 1;
        }
    }

    println!("PART 1: {}", zerocounter);

    let data = read_input(&args[1]);
    let mut pos = 50;
    let mut zerocounter = 0;

    for mut instruction in data {
        let direction = instruction.remove(0);
        let distance: i32 = instruction.parse().unwrap();

        let mut newpos: i32 = 0;
        if direction == 'L' {
            newpos = (pos - distance + 100).rem_euclid(100);
        } else if direction == 'R' {
            newpos = (pos + distance + 100).rem_euclid(100);
        }

        if newpos == 0 {
            zerocounter += 1;
        } else if pos != 0
            && ((direction == 'L' && newpos > pos)
                || (direction == 'R' && newpos < pos))
        {
            zerocounter += 1;
        }

        zerocounter += distance / 100;

        pos = newpos;
    }

    println!("PART 2: {}", zerocounter);
}
