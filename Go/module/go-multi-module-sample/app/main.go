package main

import (
	"fmt"

	"example.com/lib"
)

func main() {
	fmt.Println("Add:", lib.Add(10, 5))
	fmt.Println("Sub:", lib.Sub(10, 5))
}
