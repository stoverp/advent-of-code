import time
from argparse import ArgumentParser

def read_encrypted(file):
  encrypted = []
  with open(file, "r") as f:
    position = 0
    for line in f:
      value = int(line.strip())
      encrypted.append((position, value))
      if value == 0:
        zero_position = position
      position += 1
  return encrypted, zero_position


def get_mod(l, i):
  return l[i % len(l)]


def main(file):
  encrypted, zero_position = read_encrypted(file)
  print(f"encrypted: {encrypted}")
  decrypted = encrypted.copy()
  for step, t in enumerate(encrypted):
    new_position = decrypted.index(t) + t[1]
    if new_position <= 0:
      new_position = (len(encrypted) - 1) + new_position
    else:
      new_position %= (len(encrypted) - 1)
    decrypted.remove(t)
    decrypted.insert(new_position, t)
    print(f"step {step}: shift {t[1]}, then decrypted is {[v for i, v in decrypted]}")
  decrypted_zero_position = decrypted.index((zero_position, 0))
  print(f"\ndecrypted_zero_position: {decrypted_zero_position}")
  # print(get_mod(decrypted, decrypted_zero_position + 1000))
  # print(get_mod(decrypted, decrypted_zero_position + 2000))
  # print(get_mod(decrypted, decrypted_zero_position + 3000))
  total = 0
  for p in [1000, 2000, 3000]:
    value = get_mod(decrypted, decrypted_zero_position + p)[1]
    print(f"value at {p}th position after 0: {value}")
    total += value
  print(f"\nfinal total: {total}")


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()
  start_time = time.time()
  main(args.file)
  print("--- COMPLETED IN %s SECONDS ---" % (time.time() - start_time))
