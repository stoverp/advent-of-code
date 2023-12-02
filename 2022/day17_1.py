import re
import time
from argparse import ArgumentParser


CAVE_WIDTH = 7
PIECES = [
  {(0, 0), (1, 0), (2, 0), (3, 0)},
  {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
  {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
  {(0, 0), (0, 1), (0, 2), (0, 3)},
  {(0, 0), (1, 0), (0, 1), (1, 1)}
]


def turn_to_rock(piece, cave):
  for x, y in piece:
    while y >= len(cave):
      cave.append([False for _ in range(CAVE_WIDTH)])
    cave[y][x] = True


def drop_piece(piece, cave):
  # print(f"dropping piece {piece} ...")
  dropped_piece = []
  for x, y in piece:
    dropped_y = y - 1
    if dropped_y < 0 or (dropped_y < len(cave) and cave[dropped_y][x]):
      turn_to_rock(piece, cave)
      return None
    dropped_piece.append((x, dropped_y))
  # print(f"dropped piece: {dropped_piece}")
  return dropped_piece


def to_cave_coordinates(piece, cave):
  cave_piece = []
  max_y = 0
  for x, y in piece:
    cave_x, cave_y = x + 2, y + len(cave) + 3
    cave_piece.append((cave_x, cave_y))
    if cave_y > max_y:
      max_y = cave_y
  return cave_piece, max_y


def print_cave(piece, cave, max_y):
  print()
  for y in range(max_y, -1, -1):
    line = []
    for x in range(CAVE_WIDTH):
      if piece and (x, y) in piece:
        line.append("@")
      elif y < len(cave) and cave[y][x]:
        line.append("#")
      else:
        line.append(".")
    print("".join(line))
  # input()

def shift_piece(direction, piece, cave):
  if direction == "<":
    x_shift = -1
  elif direction == ">":
    x_shift = 1
  else:
    raise Exception(f"invalid direction: {direction}")
  # print(f"shift piece {piece} to the {'right' if x_shift == 1 else 'left'} ...")
  shifted_piece = []
  for x, y in piece:
    shifted_x = x + x_shift
    if shifted_x < 0 or shifted_x >= CAVE_WIDTH:
      return piece
    if y < len(cave) and cave[y][shifted_x]:
      return piece
    shifted_piece.append((shifted_x, y))
  # print(f"shifted piece: {shifted_piece}")
  return shifted_piece


def process_piece(piece, shifts, shift_index, cave):
  piece, max_y = to_cave_coordinates(piece, cave)
  # print(f"added piece {piece} ...")
  # print_cave(piece, cave, max_y)
  while piece:
    piece = shift_piece(shifts[shift_index], piece, cave)
    shift_index = (shift_index + 1) % len(shifts)
    # print_cave(piece, cave, max_y)
    piece = drop_piece(piece, cave)
    # print_cave(piece, cave, max_y)
  return shift_index


def main(file, n_pieces):
  with open(file, "r") as f:
    for line in f:
      shifts = list(line.strip())
  cave = []
  shift_index = 0
  for i in range(n_pieces):
    shift_index = process_piece(PIECES[i % len(PIECES)], shifts, shift_index, cave)
  print(f"\ntower is {len(cave)} units tall")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("n_pieces", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.n_pieces)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
