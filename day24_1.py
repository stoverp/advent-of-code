import sys
import time
from argparse import ArgumentParser
from collections import defaultdict


class BoardState:
  def __init__(self, position, blizzards):
    self.position = position
    self.blizzards = blizzards

  def __str__(self):
    return f"Blizzard(position={self.position}, blizzards={self.blizzards})"

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash(repr(self.position) + repr(sorted(self.blizzards.items())))

  def __eq__(self, other):
    if not other:
      return False
    return other.position == self.position and other.blizzards == self.blizzards


class Global:
  blizzard_cache = dict()


def read_blizzards(file):
  blizzards = defaultdict(list)
  with open(file, "r") as f:
    row = 0
    for line in f:
      for col, c in enumerate(line.strip()):
        if c in ">^<v":
          blizzards[(row - 1, col - 1)].append(c)
      row += 1
      n_cols = col - 1
    n_rows = row - 2
  return blizzards, n_rows, n_cols


def print_board(position, blizzards, n_rows, n_cols):
  for row in range(-1, n_rows + 1):
    for col in range(-1, n_cols + 1):
      if (row, col) == position:
        print("E", end="")
      elif (row, col) in [(-1, 0), (n_rows, n_cols - 1)]:
        print(".", end="")
      elif row < 0 or row == n_rows:
        print("#", end="")
      elif col < 0 or col == n_cols:
        print("#", end="")
      elif (row, col) in blizzards:
        if len(blizzards[row, col]) > 1:
          print(len(blizzards[row, col]), end="")
        else:
          print(blizzards[(row, col)][0], end="")
      else:
        print(".", end="")
    print()
  print()


def wrap(p, n_rows, n_cols):
  if p[0] < 0:
    return n_rows - 1, p[1]
  elif p[0] >= n_rows:
    return 0, p[1]
  elif p[1] < 0:
    return p[0], n_cols - 1
  elif p[1] >= n_cols:
    return p[0], 0
  else:
    return p


def advance(blizzards, n_rows, n_cols):
  new_blizzards = defaultdict(list)
  for p, directions in blizzards.items():
    for d in directions:
      if d == ">":
        new_p = (p[0], p[1] + 1)
      elif d == "<":
        new_p = (p[0], p[1] - 1)
      elif d == "^":
        new_p = (p[0] - 1, p[1])
      elif d == "v":
        new_p = (p[0] + 1, p[1])
      else:
        raise Exception(f"invalid direction: {d}")
      new_blizzards[wrap(new_p, n_rows, n_cols)].append(d)
  return new_blizzards


def path(start, dest, prev):
  p = dest
  path = []
  while p != start:
    path.append(p)
    p = prev[p]
  path.append(start)
  return list(reversed(path))


def in_bounds(p, n_rows, n_cols):
  return 0 <= p[0] < n_rows and 0 <= p[1] < n_cols


def adjacent(position, blizzards, n_rows, n_cols):
  candidates = [
    (position[0] - 1, position[1]),
    (position[0] + 1, position[1]),
    (position[0], position[1] - 1),
    (position[0], position[1] + 1)
  ]
  return [c for c in candidates if in_bounds(c, n_rows, n_cols) and c not in blizzards]


def get_blizzards(minute, n_rows, n_cols):
  if minute in Global.blizzard_cache:
    return Global.blizzard_cache[minute]
  Global.blizzard_cache[minute] = advance(Global.blizzard_cache[minute - 1], n_rows, n_cols)
  return Global.blizzard_cache[minute]


def bfs(start, dest, n_rows, n_cols):
  queue = [(start, 1)]
  prev = dict()
  dist = defaultdict(lambda: sys.maxsize)
  dist[start] = 1
  while queue:
    position, minute = queue.pop(0)
    if position == dest:
      return path(start, position, prev)
    next_minute = minute + 1
    next_blizzards = get_blizzards(next_minute, n_rows, n_cols)
    print_board(position, next_blizzards, n_rows, n_cols)
    for next_position in adjacent(position, next_blizzards, n_rows, n_cols):
      if next_minute < dist[next_position]:
        dist[next_position] = next_minute
        prev[next_position] = position
        queue.append((next_position, next_minute))
    # can always just wait it out
    queue.append((position, next_minute))


def main(file):
  blizzards, n_rows, n_cols = read_blizzards(file)
  print(blizzards)
  print("Initial state:")
  print_board((-1, 0), blizzards, n_rows, n_cols)
  Global.blizzard_cache[0] = blizzards
  get_blizzards(1, n_rows, n_cols)
  path = bfs((0, 0), (n_rows - 1, n_cols - 1), n_rows, n_cols)
  print(f"best path: {path}")
  minute = 1
  # include exit position for better visualization
  path.append((n_rows, n_cols - 1))
  for position in path:
    # input()
    print(f"Minute {minute}:")
    print_board(position, get_blizzards(minute, n_rows, n_cols), n_rows, n_cols)
    minute += 1


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
