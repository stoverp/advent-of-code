from argparse import ArgumentParser
from pprint import PrettyPrinter


pp = PrettyPrinter()


def pprint(object, message=""):
  print("\n" + message)
  pp.pprint(object)


def check_visibility(trees, visible, direction):
  if direction == "l" or direction == "r":
    n_slices = len(trees)
    n_trees_per_slice = len(trees[0])
  else:
    n_slices = len(trees[0])
    n_trees_per_slice = len(trees)
  for slice_index in range(n_slices):
    max_height = -1
    for tree_index in range(n_trees_per_slice):
      if direction == "l":
        row_index = slice_index
        column_index = tree_index
      elif direction == "r":
        row_index = slice_index
        column_index = n_trees_per_slice - tree_index - 1
      elif direction == "t":
        row_index = tree_index
        column_index = slice_index
      elif direction == "b":
        row_index = n_trees_per_slice - tree_index - 1
        column_index = slice_index
      else:
        raise Exception(f"invalid direction: {direction}")
      tree_height = trees[row_index][column_index]
      if tree_height > max_height:
        visible[row_index][column_index] = True
        max_height = tree_height


def initialize_visibility(n_rows, n_columns):
  visible = []
  for _ in range(n_rows):
    row = []
    for _ in range(n_columns):
      row.append(False)
    visible.append(row)
  return visible


def direction_score(trees, target_height, row_indices, column_indices):
  score = 0
  max_height = target_height
  for row_index in row_indices:
    for column_index in column_indices:
      if trees[row_index][column_index] < max_height:
        score += 1
      else:
        # there's a tree blocking our view, can't see anything beyond
        return score + 1
  return score


def scenic_score(trees, target_row, target_column):
  score = 1
  target_height = trees[target_row][target_column]
  for direction in ["u", "l", "d", "r"]:
    if direction == "l":
      row_indices = [target_row]
      column_indices = range(target_column - 1, -1, -1)
    elif direction == "r":
      row_indices = [target_row]
      column_indices = range(target_column + 1, len(trees[0]))
    elif direction == "u":
      row_indices = range(target_row - 1, -1, -1)
      column_indices = [target_column]
    else:  # direction == "d"
      row_indices = range(target_row + 1, len(trees))
      column_indices = [target_column]
    dir_score = direction_score(trees, target_height, row_indices, column_indices)
    print(f"{direction} score for tree at row {target_row}, column {target_column}: {dir_score}")
    score *= dir_score
  print(f"scenic score of row {target_row}, column {target_column}: {score}")
  return score


def main(file):
  trees = read_trees(file)
  pprint(trees, "trees:")
  # print()
  # score = scenic_score(trees, 1, 2)
  # print()
  # score = scenic_score(trees, 3, 2)
  max_r, max_c, max_score = None, None, 0
  for r in range(len(trees)):
    for c in range(len(trees[0])):
      print()
      score = scenic_score(trees, r, c)
      if score > max_score:
        max_r, max_c, max_score = r, c, score
  print(f"\nbest scenic score is at row {max_r}, column {max_c}: {max_score}")
  print()
  score = scenic_score(trees, 23, 51)


def read_trees(file):
  trees = []
  with open(file, "r") as f:
    for line in f:
      row = []
      for c in line.strip():
        row.append(int(c))
      trees.append(row)
  return trees


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  main(args.file)
