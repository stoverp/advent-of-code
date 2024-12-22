import re
import time
from argparse import ArgumentParser


def read(file):
  map = []
  with open(file, "r") as f:
    for line in f:
      map.append([int(c) for c in line.strip()])
  return map


def summits(row, col, map):
  if map[row][col] == 9:
    return 1
  total = 0
  for next_row, next_col in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
    if 0 <= next_row < len(map) and 0 <= next_col < len(map[row]) and \
        map[next_row][next_col] == map[row][col] + 1:
      total += summits(next_row, next_col, map)
  return total


def main(file):
  map = read(file)
  trailheads = []
  for row in range(len(map)):
    for col in range(len(map[row])):
      if map[row][col] == 0:
        trailheads.append((row, col))
  print(trailheads)
  total = 0
  for trailhead in trailheads:
    count = summits(*trailhead, map)
    print(count)
    total += count
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))