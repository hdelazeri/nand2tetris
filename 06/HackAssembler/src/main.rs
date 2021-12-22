use clap::Parser;

/// Simple assembler for the Hack computer of the Nand2Tetris course.
#[derive(Parser, Debug)]
#[clap(about, version, author)]
struct Args {
    /// Path to the input file
    input: String,
    /// Path to the output file
    output: Option<String>
}

fn main() {
    let args = Args::parse();

    println!("{:?}", args);
}
