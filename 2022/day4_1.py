import re
from argparse import ArgumentParser

def main(file):
  total_count = 0
  with open(file, "r") as f:
    for line in f:
      if match := re.match("(\\d+)-(\\d+),(\\d+)-(\\d+)", line):
        elf1_range, elf2_range = (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))
        total_range = (min(elf1_range[0], elf2_range[0]), max(elf1_range[1], elf2_range[1]))
        print(elf1_range, elf2_range, total_range)
        if total_range == elf1_range or total_range == elf2_range:
          print("range is contained by one elf")
          total_count += 1
  print(f"final count of contained ranges: {total_count}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
