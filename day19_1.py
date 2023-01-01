import re
import time
from argparse import ArgumentParser
from collections import defaultdict

RESOURCE_TYPES = ["ore", "clay", "obsidian", "geode"]

class Global(object):
  total_branches = 0
  cache = dict()

  @staticmethod
  def reset():
    Global.total_branches = 0
    Global.cache = dict()


class Robot(object):
  def __init__(self, type, cost):
    self.type = type
    self.cost = cost

  def __repr__(self):
    return f"Robot(type={self.type}, cost={self.format_cost()}"

  def format_cost(self):
    return " and ".join(f"{amount} {resource}" for resource, amount in sorted(self.cost.items()))


def buildable_robot_types(blueprint, collection):
  # can choose to not build a robot
  result = [None]
  for resource in RESOURCE_TYPES:
    can_build = True
    for cost_resource, cost_value in blueprint[resource].cost.items():
      if collection[cost_resource] < cost_value:
        can_build = False
    if can_build:
      result.append(resource)
  return result


# def build_robot(resource, blueprint, collection):
#   for cost_resource, cost_value in blueprint[resource].cost.items():
#     collection[cost_resource] -= cost_value
  # if resource == "geode":
  #   print(f"Spend {blueprint['geode'].format_cost()} to start building a geode-cracking robot.")
  # else:
  #   print(f"Spend {blueprint[resource].format_cost()} to start building a {resource}-collecting robot.")


# def collect(robots, collection):
#   for resource, n_robots in robots.items():
#     collection[resource] += n_robots
    # if resource == "geode":
    #   print(f"{n_robots} geode-cracking robot{'s' if n_robots > 1 else ''} crack{'s' if n_robots == 1 else ''} geodes; you now have {collection['geode']} open geodes.")
    # else:
    #   print(f"{n_robots} {resource}-collecting robot{'s' if n_robots > 1 else ''} collect{'s' if n_robots == 1 else ''} {resource}; you now have {collection[resource]} {resource}.")


def update_cache(robots, collection, minutes_remaining, choices, collected):
  # delta_collected = dict()
  # for resource in RESOURCE_TYPES:
  #   delta_collected[resource] = collected.get(resource, 0) - collection.get(resource, 0)
  Global.cache[(frozenset(robots.items()), frozenset(collection.items()), minutes_remaining)] = (choices, collected)


def read_cache(robots, collection, minutes_remaining):
  key = (frozenset(robots.items()), frozenset(collection.items()), minutes_remaining)
  if key in Global.cache:
    return Global.cache[key]
  return None


def merge(collected1, collected2):
  total = dict()
  for resource in collected1.keys():
    total[resource] = collected1.get(resource, 0) + collected2.get(resource, 0)
  return total


def greater_than(collected1, collected2):
  for resource in reversed(RESOURCE_TYPES):
    if collected1.get(resource, 0) > collected2.get(resource, 0):
      return True
    elif collected1.get(resource, 0) < collected2.get(resource, 0):
      return False
  return False


def run(blueprint, robots, collection, total_minutes, minutes_remaining):
  # print(f"\n== Minute {total_minutes + 1 - minutes_remaining} ==")
  if minutes_remaining == 0:
    Global.total_branches += 1
    if Global.total_branches % 1000000 == 0:
      print(f"branches so far: {Global.total_branches}")
    return [], collection
  cache_result = read_cache(robots, collection, minutes_remaining)
  if cache_result:
    cached_choices, collected = cache_result
    return cached_choices, collected
  buildable_types = buildable_robot_types(blueprint, collection)
  best_choices = []
  best_collected = dict()
  # collected_now = dict()
  for resource, amount in robots.items():
    collection[resource] += amount
  for build_resource_type in buildable_types:
    if build_resource_type:
      robots[build_resource_type] += 1
      for cost_resource, cost_value in blueprint[build_resource_type].cost.items():
        collection[cost_resource] -= cost_value
    # print(f"The new {build_resource_type}-collecting robot is ready; you now have {robots[build_resource_type]} of them.")
    choices, collected = run(blueprint, robots, collection.copy(), total_minutes, minutes_remaining - 1)
    if greater_than(collected, best_collected):
      best_choices = [build_resource_type] + choices
      best_collected = collected
    # restore previous state for next run
    if build_resource_type:
      robots[build_resource_type] -= 1
      for cost_resource, cost_value in blueprint[build_resource_type].cost.items():
        collection[cost_resource] += cost_value
    # for resource, amount in robots.items():
    #   collection[resource] -= amount
  update_cache(robots, collection, minutes_remaining, best_choices, best_collected)
  return best_choices, best_collected


def main(file, minutes):
  # choices = dict()
  # geodes = dict()
  # n_branches = dict()
  with open(file, "r") as f:
    blueprint = dict()
    for line in f:
      if match := re.match(f"Blueprint (\d+):", line):
        blueprint_id = int(match.group(1))
        print(f"\n\n*** Blueprint {blueprint_id} ***")
      else:
        raise Exception(f"invalid input line: {line}")
      if matches := re.findall(r"(Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?.)", line):
        for match in matches:
          print(match[0])
          type = match[1]
          cost = {match[3]: int(match[2])}
          if len(match[4]) > 0:
            cost[match[6]] = int(match[5])
          blueprint[type] = Robot(type, cost)
      else:
        raise Exception(f"invalid input line: {line}")
      Global.reset()
      # robots = {"ore": 1}
      # collection = dict()
      robots = defaultdict(int)
      robots["ore"] = 1
      collection = defaultdict(int)
      collected = dict()
      choices, collected = run(blueprint, robots, collection, minutes, minutes)
      n_branches = Global.total_branches
      print(f"\nBlueprint {blueprint_id}")
      print(f"collection: {collected}")
      print(f"choices: {choices}")
      print(f"total branches: {n_branches}")
  # print("\nTotal geodes cracked by each blueprint:")
  # print(geodes_cracked)
  # for blueprint_id in choices.keys():
  #   print(f"\nBlueprint {blueprint_id}")
  #   print(f"collection: {collection[blueprint_id]}")
  #   print(f"choices: {choices[blueprint_id]}")
  #   print(f"total branches: {n_branches[blueprint_id]}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
