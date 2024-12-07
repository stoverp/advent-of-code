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
      return i + 1
  return None


def print_grid(rows):
  for row in rows:
    print(row)


def all_smudges(original_rows):
  original_index = find_mirror(original_rows)
  cleaned_rows = original_rows.copy()
  for smudge_row in range(len(cleaned_rows)):
    for smudge_col in range(len(cleaned_rows[0])):
      fixed_char = "#" if cleaned_rows[smudge_row][smudge_col] == "." else "."
      cleaned_rows[smudge_row] = cleaned_rows[smudge_row][:smudge_col] + fixed_char + \
                                 cleaned_rows[smudge_row][smudge_col + 1:]
      index = find_mirror(cleaned_rows)
      if index is not None and index != original_index:
        print_grid(cleaned_rows)
        return index, (smudge_row, smudge_col)
      cleaned_rows = original_rows.copy()


def find_mirror(rows):
  columns = find_columns(rows)
  index = scan(columns)
  if index is not None:
    return index
  index = scan(rows)
  if index is not None:
    return index * 100
  return None


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
