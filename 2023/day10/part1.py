import re
import time
from argparse import ArgumentParser


def read_input(file):
  board = []
  with open(file, "r") as f:
    for line in f:
      board.append([c for c in line.strip()])
  start = None
  for row, line in enumerate(board):
    for col, c in enumerate(line):
      if c == "S":
        start = (row, col)
  return start, board


def adj(point, board):
  row, col = point
  match board[row][col]:
    case "|":
      return [(row - 1, col), (row + 1, col)]
    case "-":
      return [(row, col - 1), (row, col + 1)]
    case "L":
      return [(row - 1, col), (row, col + 1)]
    case "J":
      return [(row - 1, col), (row, col - 1)]
    case "7":
      return [(row, col - 1), (row + 1, col)]
    case "F":
      return [(row, col + 1), (row + 1, col)]


def start_steps(start, board):
  steps = []
  start_row, start_col = start
  for row, col in [
    (start_row - 1, start_col),
    (start_row + 1, start_col),
    (start_row, start_col - 1),
    (start_row, start_col + 1)
  ]:
    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] != ".":
      # steps.append((row, col))
      neighbors = adj((row, col), board)
      if start in neighbors:
        steps.append((row, col))
  return steps


def main(file):
  start, board = read_input(file)
  steps = start_steps(start, board)
  found = {start, steps[0], steps[1]}
  n_steps = 1
  while steps[0] != steps[1]:
    n_steps += 1
    next_steps = []
    for step in steps:
      var = [n for n in adj(step, board) if n not in found]
      next_step, = var
      next_steps.append(next_step)
    found.update(next_steps)
    steps = next_steps
  return n_steps


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
