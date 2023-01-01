import re
from argparse import ArgumentParser


def print_directory_tree(name, entry, level=0):
  print(f"{'  ' * level} - {name}", end=" ")
  if isinstance(entry, dict):
    print("(dir)")
    for name, directory in entry.items():
      print_directory_tree(name, directory, level + 1)
  else:
    print(f"(file, size={entry})")


def compute_directory_sizes(current_path, directory, sizes):
  total_size = 0
  for name, entry in directory.items():
    if isinstance(entry, dict):
      total_size += compute_directory_sizes(f"{current_path}/{name}", entry, sizes)
    else:
      total_size += entry
  sizes[current_path] = total_size
  # print(f"total size of directory {current_path}: {total_size}")
  return total_size


def main(file):
  root_directory = dict()
  current_directory = root_directory
  current_path = []
  with open(file, "r") as f:
    for line in f:
      # print("\n" + line.strip())
      if match := re.match("\$ cd (.+)", line):
        directory = match.group(1)
        if directory == "..":
          current_path.pop()
          # cd to parent path iteratively from root
          current_directory = root_directory
          for dir in current_path:
            current_directory = current_directory[dir]
        elif directory == "/":
          current_directory = root_directory
          current_path = []
        else:
          if directory not in current_directory:
            current_directory[directory] = dict()
          current_directory = current_directory[directory]
          current_path += [directory]
        # print(f"current path: {current_path}")
      elif re.match("\$ ls", line):
        pass
      elif match := re.match("dir (.+)", line):
        directory = match.group(1)
        if directory not in current_directory:
          current_directory[directory] = dict()
        # print(f"found directory: {directory}")
      elif match := re.match("(\d+) (.+)", line):
        size = int(match.group(1))
        filename = match.group(2)
        current_directory[filename] = size
        # print(f"found file: {filename}, size: {size}")
      else:
        raise Exception(f"invalid line: {line}")
  print("\nfile system:")
  print_directory_tree("/", root_directory)
  sizes = dict()
  compute_directory_sizes("", root_directory, sizes)
  # print("\ndirectory sizes:")
  # for dir, size in sizes.items():
  #   print(f"{dir}: {size}")
  small_dirs_total_size = sum([size for size in sizes.values() if size <= 100000])
  print(f"\ntotal size of small directories (<= 100000): {small_dirs_total_size}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
