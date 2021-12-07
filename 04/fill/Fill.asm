// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
// if KBD != 0 then goto BLACK, else goto WHITE
    @KBD
    D=M
    @BLACK
    D;JNE

(WHITE)
// value to be written to the pixels is 0
    @value
    M=0

// goto FILL
    @FILL
    0;JMP

(BLACK)
// value to be written to the pixels is -1
    @value
    M=-1

(FILL)
// n = 8192
    @8192
    D=A
    @n
    M=D

(LOOP)
// if n == -1 then goto START
    @n
    D=M
    @START
    D+1;JEQ

// n = n - 1
// A = SCREEN + n
    @n
    MD=M-1
    @SCREEN
    D=A+D
    @R0
    M=D

// Load value to be written to the pixels
    @value
    D=M

// Load address of the pixels
    @R0
    A=M

// Write value to the pixels
    M=D

// goto LOOP
    @LOOP
    0;JMP