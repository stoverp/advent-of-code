package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"
)

const (
	UP = iota
	RIGHT
	DOWN
	LEFT
)

type Position struct {
	row int
	col int
}

type Guard struct {
	dir int
	pos Position
}

func (g Guard) NextPosition() Position {
	switch g.dir {
	case UP:
		return Position{g.pos.row - 1, g.pos.col}
	case RIGHT:
		return Position{g.pos.row, g.pos.col + 1}
	case DOWN:
		return Position{g.pos.row + 1, g.pos.col}
	case LEFT:
		return Position{g.pos.row, g.pos.col - 1}
	default:
		panic("invalid dir: " + string(g.dir))
	}
}

func (g *Guard) Turn() {
	g.dir = (g.dir + 1) % 4
}

func (g *Guard) Move(pos Position) {
	g.pos = pos
}

func (g Guard) InBounds(numRows int, numCols int) bool {
	return 0 <= g.pos.row &&
		g.pos.row < numRows &&
		0 <= g.pos.col &&
		g.pos.col < numCols
}

func read(filename string) (map[Position]bool, Guard, int, int) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	obstacles := make(map[Position]bool)

	row := 0
	scanner := bufio.NewScanner(file)
	var guard Guard
	var numCols int
	for scanner.Scan() {
		line := scanner.Text()
		numCols = len(line)
		for col, c := range line {
			if string(c) == "#" {
				obstacles[Position{row, col}] = true
			} else if string(c) == "^" {
				guard = Guard{UP, Position{row, col}}
			}
		}
		row += 1
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return obstacles, guard, row, numCols
}

func run() int {
	obstacles, guard, numRows, numCols := read(os.Args[1])
	visited := make(map[Position]bool)
	for guard.InBounds(numRows, numCols) {
		visited[guard.pos] = true
		nextPos := guard.NextPosition()
		if _, ok := obstacles[nextPos]; ok {
			guard.Turn()
		} else {
			guard.Move(nextPos)
		}
	}
	return len(visited)
}

func main() {
	startTime := time.Now()
	fmt.Println("RESULT:", run())
	elapsed := time.Since(startTime)
	fmt.Println("completed in", elapsed.Seconds(), "seconds")
}
