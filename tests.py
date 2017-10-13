from strategies import *
import itertools
import functools
from collections import Counter
from threading import (Thread, Lock)

import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


# mods = []
# for i in range(len(modifiers)):
#     mods += list(itertools.permutations(modifiers, i+1))
#
# players = []
# for base in bases:
#     for mod in mods:
#         player = base
#         for f in mod:
#             player = f(player)
#         players.append(player)
#
# players = bases+players

players = [m(b) for m in modifiers for b in bases] + bases


times = []

points = Counter()
lock = Lock()

def worker(game):
    rank = game.play()
    for score, player in enumerate(reversed(rank)):
        with lock:
            points[str(player)] += score
    # print(points.most_common(3))

threads = []

for _ in range(100):
    games = []
    for p in itertools.combinations(players, 4):
        games.append(Clobrdo([player() for player in p]))

    for game in games:
        t = Thread(target=worker, args=(game,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(points)




# points = Counter()


# def threaded():
#     clobrdo = Clobrdo([OneByOne(), Random(), OneByOne(), Random()])
#     for i, p in enumerate(reversed(clobrdo.play())):
#         points[p.name] += i
#
# for _ in range(10000):
#     thread = Thread(target=threaded).start()
# print(points)

# no_moves = []
#
#
# for _ in range(100):
#     clobrdo = Clobrdo([Even(1), Even(2), Even(3), Even(4)])
#     print(clobrdo.play())
#     no_moves.append(clobrdo.n_moves)
#
# print(max(no_moves))
