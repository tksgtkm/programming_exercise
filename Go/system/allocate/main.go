package main

import (
	"fmt"
	"log"
	"os"
	"runtime"
	"runtime/pprof"
	"strconv"
)

// allocate test
func waistSlice() {
	var a []int
	var lastPtr *int
	for i := 0; i < 10000; i++ {
		a = append(a, i)
		if &a[0] != lastPtr {
			fmt.Println(i)
		}
		lastPtr = &a[0]
	}
}

func waistMap() {
	a := make(map[string]int)
	for i := 0; i < 10000; i++ {
		a[strconv.FormatInt(int64(i), 10)] = i
	}
}

func alloc() {
	{
		f, err := os.Create("cpu.pprof")
		if err != nil {
			log.Fatal("could not create CPU profile: ", err)
		}
		// リソースの開放
		defer f.Close()
		if err := pprof.StartCPUProfile(f); err != nil {
			log.Fatal("could not start CPU profile: ", err)
		}
		defer pprof.StopCPUProfile()
	}
	{
		f, err := os.Create("mem.pprof")
		if err != nil {
			log.Fatal("could not create memory profile: ", err)
		}
		defer f.Close()
		runtime.GC()
		if err := pprof.WriteHeapProfile(f); err != nil {
			log.Fatal("could not write memory profile: ", err)
		}
	}

	// mallocみたいにメモリを確保する
	s1 := make([]int, 1000)
	// データの長さ
	fmt.Println(len(s1))
	// Go言語では実際のデータの長さより大きめのメモリ確保を行う
	fmt.Println(cap(s1))

	s2 := make([]int, 0, 1000)
	fmt.Println(len(s2))
	fmt.Println(cap(s2))

	m := make(map[string]string, 1000)
	fmt.Println(len(m))

	waistSlice()
	waistMap()
}

// Go言語がメモリを確保していく様子が見られる
func main() {
	alloc()
}
