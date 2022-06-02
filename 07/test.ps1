$tests = "MemoryAccess/BasicTest", "MemoryAccess/PointerTest", "MemoryAccess/StaticTest", "StackArithmetic/SimpleAdd", "StackArithmetic/StackTest"

foreach ($test in $tests) {
    Write-Output "============================================="
    Write-Output "Running test $test"

    $parts = $test.Split('/')

    $vmPath = [IO.Path]::Combine($parts[0], $parts[1], "$($parts[1]).vm")
    $tstPath = [IO.Path]::Combine($parts[0], $parts[1], "$($parts[1]).tst")

    python .\VMTranslator\VMTranslator.py $vmPath

    ..\..\tools\CPUEmulator.bat $tstPath
}