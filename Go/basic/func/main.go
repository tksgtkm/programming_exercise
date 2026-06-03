package main

import (
	"errors"
	"fmt"
	"io"
	"os"
	"time"
)

func calc(x, y int) int {
	return x + y
}

func calcAge(y int, m time.Month, d int) (age int, err error) {
	b := time.Date(y, m, d, 0, 0, 0, 0, time.Local)
	n := time.Now()
	if b.After(n) {
		err = errors.New("誕生日が未来です")
		return
	}
	for {
		b = time.Date(y+age+1, m, d, 0, 0, 0, 0, time.Local)
		if b.After(n) {
			return
		}
		age++
	}
}

func doCalc(x, y int, f func(int, int) int) {
	fmt.Println()
}

func main() {
	fmt.Println(calcAge(1980, time.November, 14))
	m := func(x, y int) int {
		return x * y
	}

	doCalc(10, 20, m)

	doCalc(10, 10, func(x, y int) int {
		return x * y
	})

	fmt.Println(m(1, 2))

	f, err := os.Create("sample.txt")
	if err != nil {
		fmt.Println("err", err)
		return
	}
	defer f.Close()
	io.WriteString(f, "hello world")
}
