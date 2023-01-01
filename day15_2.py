import re
import time
from argparse import ArgumentParser


def read_sensors_and_beacons(file):
  sensors_and_beacons = []
  with open(file, "r") as f:
    for line in f:
      if match := re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$", line):
        sensor, beacon = (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))
        sensors_and_beacons.append((sensor, beacon))
      else:
        raise Exception(f"invalid input line: {line}")
  return sensors_and_beacons


def produce_map(sensors, beacons, no_beacons, x_range, y_range):
  area_map = []
  possible_distress_beacons = []
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
      else:
        possible_distress_beacons.append((x, y))
      line.append(char)
    area_map.append(line)
  return area_map, possible_distress_beacons


def find_limits(item_positions):
  sorted_by_x = sorted(item_positions)
  sorted_by_y = sorted(item_positions, key=lambda p: p[1])
  return (
    range(sorted_by_x[0][0], sorted_by_x[-1][0] + 1),
    range(sorted_by_y[0][1], sorted_by_y[-1][1] + 1)
  )


def dist(position1, position2):
  return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def old_merge_ranges(all_ranges, new_range):
  if not all_ranges:
    return [new_range]
  overlap_start = 0
  while overlap_start < len(all_ranges) and all_ranges[overlap_start][1] < new_range[0]:
    # if new range doesn't overlap current range, keep going to find start of overlap
    overlap_start += 1
  overlap_end = overlap_start
  while overlap_end < len(all_ranges) and all_ranges[overlap_end][1] < new_range[1]:
    # if new range overlaps current range, keep going to find end of overlap
    overlap_end += 1
  if overlap_start < len(all_ranges) and all_ranges[overlap_start][0] <= new_range[1]:
    # if overlapping starts, merge
    merged_start = min(new_range[0], all_ranges[overlap_start][0])
    # overlap_start = max(0, overlap_start - 1)
  else:
    merged_start = new_range[0]
  if overlap_end < len(all_ranges) and all_ranges[overlap_end][0] <= new_range[1]:
    # if overlapping ends, merge
    merged_end = max(new_range[1], all_ranges[overlap_end][1])
    overlap_end += 1
  else:
    merged_end = new_range[1]
  merged_ranges = all_ranges[:overlap_start] + [(merged_start, merged_end)] + all_ranges[overlap_end:]
  # print(f"merge {new_range} into {all_ranges}: {merged_ranges}")
  return merged_ranges


def merge_ranges(all_ranges, new_range):
  assert(isinstance(all_ranges, list))
  assert(isinstance(new_range, tuple))
  if len(all_ranges) == 0:
    return [new_range]
  elif len(all_ranges) == 1:
    # merge two ranges
    r1, r2 = sorted([all_ranges[0], new_range])
    # for this use case, adjacent ranges can be merged, e.g. [(0, 2), (3, 5)]
    if r1[1] >= (r2[0] - 1):
      return [(r1[0], max(r1[1], r2[1]))]
    else:
      return [r1, r2]
  else:
    first = merge_ranges([all_ranges[0]], new_range)
    assert(len(first) <= 2)
    if len(first) == 1:
      return merge_ranges(all_ranges[1:], first[0])
    else:
      return [first[0]] + merge_ranges(all_ranges[1:], first[-1])


def search_row(y, sensors_and_beacons, min_ordinal, max_ordinal):
  all_ranges = []
  for sensor, beacon in sensors_and_beacons:
    # print(f"add sensor {sensor}, beacon {beacon} to coverage")
    distance = dist(sensor, beacon)
    remaining_range = distance - abs(sensor[1] - y)
    if remaining_range > 0:
      full_x_range = (sensor[0] - remaining_range, sensor[0] + remaining_range)
      x_range = (max(min_ordinal, full_x_range[0]), min(max_ordinal, full_x_range[1]))
      all_ranges = merge_ranges(all_ranges, x_range)
    else:
      # print("\tsensor + beacon too far away to consider")
      pass
  possible = []
  for x in range(min_ordinal, all_ranges[0][0]):
    possible.append(x)
  for x in range(all_ranges[-1][1], max_ordinal):
    possible.append(x)
  if len(all_ranges) > 1:
    pr = all_ranges[0]
    for r in all_ranges[1:]:
      for x in range(pr[1] + 1, r[0]):
        possible.append(x)
      pr = r
  return possible


def main(file, min_ordinal, max_ordinal):
  sensors_and_beacons = read_sensors_and_beacons(file)
  for y in range(min_ordinal, max_ordinal + 1):
    if y % 100000 == 0:
      print(f"\nsearching row: {y} ...")
    possible_distress_xs = search_row(y, sensors_and_beacons, min_ordinal, max_ordinal)
    if len(possible_distress_xs) == 1:
      print(f"\nfound distress beacon at {(possible_distress_xs[0], y)}! frequency: {(possible_distress_xs[0] * 4000000) + y}")
      return
    elif len(possible_distress_xs) == 2:
      print(f"\nMORE THAN ONE POSSIBLE DISTRESS BEACON: {[(x, y) for x in possible_distress_xs]}")
      return


def test_merge_ranges(all_ranges, new_range, expected):
  result = merge_ranges(all_ranges, new_range)
  print(f"merge {all_ranges} with {new_range}: {result}")
  assert result == expected, f"result: {result} != expected: {expected}"


def test_suite():
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (1, 3), [(0, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (1, 2), [(0, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (-1, 2), [(-1, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (2, 2), [(0, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (1, 7), [(0, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (-1, 5), [(-1, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (1, 11), [(0, 11)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (-1, 11), [(-1, 11)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (2, 11), [(0, 11)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (-15, -1), [(-15, 1), (3, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (-15, -2), [(-15, -2), (0, 1), (3, 5), (7, 10)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (11, 17), [(0, 1), (3, 5), (7, 17)])
  test_merge_ranges([(0, 1), (3, 5), (7, 10)], (12, 17), [(0, 1), (3, 5), (7, 10), (12, 17)])


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("min", type=int)
  parser.add_argument("max", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.min, args.max)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
  # test_suite()