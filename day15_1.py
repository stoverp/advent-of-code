import re
from argparse import ArgumentParser


def read_sensors_and_beacons(file):
  sensors_and_beacons = []
  with open(file, "r") as f:
    for line in f:
      # print(line.strip())
      if match := re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$", line):
        sensor, beacon = (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))
        # print(f"sensor: {sensor}, beacon: {beacon}")
        sensors_and_beacons.append((sensor, beacon))
      else:
        raise Exception(f"invalid input line: {line}")
  return sensors_and_beacons


def print_map(sensors, beacons, no_beacons, x_range, y_range):
  for y in y_range:
    line = []
    for x in x_range:
      char = "."
      if (x, y) in sensors:
        char = "S"
      elif (x, y) in beacons:
        char = "B"
      elif (x, y) in no_beacons:
        char = "#"
      line.append(char)
    print("".join(line))


def find_limits(item_positions):
  sorted_by_x = sorted(item_positions)
  sorted_by_y = sorted(item_positions, key=lambda p: p[1])
  return (
    range(sorted_by_x[0][0], sorted_by_x[-1][0] + 1),
    range(sorted_by_y[0][1], sorted_by_y[-1][1] + 1)
  )


def dist(position1, position2):
  return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def old_main(file, target_row):
  sensors_and_beacons = read_sensors_and_beacons(file)
  sensors, beacons = zip(*sensors_and_beacons)
  sensors = set(sensors)
  beacons = set(beacons)
  no_beacons = set()
  # sensors_and_beacons = [((8, 7), (2, 10))]  # DEBUG
  for sensor, beacon in sensors_and_beacons:
    distance = dist(sensor, beacon)
    print(f"for sensor: {sensor}, beacon: {beacon}, all points <= {distance} squares away:")
    for y in range(sensor[1] - distance, sensor[1] + distance + 1):
      remaining_range = distance - abs(sensor[1] - y)
      for x in range(sensor[0] - remaining_range, sensor[0] + remaining_range + 1):
        no_beacons.add((x, y))
  print(no_beacons)
  x_range, y_range = find_limits(sensors.union(beacons).union(no_beacons))
  print(f"x_range: {x_range}, y_range: {y_range}")
  print_map(sensors, beacons, no_beacons, x_range, y_range)
  total = 0
  for x, y in no_beacons:
    if (x, y) not in sensors and (x, y) not in beacons and y == target_row:
      total += 1
  print(f"\nin row {target_row}, number of positions that cannot contain a beacon: {total}")


def main(file, target_row):
  sensors_and_beacons = read_sensors_and_beacons(file)
  sensors, beacons = zip(*sensors_and_beacons)
  sensors = set(sensors)
  beacons = set(beacons)
  no_beacons = set()
  for sensor, beacon in sensors_and_beacons:
    distance = dist(sensor, beacon)
    remaining_range = distance - abs(sensor[1] - target_row)
    print(f"for sensor {sensor}, beacon {beacon} is {distance} squares away.")
    print(f"\tat target row {target_row}, remaining range from sensor is {remaining_range}")
    if remaining_range > 0:
      for x in range(sensor[0] - remaining_range, sensor[0] + remaining_range + 1):
        no_beacons.add(x)
  # print(no_beacons)
  total = 0
  for x in no_beacons:
    if (x, target_row) not in sensors and (x, target_row) not in beacons:
      total += 1
  print(f"\nin row {target_row}, number of positions that cannot contain a beacon: {total}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("target_row", type=int)
  args = parser.parse_args()
  main(args.file, args.target_row)
