package main

import (
	"example.com/go-module-sample/calc"
	"example.com/go-module-sample/printer"
)

func main() {
	result1 := calc.Add(10, 5)
	result2 := calc.Sub(10, 5)

	printer.PrintResult("Add: ", result1)
	printer.PrintResult("Sub: ", result2)
}
