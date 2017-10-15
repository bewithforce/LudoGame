"""Note that these files are not essential and are just quickly put together
to test, run and visualize the results of different strategies.
This is done mainly to spread the load to multiple cores."""

import numpy as np
import matplotlib.pyplot as plt

results = []

with open("results.txt") as f:
    for no, line in enumerate(f):
        s = line.split(" ")
        ranks = [int(rank.strip(",[]\n")) for rank in s[1:]]
        p = 0
        for points, rank in enumerate(reversed(ranks)):
            p += rank * points
        if ranks:
            results.append((str(no+1)+". "+s[0], ranks, p))

objects = [result[0] for result in results]
y_pos = np.arange(len(objects))
performance = [result[1][0] for result in results]

plt.xticks(rotation=90)
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Wins')
plt.title('Number of wins from 1 945 000 games')
plt.tight_layout()

plt.show()
plt.clf()

objects = [result[0] for result in results]
y_pos = np.arange(len(objects))
performance = [result[2] for result in results]


plt.xticks(rotation=90)
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Points')
plt.title('Number of points from 1 945 000 games')
plt.tight_layout()
plt.show()
