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
        grids.append(rows)
        rows = []
      else:
        rows.append(line.strip())
  grids.append(rows)
  return grids


def scan(maze):
  for i in range(0, len(maze) - 1):
    size = min(i + 1, len(maze) - i - 1)
    left = maze[i + 1 - size:i + 1]
    right = maze[i + size:i:-1]
    if left == right:
      return i
  return None


def print_grid(rows):
  for row in rows:
    print(row)


def all_smudges(original_rows):
  index, dir = find_mirror(original_rows)
  mirror_size = min(index + 1, (len(original_rows) if dir == "row" else len(original_rows[0])) - index - 1)
  mirror_range = range(index + 1 - mirror_size, index + mirror_size)
  rows = original_rows.copy()
  for smudge_row in mirror_range if dir == "row" else range(len(rows)):
    for smudge_col in mirror_range if dir == "col" else range(len(rows[0])):
      fixed_char = "#" if rows[smudge_row][smudge_col] == "." else "."
      rows[smudge_row] = rows[smudge_row][:smudge_col] + fixed_char + rows[smudge_row][smudge_col + 1:]
      index, dir = find_mirror(rows)
      if index is not None:
        print_grid(rows)
        return (index + 1) * (100 if dir == "row" else 1), (smudge_row, smudge_col)
      rows = original_rows.copy()


def find_mirror(rows):
  columns = find_columns(rows)
  index = scan(rows)
  if index is not None:
    return index, "row"
  return scan(columns), "col"


def main(file):
  grids = read_input(file)
  total = 0
  for rows in grids:
    result, smudge = all_smudges(rows)
    print("result:", result)
    print("smudge:", smudge)
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
