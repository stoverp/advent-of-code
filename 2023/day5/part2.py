import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Dict


@dataclass()
class Map:
  dest_start: int
  source_start: int
  range: int


@dataclass()
class Category:
  source: str
  dest: str
  maps: list[Map]


def read_input(file):
  with open(file, "r") as f:
    seed_ranges = []
    source = None
    categories: Dict[str, Category] = dict()
    for line in f:
      if not line.strip():
        continue
      if match := re.match(r"^(\w+)-to-(\w+) map:$", line):
        source = match.group(1)
        categories[source] = Category(source, match.group(2), [])
      elif match := re.match(r"^(\d+) (\d+) (\d+)$", line):
        categories[source].maps.append(
          Map(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        )
      elif match := re.match(r"^seeds: (.*)$", line):
        for seed_str in re.findall(r"\d+\s+\d+", match.group(1)):
          start, num = re.split(r"\s+", seed_str)
          # seeds.extend(int(seed) for seed in range(int(start), int(start) + int(num)))
          seed_ranges.append((int(start), int(start) + int(num)))
      else:
        raise Exception(f"invalid input line: {line}")
    for category in categories.values():
      category.maps = sorted(category.maps, key=lambda m: m.source_start)
      print(f"{category.source}: {category.maps}")
  return seed_ranges, categories


def find_lower_bound(item: int, maps: list[Map]):
  low = 0
  high = len(maps) - 1
  while low < high:
    mid = (low + high) // 2
    if maps[mid].source_start == item:
      return mid
    elif maps[mid].source_start < item:
      if maps[mid + 1].source_start > item:
        return mid
      low = mid + 1
    else:
      high = mid - 1
  return low


def dest_item(item: int, category: Category):
  lower_bound = find_lower_bound(item, category.maps)
  map = category.maps[lower_bound]
  if map.source_start <= item < map.source_start + map.range:
    return (item - map.source_start) + map.dest_start
  return item


def main(file):
  seed_ranges, categories = read_input(file)
  min_location = None
  for start, end in seed_ranges:
    print(f"seed range: {start}-{end}")
    for seed in range(start, end):
      source = "seed"
      item = seed
      while source != "location":
        # print(f"{source} {item}, ", end="")
        category = categories[source]
        item = dest_item(item, category)
        source = category.dest
      if (seed - start) % 1_000_000 == 0:
        print(f"seed {seed} -> {source} {item}.")
      if not min_location or item < min_location:
        min_location = item
  return min_location


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
