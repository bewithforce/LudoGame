"""Note that these files are not essential and are just quickly put together
to test, run and visualize the results of different strategies.
This is done mainly to spread the load to multiple cores."""

from clobrdo import Clobrdo
from collections import defaultdict
from strategies import *
import pickle
import sys

Aggressive = make_aggressive
Cautious = make_cautious
Finishing = make_finishing

file = sys.argv[1]
n_players = int(sys.argv[2])

results = defaultdict(lambda: [0]*n_players)


with open(sys.argv[1]) as f:
    games = f.readlines()

l = len(games)

for no, game in enumerate(games):
    players = []
    for player in game.split(","):
        player = player.split("(")
        mods, base, name = player[:-2], player[-2].strip(")"), player[-1].strip(")\n")
        for mod in mods:
            base = mod+"("+base
        base += ")"*len(mods)
        if name in ["Aggressive", "Cautious", "Finishing", "Even", "OneByOne",
                    "Random"]:
            # How many points will I loose for this quick and dirty eval?
            players.append(eval(base+"(%s)" % name))
    rank = Clobrdo(players).play()
    for pos, player in enumerate(rank):
        results[str(player)][pos] += 1

    if not no % 100:
        print(file, no, "/", l)

with open("results_%s" % file, "wb") as f:
    pickle.dump(dict(results), f)

print(file, "Done")
