import re
import sys
import time
from argparse import ArgumentParser
from pprint import PrettyPrinter


class Global(object):
  max_depth = 0


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


def is_adjacent(cube1, cube2):
  return (abs(cube1.x - cube2.x) + abs(cube1.y - cube2.y) + abs(cube1.z - cube2.z)) == 1


def find_limits(cubes):
  by_x = sorted(cubes, key=lambda c: c.x)
  by_y = sorted(cubes, key=lambda c: c.y)
  by_z = sorted(cubes, key=lambda c: c.z)
  return range(0, by_x[-1].x + 1), range(0, by_y[-1].y + 1), range(0, by_z[-1].z + 1)


def compute_surface_area(cubes):
  pile = []
  surface_area = 0
  for cube in cubes:
    surface_area += 6
    for piled_cube in pile:
      if is_adjacent(piled_cube, cube):
        surface_area -= 2
    pile.append(cube)
  return surface_area


def in_bounds(cube, x_range, y_range, z_range):
  return (x_range[0] <= cube.x <= x_range[-1]) and \
         (y_range[0] <= cube.y <= y_range[-1]) and \
         (z_range[0] <= cube.z <= z_range[-1])


def fill_with_water_recursive(start_cube, grid, x_range, y_range, z_range, depth=0):
  if depth > Global.max_depth:
    Global.max_depth = depth
    print(f"new max depth: {Global.max_depth}")
  grid[start_cube.x][start_cube.y][start_cube.z] = True
  for coordinate in ['x', 'y', 'z']:
    for direction in [-1, 1]:
      if coordinate == 'x':
        next_cube = Cube(start_cube.x + direction, start_cube.y, start_cube.z)
      elif coordinate == 'y':
        next_cube = Cube(start_cube.x, start_cube.y + direction, start_cube.z)
      else:  # coordinate == 'z':
        next_cube = Cube(start_cube.x, start_cube.y, start_cube.z + direction)
      if in_bounds(next_cube, x_range, y_range, z_range) and not grid[next_cube.x][next_cube.y][next_cube.z]:
        fill_with_water_recursive(next_cube, grid, x_range, y_range, z_range, depth + 1)


def adjacent_cubes(cube, grid, x_range, y_range, z_range):
  cubes = []
  for coordinate in ['x', 'y', 'z']:
    for direction in [-1, 1]:
      if coordinate == 'x':
        next_cube = Cube(cube.x + direction, cube.y, cube.z)
      elif coordinate == 'y':
        next_cube = Cube(cube.x, cube.y + direction, cube.z)
      else:  # coordinate == 'z':
        next_cube = Cube(cube.x, cube.y, cube.z + direction)
      if in_bounds(next_cube, x_range, y_range, z_range) and not grid[next_cube.x][next_cube.y][next_cube.z]:
        cubes.append(next_cube)
  return cubes


def fill_with_water(start_cube, grid, x_range, y_range, z_range):
  queue = [start_cube]
  while queue:
    next_cube = queue.pop()
    grid[next_cube.x][next_cube.y][next_cube.z] = True
    next_cubes = adjacent_cubes(next_cube, grid, x_range, y_range, z_range)
    queue.extend(next_cubes)


def initialize_grid(x_range, y_range, z_range):
  grid = []
  for x in x_range:
    xs = []
    for y in y_range:
      ys = []
      for z in z_range:
        ys.append(False)
      xs.append(ys)
    grid.append(xs)
  return grid


def fill_grid(cubes, grid):
  for cube in cubes:
    grid[cube.x][cube.y][cube.z] = True


def find_air_pockets(grid, x_range, y_range, z_range):
  air_pockets = []
  for x in x_range:
    for y in y_range:
      for z in z_range:
        if not grid[x][y][z]:
          print(f"found air pocket at ({x}, {y}, {z})")
          air_pockets.append(Cube(x, y, z))
  return air_pockets


def main(file):
  cubes = read_cubes(file)
  # print(cubes)
  x_range, y_range, z_range = find_limits(cubes)
  print(f"x range: {x_range}, y range: {y_range}, z range: {z_range}\n")
  grid = initialize_grid(x_range, y_range, z_range)
  # print(len(grid), len(grid[0]), len(grid[0][0]))
  fill_grid(cubes, grid)
  # print("cubes in grid:")
  # PrettyPrinter().pprint(grid)
  fill_with_water(Cube(0, 0, 0), grid, x_range, y_range, z_range)
  # print("\nfilled with water:")
  # PrettyPrinter().pprint(grid)
  air_pockets = find_air_pockets(grid, x_range, y_range, z_range)
  print(f"\nnumber of air pockets: {len(air_pockets)}")
  surface_area = compute_surface_area(cubes)
  print(f"total surface area: {surface_area}")
  air_pocket_surface_area = compute_surface_area(air_pockets)
  print(f"total air pocket surface area: {air_pocket_surface_area}")
  exposed_area = surface_area - air_pocket_surface_area
  print(f"\nexposed surface area: {exposed_area}")


if __name__ == "__main__":
  # print(f"default recursion limit:
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
