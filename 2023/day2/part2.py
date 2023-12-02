import re
import time
from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce

def game(pulls):
  max_per_color = defaultdict(int)
  for pull in pulls:
    for color_pull in re.split(r"\s*,\s*", pull):
      num_str, color = color_pull.split(" ")
      max_per_color[color] = max(max_per_color[color], int(num_str))
  return reduce(lambda x, y: x * y, max_per_color.values())


def main(file):
  total = 0
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"Game (\d+): (.*)$", line.strip()):
        pulls = re.split(r"\s*;\s*", match.group(2))
        power = game(pulls)
        total += power
      else:
        raise Exception(f"invalid input line: {line}")
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
