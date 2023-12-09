import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass, field


@dataclass
class Card:
  id: int
  winning_nums: set[int]
  my_nums: set[int]
  num_winners: int = field(init=False)

  def __post_init__(self):
    self.num_winners = len(self.winning_nums.intersection(self.my_nums))


def read_input(file):
  cards = dict()
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"^Card\s+(\d+): (.*) \| (.*)$", line):
        index = int(match.group(1))
        cards[index] = Card(
          index,
          set(int(num_str) for num_str in re.split(r"\s+", match.group(2).strip())),
          set(int(num_str) for num_str in re.split(r"\s+", match.group(3).strip()))
        )
      else:
        raise Exception(f"invalid input line: {line}")
  return cards


def main(file):
  cards = read_input(file)
  acquired_copies = [key for key in cards.keys()]
  total_copies = 0
  while len(acquired_copies) > 0:
    card_id = acquired_copies.pop()
    total_copies += 1
    for index in range(card_id + 1, card_id + cards[card_id].num_winners + 1):
      acquired_copies.append(index)
  return total_copies


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
