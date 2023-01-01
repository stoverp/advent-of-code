import string
from argparse import ArgumentParser


PRIORITIES = string.ascii_lowercase + string.ascii_uppercase


def priority(item):
  return PRIORITIES.index(item) + 1


def read_rucksack_groups(file):
  rucksacks = list([])
  with open(file, "r") as f:
    while True:
      rucksack = []
      for _ in range(0, 3):
        text = f.readline().strip()
        if not text:
          return rucksacks
        rucksack.append(text)
      rucksacks.append(rucksack)


def main(file):
  priority_sum = 0
  for group in read_rucksack_groups(file):
    common_item = set(group[0]).intersection(set(group[1])).intersection(set(group[2])).pop()
    item_priority = priority(common_item)
    print(group, common_item, item_priority)
    priority_sum += item_priority
  print(f"\nthe final priority sum: {priority_sum}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
