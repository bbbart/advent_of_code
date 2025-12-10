use std::cmp::Reverse;
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

    let mut tiles: Vec<(i64, i64)> = Vec::new();
    for line in data {
        let cos: Vec<i64> = line.split(',').map(|x| x.parse().unwrap()).collect();
        tiles.push((cos[0], cos[1]));
    }

    let mut largest_area = i64::MIN;
    for i in 0..tiles.len() {
        for j in (i + 1)..tiles.len() {
            largest_area = largest_area.max(
                ((tiles[i].0 - tiles[j].0).abs() + 1) * ((tiles[i].1 - tiles[j].1 + 1).abs() + 1),
            );
        }
    }

    answer = largest_area;
    println!("PART 1: {:?}", answer);

    let n = tiles.len();

    let mut horizontal_edges: Vec<(i64, i64, i64)> = Vec::new();
    let mut vertical_edges: Vec<(i64, i64, i64)> = Vec::new();

    for i in 0..n {
        let (x1, y1) = tiles[i];
        let (x2, y2) = tiles[(i + 1) % n];

        if y1 == y2 {
            let (x_min, x_max) = if x1 < x2 { (x1, x2) } else { (x2, x1) };
            horizontal_edges.push((x_min, x_max, y1));
        }
        if x1 == x2 {
            let (y_min, y_max) = if y1 < y2 { (y1, y2) } else { (y2, y1) };
            vertical_edges.push((x1, y_min, y_max));
        }
    }

    let mut pairs: Vec<(usize, usize)> = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            pairs.push((i, j))
        }
    }

    pairs.sort_by_key(|&(i, j)| {
        Reverse(((tiles[i].0 - tiles[j].0).abs() + 1) * ((tiles[i].1 - tiles[j].1 + 1).abs() + 1))
    });

    // this produces the correct answer to the puzzle (for my input)
    // but I'm quite sure its not entirely correct: I believe it does not take into account every
    // possible shape of red and green tiles...
    //
    // also: it's really slow :-)
    largest_area = i64::MIN;
    for (i, j) in pairs {
        let x_min = tiles[i].0.min(tiles[j].0);
        let x_max = tiles[i].0.max(tiles[j].0);
        let y_min = tiles[i].1.min(tiles[j].1);
        let y_max = tiles[i].1.max(tiles[j].1);
        let mut good_pairing = true;
        for y in y_min..=y_max {
            let mut x_crossings: Vec<i64> = vertical_edges
                .iter()
                .filter(|&&(_, e_y_min, e_y_max)| e_y_min <= y && y <= e_y_max)
                .map(|&(x, _, _)| x)
                .collect();
            x_crossings.sort();
            if x_crossings.first().unwrap_or(&i64::MIN) > &x_min
                || x_crossings.last().unwrap_or(&i64::MAX) < &x_max
            {
                good_pairing = false;
                break;
            }
        }
        if good_pairing {
            largest_area = largest_area.max((x_max - x_min + 1) * (y_max - y_min + 1));
            break;
        }
    }

    answer = largest_area;
    println!("PART 2: {:?}", answer);
}
