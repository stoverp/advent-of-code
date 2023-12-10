import re
import time
from argparse import ArgumentParser

def read_input(file):
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      if match := re.match(r"<REGEX>$", line):
        print(f"<group 1>: {match.group(1)}")
      else:
        raise Exception(f"invalid input line: {line}")
  return -1


def main(file):
  vars = read_input(file)
  return -1


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
