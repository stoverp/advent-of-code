from argparse import ArgumentParser


WINDOW_SIZE = 4


def main(file):
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      start = find_start_position(line)
      print(f"starting position: {start}\n")


def find_start_position(line):
    window = ""
    for i, c in enumerate(line):
      # print(f"window: {window}")
      num_unique = len(set(window))
      if num_unique == WINDOW_SIZE:
        print(f"window {window} is complete and unique")
        return i
      window = window[-(WINDOW_SIZE-1):] + c


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
