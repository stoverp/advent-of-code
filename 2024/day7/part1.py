import re
import time
from argparse import ArgumentParser


def combine(expression, operands):
  if len(operands) == 0:
    return [expression]
  if not expression:
    return combine(operands[0], operands[1:])
  results = []
  for operator in ["+", "*"]:
    results.extend(combine(f"{expression} {operator} {operands[0]}", operands[1:]))
  return results


def evaluate(expression):
  pieces = expression.split(" ")
  total = 0
  operator = None
  for piece in pieces:
    if piece.isnumeric():
      total = total * int(piece) if operator == "*" else total + int(piece)
    else:
      operator = piece
  return total


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
    expressions = combine("", operands)
    for expression in expressions:
      if evaluate(expression) == target:
        print(f"{target} = {expression}")
        total += target
        break
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
