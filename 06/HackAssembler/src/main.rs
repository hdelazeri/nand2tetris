use clap::Parser;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use regex::Regex;

/// Simple assembler for the Hack computer of the Nand2Tetris course.
#[derive(Parser, Debug)]
#[clap(about, version, author)]
struct Args {
    /// Path to the input file
    input: String,
    /// Path to the output file
    output: Option<String>
}

static mut FIRST_FREE: u16 = 16;

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

fn process_a_instruction(instruction: &str, symbol_table: &mut HashMap<String, u16>) -> String {
    let mut result = String::from("0");

    let instruction = instruction.replace("@", "");

    let value = match instruction.parse::<u16>() {
        Ok(value) => value,
        Err(_) => {
            unsafe {
                let value = match symbol_table.get(&instruction) {
                    Some(value) => *value,
                    None => {
                        let value = FIRST_FREE;
                        
                        symbol_table.insert(String::from(&instruction), FIRST_FREE);

                        FIRST_FREE += 1;

                        value
                    }
                };

                value
            }
        }
    };

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

fn process_line(line: &str, symbol_table: &mut HashMap<String, u16>) -> Option<String> {
    if line.starts_with("@") {
        return Some(process_a_instruction(line, symbol_table));
    }

    Some(process_c_instruction(line))
}

fn initialize_symbol_table(symbol_table: &mut HashMap<String, u16>){
    symbol_table.insert(String::from("R0"), 0);
    symbol_table.insert(String::from("R1"), 1);
    symbol_table.insert(String::from("R2"), 2);
    symbol_table.insert(String::from("R3"), 3);
    symbol_table.insert(String::from("R4"), 4);
    symbol_table.insert(String::from("R5"), 5);
    symbol_table.insert(String::from("R6"), 6);
    symbol_table.insert(String::from("R7"), 7);
    symbol_table.insert(String::from("R8"), 8);
    symbol_table.insert(String::from("R9"), 9);
    symbol_table.insert(String::from("R10"), 10);
    symbol_table.insert(String::from("R11"), 11);
    symbol_table.insert(String::from("R12"), 12);
    symbol_table.insert(String::from("R13"), 13);
    symbol_table.insert(String::from("R14"), 14);
    symbol_table.insert(String::from("R15"), 15);
    symbol_table.insert(String::from("SP"), 0);
    symbol_table.insert(String::from("LCL"), 1);
    symbol_table.insert(String::from("ARG"), 2);
    symbol_table.insert(String::from("THIS"), 3);
    symbol_table.insert(String::from("THAT"), 4);
    symbol_table.insert(String::from("SCREEN"), 16384);
    symbol_table.insert(String::from("KBD"), 24576);
}

fn locate_labels(lines: &Vec<String>, symbol_table: &mut HashMap<String, u16>) -> Vec<String> {
    let mut new_lines= Vec::new();
    let mut label_count = 0;

    for i in 0..lines.len() {
        let line = lines.get(i).unwrap();

        if line.starts_with("(") {
            let label = line.split("(").nth(1).unwrap_or_default().split(")").nth(0).unwrap();
            symbol_table.insert(String::from(label), (i - label_count) as u16);
            label_count += 1;
        } else {
            new_lines.push(line.to_string());
        }
    }

    new_lines
}

fn remove_whitespace(lines: &Vec<String>) -> Vec<String> {
    let mut new_lines = Vec::new();

    let comment_regex = Regex::new(r"//.*").unwrap();

    for line in lines {
        let line = comment_regex.replace(line, "");

        let line = line.trim();

        if line.starts_with("//") {
            continue;
        }

        if line.is_empty() {
            continue;
        }

        new_lines.push(line.to_string());
    }

    new_lines
}

fn process_file(args: &Args) -> io::Result<()> {
    let (reader, mut writer) = get_reader_and_writer(args)?;

    let mut symbol_table = HashMap::new();
    initialize_symbol_table(&mut symbol_table);

    let lines = reader.lines().collect::<Result<Vec<_>, _>>()?;
    let lines = remove_whitespace(&lines);
    let lines = locate_labels(&lines, &mut symbol_table);

    for line in lines {
        if let Some(instruction) = process_line(&line, &mut symbol_table) {
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
