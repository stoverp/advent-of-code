import re
from argparse import ArgumentParser


ROCK = "R"
PAPER = "P"
SCISSORS = "S"
DEFEATS = {
  ROCK: SCISSORS,
  SCISSORS: PAPER,
  PAPER: ROCK
}
ELF_PLAYS = {
  "A": ROCK,
  "B": PAPER,
  "C": SCISSORS
}
YOUR_PLAYS = {
  "X": ROCK,
  "Y": PAPER,
  "Z": SCISSORS
}
PLAY_SCORE = {
  ROCK: 1,
  PAPER: 2,
  SCISSORS: 3
}


def result(elf_play, your_play):
  if DEFEATS[your_play] == elf_play:
    # win
    return 6
  elif elf_play == your_play:
    # draw
    return 3
  else:
    # lose
    return 0


def main(file):
  score = 0
  with open(file, "r") as f:
    for line in f:
      if match := re.match("([ABC])\\s*([XYZ])", line):
        elf_play = ELF_PLAYS[match.group(1)]
        your_play = YOUR_PLAYS[match.group(2)]
        print(elf_play, your_play)
      else:
        raise Exception(f"bad input line: {line}")
      score += (ps := PLAY_SCORE[your_play])
      score += (rs := result(elf_play, your_play))
      print(ps, rs)
      print()
  print(f"final score: {score}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
