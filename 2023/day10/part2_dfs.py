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
      neighbors = adj((row, col), board)
      if start in neighbors:
        steps.append((row, col))
  return steps


def main(file):
  start, board = read_input(file)
  display(board)
  loop = find_loop(start, board)
  display(board, loop)
  outside = dfs(board, loop, set(), set(), 0, 0)
  display(board, loop, outside)


def can_slide(row, col, next_row, next_col, position, board):
  # if pipe in ["L", "J", "7", "F"]:
  #   return True
  # elif next_row - row != 0:
  #   return pipe == "-"
  # elif next_col - col != 0:
  #   return pipe == "|"
  # else:
  #   raise Exception("invalid move")
  if board[row][col] == "|":
    



def dfs(board, loop, found, outside, row, col):
  for next_row, next_col in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
    if 0 <= next_row < len(board) and 0 <= next_col < len(board[0]):
      if (next_row, next_col) not in found:
        found.add((next_row, next_col))
        if (next_row, next_col) not in loop:
          # junk pipe, outside loop
          outside.add((next_row, next_col))
          dfs(board, loop, found, outside, next_row, next_col)
        elif can_slide(row, col, next_row, next_col, board[next_row][next_col]):
          dfs(board, loop, found, outside, next_row, next_col)
  return outside


def display(board, loop=None, outside=None):
  for row in range(len(board)):
    for col in range(len(board[0])):
      if not loop:
        print(board[row][col], end="")
      elif (row, col) in loop:
        print(board[row][col], end="")
      elif outside and (row, col) in outside:
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
