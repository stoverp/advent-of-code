import re
import time
from argparse import ArgumentParser


def read(file):
  letters = []
  with open(file, "r") as f:
    for line in f:
      letters.append(line.strip())
  return letters


def matches(letters, row, col):
  if letters[row + 1][col + 1] != "A":
    return False
  if sorted([letters[row][col], letters[row + 2][col + 2]]) != ["M", "S"]:
    return False
  if sorted([letters[row][col + 2], letters[row + 2][col]]) != ["M", "S"]:
    return False
  return True


def main(file):
  letters = read(file)
  print(letters)
  total = 0
  for row in range(len(letters) - 2):
    for col in range(len(letters[row]) - 2):
      if matches(letters, row, col):
        total += 1
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))