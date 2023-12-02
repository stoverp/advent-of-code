import re
from argparse import ArgumentParser
from bidict import bidict

ROCK = "R"
PAPER = "P"
SCISSORS = "S"
WIN = "W"
LOSE = "L"
DRAW = "D"
DEFEATS = bidict({
  ROCK: SCISSORS,
  SCISSORS: PAPER,
  PAPER: ROCK
})
ELF_PLAYS = {
  "A": ROCK,
  "B": PAPER,
  "C": SCISSORS
}
DESIRED_OUTCOMES = {
  "X": LOSE,
  "Y": DRAW,
  "Z": WIN
}
PLAY_SCORE = {
  ROCK: 1,
  PAPER: 2,
  SCISSORS: 3
}


def your_play(elf_play, desired_outcome):
  if desired_outcome == WIN:
    return DEFEATS.inverse[elf_play], 6
  elif desired_outcome == LOSE:
    return DEFEATS[elf_play], 0
  else:
    return elf_play, 3


def main(file):
  score = 0
  with open(file, "r") as f:
    for line in f:
      print()
      if match := re.match("([ABC])\\s*([XYZ])", line):
        elf_play = ELF_PLAYS[match.group(1)]
        desired_output = DESIRED_OUTCOMES[match.group(2)]
      else:
        raise Exception(f"bad input line: {line}")
      print(line.strip())
      the_play, outcome_score = your_play(elf_play, desired_output)
      print(elf_play, desired_output, the_play, PLAY_SCORE[the_play], outcome_score)
      score += PLAY_SCORE[the_play] + outcome_score
  print(f"final score: {score}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
