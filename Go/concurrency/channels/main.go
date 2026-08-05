package main

/*
チャネル型は、チャネルオペレーターの<-を用いて値の送受信ができる通り道

ch <- v // vをチャネルchへ送信する
v := <-ch // chから受信した変数をvへ割り当てる

マップとスライスのようにチャネルは使う前に以下のように生成する
ch := make(chan int)
*/

import "fmt"

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum
}

func main() {
	s := []int{7, 2, 8, -9, 4, 0}

	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)
	x, y := <-c, <-c

	fmt.Println(x, y, x+y)
}
