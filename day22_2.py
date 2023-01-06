import re
import time
from argparse import ArgumentParser
from copy import deepcopy
from enum import Enum


class FaceInfo(object):
  def __init__(self, id, wrappings):
    self.id = id
    self.wrappings = wrappings
    self.start_row = None
    self.start_col = None

  def start_coord(self, row, col):
    self.start_row = row
    self.start_col = col


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

  @staticmethod
  def from_abbr(abbr):
    if abbr == "R":
      return Facing.RIGHT
    elif abbr == "D":
      return Facing.DOWN
    elif abbr == "L":
      return Facing.LEFT
    elif abbr == "U":
      return Facing.UP
    else:
      raise Exception(f"invalid abbr: {abbr}")

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


def wrap(position, face_board, faces_info, max_coord):
  # convert to face coords
  face = int(face_board[position[0]][position[1]])
  face_position = (position[0] - faces_info[face].start_row, position[1] - faces_info[face].start_col, position[2])
  # wrap to new face
  new_face, new_face_position = change_face(face, face_position, faces_info, max_coord)
  # convert to real coords
  return new_face_position[0] + faces_info[new_face].start_row, new_face_position[1] + faces_info[new_face].start_col, new_face_position[2]


def change_face(face, face_position, faces_info, max_coord):
  old_row, old_col, old_facing = face_position
  new_face, new_facing = faces_info[face].wrappings[face_position[2]]
  if old_facing == Facing.RIGHT:
    if new_facing == Facing.RIGHT:
      return new_face, (old_row, 0, new_facing)
    elif new_facing == Facing.DOWN:
      return new_face, (0, max_coord - old_row, new_facing)
    elif new_facing == Facing.LEFT:
      return new_face, (max_coord - old_row, max_coord, new_facing)
    elif new_facing == Facing.UP:
      return new_face, (max_coord, old_row, new_facing)
  elif old_facing == Facing.DOWN:
    if new_facing == Facing.RIGHT:
      return new_face, (max_coord - old_col, 0, new_facing)
    elif new_facing == Facing.DOWN:
      return new_face, (0, old_col, new_facing)
    elif new_facing == Facing.LEFT:
      return new_face, (old_col, max_coord, new_facing)
    elif new_facing == Facing.UP:
      return new_face, (max_coord, max_coord - old_col, new_facing)
  elif old_facing == Facing.LEFT:
    if new_facing == Facing.RIGHT:
      return new_face, (max_coord - old_row, 0, new_facing)
    elif new_facing == Facing.DOWN:
      return new_face, (0, old_row, new_facing)
    elif new_facing == Facing.LEFT:
      return new_face, (old_row, max_coord, new_facing)
    elif new_facing == Facing.UP:
      return new_face, (max_coord, max_coord - old_row, new_facing)
  elif old_facing == Facing.UP:
    if new_facing == Facing.RIGHT:
      return new_face, (old_col, 0, new_facing)
    elif new_facing == Facing.DOWN:
      return new_face, (0, max_coord - old_col, new_facing)
    elif new_facing == Facing.LEFT:
      return new_face, (max_coord - old_col, max_coord, new_facing)
    elif new_facing == Facing.UP:
      return new_face, (max_coord, old_col, new_facing)
  raise Exception(f"invalid (old_facing={old_facing}, new_facing={new_facing}) combo")


def walk(position, column_bounds_at_row, row_bounds_at_column, face_board, faces_info, max_coord):
  if position[2] == Facing.RIGHT:
    if position[1] + 1 <= column_bounds_at_row[position[0]][1]:
      return position[0], position[1] + 1, position[2]
  elif position[2] == Facing.DOWN:
    if position[0] + 1 <= row_bounds_at_column[position[1]][1]:
      return position[0] + 1, position[1], position[2]
  elif position[2] == Facing.LEFT:
    if position[1] - 1 >= column_bounds_at_row[position[0]][0]:
      return position[0], position[1] - 1, position[2]
  elif position[2] == Facing.UP:
    if position[0] - 1 >= row_bounds_at_column[position[1]][0]:
      return position[0] - 1, position[1], position[2]
  return wrap(position, face_board, faces_info, max_coord)


def draw(position, board):
  board[position[0]][position[1]] = position[2].icon


def bounds(board):
  column_bounds_at_row = []
  max_col = 0
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
    if end_col > max_col:
      max_col = end_col
    column_bounds_at_row.append((start_col, end_col))
  row_bounds_at_column = []
  for col_index in range(max_col + 1):
    start_row = None
    end_row = None
    row_index = 0
    for row_index in range(len(board)):
      if col_index >= len(board[row_index]):
        if start_row is None:
          continue
        else:
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
  print(f"column_bounds_at_row: {column_bounds_at_row}")
  print(f"row_bounds_at_column: {row_bounds_at_column}")
  return column_bounds_at_row, row_bounds_at_column


def print_board(board):
  print()
  for row in board:
    print("".join(row))


def password(position):
  return ((position[0] + 1) * 1000) + ((position[1] + 1) * 4) + position[2].value


def populate_face_bounds(face_board, faces_info):
  last_face = None
  for row, line in enumerate(face_board):
    for col, c in enumerate(line):
      if c == ' ':
        continue
      if c != last_face:
        face = int(c)
        if faces_info[face].start_row is None:
          faces_info[face].start_coord(row, col)
        last_face = face


def read_faces(faces_file):
  face_board = []
  faces_info = dict()
  with open(faces_file, "r") as f:
    for line in f:
      if not line.strip():
        break
      face_board.append(list(line.rstrip()))
    for line in f:
      if line.startswith("#") or not line.strip():
        continue
      if match := re.match(r"(\d+): (.*)$", line):
        face = int(match.group(1))
        wrappings = dict()
        for direction, wrapping in enumerate(match.group(2).split(", ")):
          wrappings[Facing(direction)] = (int(wrapping[0]), Facing.from_abbr(wrapping[1]))
        faces_info[face] = FaceInfo(face, wrappings)
  populate_face_bounds(face_board, faces_info)
  return face_board, faces_info


def main(file, faces_file, max_coord):
  board, moves = read_input(file)
  print_board(board)
  face_board, faces_info = read_faces(faces_file)
  print_board(face_board)
  print(faces_info)
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
        new_position = walk(position, column_bounds_at_row, row_bounds_at_column, face_board, faces_info, max_coord)
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
  parser.add_argument("faces_file")
  parser.add_argument("cube_length", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.faces_file, args.cube_length - 1)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
