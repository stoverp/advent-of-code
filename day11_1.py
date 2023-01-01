import re
from argparse import ArgumentParser
from functools import reduce
from pprint import PrettyPrinter


class Monkey(object):
  def __init__(self, items, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false):
    self.items = items
    self.operation = operation
    self.divisible_test = divisible_test
    self.monkey_throw_on_true = monkey_throw_on_true
    self.monkey_throw_on_false = monkey_throw_on_false
    self.n_items_inspected = 0

  def __repr__(self):
    return f"Monkey(items={self.items}, operation={self.operation}, divisible_test={self.divisible_test}, monkey_throw_on_true={self.monkey_throw_on_true}, monkey_throw_on_false={self.monkey_throw_on_false})"


def read_monkeys(file):
  monkeys = []
  with open(file, "r") as f:
    for line in f:
      if match := re.match("Monkey (\d+):$", line):
        current_monkey = int(match.group(1))
        if current_monkey > 0:
          monkeys.append(Monkey(items, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false))
      elif re.match("\s*Starting items:", line):
        items = [int(match.group(0)) for match in re.finditer("\d+", line)]
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
  monkeys.append(Monkey(items, operation, divisible_test, monkey_throw_on_true, monkey_throw_on_false))
  return monkeys


def print_monkey_items(monkeys):
  print("\n".join(f"Monkey {i}: {monkey.items}" for i, monkey in enumerate(monkeys)))
  print()


def main(file):
  monkeys = read_monkeys(file)
  PrettyPrinter().pprint(monkeys)
  print(f"Initially, monkeys are holding items with these worry levels:")
  print_monkey_items(monkeys)
  n_rounds = 20
  for round in range(1, n_rounds + 1):
    print(f"Round {round}:\n")
    for i, monkey in enumerate(monkeys):
      print(f"Monkey {i}:")
      for item in monkey.items:
        monkey.n_items_inspected += 1
        print(f"  Monkey inspects an item with a worry level of {item}.")
        new_item = eval(monkey.operation.replace("old", str(item)))
        print(f"    run operation '{monkey.operation}' on item {item}: {new_item}.")
        new_item //= 3
        print(f"    monkey is bored, worry level divided by 3 to {new_item}.")
        is_divisible = new_item % monkey.divisible_test == 0
        print(f"    Current worry level {new_item} {'is' if is_divisible else 'is not'} divisible by {monkey.divisible_test}.")
        throw_to_monkey = monkey.monkey_throw_on_true if is_divisible else monkey.monkey_throw_on_false
        print(f"    Item with worry level {new_item} is thrown to monkey {throw_to_monkey}.")
        monkeys[throw_to_monkey].items.append(new_item)
      monkey.items = []
    print(f"After round {round}, monkeys are holding items with these worry levels:")
    print_monkey_items(monkeys)
  inspected = [monkey.n_items_inspected for monkey in monkeys]
  print("\n".join(f"Monkey {i} inspected items {n} times." for i, n in enumerate(inspected)))
  top_two_inspected = sorted(inspected, reverse=True)[:2]
  print(f"\nTotal monkey business: {reduce(lambda x, y: x * y, top_two_inspected)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
