package printer

import "fmt"

func PrintResult(label string, value int) {
	fmt.Printf("%s: %d\n", label, value)
}
