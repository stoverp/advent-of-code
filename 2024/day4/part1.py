import re
import time
from argparse import ArgumentParser


WORD = "XMAS"
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def read(file):
  letters = []
  with open(file, "r") as f:
    for line in f:
      letters.append(line.strip())
  return letters


def matches(letters, row, col, dir):
  cur_row, cur_col = row, col
  for char in WORD:
    if not (0 <= cur_row < len(letters) and 0 <= cur_col < len(letters[0])):
      return False
    if letters[cur_row][cur_col] != char:
      return False
    cur_row += dir[0]
    cur_col += dir[1]
  return True


def count_matches(letters, row, col):
  total = 0
  for dir in DIRS:
    if matches(letters, row, col, dir):
      total += 1
  return total


def main(file):
  letters = read(file)
  print(letters)
  total = 0
  for row in range(len(letters)):
    for col in range(len(letters[row])):
      total += count_matches(letters, row, col)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))