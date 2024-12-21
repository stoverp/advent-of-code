import re
import time
from argparse import ArgumentParser


def combine(operands):
  if not operands:
    return [("", 0)]
  results = []
  for partial in combine(operands[0:-1]):
    results.append(("+", partial + operands[-1]))
    results.append(("*", partial * operands[-1]))
  return results


def read(file):
  results = []
  operands = []
  with open(file, "r") as f:
    for line in f:
      numbers = [int(n) for n in re.findall(r"\d+", line)]
      results.append(numbers[0])
      operands.append(numbers[1:])
  return results, operands


def main(file):
  targets, all_operands = read(file)
  total = 0
  for target, operands in zip(targets, all_operands):
    results = combine(operands)
    print(results)
    if target in results:
      print("it works!")
      total += target
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
