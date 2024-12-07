import re
import time
from argparse import ArgumentParser


def main(file):
  with open(file, "r") as f:
    for line in f:
      numbers = re.split(r"\s+", line)
      print(numbers)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))