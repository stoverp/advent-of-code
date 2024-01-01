import re
import time
from argparse import ArgumentParser


EXPANSION_SIZE = 999999


def read_input(file):
  sky = []
  galaxies = []
  row = 0
  with open(file, "r") as f:
    for line in f:
      sky.append(line.strip())
      for col, c in enumerate(line.strip()):
        if c == "#":
          galaxies.append((row, col))
      row += 1
  return galaxies, sky


def expand_rows(sky):
  row_coords = [i for i in range(len(sky))]
  for row, line in enumerate(sky):
    if "#" not in line:
      for i in range(row + 1, len(row_coords)):
        row_coords[i] += EXPANSION_SIZE
  return row_coords


def expand_cols(sky):
  empty_cols = set(i for i in range(len(sky[0])))
  for line in sky:
    for col, c in enumerate(line):
      if c == "#" and col in empty_cols:
        empty_cols.remove(col)
  col_coords = [i for i in range(len(sky[0]))]
  for col in empty_cols:
    for i in range(col + 1, len(col_coords)):
      col_coords[i] += EXPANSION_SIZE
  return col_coords


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


def print_sky(sky):
  for line in sky:
    print(line)
  print()


def map_galaxies(galaxies, row_coords, col_coords):
  mapped_galaxies = []
  for galaxy in galaxies:
    mapped_galaxies.append((row_coords[galaxy[0]], col_coords[galaxy[1]]))
  return mapped_galaxies


def main(file):
  galaxies, sky = read_input(file)
  # print(galaxies)
  # print_sky(sky)
  row_coords = expand_rows(sky)
  # print(row_coords)
  col_coords = expand_cols(sky)
  # print(col_coords)
  mapped_galaxies = map_galaxies(galaxies, row_coords, col_coords)
  # print(mapped_galaxies)
  return distances_sum(mapped_galaxies)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
