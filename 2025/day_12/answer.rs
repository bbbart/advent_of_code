use std::collections::HashMap;
use std::convert::TryInto;
use std::env;
use std::fmt;
use std::fs::read_to_string;

fn read_input(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string());
    }

    result
}

#[derive(Debug)]
struct DFSState {
    area: Area,
    remaining: [u8; 6],
}

#[derive(Clone)]
struct Area {
    height: u8,
    width: u8,
    fields: Vec<u64>,
}

impl fmt::Debug for Area {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for i in 0..self.height {
            for j in (0..self.width).rev() {
                if self.fields[i as usize] & (1 << j) != 0 {
                    write!(f, "#")?;
                } else {
                    write!(f, ".")?;
                }
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

impl Area {
    fn available_space(&self) -> u32 {
        self.width as u32 * self.height as u32
            - self.fields.iter().map(|x| x.count_ones()).sum::<u32>()
    }

    fn fits_at(&self, shape: [u8; 3], x: u8, y: u8) -> bool {
        // (x,y) is the top left corner of the 3x3 bounding box of a shape
        [0, 1, 2].iter().all(|i| {
            self.fields
                .get((y + i) as usize)
                .map(|row| row & (shape[*i as usize] as u64) << (self.width - x - 3) == 0)
                .unwrap_or(false)
        })
    }

    fn place_at(&mut self, shape: [u8; 3], x: u8, y: u8) {
        // (x,y) is the top left corner of the 3x3 bounding box of a shape
        for i in 0..3u8 {
            let bits = (shape[i as usize] as u64) << (self.width - x - 3);
            self.fields[(y + i) as usize] |= bits;
        }
    }

    fn remove_from(&mut self, shape: [u8; 3], x: u8, y: u8) {
        // (x,y) is the top left corner of the 3x3 bounding box of a shape
        for i in 0..3u8 {
            let bits = (shape[i as usize] as u64) << (self.width - x - 3);
            self.fields[(y + i) as usize] ^= bits;
        }
    }

    // fn is_empty_at(&self, x: u8, y: u8) -> bool {
    //     self.fields[y as usize] & (1 << (self.width - x - 1)) == 0
    // }

    fn first_fit_for(&self, shape: [u8; 3]) -> Option<(u8, u8)> {
        for y in 0..self.height {
            for x in 0..=self.width - 3 {
                if self.fits_at(shape, x, y) {
                    return Some((x, y));
                }
            }
        }
        None
    }
}

#[derive(Debug)]
struct Shape {
    occupies: u8,
    orientations: Vec<[u8; 3]>,
}

impl Shape {
    fn new(chars: [[char; 3]; 3]) -> Shape {
        let mut orientations: Vec<[u8; 3]> = Vec::new();

        for rowfirst in [true, false] {
            for colreverse in [true, false] {
                let cols = if colreverse { [2, 1, 0] } else { [0, 1, 2] };
                for rowreverse in [true, false] {
                    let rows = if rowreverse { [2, 1, 0] } else { [0, 1, 2] };

                    let mut shape: Vec<u8> = Vec::new();
                    for i in rows {
                        let mut int: u8 = 0;
                        for j in cols {
                            let character: char = if rowfirst { chars[i][j] } else { chars[j][i] };
                            if character == '#' {
                                int |= 1;
                            }
                            int <<= 1
                        }
                        shape.push(int >> 1);
                    }
                    let sharray: [u8; 3] = shape.try_into().unwrap();
                    orientations.push(sharray);
                }
            }
        }
        orientations.sort();
        orientations.dedup();

        Shape {
            occupies: chars.iter().flatten().filter(|x| **x == '#').count() as u8,
            orientations: orientations,
        }
    }
}

fn dfs(state: &mut DFSState, shapes: &HashMap<u32, Shape>, shapes_order: &Vec<u32>) -> bool {
    if state.remaining.iter().map(|&x| x as u16).sum::<u16>() == 0 {
        return true;
    }

    if state.area.available_space()
        < state
            .remaining
            .iter()
            .enumerate()
            .map(|(i, x)| *x as u32 * shapes.get(&(i as u32)).unwrap().occupies as u32)
            .sum()
    {
        return false;
    }

    let shape_id = shapes_order
        .iter()
        .find(|x| state.remaining[**x as usize] > 0)
        .unwrap();
    let shape = shapes.get(shape_id);

    for orientation in &shape.unwrap().orientations {
        if let Some((x, y)) = state.area.first_fit_for(*orientation) {
            state.area.place_at(*orientation, x, y);
            state.remaining[*shape_id as usize] -= 1;

            if dfs(state, shapes, shapes_order) {
                return true;
            }

            state.remaining[*shape_id as usize] += 1;
            state.area.remove_from(*orientation, x, y);
        }
    }

    false
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let data = read_input(&args[1]);
    let mut answer: i64 = 0;

    let mut shape_id: Option<u32> = None;
    let mut shapes: HashMap<u32, Shape> = HashMap::new();
    let mut chars: Vec<[char; 3]> = Vec::with_capacity(3);

    for line in data {
        if line.is_empty() {
            let charray: [[char; 3]; 3] = chars.try_into().unwrap();
            shapes.insert(shape_id.unwrap(), Shape::new(charray));

            shape_id = None;
            chars = Vec::new();
            continue;
        }
        if !line.contains(":") {
            let mut linechars = line.chars();
            chars.push(std::array::from_fn(|_| linechars.next().unwrap()));
            continue;
        } else {
            shape_id = None;
            if !line.contains("x") {
                shape_id = line.chars().next().unwrap().to_digit(10);
                continue;
            } else {
                let parts: Vec<&str> = line.split(": ").collect();

                let (w, h) = parts[0].split_once("x").unwrap();
                let width: u8 = w.parse().unwrap();
                let height: u8 = h.parse().unwrap();
                let area: Area = Area {
                    height: height,
                    width: width,
                    fields: vec![0; height as usize],
                };

                let remaining: [u8; 6] = parts[1]
                    .split_whitespace()
                    .map(|x| x.parse::<u8>().unwrap())
                    .collect::<Vec<u8>>()
                    .try_into()
                    .unwrap();
                let mut state: DFSState = DFSState {
                    area: area,
                    remaining,
                };

                let mut shape_order: Vec<u32> = shapes.keys().cloned().collect::<Vec<u32>>();
                shape_order.sort_by_key(|x| shapes.get(x).unwrap().orientations.len());

                if dfs(&mut state, &shapes, &shape_order) {
                    answer += 1;
                }
            }
        }
    }

    println!("PART 1: {:?}", answer);
    answer = 0;

    println!("PART 2: {:?}", answer);
}
