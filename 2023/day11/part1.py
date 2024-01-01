import re
import time
from argparse import ArgumentParser


def read_input(file):
  sky = []
  with open(file, "r") as f:
    for line in f:
      sky.append(line.strip())
  return sky


def expand_rows(sky):
  new_sky = []
  for line in sky:
    if "#" not in line:
      new_sky.append(line)
    new_sky.append(line)
  return new_sky


def expand_cols(sky):
  empty_cols = set(i for i in range(len(sky[0])))
  for line in sky:
    for col, c in enumerate(line):
      if c == "#" and col in empty_cols:
        empty_cols.remove(col)
  new_sky = []
  for line in sky:
    new_line = ""
    for col, c in enumerate(line):
      if col in empty_cols:
        new_line += c
      new_line += c
    new_sky.append(new_line)
  return new_sky


def print_sky(sky):
  for line in sky:
    print(line)
  print()


def find_galaxies(sky):
  galaxies = []
  for row in range(len(sky)):
    for col in range(len(sky[0])):
      if sky[row][col] == "#":
        galaxies.append((row, col))
  return galaxies


def distances_sum(galaxies):
  total = 0
  for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
      total += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
  return total


def main(file):
  sky = read_input(file)
  print_sky(sky)
  sky = expand_rows(sky)
  sky = expand_cols(sky)
  print_sky(sky)
  galaxies = find_galaxies(sky)
  print(galaxies)
  return distances_sum(galaxies)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
