import time
from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce


def read_input(file):
  gears = dict()
  with open(file, "r") as f:
    row = 0
    nums = []
    for line in f:
      num_chars = []
      start_col, end_col = None, None
      for col, c in enumerate(line):
        if c.isnumeric():
          if len(num_chars) == 0:
            start_col = col
          num_chars.append(c)
        else:
          if c == '*':
            gears[(row, col)] = True
          if len(num_chars) > 0:
            num = int("".join(num_chars))
            nums.append({
              'num': num,
              'start_col': start_col,
              'end_col': col - 1,
              'row': row
            })
            num_chars = []
      row += 1
  return nums, gears


def adj_gears(num_object, gears, gear_nearby_nums):
  for row in [num_object['row'] - 1, num_object['row'] + 1]:
    for col in range(num_object['start_col'] - 1, num_object['end_col'] + 2):
      if (row, col) in gears:
        gear_nearby_nums[(row, col)].add(num_object['num'])
  for col in [num_object['start_col'] - 1, num_object['end_col'] + 1]:
    if (num_object['row'], col) in gears:
      gear_nearby_nums[(num_object['row'], col)].add(num_object['num'])


def main(file):
  total = 0
  nums, gears = read_input(file)
  gear_nearby_nums = defaultdict(set)
  for num_object in nums:
    adj_gears(num_object, gears, gear_nearby_nums)
  print(gear_nearby_nums)
  for nums in gear_nearby_nums.values():
    if len(nums) == 2:
      total += reduce(lambda x, y: x * y, nums)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
