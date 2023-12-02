import re
from argparse import ArgumentParser


def print_grid(head_position, tail_position):
  for y in range(4, -1, -1):
    for x in range(6):
      if (x, y) == (0, 0) and head_position != (0, 0) and tail_position != (0, 0):
        print("s", end="")
      elif (x, y) == head_position:
        print("H", end="")
      elif (x, y) == tail_position and tail_position != head_position:
        print("T", end="")
      else:
        print(".", end="")
    print()
  print()


def print_history(history):
  min_x = min(x for x, y in history)
  max_x = max(x for x, y in history)
  min_y = min(y for x, y in history)
  max_y = max(y for x, y in history)
  for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
      if (x, y) == (0, 0):
        print("s", end="")
      elif (x, y) in history:
        print("#", end="")
      else:
        print(".", end="")
    print()
  print()


def main(file):
  head_position = (0, 0)
  tail_position = (0, 0)
  tail_history = set()
  tail_history.add(tail_position)
  print("== Initial State ==\n")
  # print_grid(head_position, tail_position)
  with open(file, "r") as f:
    for line in f:
      if match := re.match("([UDRL]) (\d+)$", line):
        direction = match.group(1)
        distance = int(match.group(2))
        print(f"== {direction} {distance} ==\n")
        for _ in range(distance):
          if direction == "U":
            head_position = (head_position[0], head_position[1] + 1)
            if (head_position[1] - tail_position[1]) == 2:
              tail_position = (head_position[0], head_position[1] - 1)
          elif direction == "D":
            head_position = (head_position[0], head_position[1] - 1)
            if (head_position[1] - tail_position[1]) == -2:
              tail_position = (head_position[0], head_position[1] + 1)
          elif direction == "R":
            head_position = (head_position[0] + 1, head_position[1])
            if (head_position[0] - tail_position[0]) == 2:
              tail_position = (head_position[0] - 1, head_position[1])
          else:  # direction == "L"
            head_position = (head_position[0] - 1, head_position[1])
            if (head_position[0] - tail_position[0]) == -2:
              tail_position = (head_position[0] + 1, head_position[1])
          tail_history.add(tail_position)
          print(f"after {direction} move - head: {head_position}, tail: {tail_position}")
          # print_grid(head_position, tail_position)
      else:
        raise Exception(f"invalid line: {line}")
  print(f"\nfinal tail history: {tail_history}")
  print_history(tail_history)
  print(f"number of distinct tail positions: {len(tail_history)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
