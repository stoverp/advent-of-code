import time
from argparse import ArgumentParser


def read_input(file):
  symbols = dict()
  with open(file, "r") as f:
    row = 0
    nums = []
    for line in f:
      print(line.strip())
      num_chars = []
      start_col, end_col = None, None
      for col, c in enumerate(line):
        if c.isnumeric():
          if len(num_chars) == 0:
            start_col = col
          num_chars.append(c)
        else:
          if c not in [".", "\n"]:
            symbols[(row, col)] = True
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
  return nums, symbols


def adj(num_object, symbols):
  for row in [num_object['row'] - 1, num_object['row'] + 1]:
    for col in range(num_object['start_col'] - 1, num_object['end_col'] + 2):
      if (row, col) in symbols:
        return True
  return (num_object['row'], num_object['start_col'] - 1) in symbols or \
         (num_object['row'], num_object['end_col'] + 1) in symbols


def main(file):
  nums, symbols = read_input(file)
  print(nums, symbols)
  parts = []
  for num_object in nums:
    if adj(num_object, symbols):
      parts.append(num_object['num'])
    else:
      print(f"{num_object['num']} is not adjacent to a symbol")
  return sum(parts)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
