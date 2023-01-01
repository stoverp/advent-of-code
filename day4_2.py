import re
from argparse import ArgumentParser

def main(file):
  total_count = 0
  with open(file, "r") as f:
    for line in f:
      print()
      if match := re.match("(\\d+)-(\\d+),(\\d+)-(\\d+)", line):
        elf1_range, elf2_range = (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))
        print(elf1_range, elf2_range)
        if elf2_range[0] < elf1_range[0]:
          # swap elves to sort ranges by start
          elf2_range, elf1_range = elf1_range, elf2_range
        if elf1_range[1] >= elf2_range[0]:
          print("ranges overlap")
          total_count += 1
  print(f"final count of overlapping ranges: {total_count}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
