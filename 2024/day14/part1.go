package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"time"
)

type Robot struct {
	px int64
	py int64
	vx int64
	vy int64
}

func parseInt(s []byte) int64 {
	v, err := strconv.ParseInt(string(s), 10, 64)
	if err != nil {
		panic(err)
	}
	return v
}

func parseIntStr(s string) int64 {
	return parseInt([]byte(s))
}

func read(filename string) []Robot {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	robots := []Robot{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		re := regexp.MustCompile(`p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)`)
		matches := re.FindSubmatch([]byte(line))
		if len(matches) > 0 {
			robots = append(robots, Robot{
				px: parseInt(matches[1]),
				py: parseInt(matches[2]),
				vx: parseInt(matches[3]),
				vy: parseInt(matches[4]),
			})
		}
	}
	return robots
}

func wrap(v int64, limit int64) int64 {
	result := v % limit
	if result < 0 {
		return limit + result
	} else {
		return result
	}
}

func run(filename string, width int64, height int64) int {
	robots := read(filename)
	fmt.Println(robots)
	for range 100 {
		for i := range robots {
			robots[i].px = wrap(robots[i].px+robots[i].vx, width)
			robots[i].py = wrap(robots[i].py+robots[i].vy, height)
		}
	}
	fmt.Println(robots)
	topLeft := 0
	topRight := 0
	bottomLeft := 0
	bottomRight := 0
	for _, robot := range robots {
		xMiddle := width / 2
		yMiddle := height / 2
		if robot.px < xMiddle {
			if robot.py < yMiddle {
				topLeft += 1
			} else if robot.py > yMiddle {
				bottomLeft += 1
			}
		} else if robot.px > xMiddle {
			if robot.py < yMiddle {
				topRight += 1
			} else if robot.py > yMiddle {
				bottomRight += 1
			}
		}
	}
	fmt.Println(topLeft, bottomLeft, topRight, bottomRight)
	return topLeft * bottomLeft * topRight * bottomRight
}

func main() {
	startTime := time.Now()
	filename := os.Args[1]
	width := parseIntStr(os.Args[2])
	height := parseIntStr(os.Args[3])
	fmt.Println("RESULT:", run(filename, width, height))
	elapsed := time.Since(startTime)
	fmt.Println("completed in", elapsed.Seconds(), "seconds")
}
