package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

type Pos struct {
	row int
	col int
}

const (
	UP = iota
	RIGHT
	DOWN
	LEFT
)

func (p Pos) next(dir int) Pos {
	switch dir {
	case UP:
		return Pos{row: p.row - 1, col: p.col}
	case RIGHT:
		return Pos{row: p.row, col: p.col + 1}
	case DOWN:
		return Pos{row: p.row + 1, col: p.col}
	case LEFT:
		return Pos{row: p.row, col: p.col - 1}
	default:
		panic("invalid dir: " + string(dir))
	}
}

func (p *Pos) move(dir int) {
	dest := p.next(dir)
	p.row = dest.row
	p.col = dest.col
}

func toDir(char rune) int {
	switch char {
	case '^':
		return UP
	case '>':
		return RIGHT
	case 'v':
		return DOWN
	case '<':
		return LEFT
	default:
		panic("invalid move rune: " + string(char))
	}
}

func toString(dir int) string {
	switch dir {
	case UP:
		return "up"
	case RIGHT:
		return "right"
	case DOWN:
		return "down"
	case LEFT:
		return "left"
	default:
		panic("invalid dir: " + string(dir))
	}
}

func printBoard(board [][]rune) {
	for _, line := range board {
		fmt.Println(string(line))
	}
}

func read(filename string) ([][]rune, []int, Pos) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	board := [][]rune{}
	// boxes := []Pos{}
	moves := []int{}
	robot := Pos{}
	row := 0
	for scanner.Scan() {
		line := scanner.Text()
		if strings.Contains(line, "#") {
			board = append(board, []rune(line))
			for col, c := range line {
				// if c == 'O' {
				// 	boxes = append(boxes, Pos{row: row, col: col})
				// } else if c == '@' {
				if c == '@' {
					robot = Pos{row: row, col: col}
				}
			}
		} else if len(line) > 1 {
			for _, char := range line {
				moves = append(moves, toDir(char))
			}
		}
		row += 1
	}
	return board, moves, robot
}

func scan(board [][]rune, robot Pos, dir int) []Pos {
	// fmt.Println("scanning from robot", robot)
	curPos := robot
	moveables := []Pos{}
	for true {
		// fmt.Println("checking curPos", curPos)
		if board[curPos.row][curPos.col] == '#' {
			return []Pos{}
		} else if board[curPos.row][curPos.col] == '.' {
			// fmt.Println("returning moveables", moveables)
			return moveables
		} else if board[curPos.row][curPos.col] == 'O' || board[curPos.row][curPos.col] == '@' {
			// fmt.Println("appending moveable", curPos)
			moveables = append(moveables, curPos)
		}
		curPos = curPos.next(dir)
	}
	panic("can't get here")
}

func run(filename string) int {
	// reader := bufio.NewReader(os.Stdin)
	board, moves, robot := read(filename)
	fmt.Println("start")
	printBoard(board)
	// _, _ = reader.ReadString('\n')
	// fmt.Println(boxes)
	// fmt.Println(moves)
	// fmt.Println(robot)
	for _, dir := range moves {
		moveables := scan(board, robot, dir)
		for i := len(moveables) - 1; i >= 0; i-- {
			nextPos := moveables[i].next(dir)
			curRune := board[moveables[i].row][moveables[i].col]
			if curRune == '@' {
				robot.row = nextPos.row
				robot.col = nextPos.col
			}
			board[nextPos.row][nextPos.col] = curRune
			board[moveables[i].row][moveables[i].col] = '.'
		}
		// fmt.Println("move", toString(dir))
		// fmt.Println("moveables", moveables)
		// printBoard(board)
		// _, _ = reader.ReadString('\n')
	}
	fmt.Println("\nend")
	printBoard(board)
	total := 0
	for row := range len(board) {
		for col := range len(board[0]) {
			if board[row][col] == 'O' {
				total += 100*row + col
			}
		}
	}
	return total
}

func main() {
	startTime := time.Now()
	filename := os.Args[1]
	fmt.Println("RESULT:", run(filename))
	elapsed := time.Since(startTime)
	fmt.Println("completed in", elapsed.Seconds(), "seconds")
}
