use std::collections::{BTreeSet, BinaryHeap, HashMap, HashSet};
use std::env;
use std::fs::read_to_string;

fn read_input(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string());
    }

    result
}

fn distance(a: (usize, i64, i64, i64), b: (usize, i64, i64, i64)) -> i64 {
    // sqrt can be ignored, we only need relative distances
    (a.1 - b.1).pow(2) + (a.2 - b.2).pow(2) + (a.3 - b.3).pow(2)
}

fn find(parent: &mut HashMap<usize, usize>, x: usize) -> usize {
    let p = *parent.entry(x).or_insert(x);
    if p != x {
        let root = find(parent, p);
        parent.insert(x, root);
        root
    } else {
        x
    }
}

fn union(parent: &mut HashMap<usize, usize>, x: usize, y: usize) {
    let ra = find(parent, x);
    let rb = find(parent, y);
    if ra != rb {
        parent.insert(ra, rb);
    }
}

fn merge_sets(pairs: Vec<HashSet<usize>>) -> Vec<HashSet<usize>> {
    let mut parent: HashMap<usize, usize> = HashMap::new();

    for set in &pairs {
        let items: Vec<_> = set.iter().cloned().collect();
        for i in 1..items.len() {
            union(&mut parent, items[0], items[i]);
        }
    }

    let mut groups: HashMap<usize, HashSet<usize>> = HashMap::new();
    for set in &pairs {
        for &item in set {
            let root = find(&mut parent, item);
            groups.entry(root).or_default().insert(item);
        }
    }

    groups.into_values().collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let data = read_input(&args[1]);
    let mut answer: i64;
    let mut max_connections: usize = 1000;

    let mut boxes: Vec<(usize, i64, i64, i64)> = Vec::new();
    for i in 0..data.len() {
        let line = &data[i];

        let mut cos = line.split(',');
        boxes.push((
            i,
            cos.next().unwrap().parse().unwrap(),
            cos.next().unwrap().parse().unwrap(),
            cos.next().unwrap().parse().unwrap(),
        ))
    }

    let mut distances: BTreeSet<(i64, (usize, usize))> = BTreeSet::new();
    for i in 0..boxes.len() {
        for j in (i + 1)..boxes.len() {
            distances.insert((distance(boxes[i], boxes[j]), (boxes[i].0, boxes[j].0)));
        }
    }

    let mut pairs: Vec<HashSet<usize>> = Vec::new();
    for (_, pair) in distances.iter().take(max_connections) {
        pairs.push(HashSet::from([pair.0, pair.1]));
    }

    let mut topthree: BinaryHeap<i64> = BinaryHeap::new();
    for group in merge_sets(pairs) {
        topthree.push(-(group.len() as i64));
        if topthree.len() > 3 {
            topthree.pop();
        }
    }

    answer = topthree.into_iter().fold(-1, |a, b| -a * -b);
    println!("PART 1: {:?}", answer);

    max_connections = 1;
    loop {
        // this can be done more efficiently: just pop_left a distance in every loop and add it to
        // pairs - we then also get a wat to check if we have exhausted all possible connections
        // without forming a single large network (which is completely missing in this
        // implementation)
        pairs = Vec::new();
        for (_, pair) in distances.iter().take(max_connections) {
            pairs.push(HashSet::from([pair.0, pair.1]));
        }

        // this is of course also inredibly naive: we do the entire merge process every time, just
        // for one more pair... however, my computer seems fast enough to handle this :-D
        let groups = merge_sets(pairs);

        if groups[0].len() == boxes.len() {
            let last_connection = distances.iter().nth(max_connections - 1).unwrap().1;
            answer = boxes[last_connection.0].1 * boxes[last_connection.1].1;
            break;
        }

        max_connections += 1;
    }

    println!("PART 2: {:?}", answer);
}
