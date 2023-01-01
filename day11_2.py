import re
from argparse import ArgumentParser
from functools import reduce
from pprint import PrettyPrinter


class Monkey(object):
  def __init__(self, indices_owned, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false):
    self.indices_owned = indices_owned
    self.operation = operation
    self.divisible_test = divisible_test
    self.monkey_throw_on_true = monkey_throw_on_true
    self.monkey_throw_on_false = monkey_throw_on_false
    self.item_values = None
    self.n_items_inspected = 0

  def set_item_values(self, item_values):
    self.item_values = item_values.copy()

  def __repr__(self):
    return f"Monkey(item_view={self.item_values}, indices_owned={self.indices_owned}, operation={self.operation}, divisible_test={self.divisible_test}, monkey_throw_on_true={self.monkey_throw_on_true}, monkey_throw_on_false={self.monkey_throw_on_false})"

  def apply_operation(self, operation, item_index):
    op_str = operation.replace("old", str(self.item_values[item_index]))
    self.item_values[item_index] = eval(op_str) % self.divisible_test
    op_str

  def is_divisible(self, item_index):
    return self.item_values[item_index] % self.divisible_test == 0

  def print_items(self, monkey_index):
    print(f"Monkey {monkey_index}: " + ", ".join(f'{i} ({self.item_values[i]})' for i in self.indices_owned))


def read_monkeys(file):
  monkeys = []
  item_values = []
  with open(file, "r") as f:
    for line in f:
      if match := re.match("Monkey (\d+):$", line):
        current_monkey = int(match.group(1))
        if current_monkey > 0:
          monkeys.append(Monkey(indices_owned, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false))
      elif re.match("\s*Starting items:", line):
        new_items = [int(match.group(0)) for match in re.finditer("\d+", line)]
        indices_owned = list(range(len(item_values), len(item_values) + len(new_items)))
        item_values.extend(new_items)
      elif match := re.match("\s*Operation: new = (.*)$", line):
        operation = match.group(1)
      elif match := re.match("\s*Test: divisible by (\d+)$", line):
        divisible_test = int(match.group(1))
      elif match := re.match("\s*If true: throw to monkey (\d+)$", line):
        monkey_throw_on_true = int(match.group(1))
      elif match := re.match("\s*If false: throw to monkey (\d+)$", line):
        monkey_throw_on_false = int(match.group(1))
      elif len(line.strip()) == 0:
        continue
      else:
        raise Exception(f"invalid input line: {line}")
  monkeys.append(Monkey(indices_owned, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false))
  for monkey in monkeys:
    monkey.set_item_values(item_values)
  return monkeys


def print_monkey_items(monkeys):
  for i, monkey in enumerate(monkeys):
    monkey.print_items(i)
  print()


def main(file):
  monkeys = read_monkeys(file)
  PrettyPrinter().pprint(monkeys)
  print(f"Initially, monkeys are holding items with these worry levels:")
  print_monkey_items(monkeys)
  n_rounds = 10000
  for round in range(1, n_rounds + 1):
    # print(f"Round {round}:\n")
    for monkey_index, monkey in enumerate(monkeys):
      # print(f"Monkey {monkey_index}:")
      for item_index in monkey.indices_owned:
        monkey.n_items_inspected += 1
        # print(f"  Monkey inspects item {item_index}, with worry level of {monkey.item_values[item_index]}.")
        # print(f"    Apply operation 'new = ({monkey.operation})' on item {item_index} to all monkeys.")
        for op_monkey in monkeys:
          op_monkey.apply_operation(monkey.operation, item_index)
        is_divisible = monkey.is_divisible(item_index)
        # print(f"    Current worry level {monkey.item_values[item_index]} {'is' if is_divisible else 'is not'} divisible by {monkey.divisible_test}.")
        throw_to_monkey = monkey.monkey_throw_on_true if is_divisible else monkey.monkey_throw_on_false
        # print(f"    Item {item_index } is thrown to monkey {throw_to_monkey}.")
        monkeys[throw_to_monkey].indices_owned.append(item_index)
      monkey.indices_owned = []
      # print_monkey_items(monkeys)
    if round % 1000 == 0:
      print(f"== After round {round} ==")
      print("\n".join(f"Monkey {i} inspected items {monkey.n_items_inspected} times." for i, monkey in enumerate(monkeys)))
      print()
  top_two_inspected = sorted([monkey.n_items_inspected for monkey in monkeys], reverse=True)[:2]
  print(f"\nTotal monkey business: {reduce(lambda x, y: x * y, top_two_inspected)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
