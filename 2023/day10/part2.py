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
  dirs = []
  start_row, start_col = start
  for row, col, dir in [
    (start_row - 1, start_col, "U"),
    (start_row + 1, start_col, "D"),
    (start_row, start_col - 1, "L"),
    (start_row, start_col + 1, "R")
  ]:
    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] != ".":
      neighbors = adj((row, col), board)
      if start in neighbors:
        steps.append((row, col))
        dirs.append(dir)
  board[start_row][start_col] = pipe(dirs)
  return steps


def pipe(dirs):
  match "".join(sorted(dirs)):
    case "LR":
      return "-"
    case "DU":
      return "|"
    case "LU":
      return "J"
    case "RU":
      return "L"
    case "DL":
      return "7"
    case "DR":
      return "F"


def main(file):
  start, board = read_input(file)
  # display(board)
  loop = find_loop(start, board)
  # display(board, loop)
  inside = find_inside(board, loop)
  # display(board, loop, inside)
  return len(inside)


def find_inside(board, loop):
  inside = set()
  for row in range(len(board)):
    for col in range(len(board[0])):
      if is_inside(board, loop, row, col):
        inside.add((row, col))
  return inside


def is_inside(board, loop, row, col):
  if (row, col) in loop:
    return False
  n_crossings = 0
  start_pipe = None
  for check_col in range(col + 1, len(board[0])):
    if (row, check_col) not in loop:
      continue
    else:
      match board[row][check_col]:
        case "|":
          n_crossings += 1
        case "F":
          start_pipe = "F"
        case "L":
          start_pipe = "L"
        case "7":
          n_crossings += 2 if start_pipe == "F" else 1
          start_pipe = None
        case "J":
          n_crossings += 2 if start_pipe == "L" else 1
          start_pipe = None
  return n_crossings % 2 == 1


def display(board, loop=None, inside=None):
  for row in range(len(board)):
    for col in range(len(board[0])):
      if not loop:
        print(board[row][col], end="")
      elif (row, col) in loop:
        print(board[row][col], end="")
      elif inside:
        if (row, col) in inside:
          print("I", end="")
        else:
          print("O", end="")
      else:
        print(".", end="")
    print()
  print()


def find_loop(start, board):
  steps = start_steps(start, board)
  loop = {start, steps[0], steps[1]}
  while steps[0] != steps[1]:
    next_steps = []
    for step in steps:
      var = [n for n in adj(step, board) if n not in loop]
      next_step, = var
      next_steps.append(next_step)
    loop.update(next_steps)
    steps = next_steps
  return loop


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
