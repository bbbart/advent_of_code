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

    let width = data[0].len();
    let height = data.len();
    let mut dept: Vec<Vec<bool>> = vec![vec![false; width]; height];
    for (i, row) in data.iter().enumerate() {
        for (j, c) in row.chars().enumerate() {
            if c == '@' {
                dept[i][j] = true;
            }
        }
    }

    for x in 0..height {
        for y in 0..width {
            if !dept[x][y] {
                continue;
            }
            let mut neighbours: i16 = 0;
            for dx in -1..=1_isize {
                for dy in -1..=1_isize {
                    if dx == 0 && dy == 0 {
                        continue;
                    }

                    let nx = x.wrapping_add_signed(dx);
                    let ny = y.wrapping_add_signed(dy);
                    if nx < width && ny < height {
                        if dept[nx][ny] {
                            neighbours += 1;
                        }
                    }
                }
            }
            if neighbours < 4 {
                answer += 1;
            }
        }
    }

    println!("PART 1: {}", answer);
    answer = 0;

    loop {
        let mut toremove: Vec<(usize, usize)> = Vec::new();
        for x in 0..height {
            for y in 0..width {
                if !dept[x][y] {
                    continue;
                }
                let mut neighbours: i16 = 0;
                for dx in -1..=1_isize {
                    for dy in -1..=1_isize {
                        if dx == 0 && dy == 0 {
                            continue;
                        }

                        let nx = x.wrapping_add_signed(dx);
                        let ny = y.wrapping_add_signed(dy);
                        if nx < width && ny < height {
                            if dept[nx][ny] {
                                neighbours += 1;
                            }
                        }
                    }
                }
                if neighbours < 4 {
                    answer += 1;
                    toremove.push((x, y));
                }
            }
        }

        if toremove.is_empty() {
            break;
        } else {
            for (x, y) in toremove {
                dept[x][y] = false;
            }
        }
    }

    println!("PART 2: {:?}", answer);
}
