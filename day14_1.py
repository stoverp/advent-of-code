import re
from argparse import ArgumentParser


INITIAL_SAND_POSITION = (500, 0)


def read_rocks(file):
  rocks = set()
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
            rocks.add((x, y))
        prev_rock = rock
  return rocks


def print_cave(rocks, sand, falling_unit, min_x, max_x, max_y):
  for y in range(0, max_y + 1):
    for x in range(min_x, max_x + 1):
      if (x, y) == falling_unit:
        print("+", end="")
      elif (x, y) in rocks:
        print("#", end="")
      elif (x, y) in sand:
        print("o", end="")
      else:
        print(".", end="")
    print()


def drop(falling_unit, rocks, sand):
  obstacles = rocks.union(sand)
  if (falling_unit[0], falling_unit[1] + 1) not in obstacles:
    return falling_unit[0], falling_unit[1] + 1
  elif (falling_unit[0] - 1, falling_unit[1] + 1) not in obstacles:
    return falling_unit[0] - 1, falling_unit[1] + 1
  elif (falling_unit[0] + 1, falling_unit[1] + 1) not in obstacles:
    return falling_unit[0] + 1, falling_unit[1] + 1
  else:
    sand.add(falling_unit)
    return INITIAL_SAND_POSITION


def main(file):
  rocks = read_rocks(file)
  sorted_by_x = sorted(rocks)
  sorted_by_y = sorted(rocks, key=lambda r: r[1])
  min_x, max_x = sorted_by_x[0][0], sorted_by_x[-1][0]
  max_y = sorted_by_y[-1][1]
  sand = set()
  falling_unit = INITIAL_SAND_POSITION
  print_cave(rocks, sand, falling_unit, min_x, max_x, max_y)
  # keep dropping sand until a unit falls into the abyssF
  i = 0
  while falling_unit[1] <= max_y:
    # input()
    falling_unit = drop(falling_unit, rocks, sand)
    if i % 1000 == 0:
      print(f"\n== Round {i} ==")
      print_cave(rocks, sand, falling_unit, min_x, max_x, max_y)
    i += 1
  print_cave(rocks, sand, falling_unit, min_x, max_x, max_y)
  print(f"\nfinal units of sand: {len(sand)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
