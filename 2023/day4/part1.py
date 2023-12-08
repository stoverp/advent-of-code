import re
import time
from argparse import ArgumentParser

def main(file):
  score = 0
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"^Card\s+(\d+): (.*) \| (.*)$", line):
        card_num = match.group(1)
        winning_nums = set(int(num_str) for num_str in re.split(r"\s+", match.group(2).strip()))
        my_nums = set(int(num_str) for num_str in re.split(r"\s+", match.group(3).strip()))
        num_winner_picks = len(winning_nums.intersection(my_nums))
        if num_winner_picks > 0:
          score += 2 ** (num_winner_picks - 1)
      else:
        raise Exception(f"invalid input line: {line}")
  return score


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
