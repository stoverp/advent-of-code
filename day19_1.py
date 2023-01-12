import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, astuple
from enum import Enum
from pprint import PrettyPrinter


class Global:
  n_states_searched: int = 0
  ub_cache: dict = dict()
  ub_cache_hits: int = 0
  ub_cache_reads: int = 0
  lb_cache: dict = dict()
  lb_cache_hits: int = 0
  lb_cache_reads: int = 0

  @classmethod
  def read_ub_cache(cls, key):
    cls.ub_cache_reads += 1
    if key in cls.ub_cache:
      cls.ub_cache_hits += 1
      return cls.ub_cache[key]
    else:
      return None

  @classmethod
  def read_lb_cache(cls, key):
    cls.lb_cache_reads += 1
    if key in cls.lb_cache:
      cls.lb_cache_hits += 1
      return cls.lb_cache[key]
    else:
      return None


class Resource(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3

  def __str__(self):
    return self.name.lower()

  def __repr__(self):
    return str(self)


@dataclass
class MaterialSet:
  ore: int = 0
  clay: int = 0
  obsidian: int = 0
  geode: int = 0

  def __post_init__(self):
    self.data = (self.ore, self.clay, self.obsidian, self.geode)

  def __add__(self, other):
    return MaterialSet(*[a + b for a, b in zip(self.data, other.data)])

  def __sub__(self, other):
    return MaterialSet(*[a - b for a, b in zip(self.data, other.data)])

  def __mul__(self, other: int):
    return MaterialSet(*[a * other for a in self.data])

  def __le__(self, other):
    return all(a <= b for a, b in zip(self.data, other.data))

  def __getitem__(self, item):
    return getattr(self, str(item))

  def __hash__(self):
    return hash(self.data)

  def format_cost(self):
    return " and ".join(f"{amount} {attr}" for attr, amount in asdict(self).items() if amount > 0)

  def add_one_resource(self, resource):
    return self + MaterialSet(**{str(resource): 1})

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


def read_blueprints(file: str):
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


def print_blueprint(id: int, blueprint: dict):
  print(f"\n\n*** Blueprint {id} ***")
  for resource in Resource:
    print(f"  Each {resource.name.lower()} robot costs {blueprint[resource].format_cost()}.")


def upper_bound(state: State, blueprint: dict) -> int:
  materials, robots, minutes_remaining = state.materials, state.robots, state.minutes_remaining
  # cache_key = (materials.data, robots.data, minutes_remaining)
  # if cached_result := Global.read_ub_cache(cache_key):
  #   return cached_result
  for _ in range(state.minutes_remaining):
    materials += robots
    # can we buy a robot, starting with most valuable?
    for resource in reversed(Resource):
      if blueprint[resource] <= materials:
        # for upper bound, don't pay the cost
        robots = robots.add_one_resource(resource)
        break
  # Global.ub_cache[cache_key] = materials.geode
  return materials.geode


def lower_bound(state: State, blueprint: dict) -> int:
  materials, robots, minutes_remaining = state.materials, state.robots, state.minutes_remaining
  # cache_key = (materials.data, robots.data, minutes_remaining)
  # if cached_materials := Global.read_lb_cache(cache_key):
  #   return cached_materials
  geode_cost = blueprint[Resource.GEODE]
  for _ in range(state.minutes_remaining):
    if geode_cost <= materials:
      materials -= geode_cost
      materials += robots
      robots = robots.add_one_resource(Resource.GEODE)
    else:
      materials += robots
  # Global.lb_cache[cache_key] = materials.geode
  return materials.geode


def prune_strictly_worse(states):
  good_states = []
  for state in states:
    strictly_worse = False
    for other_state in states[:1000]:
      if state.minutes_remaining != other_state.minutes_remaining:
        continue
      if state.materials == other_state.materials and state.robots == other_state.robots:
        continue
      if state.materials <= other_state.materials and state.robots <= other_state.robots:
        strictly_worse = True
        break
    if not strictly_worse:
      good_states.append(state)
  return good_states


def consider(queue, state):
  for queued_state in reversed(queue):
    if queued_state.minutes_remaining != state.minutes_remaining:
      # only consider states at the back of the queue with equivalent minutes remaining
      break
    if state.materials <= queued_state.materials and state.robots <= queued_state.robots:
      return
  queue.append(state)


def find_max_geodes(blueprint: dict, minutes: int):
  Global.lb_cache = dict()
  Global.ub_cache = dict()
  max_ore_cost = max(cost.ore for cost in blueprint.values())
  best_result = 0
  best_final_state: State = None
  initial_state = State(MaterialSet(), MaterialSet(ore=1), None, minutes, None)
  queue = [initial_state]
  while queue:
    state = queue.pop(0)
    Global.n_states_searched += 1
    if (lb := lower_bound(state, blueprint)) > best_result:
      best_result = lb
      best_final_state = state
    if state.minutes_remaining == 0:
      continue
    elif upper_bound(state, blueprint) <= best_result:
      continue
    else:
      minutes_remaining = state.minutes_remaining - 1
      # consider state with no robots built
      consider(queue, State(
        state.materials + state.robots,
        state.robots,
        None,
        minutes_remaining,
        state
      ))
      # consider states with each type of robot built (if affordable)
      for robot_type in Resource:
        if robot_type == Resource.ORE and state.materials.ore >= max_ore_cost:
          # we already have enough ore to build anything, no need to create an ore robot
          continue
        elif blueprint[robot_type] <= state.materials:
          consider(queue, State(
            state.materials + state.robots - blueprint[robot_type],
            state.robots.add_one_resource(robot_type),
            robot_type,
            minutes_remaining,
            state
          ))
      queue = prune_strictly_worse(queue)
  return best_result, best_final_state


def path(final_state: State) -> list[State]:
  path = []
  state = final_state
  while state:
    path.append(state)
    state = state.parent
  return list(reversed(path))


def trace(final_state, blueprint, minutes_remaining):
  state_path = path(final_state)
  materials = MaterialSet()
  robots = MaterialSet(ore=1)
  for minute in range(1, minutes_remaining + 1):
    print(f"\n== Minute {minute} ==")
    built_robot = None
    if minute < len(state_path):
      built_robot = state_path[minute].built_robot_type
    elif blueprint[Resource.GEODE] <= materials:
      built_robot = Resource.GEODE
    if built_robot:
      materials = materials - blueprint[built_robot]
      print(f"Spend {blueprint[built_robot].format_cost()} to start building a {built_robot}-collecting robot.")
    materials = materials + robots
    for resource, amount in asdict(robots).items():
      if amount == 0:
        continue
      print(f"{amount} {resource}-collecting robot{'s' if amount > 1 else ''} collect{'' if amount > 1 else 's'} {amount} {resource}; you now have {materials[resource]} {resource}.")
    if built_robot:
      robots = robots.add_one_resource(built_robot)
      print(f"The new {built_robot}-collecting robot is ready; you now have {robots[built_robot]} of them.")
    minute += 1
  print(f"\nSearched {Global.n_states_searched} states.")
  # print(f"UB cache reads: {Global.ub_cache_reads}. UB cache hits: {Global.ub_cache_hits}.")


def main(file: str, minutes: int):
  blueprints = read_blueprints(file)
  for id, blueprint in blueprints.items():
    # id = 2
    blueprint = blueprints[id]
    print_blueprint(id, blueprint)
    result, final_state = find_max_geodes(blueprint, minutes)
    trace(final_state, blueprint, minutes)
    print(f"\nresult: {result}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
