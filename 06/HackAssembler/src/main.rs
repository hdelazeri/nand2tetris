use clap::Parser;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::Path;

/// Simple assembler for the Hack computer of the Nand2Tetris course.
#[derive(Parser, Debug)]
#[clap(about, version, author)]
struct Args {
    /// Path to the input file
    input: String,
    /// Path to the output file
    output: Option<String>
}

fn get_reader_and_writer(args: &Args) -> io::Result<(BufReader<File>, BufWriter<File>)> {
    let file = File::open(&args.input)?;
    let reader = BufReader::new(file);

    let file = match &args.output {
        Some(filename) => File::create(filename)?,
        None => File::create(Path::new(&args.input).with_extension("hack"))?
    };
    let writer = BufWriter::new(file);

    return Ok((reader, writer));
}

fn process_a_instruction(instruction: &str) -> String {
    let mut result = String::from("0");

    let instruction = instruction.replace("@", "");

    let value = instruction.parse::<u16>().unwrap();

    result.push_str(&format!("{:015b}", value));

    result
}

fn process_line(line: &str) -> Option<String> {
    let line = line.trim();

    if line.starts_with("//") {
        return None;
    }

    if line.is_empty() {
        return None;
    }

    if line.starts_with("@") {
        return Some(process_a_instruction(line));
    }

    Some(line.to_string())
}

fn process_file(args: &Args) -> io::Result<()> {
    let (reader, mut writer) = get_reader_and_writer(args)?;

    for line in reader.lines() {
        let line = line?;
        
        process_line(&line);

        if let Some(instruction) = process_line(&line) {
            println!("{:?}", instruction);

            writer.write(instruction.as_bytes())?;
            writer.write("\n".as_bytes())?;
        }
    }

    Ok(())
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    process_file(&args)?;

    Ok(())
}
