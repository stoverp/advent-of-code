package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"strconv"
	"time"
)

type Coord struct {
	x float64
	y float64
}

type Machine struct {
	aButton    Coord
	bButton    Coord
	prizeCoord Coord
}

func parseFloat(s []byte) float64 {
	v, err := strconv.ParseFloat(string(s), 64)
	if err != nil {
		panic(err)
	}
	return v
}

func isInt(v float64) bool {
	return math.Abs(float64(math.Round(v))-v) < 1e-5
}

func read(filename string) []Machine {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	buttons := []Coord{}
	machines := []Machine{}

	scanner := bufio.NewScanner(file)
	buttonRe := regexp.MustCompile(`Button ([AB]): X\+(\d+), Y\+(\d+)`)
	// prizeRe := regexp.MustCompile(`Prize: X=(\d+), Y=(\d+)`)
	prizeRe := regexp.MustCompile(`Prize: X=(\d+), Y=(\d+)`)
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		matches := buttonRe.FindSubmatch([]byte(line))
		if len(matches) > 0 {
			// fmt.Printf("%q\n", matches[1:])
			buttons = append(buttons, Coord{x: parseFloat(matches[2]), y: parseFloat(matches[3])})
		} else {
			matches := prizeRe.FindSubmatch([]byte(line))
			// fmt.Printf("%q\n", matches)
			if len(matches) > 0 {
				machines = append(machines,
					Machine{
						aButton: buttons[0],
						bButton: buttons[1],
						prizeCoord: Coord{
							x: parseFloat(matches[1]),
							y: parseFloat(matches[2]),
						},
					})
				buttons = []Coord{}
			}
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return machines
}

func run() int {
	machines := read(os.Args[1])
	total := 0
	for _, machine := range machines {
		fmt.Println(machine)
		bPresses := (machine.prizeCoord.y - machine.prizeCoord.x*machine.aButton.y/machine.aButton.x) /
			(machine.bButton.y - machine.bButton.x*machine.aButton.y/machine.aButton.x)
		aPresses := (machine.prizeCoord.x - bPresses*machine.bButton.x) / machine.aButton.x
		fmt.Println(aPresses, bPresses)
		if isInt(aPresses) && isInt(bPresses) {
			fmt.Println("it works!")
			total += int(3*math.Round(aPresses) + math.Round(bPresses))
		} else {
			fmt.Println("does not work")
		}
		fmt.Println()
	}
	return total
}

func main() {
	startTime := time.Now()
	fmt.Println("RESULT:", run())
	elapsed := time.Since(startTime)
	fmt.Println("completed in", elapsed.Seconds(), "seconds")
}
