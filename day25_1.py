import time
from argparse import ArgumentParser


DECODING = {
  "=": -2,
  "-": -1,
  "0": 0,
  "1": 1,
  "2": 2
}

ENCODING = dict((v, k) for k, v in DECODING.items())


def parse(line):
  # snafu = []
  # for c in line.strip():
  #   try:
  #     i = int(c)
  #     if i > 2:
  #       raise Exception(f"digit {i} too large, in input {line}")
  #     snafu.append(i)
  #   except ValueError:
  #     if c == "-":
  #       snafu.append(-1)
  #     elif c == "=":
  #       snafu.append(-2)
  #     else:
  #       raise Exception(f"invalid character {c}, in input {line}")
  # return snafu
  return [DECODING[c] for c in line.strip()]


def read_snafus(file):
  snafus = []
  with open(file, "r") as f:
    for line in f:
      snafus.append(parse(line))
  return snafus


def decode(snafu):
  number = 0
  for position, digit in enumerate(reversed(snafu)):
    number += digit * (5**position)
  return number


def max_value(position):
  total = 0
  for i in range(position + 1):
    total += 2 * (5 ** i)
  return total


def get_digit(number, position):
  if number < 0:
    digit = 0
    remainder = number + 5 ** position
    while remainder <= max_value(position - 1):
      remainder += 5 ** position
      digit -= 1
  else:
    digit = 0
    remainder = number - 5 ** position
    while remainder >= -max_value(position - 1):
      remainder -= 5 ** position
      digit += 1
  return digit

def encode(number):
  max_position = 1
  while max_value(max_position) < number:
    max_position += 1
  snafu = []
  remainder = number
  for position in range(max_position, -1, -1):
    digit = get_digit(remainder, position)
    snafu.append(digit)
    remainder -= (digit * (5 ** position))
  result = "".join(ENCODING[d] for d in snafu)
  print(f"{number} encodes to {result}, decodes to {decode(snafu)}")
  return result


def main(file):
  snafus = read_snafus(file)
  sum = 0
  for snafu in snafus:
    number = decode(snafu)
    print(f"{snafu} => {number}")
    sum += number
  print(f"\nsum: {sum}, snafu encoding: {encode(sum)}")


def test():
  assert encode(4890) == "2=-1=0"
  assert encode(1747) == "1=-0-2"
  assert encode(906) == "12111"
  assert encode(198) == "2=0="
  assert encode(11) == "21"
  assert encode(201) == "2=01"
  assert encode(31) == "111"
  assert encode(1257) == "20012"
  assert encode(32) == "112"
  assert encode(353) == "1=-1="
  assert encode(107) == "1-12"
  assert encode(7) == "12"
  assert encode(3) == "1="
  assert encode(37) == "122"


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  # main(args.file)
  test()
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
