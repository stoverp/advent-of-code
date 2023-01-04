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

  def params(self, monkeys):
    known_value, known_i, unknown_variable = None, None, None
    for i, operand in enumerate(self.operands):
      print(f"operand monkey: {monkeys[operand]}")
      if monkeys[operand].result:
        known_i = i
        known_value = monkeys[operand].result
      else:
        unknown_variable = operand
    return known_value, known_i, unknown_variable


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
          if name == "humn":
            # humn is you, don't know result
            monkey = Monkey("humn")
          else:
            monkey = Monkey(name, result=int(number_match.group(1)))
            queue.append(name)
        else:
          raise Exception(f"invalid input line: {line}")
        monkeys[name] = monkey
      else:
        raise Exception(f"invalid input line: {line}")
  return monkeys, dependees, queue


def print_monkeys(monkeys):
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


def equate(monkeys):
  print(f"\nroot monkey: {monkeys['root']}")
  known_value, known_i, unknown_variable = monkeys["root"].params(monkeys)
  print(f"at root, need to make {unknown_variable} == {known_value} ...\n")
  monkey = monkeys[unknown_variable]
  monkey.result = known_value
  while unknown_variable != "humn":
    print(f"resolving {monkey} ...")
    known_value, known_i, unknown_variable = monkey.params(monkeys)
    if monkey.operation == "+":
      # unknown + known_value = desired_result
      monkeys[unknown_variable].result = monkey.result - known_value
    elif monkey.operation == "*":
      # unknown * known_value = desired_result
      monkeys[unknown_variable].result = monkey.result / known_value
    elif monkey.operation == "-":
      if known_i == 0:
        # known_value - unknown = desired_result
        monkeys[unknown_variable].result = known_value - monkey.result
      else:
        # unknown - known_value = desired_result
        monkeys[unknown_variable].result = monkey.result + known_value
    elif monkey.operation == "/":
      if known_i == 0:
        # known_value / unknown = desired_result
        monkeys[unknown_variable].result = known_value / monkey.result
      else:
        # unknown / known_value = desired_result
        monkeys[unknown_variable].result = monkey.result * known_value
    else:
      raise Exception(f"unknown operation for monkey {monkey}")
    monkey = monkeys[unknown_variable]


def main(file):
  monkeys, dependees, queue = read_monkeys(file)
  print("\nMonkeys:")
  print_monkeys(monkeys)
  print("\nDependees:")
  print("\n".join(f"{name}: {d}" for name, d in dependees.items()))
  print("\nQueue:")
  print(queue)
  print("\nFirst attempt at resolved monkeys:")
  resolve_monkeys(monkeys, dependees, queue)
  print_monkeys(monkeys)
  print()
  # now we should have resolved one side of root, let's look up the other side
  equate(monkeys)
  print(f"\nfinal human state: {monkeys['humn']}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
