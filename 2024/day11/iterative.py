import re
import time
from argparse import ArgumentParser


def read(file):
  with open(file, "r") as f:
    for line in f:
      stones = [int(piece) for piece in line.strip().split(" ")]
      return stones


def iterate(stone):
  if stone == 0:
    return [1]
  digits = str(stone)
  if len(digits) % 2 == 0:
    midpoint = len(digits) // 2
    return [int(digits[0:midpoint]), int(digits[midpoint:])]
  return [stone * 2024]


def main(file, times):
  stones = read(file)
  print(stones)
  for _ in range(times):
    next_stones = []
    for stone in stones:
      next_stones.extend(iterate(stone))
    stones = next_stones
  return len(stones)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("times", type=int)
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file, args.times))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))