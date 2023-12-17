import re
import time
from argparse import ArgumentParser


def read_input(file):
  all_numbers = []
  with open(file, "r") as f:
    for line in f:
      numbers = [int(n) for n in line.strip().split(" ")]
      all_numbers.append(numbers)
  return all_numbers


def find_derivations(numbers):
  all_zeroes = False
  derivations = [numbers]
  while not all_zeroes:
    all_zeroes = True
    diffs = []
    prev = derivations[-1]
    for i in range(1, len(prev)):
      value = prev[i] - prev[i - 1]
      diffs.append(value)
      if value != 0:
        all_zeroes = False
    derivations.append(diffs)
  return derivations


def main(file):
  all_numbers = read_input(file)
  total = 0
  for numbers in all_numbers:
    derivations = find_derivations(numbers)
    derivations[-1].append(0)
    for i in range(len(derivations) - 2, -1, -1):
      derivations[i].append(derivations[i][-1] + derivations[i+1][-1])
    total += derivations[0][-1]
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
