import re
from argparse import ArgumentParser


SIGNAL_STRENGTH_CYCLES = [20, 60, 100, 140, 180, 220]
signal_strengths = []


def tick(cycle, x):
  current_cycle = cycle + 1
  if current_cycle in SIGNAL_STRENGTH_CYCLES:
    print(f"during cycle {current_cycle}, x: {x}")
    signal_strength = current_cycle * x
    print(f"SIGNAL STRENGTH DURING CYCLE {current_cycle}: {signal_strength}")
    signal_strengths.append(signal_strength)
  return current_cycle


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
  print(f"final x: {x}")
  print(f"final signal strengths: {signal_strengths}")
  print(f"SUM OF SIGNAL STRENGTHS: {sum(signal_strengths)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
