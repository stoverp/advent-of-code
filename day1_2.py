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

  top_elves = sorted(elves, reverse=True)[0:3]
  print(f"top elves: {top_elves}")
  print(f"total top elf calories: {sum(top_elves)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args)
