package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"
)

type Book struct {
	Title      string    `json:"title"`
	Authors    string    `json:"author"`
	Publisher  string    `json:"publisher"`
	ReleasedAt time.Time `json:"release_at"`
	ISBN       string    `json:"isbn"`
}

func useStruct() {
	var b Book

	b2 := Book{
		Title: "Twisted Network Programming Essentials",
	}

	b3 := &Book{
		Title: "カンフーマック――猛獣を飼いならす310の技",
	}

	fmt.Println(b)
	fmt.Println(b2)
	fmt.Println(b3)
}

func main() {
	f, err := os.Open("book.json")
	if err != nil {
		log.Fatal("file open error: ", err)
	}
	d := json.NewDecoder(f)
	var b Book
	d.Decode(&b)
	fmt.Println(b)
}
