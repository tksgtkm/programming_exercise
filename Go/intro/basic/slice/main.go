package main

import "fmt"

func main() {
	var nums [3]int = [3]int{1, 2, 3}

	fmt.Println(nums[0])

	fmt.Println(len(nums))

	fmt.Println(nums)

	// 変数の宣言と代入を同時に行う場合は:=演算子を使う
	hs := map[int]string{
		200: "OK",
		404: "not Found",
	}

	authors := make(map[string][]string)

	authors["Go"] = []string{"Robert Griesmer", "Rob Pike", "Ken Thompson"}

	status := hs[200]
	fmt.Println(status)

	fmt.Println(hs[0])

	status, ok := hs[304]

	fmt.Println(hs, ok)
}
