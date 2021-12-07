// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// a = R[0]
    @R0
    D=M
    @a
    M=D

// b = R[1]
    @R1
    D=M
    @b
    M=D

// sum = 0
    @sum
    M=0

(LOOP)
// if b == 0 goto FINISH
    @b
    D=M
    @FINISH
    D;JEQ

// sum = sum + a
    @sum
    D=M
    @a
    D=D+M
    @sum
    M=D

// b = b - 1
    @b
    M=M-1

// Back to start of loop
    @LOOP
    0;JMP

(FINISH)
    @sum
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP