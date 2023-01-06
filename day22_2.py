import re
import time
from argparse import ArgumentParser
from copy import deepcopy
from enum import Enum


class Facing(bytes, Enum):
  RIGHT = (0, ">")
  DOWN = (1, "v")
  LEFT = (2, "<")
  UP = (3, "^")

  def __new__(cls, value, icon):
    obj = bytes.__new__(cls, [value])
    obj._value_ = value
    obj.icon = icon
    return obj

  def __str__(self):
    return self.name.lower()

  def __repr__(self):
    return str(self)

  def turn(self, direction):
    assert direction in "LR"
    return Facing((self.value + (1 if direction == "R" else -1)) % len(Facing))


def read_input(file):
  board = []
  with open(file, "r") as f:
    for line in f:
      if not line.strip():
        break
      board.append(list(line.rstrip()))
    moves = re.findall(r"\d+|[LR]", f.readline())
  return board, moves


def wrap(value, bounds):
  if value > bounds[1]:
    # wrap to the left side
    return bounds[0]
  elif value < bounds[0]:
    # wrap to the right side
    return bounds[1]
  return value


def walk(position, column_bounds_at_row, row_bounds_at_column):
  if position[2] == Facing.RIGHT:
    row = position[0]
    col = wrap(position[1] + 1, column_bounds_at_row[position[0]])
    return row, col, position[2]
  elif position[2] == Facing.DOWN:
    row = wrap(position[0] + 1, row_bounds_at_column[position[1]])
    col = position[1]
    return row, col, position[2]
  elif position[2] == Facing.LEFT:
    row = position[0]
    col = wrap(position[1] - 1, column_bounds_at_row[position[0]])
    return row, col, position[2]
  elif position[2] == Facing.UP:
    row = wrap(position[0] - 1, row_bounds_at_column[position[1]])
    col = position[1]
    return row, col, position[2]
  raise Exception(f"invalid facing direction in {position}")


def draw(position, board):
  board[position[0]][position[1]] = position[2].icon


def bounds(board):
  column_bounds_at_row = []
  max_row_index = 0
  for row in board:
    start_col = None
    end_col = None
    col_index = 0
    for col_index, c in enumerate(row):
      if c in ".#" and start_col is None:
        start_col = col_index
      elif c == " " and start_col is not None:
        end_col = col_index - 1
        break
    # if we get to the end of the row before finding a space, end is last column
    end_col = end_col or col_index
    if end_col > max_row_index:
      max_row_index = end_col
    column_bounds_at_row.append((start_col, end_col))
  row_bounds_at_column = []
  for col_index in range(max_row_index + 1):
    start_row = None
    end_row = None
    row_index = 0
    for row_index in range(len(board)):
      if col_index >= len(board[row_index]):
        end_row = row_index - 1
        break
      elif board[row_index][col_index] in ".#" and start_row is None:
        start_row = row_index
      elif board[row_index][col_index] == " " and start_row is not None:
        end_row = row_index - 1
        break
    # if we get to the end of the column before finding a space, end is last row
    end_row = end_row or row_index
    row_bounds_at_column.append((start_row, end_row))
  print(f"row_bounds: {column_bounds_at_row}")
  print(f"col_bounds: {row_bounds_at_column}")
  return column_bounds_at_row, row_bounds_at_column


def print_board(board):
  print()
  for row in board:
    print("".join(row))


def password(position):
  return ((position[0] + 1) * 1000) + ((position[1] + 1) * 4) + position[2].value


def main(file):
  board, moves = read_input(file)
  print_board(board)
  column_bounds_at_row, row_bounds_at_column = bounds(board)
  walked_on_board = deepcopy(board)
  # find starting position
  position = None
  for col, c in enumerate(board[0]):
    if c == '.':
      position = (0, col, Facing.RIGHT)
      break
  print(f"starting position: {position}")
  draw(position, walked_on_board)
  for move in moves:
    try:
      distance = int(move)
      for _ in range(distance):
        new_position = walk(position, column_bounds_at_row, row_bounds_at_column)
        if board[new_position[0]][new_position[1]] == ".":
          # we can move forward to this open space
          position = new_position
          draw(position, walked_on_board)
      print(f"{move}: move {distance} spaces {position[2]}, new position: {position}")
    except ValueError:
      position = (position[0], position[1], position[2].turn(move))
      draw(position, walked_on_board)
      print(f"{move}: turn {'right' if move == 'R' else 'left'}, new position: {position}")
  print_board(walked_on_board)
  print(f"\nfinal position: {position}, password: {password(position)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
