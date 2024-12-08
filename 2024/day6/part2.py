import re
import time
from argparse import ArgumentParser
from enum import Enum
from dataclasses import dataclass
from copy import copy


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


def print_lab(obstacles, new_obstacle, guard, positions, num_rows, num_cols):
  for row in range(num_rows):
    for col in range(num_cols):
      if (row, col) in obstacles:
        print("#", end="")
      elif (row, col) == new_obstacle:
        print("O", end="")
      elif guard.row == row and guard.col == col:
        print(guard.dir.char, end="")
      elif (row, col) in positions:
        print("X", end="")
      else:
        print(".", end="")
    print()


def is_guard_stuck(obstacles, guard, num_rows, num_cols):
  positions = set()
  # print_lab(obstacles, guard, positions, num_rows, num_cols)
  # input()
  while 0 <= guard.row < num_rows and 0 <= guard.col < num_cols:
    positions.add((guard.dir, guard.row, guard.col))
    next_position = guard.next_pos()
    if (guard.dir, next_position[0], next_position[1]) in positions:
      return True
    if next_position in obstacles:
      guard.turn()
    else:
      guard.row, guard.col = next_position
    # print_lab(obstacles, guard, positions, num_rows, num_cols)
    # input()
  return False


def main(file):
  obstacles, starting_guard, num_rows, num_cols = read(file)
  # print(obstacles)
  # print(guard)
  # print(num_rows, num_cols)
  total = 0
  for row in range(num_rows):
    for col in range(num_cols):
      print(row, col)
      if (row, col) not in obstacles:
        guard = copy(starting_guard)
        new_obstacle = (row, col)
        if is_guard_stuck(obstacles | {new_obstacle}, guard, num_rows, num_cols):
          total += 1
          # print(row, col, "STUCK")
          # print_lab(obstacles, new_obstacle, guard, set(), num_rows, num_cols)
          # print()
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))