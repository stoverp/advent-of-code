import re
from argparse import ArgumentParser

import numpy as np


class Knot(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash((self.x, self.y))

  def __repr__(self):
    return f"Knot({self.x}, {self.y})"


def print_grid(rope, min_x, max_x, min_y, max_y):
  for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
      printed_char = "s" if (x, y) == (0, 0) else "."
      for i, knot in reversed(list(enumerate(rope))):
        if (x, y) == (knot.x, knot.y):
          printed_char = "H" if i == 0 else str(i)
      print(printed_char, end="")
    print()
  print()


def find_limits(positions):
  sorted_by_x = sorted(positions, key=lambda k: k.x)
  sorted_by_y = sorted(positions, key=lambda k: k.y)
  return sorted_by_x[0].x, sorted_by_x[-1].x, sorted_by_y[0].y, sorted_by_y[-1].y


def print_history(history, min_x, max_x, min_y, max_y):
  for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
      if (x, y) == (0, 0):
        print("s", end="")
      elif Knot(x, y) in history:
        print("#", end="")
      else:
        print(".", end="")
    print()


def create_rope(n_knots):
  return [Knot(0, 0) for _ in range(n_knots)]


def move_rope(rope, direction):
  # move head
  if direction == "U":
    rope[0].y += 1
  elif direction == "D":
    rope[0].y -= 1
  elif direction == "R":
    rope[0].x += 1
  else:  # direction == "L"
    rope[0].x -= 1
  # move rest of rope
  for i in range(1, len(rope)):
    x_gap, y_gap = (rope[i - 1].x - rope[i].x, rope[i - 1].y - rope[i].y)
    if abs(x_gap) + abs(y_gap) >= 3:
      # leader is 2 away in one dir, at least 1 away in the other: move diagonally towards leader
      rope[i].x += np.sign(x_gap)
      rope[i].y += np.sign(y_gap)
    elif abs(x_gap) == 2:
      # leader is 2 away in x dir
      rope[i].x += np.sign(x_gap)
    elif abs(y_gap) == 2:
      # leader is 2 away in y dir
      rope[i].y += np.sign(y_gap)


def main(file, min_x, max_x, min_y, max_y, debug=False):
  rope = create_rope(10)
  tail_history = set()
  tail_history.add(rope[-1])
  if debug:
    print("== Initial State ==\n")
    print_grid(rope, min_x, max_x, min_y, max_y)
  with open(file, "r") as f:
    for line in f:
      if match := re.match("([UDRL]) (\d+)$", line):
        direction = match.group(1)
        distance = int(match.group(2))
        print(f"== {direction} {distance} ==\n")
        for _ in range(distance):
          move_rope(rope, direction)
          tail_history.add(Knot(rope[-1].x, rope[-1].y))
          # print(f"after {direction} move - rope: {rope}")
        if debug:
          print_grid(rope, min_x, max_x, min_y, max_y)
      else:
        raise Exception(f"invalid line: {line}")
  print(f"\nfinal tail history: {tail_history}")
  print_history(tail_history, min_x, max_x, min_y, max_y)
  print(f"final limits: {find_limits(tail_history)}\n")
  print(f"number of distinct tail positions: {len(tail_history)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  if args.file.endswith("test.txt"):
    main(args.file, 0, 5, 0, 5, debug=True)
  elif args.file.endswith("test2.txt"):
    main(args.file, -11, 14, -5, 15, debug=True)
  elif args.file.endswith("real.txt"):
    main(args.file, -17, 334, -13, 217, debug=False)
  else:
    raise Exception(f"unexpected file: {args.file}")
