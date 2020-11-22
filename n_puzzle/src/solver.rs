#[path = "npuzzle.rs"] mod npuzzle;
use dict::{ Dict, DictIface };
pub use npuzzle::*;
// #[path = "position.rs"] pub mod position;
// use position::{Pos, Direction, rand_move_vec};

pub struct Solver {
	pub npuzzle_origin: Npuzzle,
	pub queue: Vec<Npuzzle>,
	pub solution: Npuzzle,
	pub index_map: Vec<Pos>,
	pub state_dict: Dict<String>,
}

impl Solver {
	pub fn new(puzzle: Npuzzle)-> Solver {
		let mut solver = Solver {
			npuzzle_origin: puzzle.clone(),
			queue: vec![puzzle.clone()],
			solution: Npuzzle::gen_solution(puzzle.size),
			index_map: vec![Pos{x: 0, y:0}; puzzle.size * puzzle.size],
			state_dict: Dict::<String>::new(),
		};
		let mut x = 0;
		while x < solver.solution.size
		{
			let mut y = 0;
			while y < solver.solution.size
			{
				solver.index_map[solver.solution.puzzle[x][y] as usize] = Pos {x, y};
				y += 1;
			}
			x += 1;
		};
		solver
	}

	fn print_queue(queue: &Vec<Npuzzle>, max: usize, min: usize, spot: usize) {
		let mut i = 0;
		print!("Len: {}, Max: {}, Min: {}, Spot: {}\n", queue.len(), max, min, spot);
		while i < queue.len() {
			if spot == i {
				print!("{}[94m", 27 as char);
			}
			else if min == i {
				print!("{}[91m", 27 as char);
			}
			else if max == i {
				print!("{}[92m", 27 as char);
			}
			print!("{} ", queue[i].cost);
			print!("{}[0m", 27 as char);
			i += 1;
		}
		print!("\n\n");
	}

	fn save_state(&mut self, state: Npuzzle){
		let mut min: usize = 0;
		let mut max: usize = self.queue.len();

		if max > 0 {
			max -= 1;
		}
		let mut spot: usize = ((max - min) / 2) + min;
		// print!("In: {} \n", state.cost);
		// Solver::print_queue(&self.queue, max, min, spot);
		while max - min > 1 && self.queue[max].cost < self.queue[min].cost {
			if self.queue[spot].cost < state.cost {
				max = spot;
			} else if self.queue[spot].cost > state.cost {
				min = spot;
			} else {
				break ;
			}
			spot = ((max - min) / 2) + min;
			// Solver::print_queue(&self.queue, max, min, spot);
		}
		// print!("Choice: \n");
		// Solver::print_queue(&self.queue, max, min, spot);
		let mut s = String::new();
		for x in 0.. state.size{
			for y in 0.. state.size{
				s.push_str(&state.puzzle[x][y].to_string())
			}
		}
		match self.state_dict.get(&s) {
			Some(_) => (),
			None => {
				self.state_dict.add(s, "".to_string());
				if self.queue.len() > 0 && state.cost < self.queue[spot].cost{
					self.queue.insert(spot + 1, state);
				} else {
					self.queue.insert(spot, state);
				}
			},
		}
		// print!("\n");
	}

	fn cost(&mut self, state: &Npuzzle) -> usize {
		let mut cost : usize = 0;
		let mut x  = 0;
		while x < state.size {
			let mut y = 0;
			while y < state.size {
				if state.puzzle[x][y] != 0 {
					let pos = self.index_map[state.puzzle[x][y] as usize];
					let hort = if x > pos.x { x - pos.x } else { pos.x - x };
					let vert = if y > pos.y { y - pos.y } else { pos.y - y };
					cost += hort + vert;
				}
				y += 1;
			}
			x += 1;
		}
		cost + state.historic.len()
	}

	pub fn a_star(&mut self) {
		let mut i = 0;
		loop {
			let state = self.queue.pop().unwrap();
			print!("{}[5;0H", 27 as char);
			print!("\nIteration: {} \n", i);
			i += 1;
			print!("{}", state);
			print!("Cost: {} \n", state.cost);

			for dir in &[Direction::UP, Direction::DOWN, Direction::LEFT, Direction::RIGHT]{
				// print!("Dir proposed\n");
				if state.historic.len() == 0 || *dir != Direction::invert(*state.historic.last().unwrap()){
					let mut child = state.clone();
					child.move_zero(*dir);
					child.cost = self.cost(&child);
					// print!("Child created with cost {}\n", child.cost);
					if child.puzzle == self.solution.puzzle {
						print!("Game Over!\n{}\n", child);
						return ;
					}
					self.save_state(child);
				}
			// if self.queue.len() > 10 {
			// 	return ;
			// }
			}
			print!("Queue len: {:?} \n", self.queue.len());
		}
	}
}
