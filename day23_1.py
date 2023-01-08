import sys
import time
from argparse import ArgumentParser
from collections import defaultdict
from enum import Enum


def to_xy_offsets(x_offsets, y_offsets, excluded):
  return [(x, y) for x in x_offsets for y in y_offsets if (x, y) not in excluded]


SCAN_OFFSETS = [-1, 0, 1]
ADJACENT_OFFSETS = to_xy_offsets(SCAN_OFFSETS, SCAN_OFFSETS, [(0, 0)])


class Move(bytes, Enum):
  NORTH = (0, 0, 1)
  SOUTH = (1, 0, -1)
  WEST = (2, -1, 0)
  EAST = (3, 1, 0)

  def __new__(cls, value, x, y):
    obj = bytes.__new__(cls, [value])
    obj._value_ = value
    obj.x = x
    obj.y = y
    obj.x_offsets = SCAN_OFFSETS if x == 0 else [x]
    obj.y_offsets = SCAN_OFFSETS if y == 0 else [y]
    return obj

  def __str__(self):
    return self.name.lower()

  def __repr__(self):
    return str(self)


class Elf(object):
  def __init__(self, id, x, y):
    self.id = id
    self.x = x
    self.y = y

  def __hash__(self):
    return hash((self.id, self.x, self.y))

  def __eq__(self, other):
    if not other:
      return False
    return self.id == other.id and self.x == other.x and self.y == other.y

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f"Elf(id={self.id}, x={self.x}, y={self.y})"


def read_elves(file):
  elves_present = []
  with open(file, "r") as f:
    for line in f:
      elves_present.append([True if c == '#' else False for c in line.strip()])
  elves = dict()
  elf_id = 0
  for row, line in enumerate(elves_present):
    for col, v in enumerate(line):
      if v:
        elves[(col, len(elves_present) - 1 - row)] = elf_id
        elf_id += 1
  return elves


def find_bounds(elves):
  sorted_by_x = sorted(elves.keys())
  sorted_by_y = sorted(elves.keys(), key=lambda k: k[1])
  return (sorted_by_x[0][0], sorted_by_x[-1][0]), (sorted_by_y[0][1], sorted_by_y[-1][1])


def print_board(elves):
  n_empty_ground = 0
  x_bounds, y_bounds = find_bounds(elves)
  for y in range(y_bounds[1], y_bounds[0] - 1, -1):
    for x in range(x_bounds[0], x_bounds[1] + 1):
      if (x, y) in elves:
        # print(elves[(x, y)], end="")
        print("#", end="")
      else:
        n_empty_ground += 1
        print(".", end="")
    print()
  print()
  return n_empty_ground


def is_clear(offsets, elf_position, elves):
  for (x, y) in offsets:
    if (elf_position[0] + x, elf_position[1] + y) in elves:
      return False
  return True


def proposed_move(elf_position, elves, move_order):
  if is_clear(ADJACENT_OFFSETS, elf_position, elves):
    return None
  else:
    for move in move_order:
      if is_clear(to_xy_offsets(move.x_offsets, move.y_offsets, []), elf_position, elves):
        return elf_position[0] + move.x, elf_position[1] + move.y
  return None


def shift_move_order(move_order):
  move_order.append(move_order.pop(0))


def run(move_order, elves):
  proposed_moves = defaultdict(list)
  for elf_position, elf_id in elves.items():
    new_position = proposed_move(elf_position, elves, move_order)
    if new_position:
      proposed_moves[new_position].append((elf_id, elf_position))
  print(f"proposed moves: {proposed_moves}")
  if not proposed_moves:
    return True
  for new_position, old_elves in proposed_moves.items():
    if len(old_elves) == 1:
      elf_id, old_position = old_elves[0]
      elves[new_position] = elf_id
      del elves[old_position]
  return False


def main(file, n_rounds):
  n_empty_ground = None
  elves = read_elves(file)
  print("== Initial State ==")
  print_board(elves)
  move_order = [Move.NORTH, Move.SOUTH, Move.WEST, Move.EAST]
  round = 0
  for round in range(1, n_rounds + 1):
    print(f"move order: {move_order}")
    is_done = run(move_order, elves)
    if is_done:
      break
    shift_move_order(move_order)
    print(f"elves after applying non-colliding proposed moves: {elves}")
    print(f"\n== End of Round {round} ==")
    n_empty_ground = print_board(elves)
  print(f"\nfirst round where no elf moved: {round}")
  print(f"final number of empty ground tiles: {n_empty_ground}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("--n_rounds", type=int, default=sys.maxsize)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.n_rounds)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
