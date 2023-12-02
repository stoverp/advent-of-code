import time
from argparse import ArgumentParser

def read_encrypted(file, key):
  encrypted = []
  with open(file, "r") as f:
    position = 0
    for line in f:
      value = int(line.strip()) * key
      encrypted.append((position, value))
      if value == 0:
        zero_position = position
      position += 1
  return encrypted, zero_position


def get_mod(l, i):
  return l[i % len(l)]


def mix(decrypted, encrypted):
  for step, t in enumerate(encrypted):
    old_position = decrypted.index(t)
    new_position = old_position + t[1]
    new_position %= (len(encrypted) - 1)
    decrypted.remove(t)
    decrypted.insert(new_position, t)
    # print(f"step {step}: shift {t[1]}, then decrypted is {[v for i, v in decrypted]}")


def main(file, key):
  encrypted, zero_position = read_encrypted(file, key)
  print("Initial arrangement:")
  print([v for i, v in encrypted])
  decrypted = encrypted.copy()
  for round in range(10):
    mix(decrypted, encrypted)
    print(f"\nAfter {round + 1} rounds of mixing:")
    print([v for i, v in decrypted])
  decrypted_zero_position = decrypted.index((zero_position, 0))
  print(f"\ndecrypted_zero_position: {decrypted_zero_position}")
  total = 0
  for p in [1000, 2000, 3000]:
    value = get_mod(decrypted, decrypted_zero_position + p)[1]
    print(f"value at {p}th position after 0: {value}")
    total += value
  print(f"\nfinal total: {total}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  parser.add_argument("key", type=int)
  args = parser.parse_args()
  start_time = time.time()
  main(args.file, args.key)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
