import time
from argparse import ArgumentParser
from collections import defaultdict


class BoardState:
  def __init__(self, position, blizzards, description):
    self.position = position
    self.blizzards = blizzards
    self.description = description

  def __str__(self):
    return f"BoardState(position={self.position}, blizzards={self.blizzards})"

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash((self.position, hash(self.blizzards)))

  def __eq__(self, other):
    if not other:
      return False
    return other.position == self.position and other.blizzards == self.blizzards

  def print(self, minute=None):
    minute_str = f"Minute {minute}, " if minute else ""
    print(f"{minute_str}{self.description}:")
    self.blizzards.print(self.position)


class Blizzards:
  def __init__(self, blizzards_dict, n_rows, n_cols):
    self.blizzards_dict = blizzards_dict
    self.n_rows = n_rows
    self.n_cols = n_cols

  def __str__(self):
    return f"Blizzards(blizzards_dict={self.blizzards_dict}, n_rows={self.n_rows}, n_cols={self.n_cols})"

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash((repr(sorted(self.blizzards_dict.items())), self.n_rows, self.n_cols))

  def __eq__(self, other):
    if not other:
      return False
    return other.blizzards_dict == self.blizzards_dict and other.n_rows == self.n_rows and other.n_cols == self.n_cols

  def __contains__(self, item):
    return item in self.blizzards_dict

  def wrap(self, p):
    if p[0] < 0:
      return self.n_rows - 1, p[1]
    elif p[0] >= self.n_rows:
      return 0, p[1]
    elif p[1] < 0:
      return p[0], self.n_cols - 1
    elif p[1] >= self.n_cols:
      return p[0], 0
    else:
      return p

  def advance(self):
    if self in Global.blizzard_cache:
      return Global.blizzard_cache[self]
    next_blizzards_dict = defaultdict(list)
    for p, directions in self.blizzards_dict.items():
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
        next_blizzards_dict[self.wrap(new_p)].append(d)
    blizzards = Blizzards(next_blizzards_dict, self.n_rows, self.n_cols)
    Global.blizzard_cache[self] = blizzards
    return blizzards

  def print(self, position):
    for row in range(-1, self.n_rows + 1):
      for col in range(-1, self.n_cols + 1):
        if (row, col) == position:
          print("E", end="")
        elif (row, col) in [(-1, 0), (self.n_rows, self.n_cols - 1)]:
          print(".", end="")
        elif row < 0 or row == self.n_rows:
          print("#", end="")
        elif col < 0 or col == self.n_cols:
          print("#", end="")
        elif (row, col) in self.blizzards_dict:
          if len(self.blizzards_dict[row, col]) > 1:
            print(len(self.blizzards_dict[row, col]), end="")
          else:
            print(self.blizzards_dict[(row, col)][0], end="")
        else:
          print(".", end="")
      print()
    print()


class Global:
  blizzard_cache = dict()


def read_blizzards(file):
  blizzards_dict = defaultdict(list)
  with open(file, "r") as f:
    row = 0
    for line in f:
      for col, c in enumerate(line.strip()):
        if c in ">^<v":
          blizzards_dict[(row - 1, col - 1)].append(c)
      row += 1
      n_cols = col - 1
    n_rows = row - 2
  return Blizzards(blizzards_dict, n_rows, n_cols)


def path(start_state, dest_state, prev):
  state = dest_state
  path = []
  while state != start_state:
    path.append(state)
    state = prev[state]
  path.append(start_state)
  return list(reversed(path))


def in_bounds(p, n_rows, n_cols):
  return 0 <= p[0] < n_rows and 0 <= p[1] < n_cols


def adjacent(position, blizzards):
  candidates = [
    (position, "wait"),
    ((position[0] - 1, position[1]), "move up"),
    ((position[0] + 1, position[1]), "move down"),
    ((position[0], position[1] - 1), "move left"),
    ((position[0], position[1] + 1), "move right")
  ]
  return [(p, d) for p, d in candidates if in_bounds(p, blizzards.n_rows, blizzards.n_cols) and p not in blizzards]


def bfs(start_state, dest_pos):
  queue = [start_state]
  parent = dict()
  visited = set()
  max_distance = 0
  while queue:
    state = queue.pop(0)
    if state.position == dest_pos:
      return path(start_state, state, parent)
    next_blizzards = state.blizzards.advance()
    for next_position, description in adjacent(state.position, next_blizzards):
      next_state = BoardState(next_position, next_blizzards, description)
      if next_state not in visited:
        if next_state.position[0] + next_state.position[1] > max_distance:
          max_distance = next_state.position[0] + next_state.position[1]
          print(f"furthest position evaluated: {next_state.position}")
        visited.add(next_state)
        parent[next_state] = state
        queue.append(next_state)


def main(file):
  initial_blizzards = read_blizzards(file)
  n_rows, n_cols = initial_blizzards.n_rows, initial_blizzards.n_cols
  initial_state = BoardState((-1, 0), initial_blizzards, "initial state")
  initial_state.print()
  # the first step is always the same
  start_state = BoardState((0, 0), initial_blizzards.advance(), "move down")
  path = bfs(start_state, (n_rows - 1, n_cols - 1))
  # print(f"best path: {path}")
  # include exit position for better visualization
  path.append(BoardState((n_rows, n_cols - 1), path[-1].blizzards.advance(), "move down"))
  minute = 0
  for state in path:
    minute += 1
    state.print(minute)
  print(f"\nminimum number of minutes to reach the goal: {minute}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("\n--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
