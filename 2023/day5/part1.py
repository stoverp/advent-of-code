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
    seeds = None
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
        seeds = [int(seed) for seed in re.findall(r"\d+", match.group(1))]
      else:
        raise Exception(f"invalid input line: {line}")
  return seeds, categories


def dest_item(item: int, category: Category):
  for map in category.maps:
    if map.source_start <= item < map.source_start + map.range:
      return (item - map.source_start) + map.dest_start
  return item


def main(file):
  seeds, categories = read_input(file)
  locations = []
  for seed in seeds:
    source = "seed"
    item = seed
    while source != "location":
      print(f"{source} {item}, ", end="")
      category = categories[source]
      item = dest_item(item, category)
      source = category.dest
    print(f"{source} {item}.")
    locations.append(item)
  return min(locations)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
