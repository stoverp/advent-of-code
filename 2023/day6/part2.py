import re
import time
from argparse import ArgumentParser


def read_input(file):
  time = None
  distance = None
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"^Time: (.*)$", line):
        time = int("".join(re.split(r"\s+", match.group(1).strip())))
      elif match := re.match(r"^Distance: (.*)$", line):
        distance = int("".join(re.split(r"\s+", match.group(1).strip())))
      else:
        raise Exception(f"invalid input line: {line}")
  return time, distance


def main(file):
  time, best_distance = read_input(file)
  num_wins = 0
  for button_time in range(1, time - 1):
    speed = button_time
    distance = speed * (time - button_time)
    if distance > best_distance:
      num_wins += 1
  return num_wins


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
