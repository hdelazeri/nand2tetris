#!/bin/bash

TESTS=("MemoryAccess/BasicTest" "MemoryAccess/PointerTest" "MemoryAccess/StaticTest" "StackArithmetic/SimpleAdd" "StackArithmetic/StackTest")

for test in "${TESTS[@]}"
do
    echo "Running test $test"
    
    BASE=$(basename $test)

    python ./VMTranslator/VMTranslator.py "./$test/$BASE.vm"

    ../../tools/CPUEmulator.sh "./$test/$BASE.tst"
done