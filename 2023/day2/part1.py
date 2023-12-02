import re
import time
from argparse import ArgumentParser

BAG = {
  "red": 12,
  "green": 13,
  "blue": 14
}


def game(pulls):
  for pull in pulls:
    print("pull:")
    for color_pull in re.split("\s*,\s*", pull):
      print(color_pull)
      num_str, color = color_pull.split(" ")
      if int(num_str) > BAG[color]:
        return False
  return True


def main(file):
  total = 0
  with open(file, "r") as f:
    for line in f:
      print(line.strip())
      if match := re.match(r"Game (\d+): (.*)$", line.strip()):
        game_num = int(match.group(1))
        pulls = re.split(r"\s*;\s*", match.group(2))
        possible = game(pulls)
        print(f"Game {game_num} is {'' if possible else 'not '}possible\n")
        if possible:
          total += game_num
      else:
        raise Exception(f"invalid input line: {line}")
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
