// mod npuzzle;
mod solver;
use solver::Solver;
//  #[path = "position.rs"] mod position;
// use npuzzle::position::{Pos, Direction};
use clap::{Arg, App};

struct Options {
	size: usize,
	shuffle: usize,
}

fn arg_parse() -> Options{
    let matches = App::new("N-Puzzle")
        .version("0.1.0")
        .author("Ezalos, Alikae")
        .about("Solver of N-Puzzles")
        .arg(Arg::with_name("size")
                 .short("s")
                 .long("size")
                 .takes_value(true)
                 .help("Generate a N-Puzzle of size s"))
        .arg(Arg::with_name("n-shuffle")
                 .short("n")
                 .long("n-shuffle")
                 .takes_value(true)
                 .help("Number of shuffle from solved state. 0 for full random"))
        .get_matches();

    let opt: Options = Options{
		size:    matches.value_of("size").unwrap_or("3").parse().unwrap(),
		shuffle: matches.value_of("n-shuffle").unwrap_or("1000").parse().unwrap(),
	};
	opt
}
// /!\ Do not explore twice the same state



fn main() {
    let opt = arg_parse();
	let mut b = solver::Npuzzle::gen_solution(opt.size);
	b.shuffle_n(opt.shuffle);
	println!("{}", b);
	let mut solver = Solver::new(b);
	solver.a_star();
}
