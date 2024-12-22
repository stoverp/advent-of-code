import re
import time
from argparse import ArgumentParser


def read(file):
  with open(file, "r") as f:
    for line in f:
      stones = [int(piece) for piece in line.strip().split(" ")]
      return stones


def iterate(stone, times):
  if times == 0:
    return [stone]
  if stone == 0:
    return iterate(1, times - 1)
  digits = str(stone)
  if len(digits) % 2 == 0:
    midpoint = len(digits) // 2
    return iterate(int(digits[0:midpoint]), times - 1) + \
      iterate(int(digits[midpoint:]), times - 1)
  return iterate(stone * 2024, times - 1)


def main(file, times):
  stones = read(file)
  print(stones)
  result = []
  for stone in stones:
    result.extend(iterate(stone, times))
  print(result)
  return len(result)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("times", type=int)
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file, args.times))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))