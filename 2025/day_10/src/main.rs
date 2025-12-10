use good_lp::solvers::highs::highs;
use good_lp::*;
use std::collections::{HashSet, VecDeque};
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

    for line in &data {
        let mut target: u64 = 0;
        let mut masks: Vec<u64> = Vec::new();

        let elements: Vec<&str> = line.split(" ").collect();
        for element in elements {
            // set target
            if element.chars().nth(0).unwrap() == '[' {
                for char in element.chars().rev() {
                    if char == '#' {
                        target |= 1;
                        target <<= 1;
                    } else if char == '.' {
                        target <<= 1;
                    }
                }
                target >>= 1;
            }

            // collect masks
            if element.chars().nth(0).unwrap() == '(' {
                let mut mask: u64 = 0;
                for char in element.chars() {
                    if char == ')' {
                        masks.push(mask);
                        break;
                    }
                    if char.is_digit(10) {
                        mask |= 1 << char.to_digit(10).unwrap();
                    }
                }
            }
        }

        // BFS
        let mut queue: VecDeque<(u64, Vec<usize>)> = VecDeque::new();
        let mut visited: HashSet<u64> = HashSet::new();

        queue.push_back((0, Vec::new()));
        visited.insert(0);

        while let Some((state, used)) = queue.pop_front() {
            if state == target {
                answer += used.len() as i64;
                break;
            }

            for (i, &mask) in masks.iter().enumerate() {
                let new_state = state ^ mask;
                if !visited.contains(&new_state) {
                    visited.insert(new_state);
                    let mut new_used = used.clone();
                    new_used.push(i);
                    queue.push_back((new_state, new_used));
                }
            }
        }
    }

    println!("PART 1: {:?}", answer);
    answer = 0;

    for line in &data {
        let mut target: Vec<i32> = Vec::new();
        let mut buttons: Vec<Vec<usize>> = Vec::new();

        let elements: Vec<&str> = line.split(" ").collect();
        for element in elements {
            // set target
            if element.chars().nth(0).unwrap() == '{' {
                let trimmed = &element[1..element.len() - 1];
                for number in trimmed.split(",") {
                    target.push(number.parse().unwrap());
                }
            }

            // collect masks
            if element.chars().nth(0).unwrap() == '(' {
                let mut button: Vec<usize> = Vec::new();
                for char in element.chars() {
                    if char == ')' {
                        buttons.push(button);
                        break;
                    }
                    if char.is_digit(10) {
                        button.push(char.to_digit(10).unwrap() as usize);
                    }
                }
            }
        }

        // ILP
        let n_dims = target.len();

        let mut problem = ProblemVariables::new();
        let vars: Vec<Variable> = (0..buttons.len())
            .map(|_| problem.add(variable().integer().min(0)))
            .collect();

        let objective: Expression = vars.iter().copied().sum();

        let mut solver = problem.minimise(objective).using(highs);

        for dim in 0..n_dims {
            let sum: Expression = buttons
                .iter()
                .zip(&vars)
                .filter(|(s, _)| s.contains(&dim))
                .map(|(_, &v)| v)
                .sum();
            solver = solver.with(constraint!(sum == target[dim]));
        }

        if let Ok(solution) = solver.solve() {
            let subtotal: i64 = vars.iter().map(|&v| solution.value(v).round() as i64).sum();
            answer += subtotal;
        } else {
            println!("ERRRRRRRRRRRRRR");
        }
    }

    println!("PART 2: {:?}", answer);
}
