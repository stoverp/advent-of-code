import re
import time
from argparse import ArgumentParser
from collections import defaultdict


class Monkey(object):
  def __init__(self, name, operands=None, operation=None, result=None):
    self.name = name
    self.operands = operands
    self.operation = operation
    self.result = result

  def __repr__(self):
    return f"Monkey(name={self.name}, operands={self.operands}, operation={self.operation}, result={self.result})"

  def resolve(self, values):
    self.result = eval(self.operation.join(str(v) for v in values))


def read_monkeys(file):
  monkeys = dict()
  dependees = defaultdict(list)
  queue = []
  with open(file, "r") as f:
    for line in f:
      # print("\n" + line.strip())
      if match := re.match(r"(\w+): (.+)$", line):
        name = match.group(1)
        rhs = match.group(2)
        # print(f"monkey: {name}, rhs: {rhs}")
        if operand_match := re.match(r"(\w+) ([+-/*]) (\w+)", rhs):
          operands = [operand_match.group(1), operand_match.group(3)]
          operation = operand_match.group(2)
          monkey = Monkey(name, operands=operands, operation=operation)
          for operand in operands:
            dependees[operand].append(name)
        elif number_match := re.match(r"(-?\d+)$", rhs):
          monkey = Monkey(name, result=int(number_match.group(1)))
          queue.append(name)
        else:
          raise Exception(f"invalid input line: {line}")
        monkeys[name] = monkey
      else:
        raise Exception(f"invalid input line: {line}")
  return monkeys, dependees, queue


def print_monkeys(monkeys):
  print("\nMonkeys:")
  print("\n".join(str(m) for m in monkeys.values()))


def resolve_monkeys(monkeys, dependees, queue):
  while queue:
    monkey_name = queue.pop()
    for dep_monkey in dependees[monkey_name]:
      operands = monkeys[dep_monkey].operands
      resolved_values = []
      for operand in operands:
        if monkeys[operand].result:
          resolved_values.append(monkeys[operand].result)
      if len(resolved_values) == len(operands):
        # we can resolve this monkey!
        monkeys[dep_monkey].resolve(resolved_values)
        # add our newly resolved monkey to the queue
        queue.append(dep_monkey)


def main(file):
  monkeys, dependees, queue = read_monkeys(file)
  print_monkeys(monkeys)
  print("\nDependees:")
  print("\n".join(f"{name}: {d}" for name, d in dependees.items()))
  print("\nQueue:")
  print(queue)
  resolve_monkeys(monkeys, dependees, queue)
  print_monkeys(monkeys)
  print(f"\nroot yells {monkeys['root'].result}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
