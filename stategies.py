from clobrdo import *
from contextlib import suppress, contextmanager
from random import shuffle


@contextmanager
def try_move():
    with suppress(IllegalMove):
        yield
        return


class OneByOne(BasePlayer):
    """They will always prefer moving pieces further down the road entering new one only when no other choice is
    available."""

    def strategy(self):
        for piece in reversed(sorted(self.pieces())):
            with try_move():
                self.move(piece)
        with try_move():
            self.move(START)


class Random(BasePlayer):
    """They will randomly choose the piece to move with."""

    def strategy(self):
        pieces = [-1] + self.pieces()
        shuffle(pieces)
        for piece in pieces:
            with try_move():
                self.move(piece)

clobrdo = Clobrdo([OneByOne(1), Random(1), OneByOne(2), Random(2)])
print(clobrdo.play())
