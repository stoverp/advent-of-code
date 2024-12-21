import re
import time
import math
from argparse import ArgumentParser
from collections import defaultdict


def read(file):
  antennas = defaultdict(set)
  row = 0
  num_cols = None
  with open(file, "r") as f:
    for line in f:
      num_cols = len(line.strip())
      for col, c in enumerate(line.strip()):
        if c != ".":
          antennas[c].add((row, col))
      row += 1
  return antennas, row, num_cols


def print_map(antennas, num_rows, num_cols):
  map = [["." for _ in range(num_cols)] for _ in range(num_rows)]
  for c, positions in antennas.items():
    for row, col in positions:
      map[row][col] = c
  for row in range(num_rows):
    for col in range(num_cols):
      print(map[row][col], end="")
    print()


def antinodes(pos1, pos2, num_rows, num_cols):
  rise, run = slope(pos1, pos2)
  points = set()
  for dir in [1, -1]:
    row, col = pos1
    while 0 <= row < num_rows and 0 <= col < num_cols:
      small_dist, big_dist = sorted([abs(row - pos1[0]), abs(row - pos2[0])])
      if big_dist == small_dist * 2:
        points.add((row, col))
      row += rise * dir
      col += run * dir
  return points


def slope(pos1, pos2):
  row1, col1 = pos1
  row2, col2 = pos2
  rise = row1 - row2
  run = col1 - col2
  gcd = math.gcd(rise, run)
  return rise // gcd, run // gcd


def pairs(l):
  results = []
  for i, item1 in enumerate(l):
    for item2 in l[i+1:]:
      results.append((item1, item2))
  return results


def all_antinodes(antennas, num_rows, num_cols):
  points = set()
  for c, positions in antennas.items():
    for pos1, pos2 in pairs(list(positions)):
      points.update(antinodes(pos1, pos2, num_rows, num_cols))
  return points


def main(file):
  antennas, num_rows, num_cols = read(file)
  antennas["#"] = all_antinodes(antennas, num_rows, num_cols)
  print_map(antennas, num_rows, num_cols)
  return len(antennas["#"])


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))