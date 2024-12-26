import re
import time
from argparse import ArgumentParser
from collections import defaultdict


def read(file):
  garden = []
  with open(file, "r") as f:
    for line in f:
      garden.append([c for c in line.strip()])
  return garden


def explore_region(row, col, garden, region):
  region.add((row, col))
  for next_row, next_col in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
    if (next_row, next_col) not in region and \
        0 <= next_row < len(garden) and 0 <= next_col < len(garden[0]) and \
        garden[next_row][next_col] == garden[row][col]:
      explore_region(next_row, next_col, garden, region)


def merge_something(ranges):
  if len(ranges) <= 1:
    return False
  # print(ranges)
  for i, first in enumerate(ranges):
    for second in ranges[i+1:]:
      first_start, first_end, first_coord = first
      second_start, second_end, second_coord = second
      if first_coord == second_coord and \
          (abs(second_end - first_start) <= 1 or abs(second_start - first_end) <= 1):
        # print(first, second)
        ranges.remove(first)
        ranges.remove(second)
        ranges.append((min(first_start, second_start), max(first_end, second_end), first_coord))
        # print(ranges)
        return True
  return False


def main(file):
  garden = read(file)
  print(garden)
  visited = set()
  regions = list()
  for row in range(len(garden)):
    for col in range(len(garden[0])):
      if (row, col) not in visited:
        region = set()
        explore_region(row, col, garden, region)
        if region:
          regions.append(region)
          visited.update(region)
  print(regions)
  total = 0
  for region in regions:
    side_ranges = defaultdict(list)
    for position in region:
      row, col = position
      for type, adj_row, adj_col, coord in [
          ("top", row - 1, col, 1), 
          ("bottom", row + 1, col, 1), 
          ("left", row, col - 1, 0), 
          ("right", row, col + 1, 0)
        ]:
        if (adj_row, adj_col) not in region:
          side_ranges[type].append((position[coord], position[coord], position[(coord + 1) % 2]))
    num_sides = 0
    for type, ranges in side_ranges.items():
      while (merge_something(ranges)):
        pass
      num_sides += len(ranges)
    print(num_sides, region)
    total += num_sides * len(region)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))