import re
import time
from argparse import ArgumentParser

def read(file):
  pairs = []
  read_pairs = True
  with open(file, "r") as f:
    for line in f:
      for match in re.finditer(r"mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)|(?P<do>do)\(\)|(?P<dont>don't)\(\)", line):
        print(match)
        if match.group("do"):
          print("do")
          read_pairs = True
        elif match.group("dont"):
          print("dont")
          read_pairs = False
        elif read_pairs:
          pairs.append((int(match.group("x")), int(match.group("y"))))
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