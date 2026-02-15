package main

import (
	"log"
	"strings"
)

func main() {
	src := []string{"Back", "To", "The", "Future", "Part", "III"}
	var title string
	for i, word := range src {
		if i != 0 {
			title += " "
		}
		title += word
	}
	log.Println(title)

	displayTitle := "1990年7月6日公開 - " + title + " - ロバート・ゼメキス"
	log.Println(displayTitle)

	var builder strings.Builder
	builder.Grow(100)
	for i, word := range src {
		if i != 0 {
			builder.WriteByte(' ')
		}
		builder.WriteString(word)
	}
	log.Println(builder.String())
}
