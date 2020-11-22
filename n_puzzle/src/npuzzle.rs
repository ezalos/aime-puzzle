/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   npuzzle.rs                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalos <ezalos@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/11/22 13:22:28 by ezalos            #+#    #+#             */
/*   Updated: 2020/11/22 21:58:58 by ezalos           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#[path = "position.rs"] pub mod position;
pub use position::{Pos, Direction, rand_move_vec};

use std::fmt;
use rand::thread_rng;
use rand::seq::SliceRandom;

pub type Tint = u16;

#[derive(Clone)]
pub struct Npuzzle {
	pub size: usize,
	pub puzzle: Vec<Vec<Tint>>,
	pub historic: Vec<Direction>,
	pub zero: Pos,
	pub cost: usize,
}

impl Npuzzle {
	pub fn new(size: usize)-> Npuzzle {
		let mut puzzle = Npuzzle {
			size,
			puzzle: vec![vec![0; size]; size],
			historic: vec![],
			zero: Pos {
				x: size / 2,
				y: (size - 1) / 2,
			},
			cost: 0,
		};

		let mut rng = thread_rng();
		let mut vec: Vec<Tint> = vec![];
		for i in 0..size * size {
		    vec.push(i as Tint);
		}
		vec.shuffle(&mut rng);

		let mut x = 0;
		while x < size
		{
			let mut y = 0;
			while y < size
			{
				puzzle.puzzle[x][y] = vec[x * size + y];
				if puzzle.puzzle[x][y] == 0{
					puzzle.zero.x = x;
					puzzle.zero.y = y;
				}
				y += 1;
			}
			x += 1;
		};
		puzzle
	}

	fn valid_pos(&self, pos: &Pos)-> bool{
		pos.x < self.size && pos.y < self.size
	}

	fn fill_line(&mut self, pos: Pos, dir: Direction) -> Pos {
		let mut prev = pos;
		let mut next = pos + dir;
		while self.valid_pos(&next) && self.puzzle[next.x][next.y] == 0
		{
			self.puzzle[next.x][next.y] = self.puzzle[prev.x][prev.y] + 1;
			prev = next;
			next = prev + dir;
		}
		prev
	}

	pub fn gen_solution(size: usize)-> Npuzzle {
		let mut puzzle = Npuzzle {
			size,
			puzzle: vec![vec![0; size]; size],
			historic: vec![],
			zero: Pos {
				x: size / 2,
				y: (size - 1) / 2,
			},
			cost: 0,
		};
		let mut pos = Pos {x: 0, y:0};
		if size > 1 {
			puzzle.puzzle[pos.x][pos.y] = 1;
		}
		while puzzle.puzzle[pos.x][pos.y] < ((size * size) - 1) as Tint {
			pos = puzzle.fill_line(pos, Direction::RIGHT);
			pos = puzzle.fill_line(pos, Direction::DOWN);
			pos = puzzle.fill_line(pos, Direction::LEFT);
			pos = puzzle.fill_line(pos, Direction::UP);
		}
		puzzle
	}

	pub fn swap(&mut self, from: Pos, to: Pos) {
		// UNSAFE NOW
		let tmp = self.puzzle[from.x][from.y];
		self.puzzle[from.x][from.y] = self.puzzle[to.x][to.y];
		self.puzzle[to.x][to.y] = tmp;
	}

	pub fn move_zero(&mut self, dir: Direction) {
		let new_zero = self.zero + dir;
		let zero = self.zero;
		if self.valid_pos(&new_zero){
			self.swap(zero, new_zero);
			self.zero = new_zero;
			self.historic.push(dir);
		}
	}

	pub fn apply_moves(&mut self, moves: Vec<Direction>) {
		for step in &moves {
			self.move_zero(*step);
			// print!("{}[5;0H", 27 as char);
			// print!("{}", self);
		}
	}

	pub fn shuffle_n(&mut self, size: usize){
		self.apply_moves(rand_move_vec(size));
		self.historic = vec![];
	}
}


impl fmt::Display for Npuzzle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		let sol = Npuzzle::gen_solution(self.size);

		let max: f64 = self.size as f64 * self.size as f64;
		let width = (max.log(10.0) + 1.0) as usize;
		let mut x = 0;
		while x < self.size {
			let mut y = 0;
			while y < self.size {
				let case = self.puzzle[x][y];

				if case == 0 {
					print!("{}[94m", 27 as char);
				}
				else if case == sol.puzzle[x][y]{
					print!("{}[92m", 27 as char);
				}
				else{
					print!("{}[91m", 27 as char);
				}
				write!(f, "{:width$} ", case, width=width);
				print!("{}[0m", 27 as char);
				y += 1;
			}
			x += 1;
			write!(f, "\n");
		}
		// print!("{:?}", self.historic);
		write!(f, "\n")
    }
}
