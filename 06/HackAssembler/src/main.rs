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

fn split_c_instruction(instruction: &str) -> (&str, &str, &str) {
    if instruction.split("=").count() == 2 {
        let dest = instruction.split("=").nth(0).unwrap_or_default();
        let comp = instruction.split("=").nth(1).unwrap_or_default().split(";").nth(0).unwrap();
        let jmp = instruction.split(";").nth(1).unwrap_or_default();

        return (dest, comp, jmp);
    } else {
        let dest = "";
        let comp = instruction.split(";").nth(0).unwrap();
        let jmp = instruction.split(";").nth(1).unwrap_or_default();

        return (dest, comp, jmp);
    }
}

fn process_c_instruction(instruction: &str) -> String {
    let mut result = String::from("111");

    let (dest, mut comp, jmp) = split_c_instruction(instruction);

    // a bit
    if comp.contains("M") {
        result.push_str("1");
    } else {
        result.push_str("0");
    }

    let new_comp = comp.replace("M", "A");
    comp = &new_comp;

    // c bits
    match comp {
        "0" => result.push_str("101010"),
        "1" => result.push_str("111111"),
        "-1" => result.push_str("111010"),
        "D" => result.push_str("001100"),
        "A" => result.push_str("110000"),
        "!D" => result.push_str("001101"),
        "!A" => result.push_str("110001"),
        "-D" => result.push_str("001111"),
        "-A" => result.push_str("110011"),
        "D+1" => result.push_str("011111"),
        "A+1" => result.push_str("110111"),
        "D-1" => result.push_str("001110"),
        "A-1" => result.push_str("110010"),
        "D+A" => result.push_str("000010"),
        "D-A" => result.push_str("010011"),
        "A-D" => result.push_str("000111"),
        "D&A" => result.push_str("000000"),
        "D|A" => result.push_str("010101"),
        _ => panic!("Unknown comp: {}", comp)
    }

    // dest bits
    if dest.contains("A") {
        result.push_str("1");
    } else {
        result.push_str("0");
    }

    if dest.contains("D") {
        result.push_str("1");
    } else {
        result.push_str("0");
    }

    if dest.contains("M") {
        result.push_str("1");
    } else {
        result.push_str("0");
    }

    // jmp bits
    match jmp {
        "" => result.push_str("000"),
        "JGT" => result.push_str("001"),
        "JEQ" => result.push_str("010"),
        "JGE" => result.push_str("011"),
        "JLT" => result.push_str("100"),
        "JNE" => result.push_str("101"),
        "JLE" => result.push_str("110"),
        "JMP" => result.push_str("111"),
        _ => panic!("Unknown jmp: {}", jmp)
    }

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

    Some(process_c_instruction(line))
}

fn process_file(args: &Args) -> io::Result<()> {
    let (reader, mut writer) = get_reader_and_writer(args)?;

    for line in reader.lines() {
        let line = line?;
        
        process_line(&line);

        if let Some(instruction) = process_line(&line) {
            // println!("{:?}", instruction);

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
