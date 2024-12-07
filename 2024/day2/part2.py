import re
import time
from argparse import ArgumentParser
from numbers import Number


def is_safe_dampened(numbers):
  if is_safe(numbers):
    return True
  for i in range(len(numbers)):
    short_numbers = numbers[0:i] + numbers[i+1:]
    if is_safe(short_numbers):
      return True
  return False


def is_safe(numbers):
  direction = None
  last_n = None
  for n in numbers:
    if last_n is not None:
      if 1 <= abs(last_n - n) <= 3:
        current_direction = 1 if n > last_n else -1
        if direction is None:
          direction = current_direction
        elif direction != current_direction:
          return False
      else:
        return False
    last_n = n
  return True


def main(file):
  safe_count = 0
  with open(file, "r") as f:
    for line in f:
      numbers = [int(n) for n in re.split(r"\s+", line.strip())]
      safe = is_safe_dampened(numbers)
      if safe:
        safe_count += 1
      print(numbers, safe)
  return safe_count


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))