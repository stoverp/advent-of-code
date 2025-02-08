package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

func read(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}
}

func run(filename string) int {
	read(filename)
	total := 0
	return total
}

func main() {
	startTime := time.Now()
	filename := os.Args[1]
	fmt.Println("RESULT:", run(filename))
	elapsed := time.Since(startTime)
	fmt.Println("completed in", elapsed.Seconds(), "seconds")
}
