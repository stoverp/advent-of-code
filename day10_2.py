import re
from argparse import ArgumentParser


WIDTH = 40


def tick(cycle, x):
  position = cycle % WIDTH
  if position == 0:
    print()
  if position in [x - 1, x, x + 1]:
    print("#", end="")
  else:
    print(" ", end="")
  return cycle + 1


def main(file):
  x = 1
  cycle = 0
  with open(file, "r") as f:
    for line in f:
      if line.startswith("noop"):
        # print("instruction: noop")
        cycle = tick(cycle, x)
      elif match := re.match("addx (-?\d+)$", line):
        v = int(match.group(1))
        # print(f"instruction: addx {v}")
        cycle = tick(cycle, x)
        cycle = tick(cycle, x)
        x += v
      else:
        raise Exception(f"invalid input line: {line}")
  # print(f"final x: {x}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
