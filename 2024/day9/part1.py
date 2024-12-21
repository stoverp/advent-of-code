import re
import time
from argparse import ArgumentParser


def read(file):
  disk = []
  file_id = 0
  with open(file, "r") as f:
    for line in f:
      for i, c in enumerate(line.strip()):
        if i % 2 == 0:
          # file
          disk.extend([file_id] * int(c))
          file_id += 1
        else:
          # space
          disk.extend(["."] * int(c))
  return disk


def print_disk(disk):
  print("".join(str(n) for n in disk))


def first_index(disk, val):
  for i, c in enumerate(disk):
    if c == val:
      return i


def checksum(disk):
  total = 0
  for i, n in enumerate(disk):
    total += i * n
  return total


def main(file):
  disk = read(file)
  print_disk(disk)
  empty_indices = []
  for i, val in enumerate(disk):
    if val == ".":
      empty_indices.append(i)
  while empty_indices:
    moving_c = disk.pop()
    if moving_c == ".":
      continue
    empty_index = empty_indices.pop(0)
    if empty_index > len(disk):
      disk.append(moving_c)
    else:
      disk[empty_index] = moving_c
  print_disk(disk)
  return checksum(disk)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))