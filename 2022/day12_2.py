from argparse import ArgumentParser


def read_elevations(file):
  elevations = []
  with open(file, "r") as f:
    row_index = 0
    for line in f:
      row = []
      for column_index, c in enumerate(line.strip()):
        if c == "S":
          start = (row_index, column_index)
          row.append(elevation("a"))
        elif c == "E":
          end = (row_index, column_index)
          row.append(elevation("z"))
        else:
          row.append(elevation(c))
      elevations.append(row)
      row_index += 1
  return elevations, start, end


def elevation(char):
  return ord(char) - ord("a")


def print_map(path, elevations, start, end):
  move_map = initialize_move_map(elevations)
  prev_node = path[0]
  for node in path[1:]:
    move_map[prev_node[0]][prev_node[1]] = direction(prev_node, node)
    prev_node = node
  for row_index, row in enumerate(move_map):
    for column_index, c in enumerate(row):
      printed = str(c)
      if (row_index, column_index) == start:
        printed += "S"
      elif (row_index, column_index) == end:
        printed += "E"
      else:
        printed += str(elevations[row_index][column_index])
      print(printed + "\t", end="")
    print()


def initialize_move_map(elevations):
  move_map = []
  for row in elevations:
    move_map.append(["." for _ in range(len(row))])
  return move_map


def direction(prev_position, position):
  if prev_position[0] != position[0]:
    return "v" if position[0] - prev_position[0] == 1 else "^"
  else:
    return ">" if position[1] - prev_position[1] == 1 else "<"


def adjacent(node, elevations):
  adjacent_nodes = []
  if node[0] + 1 < len(elevations):
    adjacent_nodes.append((node[0] + 1, node[1]))
  if node[0] - 1 >= 0:
    adjacent_nodes.append((node[0] - 1, node[1]))
  if node[1] + 1 < len(elevations[0]):
    adjacent_nodes.append((node[0], node[1] + 1))
  if node[1] - 1 >= 0:
    adjacent_nodes.append((node[0], node[1] - 1))
  adjacent_nodes = list(filter(
    lambda p: elevations[p[0]][p[1]] - elevations[node[0]][node[1]] <= 1,
    adjacent_nodes))
  return adjacent_nodes


def path(predecessors, end):
  if end not in predecessors:
    return []
  node = end
  path = [end]
  while node in predecessors:
    node = predecessors[node]
    path.insert(0, node)
  return path


def shortest_path(elevations, start, end):
  visited = {start}
  predecessors = dict()
  queue = [start]
  while len(queue) > 0:
    node = queue.pop(0)
    if node == end:
      break
    for adjacent_node in adjacent(node, elevations):
      if adjacent_node not in visited:
        visited.add(adjacent_node)
        predecessors[adjacent_node] = node
        queue.append(adjacent_node)
  return path(predecessors, end)


def main(file):
  elevations, start, end = read_elevations(file)
  print_map([start], elevations, start, end)
  starting_points = []
  for ri, row in enumerate(elevations):
    for ci, value in enumerate(row):
      if value == 0:
        starting_points.append((ri, ci))
  max_steps, best_path = None, None
  for start in starting_points:
    print(f"start: {start}, end: {end}")
    path = shortest_path(elevations, start, end)
    if not path:
      print("no path exists.")
      continue
    n_steps = len(path) - 1
    print(f"number of steps: {n_steps}")
    if not max_steps or n_steps < max_steps:
      best_path = path
      max_steps = n_steps
  print_map(best_path, elevations, start, end)
  print(f"BEST STARTING POINT IS {best_path[0]}: {max_steps} STEPS TO THE TOP.")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
