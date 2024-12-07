import re
import time
from argparse import ArgumentParser


def read(file):
  first_column = []
  second_column = []
  with open(file, "r") as f:
    for line in f:
      first, second, _ = re.split(r"\s+", line)
      print(first, second)
      first_column.append(int(first))
      second_column.append(int(second))
  return sorted(first_column), sorted(second_column)


def main(file):
  first_column, second_column = read(file)
  total = 0
  for first, second in zip(first_column, second_column):
    total += abs(first - second)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
