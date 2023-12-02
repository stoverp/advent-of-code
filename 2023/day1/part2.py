import re
import time
from argparse import ArgumentParser

DIGITS = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
  "six": 6,
  "seven": 7,
  "eight": 8,
  "nine": 9,
}

PATTERN = re.compile(r"(?=(" + "|".join(DIGITS.keys()) + r"|\d))")
print(PATTERN)

def first_digit(candidates):
  for c in candidates:
    if c.isnumeric():
      return str(c)
    elif c in DIGITS:
      return str(DIGITS[c])


def candidates(string):
  result = re.findall(PATTERN, string)
  print(result)
  return result


def main(file):
  nums = []
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      num = int(first_digit(candidates(line)) + first_digit(candidates(line)[::-1]))
      print(num, "\n")
      nums.append(num)
  return sum(nums)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
