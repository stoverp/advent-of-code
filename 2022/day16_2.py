import re
import time
from argparse import ArgumentParser
from queue import PriorityQueue


STARTING_VALVE = "AA"
INF = 1000


class Valve(object):
  def __init__(self, name, flow_rate, connected_valves):
    self.name = name
    self.flow_rate = flow_rate
    self.connected_valves = connected_valves
    self.opened = False

  def open(self):
    self.opened = True

  def close(self):
    self.opened = False

  def __repr__(self):
    return f"Valve(name={self.name}, flow_rate={self.flow_rate}, connected_valves={self.connected_valves}, opened={self.opened})"


def read_valves(file):
  valves = dict()
  with open(file, "r") as f:
    for line in f:
      if match := re.match(r"Valve (?P<name>\w+) has flow rate=(?P<flow>\d+); tunnel(s?) lead(s?) to valve(s?) (?P<valves>.*)$", line):
        name = match.group("name")
        flow = int(match.group("flow"))
        connected_valves = re.split(r",\s*", match.group("valves"))
        valves[name] = Valve(name, flow, connected_valves)
      else:
        raise Exception(f"invalid input line: {line}")
  return valves


def find_best_score(my_target, my_distance, elephant_target, elephant_distance, valves, all_distances, minutes_remaining, my_path, elephant_path, depth=0):
  if minutes_remaining == 0:
    return 0, my_path, elephant_path
  open_score = 0
  my_next_targets = []
  elephant_next_targets = []
  valves_to_open = []
  if my_distance == 0:
    # if I'm at a valve
    assert not valves[my_target].opened, f"my target {valves[my_target]} already open"
    my_open_score = 0
    if my_target != STARTING_VALVE:
      valves_to_open.append(my_target)
      my_open_score = minutes_remaining * valves[my_target].flow_rate
      open_score += my_open_score
    my_path = my_path + [(my_target, my_open_score)]
    # choose next targets
    for candidate in all_distances.keys():
      if candidate != STARTING_VALVE and candidate != my_target and candidate != elephant_target and not valves[candidate].opened:
        my_next_targets.append((candidate, all_distances[my_target][candidate]))
    if len(my_next_targets) == 0:
      # if you're out of targets, just sit still
      my_next_targets = [(None, INF)]
  else:
    # still headed to same target
    my_next_targets.append((my_target, my_distance - 1))
  if elephant_distance == 0:
    # if elephant at a valve
    assert not valves[elephant_target].opened, f"elephant target {valves[elephant_target]} already open"
    elephant_open_score = 0
    if elephant_target != STARTING_VALVE:
      valves_to_open.append(elephant_target)
      elephant_open_score = minutes_remaining * valves[elephant_target].flow_rate
      open_score += elephant_open_score
    elephant_path = elephant_path + [(elephant_target, elephant_open_score)]
    # choose next targets
    for candidate in all_distances.keys():
      if candidate != STARTING_VALVE and candidate != my_target and candidate != elephant_target and not valves[candidate].opened:
        elephant_next_targets.append((candidate, all_distances[elephant_target][candidate]))
    if len(elephant_next_targets) == 0:
      # if you're out of targets, just sit still
      elephant_next_targets = [(None, INF)]
  else:
    # still headed to same target
    elephant_next_targets.append((elephant_target, elephant_distance - 1))
  best_sub_score = 0
  my_best_path, elephant_best_path = my_path, elephant_path
  for my_next_target, my_next_distance in my_next_targets:
    for elephant_next_target, elephant_next_distance in elephant_next_targets:
      if my_next_target == elephant_next_target:
        continue
      for valve_name in valves_to_open:
        valves[valve_name].open()
      sub_score, my_sub_path, elephant_sub_path = find_best_score(
        my_next_target,
        my_next_distance,
        elephant_next_target,
        elephant_next_distance,
        valves,
        all_distances,
        minutes_remaining - 1,
        my_path,
        elephant_path,
        depth + 1)
      for valve_name in valves_to_open:
        valves[valve_name].close()
      if sub_score > best_sub_score:
        best_sub_score = sub_score
        my_best_path = my_sub_path
        elephant_best_path = elephant_sub_path
  return open_score + best_sub_score, my_best_path, elephant_best_path


def find_shortest_distance(valves, source):
  distances = {source: 0}
  pq = PriorityQueue()
  for valve in valves.values():
    if valve.name != source:
      distances[valve.name] = INF
    pq.put((distances[valve.name], valve.name))
  while not pq.empty():
    d, current_valve = pq.get()
    if current_valve in distances and distances[current_valve] < d:
      # valves can be added more than once, so skip if we already have a shorter distance to the current valve
      continue
    for connected_valve in valves[current_valve].connected_valves:
      alt_distance = distances[current_valve] + 1
      if alt_distance < distances[connected_valve]:
        distances[connected_valve] = alt_distance
        pq.put((alt_distance, connected_valve))
  return dict([(valve_name, distance) for valve_name, distance in distances.items() if valves[valve_name].flow_rate > 0])


def main(file, minutes_remaining):
  valves = read_valves(file)
  print(valves)
  all_distances = {}
  for valve_name in valves.keys():
    if valve_name == STARTING_VALVE or valves[valve_name].flow_rate > 0:
      all_distances[valve_name] = find_shortest_distance(valves, valve_name)
      print(f"{valve_name}: {all_distances[valve_name]}")
  score, my_path, elephant_path = find_best_score(STARTING_VALVE, 0, STARTING_VALVE, 0, valves, all_distances, minutes_remaining, [], [])
  print(f"\nFINAL SCORE: {score}")
  print(f"my_path: {my_path}")
  print(f"elephant_path: {elephant_path}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
