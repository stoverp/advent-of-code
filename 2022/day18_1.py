import re
import time
from argparse import ArgumentParser

class Cube(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return f"Cube(x={self.x}, y={self.y}, z={self.z})"


def read_cubes(file):
  cubes = []
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"(\d+),(\d+),(\d+)$", line):
        cubes.append(Cube(int(match.group(1)), int(match.group(2)), int(match.group(3))))
      else:
        raise Exception(f"invalid input line: {line}")
  return cubes


def adjacent(cube1, cube2):
  return (abs(cube1.x - cube2.x) + abs(cube1.y - cube2.y) + abs(cube1.z - cube2.z)) == 1


def main(file):
  cubes = read_cubes(file)
  print(cubes)
  pile = []
  surface_area = 0
  for cube in cubes:
    surface_area += 6
    for piled_cube in pile:
      if adjacent(piled_cube, cube):
        surface_area -= 2
    pile.append(cube)
  print(f"\ntotal surface area: {surface_area}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
