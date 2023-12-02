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


def main(file):
  trees = read_trees(file)
  visible = initialize_visibility(len(trees), len(trees[0]))
  pprint(trees, "trees:")
  check_visibility(trees, visible, "l")
  pprint(visible, "visible left-right:")
  check_visibility(trees, visible, "r")
  pprint(visible, "also visible right-left:")
  check_visibility(trees, visible, "t")
  pprint(visible, "also visible top-bottom:")
  check_visibility(trees, visible, "b")
  pprint(visible, "also visible bottom-top:")
  total_visible_trees = 0
  for row in visible:
    for tree_visible in row:
      if tree_visible:
        total_visible_trees += 1
  print(f"\ntotal number visible: {total_visible_trees}")


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
