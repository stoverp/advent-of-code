import re
import time
from argparse import ArgumentParser
from enum import Enum

START_VALVE = "AA"
SAMPLE_RATE = 1000000


class Global:
  possibilities_calculated = 0


class Action(Enum):
  MOVE = 1
  OPEN = 2


class Valve(object):
  def __init__(self, name, flow_rate, connected_valves):
    self.name = name
    self.flow_rate = flow_rate
    self.connected_valves = connected_valves

  def __repr__(self):
    return f"Valve(name={self.name}, flow_rate={self.flow_rate}, connected_valves={self.format_connected_valves()})"

  def __str__(self):
    return self.__repr__()

  def __dict__(self):
    return {
      "name": self.name,
      "flow_rate": self.flow_rate,
      "connected_valves": self.connected_valves,
    }

  def format_connected_valves(self):
    return "{\n  " + "\n  ".join(f"{name}: {format_path(path)}" for name, path in self.connected_valves.items()) + "\n}"


def read_valves(file):
  valves = dict()
  with open(file, "r") as f:
    for line in f:
      # print(line.strip())
      if match := re.match(r"Valve (?P<name>\w+) has flow rate=(?P<flow>\d+); tunnel(s?) lead(s?) to valve(s?) (?P<valves>.*)$", line):
        name = match.group("name")
        flow = int(match.group("flow"))
        connected_valve_list = re.split(r",\s*", match.group("valves"))
        connected_valves = dict([(valve, [(Action.MOVE, valve)]) for valve in connected_valve_list])
        # print(f"name: {name}, flow: {flow}, valves: {connected_valves}")
        valves[name] = Valve(name, flow, connected_valves)
      else:
        raise Exception(f"invalid input line: {line}")
  return valves


def find_best_path(valves, current_score, current_path, valves_opened, visited_since_opening, minutes_remaining):
  if minutes_remaining == 0:
    if Global.possibilities_calculated % SAMPLE_RATE == 0:
      print(f"possibility #{Global.possibilities_calculated}, score: {current_score}, path: {format_path(current_path)}")
    Global.possibilities_calculated += 1
    return current_score, current_path
  current_valve = valves[current_path[-1][1]]
  best_score, best_path = 0, []
  # check what best path would be if we opened the current valve
  if (current_valve.name not in valves_opened) and (current_valve.flow_rate > 0):
    best_score, best_path = find_best_path(
      valves,
      current_score + (current_valve.flow_rate * (minutes_remaining - 1)),
      current_path + [(Action.OPEN, current_valve.name)],
      valves_opened.union([current_valve.name]),
      frozenset(),
      minutes_remaining - 1)
  for connected_valve_name, path_to_connected_valve in current_valve.connected_valves.items():
    if connected_valve_name in visited_since_opening:
      # don't visit a valve we've already visited if we haven't opened a valve in between
      # this is a zero-value cycle that we can skip
      continue
    if minutes_remaining < len(path_to_connected_valve):
      # don't have time to visit this node
      continue
    # see if score improves if we instead move to valve_name
    score, path = find_best_path(
      valves,
      current_score,
      current_path + path_to_connected_valve,
      valves_opened,
      visited_since_opening.union([connected_valve_name]),
      minutes_remaining - len(path_to_connected_valve))
    if score > best_score:
      best_score, best_path = score, path
  return best_score, best_path


def format_path(path):
  return "[" + ", ".join([("O" if action == Action.OPEN else "") + valve for action, valve in path]) + "]"


def find_shortest_path_through_blocked_valves(valves, source_name, dest_name):
  visited = {source_name}
  predecessors = dict()
  queue = [source_name]
  while len(queue) > 0:
    valve_name = queue.pop(0)
    if valve_name == dest_name:
      break
    for connected_valve in valves[valve_name].connected_valves.keys():
      if connected_valve != dest_name and valves[connected_valve].flow_rate > 0:
        continue
      if connected_valve not in visited:
        visited.add(connected_valve)
        predecessors[connected_valve] = valve_name
        queue.append(connected_valve)
  return path(predecessors, dest_name)[1:]


def path(predecessors, dest):
  node = dest
  path = [dest]
  while node in predecessors:
    node = predecessors[node]
    path.insert(0, node)
  return path

def simplify_valves(valves):
  simple_valves = dict()
  unblocked_valves = dict()
  for valve in valves.values():
    if valve.flow_rate > 0:
      unblocked_valves[valve.name] = valve
  for current_valve in [START_VALVE] + list(unblocked_valves.keys()):
    connected_valves = dict()
    for dest in unblocked_valves.keys():
      if current_valve == dest:
        continue
      path = find_shortest_path_through_blocked_valves(valves, current_valve, dest)
      if path:
        connected_valves[dest] = [(Action.MOVE, valve) for valve in path]
    simple_valves[current_valve] = Valve(current_valve, valves[current_valve].flow_rate, connected_valves)
  return simple_valves


def main(file):
  valves = read_valves(file)
  # print(valves)
  valves = simplify_valves(valves)
  print("Simplified valves:")
  for key in sorted(valves.keys()):
    print(valves[key])
  score, path = find_best_path(valves, 0, [(Action.MOVE, "AA")], frozenset(), frozenset(), 25)
  print(f"\nFINAL SCORE: {score}, BEST PATH: {format_path(path)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
