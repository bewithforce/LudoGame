from strategies import *
import itertools
import multiprocessing
import subprocess
import pickle
import os
from collections import defaultdict

PLAYER_COUNT = 4


def chunks(l, n):
    avg = len(l) / float(n)
    out = []
    last = 0.0

    while last < len(l):
        out.append(l[int(last):int(last + avg)])
        last += avg

    return out


cores = multiprocessing.cpu_count()

mods = []
for i in range(len(modifiers)):
    mods += list(itertools.permutations(modifiers, i+1))

players = []
for base in bases:
    for mod in mods:
        player = base
        for f in mod:
            player = f(player)
        players.append(player)

players = bases+players

# players = [m(b) for m in modifiers for b in bases] + bases


times = []

results = []


games = []

for p in itertools.combinations(players, PLAYER_COUNT):
    games.append(([str(player()) for player in p]))

print(cores)

files = []


for no, chunk in enumerate(chunks(games, cores)):
    filename = "chunk_%d" % no
    with open(filename, "w") as f:
        for game in chunk:
            f.write(",".join(game))
            f.write("\n")
    files.append(filename)

processes = []

for file in files:
    processes.append(subprocess.Popen(["python3", "-u", "run_chunk.py", file, str(PLAYER_COUNT)]))

for file, process in zip(files, processes):
    process.wait()
    res = defaultdict(lambda: [0]*PLAYER_COUNT, pickle.load(open("results_" + file, "rb")))
    results.append(res)

os.system("rm results_* chunk_*")
result = defaultdict(lambda: [0]*PLAYER_COUNT)
for r in results:
    for k, v in r.items():
        result[k] = [k1 + k2 for k1, k2 in zip(result[k], r[k])]

l = sorted(result.items(), key=lambda x: x[1], reverse=True)
for i in l:
    print(i[0], i[1])
