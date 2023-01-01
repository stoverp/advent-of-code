from argparse import ArgumentParser
from functools import cmp_to_key


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


def read_packets(file):
  packets = []
  with open(file, "r") as f:
    for line in f:
      if not line.strip():
        continue
      packets.append(eval(line))
  return packets


def main(file):
  divider_packets = [
    [[2]],
    [[6]]
  ]
  packets = read_packets(file)
  packets.extend(divider_packets)
  packets.sort(key=cmp_to_key(in_order))
  print("\nsorted packets:")
  print("\n".join(str(packet) for packet in packets))
  divider_indices = []
  for divider_packet in divider_packets:
    divider_indices.append(packets.index(divider_packet) + 1)
  print(f"\ndivider positions: {divider_indices}, decoder key: {divider_indices[0] * divider_indices[1]}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
