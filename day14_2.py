import re
import time
from argparse import ArgumentParser
from copy import deepcopy

INITIAL_SAND_POSITION = (500, 0)


def taken(grid, position):
  return grid[position[1]][position[0]]


def add(grid, position):
  grid[position[1]][position[0]] = True


def read_rocks(file):
  rocks_set = set()
  with open(file, "r") as f:
    for line in f:
      pieces = re.split("\s*->\s*", line.strip())
      path = []
      for piece in pieces:
        if match := re.match("(\d+)\s*,\s*(\d+)$", piece):
          path.append((int(match.group(1)), int(match.group(2))))
        else:
          raise Exception(f"invalid point: {piece}")
      prev_rock = path[0]
      for rock in path[1:]:
        x_start, x_end = sorted([prev_rock[0], rock[0]])
        y_start, y_end = sorted([prev_rock[1], rock[1]])
        for x in range(x_start, x_end + 1):
          for y in range(y_start, y_end + 1):
            rocks_set.add((x, y))
        prev_rock = rock
  sorted_by_x = sorted(rocks_set)
  min_x, max_x = sorted_by_x[0][0], sorted_by_x[-1][0]
  sorted_by_y = sorted(rocks_set, key=lambda r: r[1])
  max_y = sorted_by_y[-1][1] + 2
  rocks = []
  for y in range(0, max_y + 1):
    row = []
    for x in range(min_x, max_x + 1):
      row.append(True if (x, y) in rocks_set else False)
    rocks.append(row)
  return rocks, min_x, max_x, max_y


def print_cave(rocks, obstacles, falling_unit, min_x, max_x, max_y):
  for y in range(0, max_y + 1):
    for x in range(min_x - 2, max_x + 3):
      if y == max_y:
        print("#", end="")
      elif (x, y) == falling_unit:
        print("+", end="")
      elif taken(rocks, (x, y)):
        print("#", end="")
      elif taken(obstacles, (x, y)):
        print("o", end="")
      else:
        print(".", end="")
    print()


def drop(falling_unit, obstacles, max_y):
  if taken(obstacles, INITIAL_SAND_POSITION):
    # full of sand, can't drop
    return None
  if falling_unit[1] == max_y - 1:
    add(obstacles, falling_unit)
    return INITIAL_SAND_POSITION
  elif taken(obstacles, (falling_unit[0], falling_unit[1] + 1)):
    return falling_unit[0], falling_unit[1] + 1
  elif taken(obstacles, (falling_unit[0] - 1, falling_unit[1] + 1)):
    return falling_unit[0] - 1, falling_unit[1] + 1
  elif taken(obstacles, (falling_unit[0] + 1, falling_unit[1] + 1)):
    return falling_unit[0] + 1, falling_unit[1] + 1
  else:
    obstacles.add(falling_unit)
    return INITIAL_SAND_POSITION


def n_true(grid):
  return sum([v for row in grid for v in row if v])


def main(file):
  rocks, min_x, max_x, max_y = read_rocks(file)
  obstacles = deepcopy(rocks)
  falling_unit = INITIAL_SAND_POSITION
  print_cave(rocks, obstacles, falling_unit, min_x, max_x, max_y)
  # keep dropping sand until the initial position is occupied
  i = 0
  while falling_unit := drop(falling_unit, obstacles, max_y):
    if i % 100000 == 0:
      print(f"\n== Round {i} ==")
      print_cave(rocks, obstacles, falling_unit, min_x, max_x, max_y)
      # time.sleep(1)
    i += 1
  print(f"\n== Final ==")
  print_cave(rocks, obstacles, falling_unit, min_x, max_x, max_y)
  print(f"\nfinal units of sand: {n_true(obstacles) - n_true(rocks)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
