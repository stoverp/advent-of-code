import re
import time
from argparse import ArgumentParser


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
    perimeter = 0
    for row, col in list(region):
      for adj in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if adj not in region:
          perimeter += 1
    area = len(region)
    print(area, perimeter, perimeter * area, region)
    total += area * perimeter
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))