use std::collections::HashMap;
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
    let mut answer: i64;

    let mut graph: HashMap<String, Vec<String>> = HashMap::new();

    for line in &data {
        let fromto: Vec<&str> = line.split(": ").collect();
        let from = fromto.get(0).unwrap().to_string();
        let tos = graph.entry(from.clone()).or_insert(Vec::new());
        for to in fromto.get(1).unwrap().split(" ") {
            tos.push(to.to_string());
        }
    }

    fn count_dfs(
        graph: &HashMap<String, Vec<String>>,
        current: String,
        end: String,
        memo: &mut HashMap<String, Option<usize>>,
    ) -> usize {
        if current == end {
            return 1;
        }
        if let Some(Some(count)) = memo.get(&current) {
            return *count;
        }

        let count = graph[&current]
            .iter()
            .map(|neighbour| count_dfs(graph, neighbour.clone(), end.clone(), memo))
            .sum();

        memo.insert(current, Some(count));
        count
    }

    let mut memo: HashMap<String, Option<usize>> = HashMap::new();
    answer = count_dfs(&graph, "you".to_string(), "out".to_string(), &mut memo) as i64;
    println!("PART 1: {:?}", answer);

    fn count_correct_dfs(
        graph: &HashMap<String, Vec<String>>,
        current: String,
        end: String,
        required: (String, String),
        seen: (bool, bool),
        memo: &mut HashMap<(String, bool, bool), usize>,
    ) -> usize {
        if current == end {
            return if seen.0 && seen.1 { 1 } else { 0 };
        }

        let key = (current.clone(), seen.0, seen.1);
        if let Some(&count) = memo.get(&key) {
            return count;
        }

        let count = graph
            .get(&current)
            .map(|neighbours| {
                neighbours
                    .iter()
                    .map(|neighbour| {
                        let new_seen = (
                            seen.0 || neighbour == &required.0,
                            seen.1 || neighbour == &required.1,
                        );
                        count_correct_dfs(
                            graph,
                            neighbour.clone(),
                            end.clone(),
                            required.clone(),
                            new_seen,
                            memo,
                        )
                    })
                    .sum()
            })
            .unwrap_or(0);

        memo.insert(key, count);
        count
    }

    let mut memo: HashMap<(String, bool, bool), usize> = HashMap::new();
    let seen = (false, false);
    answer = count_correct_dfs(
        &graph,
        "you".to_string(),
        "out".to_string(),
        ("dac".to_string(), "fft".to_string()),
        seen,
        &mut memo,
    ) as i64;
    println!("PART 2: {:?}", answer);
}
