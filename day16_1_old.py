import re
import time
from argparse import ArgumentParser
from enum import Enum


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
    return f"Valve(name={self.name}, flow_rate={self.flow_rate}, connected_valves={self.connected_valves})"


def read_valves(file):
  valves = dict()
  with open(file, "r") as f:
    for line in f:
      # print(line.strip())
      if match := re.match(r"Valve (?P<name>\w+) has flow rate=(?P<flow>\d+); tunnel(s?) lead(s?) to valve(s?) (?P<valves>.*)$", line):
        name = match.group("name")
        flow = int(match.group("flow"))
        connected_valves = re.split(r",\s*", match.group("valves"))
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
  for connected_valve in current_valve.connected_valves:
    if connected_valve in visited_since_opening:
      # don't visit a valve we've already visited if we haven't opened a valve in between
      # this is a zero-value cycle that we can skip
      continue
    # see if score improves if we instead move to valve_name
    action = (Action.MOVE, connected_valve)
    score, path = find_best_path(
      valves,
      current_score,
      current_path + [action],
      valves_opened,
      visited_since_opening.union([connected_valve]),
      minutes_remaining - 1)
    if score > best_score:
      best_score, best_path = score, path
  return best_score, best_path


def format_path(path):
  return "[" + ", ".join([("O" if action == Action.OPEN else "") + valve for action, valve in path]) + "]"


def main(file, minutes):
  valves = read_valves(file)
  print(valves)
  score, path = find_best_path(valves, 0, [(Action.MOVE, "AA")], frozenset(), frozenset(), minutes)
  print(f"\nFINAL SCORE: {score}, BEST PATH: {format_path(path)}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
