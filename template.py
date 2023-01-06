import re
import time
from argparse import ArgumentParser

def main(file):
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      if match := re.match("<REGEX>$", line):
        print(f"<group 1>: {match.group(1)}")
      else:
        raise Exception(f"invalid input line: {line}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
