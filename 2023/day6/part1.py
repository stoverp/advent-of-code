import re
import time
from argparse import ArgumentParser


def read_input(file):
  times = None
  distances = None
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"^Time: (.*)$", line):
        times = re.split(r"\s+", match.group(1).strip())
      elif match := re.match(r"^Distance: (.*)$", line):
        distances = re.split(r"\s+", match.group(1).strip())
      else:
        raise Exception(f"invalid input line: {line}")
  return [(int(time), int(distance)) for time, distance in zip(times, distances)]


def main(file):
  races = read_input(file)
  total = 1
  for time, best_distance in races:
    num_wins = 0
    for button_time in range(1, time - 1):
      speed = button_time
      distance = speed * (time - button_time)
      if distance > best_distance:
        num_wins += 1
    total *= num_wins
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
