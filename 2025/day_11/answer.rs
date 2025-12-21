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

    fn count_valid_dfs(
        graph: &HashMap<String, Vec<String>>,
        current: String,
        end: &str,
        mut valid_path: (bool, bool),
        memo: &mut HashMap<(String, (bool, bool)), Option<usize>>,
    ) -> usize {
        if current == end {
            if valid_path == (true, true) {
                return 1;
            } else {
                return 0;
            }
        }

        if let Some(Some(count)) = memo.get(&(current.clone(), valid_path)) {
            return *count;
        }

        if current == "dac" {
            valid_path.0 = true;
        }
        if current == "fft" {
            valid_path.1 = true;
        }

        let count = graph[&current]
            .iter()
            .map(|neighbour| {
                count_valid_dfs(graph, neighbour.clone(), end, valid_path, memo)
            })
            .sum();

        memo.insert((current, valid_path), Some(count));
        count
    }

    let mut memo: HashMap<(String, (bool, bool)), Option<usize>> = HashMap::new();
    let valid_path = (false, false);
    answer = count_valid_dfs(
        &graph,
        "svr".to_string(),
        "out",
        valid_path,
        &mut memo,
    ) as i64;

    println!("PART 2: {:?}", answer);
}
