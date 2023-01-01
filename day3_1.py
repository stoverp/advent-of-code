import string
from argparse import ArgumentParser


PRIORITIES = string.ascii_lowercase + string.ascii_uppercase


def priority(item):
  return PRIORITIES.index(item) + 1


def main(file):
  priority_sum = 0
  with open(file, "r") as f:
    for line in f:
      text = line.strip()
      midpoint = int(len(text) / 2)
      compartment1, compartment2 = text[0:midpoint], text[midpoint:]
      common_item = set(compartment1).intersection(set(compartment2)).pop()
      item_priority = priority(common_item)
      print(compartment1, compartment2, common_item, item_priority)
      priority_sum += item_priority
  print(f"\nfinal priority sum: {priority_sum}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
