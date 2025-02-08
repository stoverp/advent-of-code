import re
import time
from argparse import ArgumentParser
from enum import Enum
from dataclasses import dataclass

class Dir(bytes, Enum):
  def __new__(cls, value, char, row_change, col_change):
    obj = bytes.__new__(cls, [value])
    obj._value_ = value
    obj.char = char
    obj.row_change = row_change
    obj.col_change = col_change
    return obj
  def __repr__(self):
    return self.char
  UP = (0, "^", -1, 0)
  RIGHT = (1, ">", 0, 1)
  DOWN = (2, "v", 1, 0)
  LEFT = (3, "<", 0, -1)


@dataclass
class Guard:
  dir: Dir
  row: int
  col: int

  def turn(self):
    self.dir = Dir((self.dir.value + 1) % len(Dir))

  def next_pos(self):
    return self.row + self.dir.row_change, self.col + self.dir.col_change


def read(file):
  obstacles = set()
  guard = None
  with open(file, "r") as f:
    row = 0
    for line in f:
      for col, c in enumerate(line.strip()):
        if c == "#":
          obstacles.add((row, col))
        elif c == "^":
          guard = Guard(Dir.UP, row, col)
      row += 1
  return obstacles, guard, row, col + 1


def print_lab(obstacles, guard, positions, num_rows, num_cols):
  for row in range(num_rows):
    for col in range(num_cols):
      if (row, col) in obstacles:
        print("#", end="")
      elif guard.row == row and guard.col == col:
        print(guard.dir.char, end="")
      elif (row, col) in positions:
        print("X", end="")
      else:
        print(".", end="")
    print()


def main(file):
  obstacles, guard, num_rows, num_cols = read(file)
  positions = set()
  while 0 <= guard.row < num_rows and 0 <= guard.col < num_cols:
    positions.add((guard.row, guard.col))
    next_position = guard.next_pos()
    if next_position in obstacles:
      guard.turn()
    else:
      guard.row, guard.col = next_position
  return len(positions)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))