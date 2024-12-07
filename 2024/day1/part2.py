import re
import time
from argparse import ArgumentParser
from collections import defaultdict


def read(file):
  first_column = []
  second_counts = defaultdict(int)
  with open(file, "r") as f:
    for line in f:
      first, second, _ = re.split(r"\s+", line)
      first_column.append(int(first))
      second_counts[int(second)] += 1
  return first_column, second_counts


def main(file):
  first_column, second_counts = read(file)
  total = 0
  for first in first_column:
    total += second_counts[first] * first
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
