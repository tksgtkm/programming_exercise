package main

import (
	"fmt"
	"time"
)

func addDate() {
	jst, _ := time.LoadLocation("Asia/Tokyo")
	now := time.Date(2026, 2, 8, 16, 46, 00, 000, jst)
	nextMonth := now.AddDate(0, 1, 0)
	fmt.Println(nextMonth)

	normal := time.Date(2026, 2, 28, 00, 00, 00, 000, jst)
	fmt.Println(normal)
}

func next() {
	jst, _ := time.LoadLocation("Asia/Tokyo")

	now := time.Date(2026, 1, 31, 00, 00, 00, 000, jst)
	nextMonth := now.AddDate(0, 1, 0)
	fmt.Println(nextMonth)
}

func NextMonth(t time.Time) time.Time {
	year1, month2, day := t.Date()
	first := time.Date(year1, month2, 1, 0, 0, 0, 0, time.UTC)
	year2, month2, _ := first.AddDate(0, 1, 0).Date()
	nextMonthTime := time.Date(year2, month2, day, 0, 0, 0, 0, time.UTC)
	if month2 != nextMonthTime.Month() {
		return first.AddDate(0, 2, -1)
	}
	return nextMonthTime
}

func main() {
	addDate()
	next()
}
