import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Node:
  name: str
  left: str
  right: str


def read_input(file):
  with open(file, "r") as f:
    nodes = dict()
    for line in f:
      if not line.strip():
        continue
      if match := re.match(r"^([RL]+)$", line):
        instructions = [c for c in match.group(1)]
      elif match := re.match(r"^(\w+) = \((\w+), (\w+)\)$", line):
        nodes[match.group(1)] = Node(match.group(1), match.group(2),  match.group(3))
      else:
        raise Exception(f"invalid input line: {line}")
  return instructions, nodes


def main(file):
  instructions, nodes = read_input(file)
  print(instructions)
  print(nodes)
  location = "AAA"
  print(location)
  num_steps = 0
  while location != "ZZZ":
    num_steps += 1
    instruction = instructions.pop(0)
    instructions.append(instruction)
    match instruction:
      case "L":
        location = nodes[location].left
      case "R":
        location = nodes[location].right
    print(location)
  return num_steps


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
