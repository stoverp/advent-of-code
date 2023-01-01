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


def find_best_score(current_valve, valves, all_distances, minutes_remaining):
  best_score = 0
  for valve_name, distance in all_distances[current_valve].items():
    if distance == 0 or valves[valve_name].opened:
      continue
    if minutes_remaining > (distance + 1):
      valves[valve_name].open()
      time_left = minutes_remaining - (distance + 1)
      pressure_released = time_left * valves[valve_name].flow_rate
      score = pressure_released + find_best_score(valve_name, valves, all_distances, time_left)
      valves[valve_name].close()
      if score > best_score:
        best_score = score
  return best_score


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
  score = find_best_score(STARTING_VALVE, valves, all_distances, minutes_remaining)
  print(f"\nFINAL SCORE: {score}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("minutes", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.minutes)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
