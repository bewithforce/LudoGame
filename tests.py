from strategies import *
import itertools
from collections import Counter
import time


def save(obj):
    return obj.__class__, obj.__dict__


def load(cls, attributes):
    obj = cls.__new__(cls)
    obj.__dict__.update(attributes)
    return obj


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


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

points = Counter()


games = []

for p in itertools.combinations(players, 4):
    games.append(Clobrdo([player() for player in p]))

l = len(games)
aver = 0
print(l)

for i, game in enumerate(games):
    with Timer() as t:
        rank = game.play()
        for score, player in enumerate(reversed(rank)):
            points[str(player)] += score
    a = t.interval
    aver = (aver*(i+1) + a)/(i+2)
    if not i % 100:
        print(a)
        print(aver)
        print(i, (l - i)*aver/60)
        print(points.most_common(4))
        print()


print(points)



# points = Counter()

# def threaded():
#     clobrdo = Clobrdo([OneByOne(), Random(), OneByOne(), Random()])
#     for i, p in enumerate(reversed(clobrdo.play())):
#         points[p.name] += i
#
# q = Queue()
# threads = []
# number_of_threads = 10
# for i in range(number_of_threads):
#     t = Thread(target=worker)
#     t.start()
#     threads.append(t)
#
#
#     if i == 100:
#         break
#
# # block until all tasks are done
# q.join()
#
# # stop workers
# for i in range(number_of_threads):
#     q.put(None)
# for t in threads:
#     t.join()
# times.append(timer.interval)
# print(timer.interval)
#
# print(sum(times)/len(times))
