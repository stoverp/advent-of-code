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
          disk.extend([str(file_id)] * int(c))
          file_id += 1
        else:
          # space
          disk.extend(["."] * int(c))
  return disk, file_id


def print_disk(disk):
  print("".join(str(n) for n in disk))


def checksum(disk):
  total = 0
  for i, v in enumerate(disk):
    if v.isnumeric():
      total += i * int(v)
  return total


def has_room(empty_indices, file_indices):
  contiguous = 1
  last_v = None
  length = len(file_indices)
  for index, v in enumerate(empty_indices):
    if v > file_indices[0]:
      return None
    if last_v is None or v - last_v > 1:
      contiguous = 1
    else:
      contiguous += 1
    if contiguous == length:
      return index - (length - 1)
    last_v = v
  return None


def main(file):
  disk, num_files = read(file)
  # print_disk(disk)
  print(disk)
  empty_indices = []
  for i, val in enumerate(disk):
    if val == ".":
      empty_indices.append(i)
  for file_id in range(num_files - 1, -1, -1):
    file_indices = [i for i, v in enumerate(disk) if v == str(file_id)]
    empty_index = has_room(empty_indices, file_indices)
    if empty_index is not None:
      for i in file_indices:
        disk[i] = "."
        disk[empty_indices.pop(empty_index)] = str(file_id)
  # print_disk(disk)
  print(disk)
  return checksum(disk)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))