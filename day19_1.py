import re
import time
from argparse import ArgumentParser
from enum import Enum


class Resource(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3


class Global(object):
  total_branches = 0
  cache = dict()
  cache_hits = 0
  cache_misses = 0

  @staticmethod
  def reset():
    Global.total_branches = 0
    Global.cache = dict()
    Global.cache_hits = 0
    Global.cache_misses = 0


class Robot(object):
  def __init__(self, type, cost):
    self.type = type
    self.cost = cost

  def __repr__(self):
    return f"Robot(type={self.type}, cost={self.format_cost()}"

  def format_cost(self):
    return " and ".join(f"{amount} {Resource(index).name.lower()}" for index, amount in enumerate(self.cost) if amount > 0)


def buildable_robot_types(blueprint, collection):
  # can choose to not build a robot
  result = [None]
  for resource in Resource:
    can_build = True
    for cost_resource_index, cost_value in enumerate(blueprint[resource].cost):
      if collection[cost_resource_index] < cost_value:
        can_build = False
    if can_build:
      result.append(resource)
  return result


def update_cache(robots, collection, minutes_remaining, choices, collected):
  Global.cache[(robots, collection, minutes_remaining)] = (choices, collected)


def read_cache(robots, collection, minutes_remaining):
  key = (robots, collection, minutes_remaining)
  if key in Global.cache:
    return Global.cache[key]
  return None


def merge(collected1, collected2):
  total = dict()
  for resource in collected1.keys():
    total[resource] = collected1.get(resource, 0) + collected2.get(resource, 0)
  return total


def greater_than(collected1, collected2):
  for resource in reversed(Resource):
    if collected1[resource.value] > collected2[resource.value]:
      return True
    elif collected1[resource.value] < collected2[resource.value]:
      return False
  return False


def update_amounts(amounts, resource, value):
  return tuple(amount + (value if index == resource.value else 0) for index, amount in enumerate(amounts))


def add_amounts(amounts1, amounts2, factor=1):
  return tuple(a1 + (a2 * factor) for a1, a2 in zip(amounts1, amounts2))


def subtract_amounts(amounts1, amounts2):
  return add_amounts(amounts1, amounts2, factor=-1)


def run(blueprint, robots, collection, total_minutes, minutes_remaining):
  if minutes_remaining == 0:
    Global.total_branches += 1
    if Global.total_branches % 1000000 == 0:
      print(f"branches so far: {Global.total_branches}")
    return [], collection
  cache_result = read_cache(robots, collection, minutes_remaining)
  if cache_result:
    Global.cache_hits += 1
    return cache_result
  Global.cache_misses += 1
  buildable_types = buildable_robot_types(blueprint, collection)
  best_choices = []
  best_collected = init_resource_amounts()
  collection = add_amounts(collection, robots)
  for build_resource_type in buildable_types:
    if build_resource_type:
      robots = update_amounts(robots, build_resource_type, 1)
      collection = subtract_amounts(collection, blueprint[build_resource_type].cost)
    choices, collected = run(blueprint, robots, collection, total_minutes, minutes_remaining - 1)
    if greater_than(collected, best_collected):
      best_choices = [build_resource_type] + choices
      best_collected = collected
  update_cache(robots, collection, minutes_remaining, best_choices, best_collected)
  return best_choices, best_collected


def init_resource_amounts():
  return 0, 0, 0, 0


def print_choices(choices, blueprint, minutes_remaining):
  robots = [1, 0, 0, 0]
  collection = [0, 0, 0, 0]
  for build_robot_type, minute in zip(choices, range(minutes_remaining)):
    print(f"\n== Minute {minute + 1} ==")
    if build_robot_type:
      for resource_type, amount in enumerate(blueprint[build_robot_type].cost):
        collection[resource_type] -= amount
      if build_robot_type == Resource.GEODE:
        print(f"Spend {blueprint[Resource.GEODE].format_cost()} to start building a geode-cracking robot.")
      else:
        print(f"Spend {blueprint[build_robot_type].format_cost()} to start building a {build_robot_type.name.lower()}-collecting robot.")
    for resource_type, n_robots in enumerate(robots):
      if n_robots == 0:
        continue
      collection[resource_type] += n_robots
      resource = Resource(resource_type)
      if resource_type == Resource.GEODE:
        print(f"{n_robots} geode-cracking robot{'s' if n_robots > 1 else ''} crack{'s' if n_robots == 1 else ''} geodes; you now have {collection[Resource.GEODE.value]} open geodes.")
      else:
        print(f"{n_robots} {resource.name.lower()}-collecting robot{'s' if n_robots > 1 else ''} collect{'s' if n_robots == 1 else ''} {resource.name.lower()}; you now have {collection[resource_type]} {resource.name.lower()}.")
    if build_robot_type:
      robots[build_robot_type.value] += 1
      print(f"The new {build_robot_type.name.lower()}-collecting robot is ready; you now have {robots[build_robot_type.value]} of them.")


def main(file, minutes):
  with open(file, "r") as f:
    Global.reset()
    blueprint = dict()
    for line in f:
      if match := re.match(f"Blueprint (\d+):", line):
        blueprint_id = int(match.group(1))
      else:
        raise Exception(f"invalid input line: {line}")
      if matches := re.findall(r"(Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?.)", line):
        for match in matches:
          robot_type = Resource[match[1].upper()]
          cost = update_amounts(init_resource_amounts(), Resource[match[3].upper()], int(match[2]))
          if len(match[4]) > 0:
            cost = update_amounts(cost, Resource[match[6].upper()], int(match[5]))
          blueprint[robot_type] = Robot(robot_type, cost)
      else:
        raise Exception(f"invalid input line: {line}")
      print(f"\n\n*** Blueprint {blueprint_id} ***")
      for resource in Resource:
        print(f"  Each {resource.name.lower()} robot costs {blueprint[resource].format_cost()}.")
      robots = (1, 0, 0, 0)
      collection = init_resource_amounts()
      choices, collected = run(blueprint, robots, collection, minutes, minutes)
      print_choices(choices, blueprint, minutes)
      print(f"\nchoices: {choices}")
      print(f"final collection: {collected}")
      print(f"cache hits: {Global.cache_hits}")
      print(f"cache misses: {Global.cache_misses}")
      print(f"total branches examined: {Global.total_branches}")
      return


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
