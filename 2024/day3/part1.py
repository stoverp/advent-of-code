import re
import time
from argparse import ArgumentParser

def read(file):
  pairs = []
  with open(file, "r") as f:
    for line in f:
      matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
      pairs.extend([(int(x), int(y)) for x, y in matches])
  return pairs


def main(file):
  pairs = read(file)
  print(pairs)
  total = 0
  for x, y in pairs:
    total += x * y
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))