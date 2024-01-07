import re
import time
from argparse import ArgumentParser


def find_columns(rows):
  columns = ["" for _ in range(len(rows[0]))]
  for row in rows:
    for col, c in enumerate(row):
      columns[col] += c
  return columns


def read_input(file):
  grids = []
  rows = []
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      if not line.strip():
        grids.append((rows, find_columns(rows)))
        rows = []
      else:
        rows.append(line.strip())
  grids.append((rows, find_columns(rows)))
  return grids


def scan(maze):
  for i in range(0, len(maze) - 1):
    size = min(i + 1, len(maze) - i - 1)
    left = maze[i + 1 - size:i + 1]
    right = maze[i + size:i:-1]
    # print("i:", i)
    # print("size:", size)
    # print("left side:", left)
    # print("right side:", right)
    if left == right:
      return i + 1
  return None


def find_mirror(rows, columns):
  print("rows:", rows)
  print("columns", columns)
  index = scan(rows)
  if index is not None:
    return index * 100
  return scan(columns)


def main(file):
  grids = read_input(file)
  total = 0
  for rows, columns in grids:
    result = find_mirror(rows, columns)
    print("result:", result)
    print()
    total += result
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
