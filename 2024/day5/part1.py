import re
import time
from argparse import ArgumentParser
from collections import defaultdict


def read(file):
  order = defaultdict(set)
  printings = []
  with open(file, "r") as f:
    for line in f:
      if "|" in line:
        x, y = [int(n) for n in line.strip().split("|")]
        order[x].add(y)
      elif "," in line:
        printings.append([int(n) for n in line.strip().split(",")])
  return order, printings


def is_ordered(printing, order):
  for i, page in enumerate(printing):
    for previous_page in printing[0:i]:
      if previous_page in order[page]:
        return False
  return True


def main(file):
  order, printings = read(file)
  total = 0
  for printing in printings:
    ordered = is_ordered(printing, order)
    print(printing, ordered)
    if ordered:
      total += printing[len(printing) // 2]
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))