import re
import time
from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class Strength(Enum):
  HIGH_CARD = 1
  ONE_PAIR = 2
  TWO_PAIR = 3
  THREE_OF_A_KIND = 4
  FULL_HOUSE = 5
  FOUR_OF_A_KIND = 6
  FIVE_OF_A_KIND = 7


@dataclass
class Hand:
  cards: str
  bid: int


def strength(cards):
  count_by_label = defaultdict(int)
  for card in cards:
    count_by_label[card] += 1
  match sorted(count_by_label.values()):
    case [5]:
      return Strength.FIVE_OF_A_KIND
    case [1, 4]:
      return Strength.FOUR_OF_A_KIND
    case [2, 3]:
      return Strength.FULL_HOUSE
    case [1, 1, 3]:
      return Strength.THREE_OF_A_KIND
    case [1, 2, 2]:
      return Strength.TWO_PAIR
    case [1, 1, 1, 2]:
      return Strength.ONE_PAIR
    case _:
      return Strength.HIGH_CARD


def read_input(file):
  hands_by_strength = defaultdict(list)
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"(\w+) (\d+)$", line):
        cards = match.group(1)
        hands_by_strength[strength(cards)].append(Hand(cards, int(match.group(2))))
      else:
        raise Exception(f"invalid input line: {line}")
  return hands_by_strength


def to_hex(card):
  match card:
    case "T":
      return "A"
    case "J":
      return "B"
    case "Q":
      return "C"
    case "K":
      return "D"
    case "A":
      return "E"
    case _:
      return card


def main(file):
  hands_by_strength = read_input(file)
  sorted_hands = []
  for strength in Strength:
    sorted_hands.extend(sorted(hands_by_strength[strength], key=lambda hand: [to_hex(card) for card in hand.cards]))
  total = 0
  for rank, hand in enumerate(sorted_hands):
    print(hand.cards)
    total += hand.bid * (rank + 1)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
