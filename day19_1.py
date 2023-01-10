import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, astuple
from enum import Enum


class Resource(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3

  def __str__(self):
    return self.name.lower()

  def __repr__(self):
    return str(self)


@dataclass(frozen=True)
class MaterialSet:
  ore: int = 0
  clay: int = 0
  obsidian: int = 0
  geode: int = 0

  def __add__(self, other):
    return MaterialSet(*[a + b for a, b in zip(astuple(self), astuple(other))])

  def __sub__(self, other):
    return MaterialSet(*[a - b for a, b in zip(astuple(self), astuple(other))])

  def __le__(self, other):
    return all(a <= b for a, b in zip(astuple(self), astuple(other)))

  def __getitem__(self, item):
    return getattr(self, str(item))

  def format_cost(self):
    return " and ".join(f"{amount} {attr}" for attr, amount in asdict(self).items() if amount > 0)

  @classmethod
  def from_dict(cls, d):
    return MaterialSet(
      d.get(Resource.ORE, 0),
      d.get(Resource.CLAY, 0),
      d.get(Resource.OBSIDIAN, 0),
      d.get(Resource.GEODE, 0)
    )


@dataclass(frozen=True)
class State:
  materials: MaterialSet
  robots: MaterialSet
  built_robot_type: Resource
  minutes_remaining: int
  parent: 'State'


def read_blueprints(file):
  blueprints = dict()
  with open(file, "r") as f:
    for line in f:
      if match := re.match(f"Blueprint (\d+):", line):
        blueprint_id = int(match.group(1))
      else:
        raise Exception(f"invalid input line: {line}")
      if matches := re.findall(r"Each (\w+) robot costs (.*?)\.", line):
        blueprint = dict()
        for match in matches:
          robot_type = Resource[match[0].upper()]
          materials_dict = dict()
          for resource_cost in match[1].split(" and "):
            amount, type = resource_cost.split(" ")
            materials_dict[Resource[type.upper()]] = int(amount)
          materials = MaterialSet.from_dict(materials_dict)
          blueprint[robot_type] = materials
      else:
        raise Exception(f"invalid input line: {line}")
      blueprints[blueprint_id] = blueprint
  return blueprints


def print_blueprint(id, blueprint):
  print(f"\n\n*** Blueprint {id} ***")
  for resource in Resource:
    print(f"  Each {resource.name.lower()} robot costs {blueprint[resource].format_cost()}.")


def find_max_geodes(blueprint, minutes):
  best_state = None
  initial_state = State(MaterialSet(), MaterialSet(ore=1), None, minutes, None)
  queue = [initial_state]
  while queue:
    state = queue.pop(0)
    minutes_remaining = state.minutes_remaining - 1
    if minutes_remaining == 0:
      # if best_state and state.materials.geode > best_state.materials.geode:
      if not best_state or state.materials.obsidian > best_state.materials.obsidian:
        best_state = state
    else:
      # consider state with no robots built
      queue.append(State(
        state.materials + state.robots,
        state.robots,
        None,
        minutes_remaining,
        state
      ))
      # consider states with each type of robot built (if affordable)
      for robot_type in Resource:
        if blueprint[robot_type] <= state.materials:
          queue.append(State(
            state.materials + state.robots - blueprint[robot_type],
            state.robots + MaterialSet.from_dict({robot_type: 1}),
            robot_type,
            minutes_remaining,
            state
          ))
  return best_state


def path(final_state):
  path = []
  state = final_state
  while state:
    path.append(state)
    state = state.parent
  return list(reversed(path))


def main(file, minutes):
  blueprints = read_blueprints(file)
  # DEBUG: first blueprint only
  blueprint = blueprints[1]
  print_blueprint(1, blueprint)
  final_state = find_max_geodes(blueprint, minutes)
  state_path = path(final_state)
  minute = 1
  materials = MaterialSet()
  robots = MaterialSet(ore=1)
  for state in state_path:
    print(f"== Minute {minute} ==")
    if state.built_robot_type:
      materials = materials - blueprint[state.built_robot_type]
      print(f"Spend {blueprint[state.built_robot_type].format_cost()} to start building a {state.built_robot_type.name.lower()}-collecting robot.")
    materials = materials + robots
    for resource, amount in asdict(robots).items():
      if amount == 0:
        continue
      print(f"{amount} {resource}-collecting robot{'s' if amount > 1 else ''} collect{'' if amount > 1 else 's'} {amount} {resource}; you now have {materials[resource]} {resource}")
    if state.built_robot_type:
      robots = robots + MaterialSet.from_dict({state.built_robot_type: 1})
      print(f"The new {state.built_robot_type}-collecting robot is ready; you now have {robots[state.built_robot_type]} of them.")
    minute += 1


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
