from argparse import ArgumentParser

def main(args):
  i = 0
  elves = [0]
  with open(args.file, "r") as f:
    for line in f:
      text = line.strip()
      if text.isnumeric():
        elves[i] += int(text)
      else:
        i += 1
        elves.append(0)
  print(f"{len(elves)} elves")
  print(f"elf calories: {elves}")
  print(f"max calories: {max(elves)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args)
