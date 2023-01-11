import re
import time
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, astuple
from enum import Enum

class Global:
  n_states_searched: int = 0
  ub_cache: dict = dict()
  ub_cache_hits: int = 0
  ub_cache_reads: int = 0
  # lb_cache: dict = dict()
  # lb_cache_hits: int = 0
  # lb_cache_reads: int = 0

  @classmethod
  def read_ub_cache(cls, key):
    cls.ub_cache_reads += 1
    if key in cls.ub_cache:
      cls.ub_cache_hits += 1
      return cls.ub_cache[key]
    else:
      return None

  # @classmethod
  # def read_lb_cache(cls, key):
  #   cls.lb_cache_reads += 1
  #   if key in cls.lb_cache:
  #     cls.lb_cache_hits += 1
  #     return cls.lb_cache[key]
  #   else:
  #     return None


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

  def __mul__(self, other: int):
    return MaterialSet(*[a * other for a in astuple(self)])

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

  @classmethod
  def from_resource(cls, resource, amount):
    return cls.from_dict({resource: amount})


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


def upper_bound_materials(candidate: State, blueprint: dict) -> MaterialSet:
  materials, robots, minutes_remaining = candidate.materials, candidate.robots, candidate.minutes_remaining
  cache_key = (astuple(materials), astuple(robots), minutes_remaining)
  if cached_materials := Global.read_ub_cache(cache_key):
    return cached_materials
  for t in range(candidate.minutes_remaining):
    materials += robots
    # can we buy a robot, starting with most valuable?
    for resource in reversed(Resource):
      if blueprint[resource] <= materials:
        # for upper bound, don't pay the cost
        robots = robots + MaterialSet.from_resource(resource, 1)
        break
  Global.ub_cache[cache_key] = materials
  return materials


def lower_bound_materials(state: State) -> MaterialSet:
  # materials, robots, minutes_remaining = candidate.materials, candidate.robots, candidate.minutes_remaining
  # cache_key = (astuple(materials), astuple(robots), minutes_remaining)
  # if cached_materials := Global.read_lb_cache(cache_key):
  #   return cached_materials
  # materials += robots * minutes_remaining
  # Global.lb_cache[cache_key] = materials
  # return materials
  return state.materials + (state.robots * state.minutes_remaining)


def find_max_geodes(blueprint: dict, minutes: int) -> State:
  # best_final_materials = None
  best_final_state: State = None
  initial_state = State(MaterialSet(), MaterialSet(ore=1), None, minutes, None)
  queue = [initial_state]
  while queue:
    state = queue.pop(0)
    # lb_materials = lower_bound_materials(state)
    # if not best_final_materials or lb_materials.obsidian >= best_final_materials.obsidian:
    #   # the lower-bound of materials collected by the current state is better than what we've found so far
    #   best_final_materials = lb_materials
    #   # hopefully on the last step, this will contain the correct parent
    #   best_final_state = state
    if not best_final_state or best_final_state.materials.obsidian < state.materials.obsidian:
      best_final_state = state
    minutes_remaining = state.minutes_remaining - 1
    if minutes_remaining > 0:
      # consider state with no robots built
      candidates = [State(
        state.materials + state.robots,
        state.robots,
        None,
        minutes_remaining,
        state
      )]
      # consider states with each type of robot built (if affordable)
      for robot_type in Resource:
        if blueprint[robot_type] <= state.materials:
          candidates.append(State(
            state.materials + state.robots - blueprint[robot_type],
            state.robots + MaterialSet.from_resource(robot_type, 1),
            robot_type,
            minutes_remaining,
            state
          ))
      for candidate in candidates:
        ub_materials = upper_bound_materials(candidate, blueprint)
        if best_final_state and best_final_state.materials <= ub_materials:
          # the upper-bound of what this state can collect at least as good as what we've found already
          Global.n_states_searched += 1
          queue.append(candidate)
  return best_final_state


def path(final_state: State) -> list[State]:
  path = []
  state = final_state
  while state:
    path.append(state)
    state = state.parent
  return list(reversed(path))


def main(file: str, minutes: int):
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
      print(f"{amount} {resource}-collecting robot{'s' if amount > 1 else ''} collect{'' if amount > 1 else 's'} {amount} {resource}; you now have {materials[resource]} {resource}.")
    if state.built_robot_type:
      robots = robots + MaterialSet.from_resource(state.built_robot_type, 1)
      print(f"The new {state.built_robot_type}-collecting robot is ready; you now have {robots[state.built_robot_type]} of them.")
    minute += 1
  print(f"\nSearched {Global.n_states_searched} states.")
  print(f"UB cache reads: {Global.ub_cache_reads}. UB cache hits: {Global.ub_cache_hits}.")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
