import re
import time
from argparse import ArgumentParser


N_COPIES = 1


def read_input(file):
  lines = []
  with open(file, "r") as f:
    for line in f:
      if line.startswith("//"):
        continue
      springs, counts_str = line.strip().split(" ")
      print(springs)
      counts = [int(c) for c in counts_str.split(",")]
      lines.append(("?".join([springs] * N_COPIES), counts * N_COPIES))
  return lines


def num_arrangements(springs, counts, current_count):
  if len(springs) == 0:
    return 1 if len(counts) == 0 or counts == [current_count] else 0
  elif len(counts) == 0:
    if "#" in springs:
      return 0
    else:
      return 1
  match springs[0]:
    case ".":
      if current_count == 0:
        return num_arrangements(springs[1:], counts, 0)
      else:
        if current_count != counts[0]:
          return 0
        return num_arrangements(springs[1:], counts[1:], 0)
    case "#":
      return num_arrangements(springs[1:], counts, current_count + 1)
    case "?":
      return sum(num_arrangements(spring + springs[1:], counts, current_count)
        for spring in [".", "#"])


def main(file):
  lines = read_input(file)
  total = 0
  for line_number, (springs, counts) in enumerate(lines):
    arrangements = num_arrangements(springs, counts, 0)
    print(f"line #{line_number + 1}: \n{springs} {counts}\n{arrangements}\n")
    total += arrangements
  return total


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  print("\nRESULT:", main(args.file))
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
