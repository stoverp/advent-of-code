from argparse import ArgumentParser


def read_next_pair(f):
  left, right = f.readline().strip(), f.readline().strip()
  f.readline()
  return (eval(left), eval(right)) if (left and right) else None


def in_order(left, right, depth=0):
  print(f"{'  ' * depth}- Compare {left} vs\n{'  ' * depth}          {right}")
  if isinstance(left, int) and isinstance(right, int):
    if left == right:
      return 0
    elif left < right:
      print(f"{'  ' * (depth + 1)}- Left side is smaller, so inputs are in the right order")
      return -1
    else:  # right > left
      print(f"{'  ' * (depth + 1)}- Right side is smaller, so inputs are not in the right order")
      return 1
  if isinstance(left, int):
    left = [left]
    print(f"{'  ' * (depth + 1)}- Mixed types; convert left to {left} and retry comparison")
  if isinstance(right, int):
    right = [right]
    print(f"{'  ' * (depth + 1)}- Mixed types; convert right to {right} and retry comparison")
  for i in range(len(left)):
    if i >= len(right):
      print(f"{'  ' * (depth + 1)}- Right side ran out of items, so inputs are not in the right order")
      return 1
    order = in_order(left[i], right[i], depth + 1)
    if order != 0:
      return order
  if len(left) == len(right):
    return 0
  else:
    print(f"{'  ' * (depth + 1)}- Left side ran out of items, so inputs are in the right order")
    return -1


def main(file):
  with open(file, "r") as f:
    good_pairs = []
    pair_number = 1
    while (pair := read_next_pair(f)):
      (left, right) = pair
      print(f"\n== Pair {pair_number} ==")
      if in_order(left, right) != 1:
        good_pairs.append(pair_number)
      pair_number += 1
  print(f"\nin-order pairs: {good_pairs}")
  print(f"sum: {sum(good_pairs)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
