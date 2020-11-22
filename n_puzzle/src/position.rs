use rand::thread_rng;
use rand::Rng;
use std::fmt;

#[derive(Copy, Clone, PartialEq)]
pub enum Direction {
	RIGHT,
	DOWN,
	LEFT,
	UP,
}

#[derive(Copy, Clone)]
pub struct Pos {
	pub x: usize,
	pub y: usize,
}

impl std::ops::Add<Direction> for Pos {
    type Output = Self;

    fn add(self, dir: Direction) -> Self {
		// UNSAFE
		let (x, y): (isize, isize) = match dir {
			Direction::UP => (1, 0),
			Direction::DOWN => (-1, 0),
			Direction::LEFT => (0, -1),
			Direction::RIGHT => (0, 1),
		};
        Self {
			x: (self.x as isize + x) as usize,
			y: (self.y as isize + y) as usize,
        }
    }
}

impl Direction {
	pub fn invert(dir: Direction)-> Direction{
		match dir {
			Direction::UP => Direction::DOWN,
			Direction::DOWN => Direction::UP,
			Direction::LEFT => Direction::RIGHT,
			Direction::RIGHT => Direction::LEFT,
		}
	}
}

pub fn rand_move_vec(size: usize)-> Vec<Direction>{
	let shuffle_size = size;
	let mut vec_dir: Vec<Direction> = vec![];
	let mut rng = thread_rng();
	for _i in 0.. shuffle_size{
		let dir = rng.gen_range(0, 4);
		match dir {
			0 => vec_dir.push(Direction::UP),
			1 => vec_dir.push(Direction::DOWN),
			2 => vec_dir.push(Direction::LEFT),
			3 => vec_dir.push(Direction::RIGHT),
			_ => (),
		}
	};
	vec_dir
}

impl fmt::Debug for Direction {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		match self {
			Direction::UP    => write!(f, "^"),
			Direction::DOWN  => write!(f, "v"),
			Direction::LEFT  => write!(f, "<"),
			Direction::RIGHT => write!(f, ">"),
		}
    }
}
