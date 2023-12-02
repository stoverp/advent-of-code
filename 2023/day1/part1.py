import re
import time
from argparse import ArgumentParser

def first_int(chars):
  for c in chars:
    if c.isnumeric():
      return c


def main(file):
  nums = []
  with open(file, "r") as f:
    for line in f:
      num = int(first_int(line) + first_int(line[::-1]))
      nums.append(num)
  return sum(nums)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
