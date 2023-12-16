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


def strength(cards) -> Strength:
  count_by_label = defaultdict(int)
  num_jokers = 0
  for card in cards:
    if card == "J":
      num_jokers += 1
    else:
      count_by_label[card] += 1
  counts = sorted(count_by_label.values(), reverse=True)
  match (counts[0] if counts else 0) + num_jokers:
    case 5:
      return Strength.FIVE_OF_A_KIND
    case 4:
      return Strength.FOUR_OF_A_KIND
    case 3:
      return Strength.FULL_HOUSE if counts[1] > 1 else Strength.THREE_OF_A_KIND
    case 2:
      return Strength.TWO_PAIR if counts[1] > 1 else Strength.ONE_PAIR
    case 1:
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
    case "J":
      return "1"
    case "T":
      return "A"
    case "Q":
      return "B"
    case "K":
      return "C"
    case "A":
      return "D"
    case _:
      return card


def main(file):
  hands_by_strength = read_input(file)
  sorted_hands = []
  for strength in Strength:
    sorted_hands.extend([(hand, strength) for hand in sorted(hands_by_strength[strength],
      key=lambda hand: [to_hex(card) for card in hand.cards])])
  total = 0
  for rank, (hand, strength) in enumerate(sorted_hands):
    print(hand.cards, hand.bid, strength)
    total += hand.bid * (rank + 1)
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
