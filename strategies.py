"""This module implements different strategies and modifiers of them."""
from random import shuffle

from baseplayer import BasePlayer
from clobrdo import START


class OneByOne(BasePlayer):
    """Will always prefer moving pieces further down the road entering new one
    only when no other choice is available."""

    def __init__(self, name=""):
        super(OneByOne, self).__init__(name=name)
        self.name = "OneByOne(%s)" % self.name

    def strategy(self):
        for piece in reversed(sorted(self.pieces())):
            if self.move(piece):
                return
        if self.move(START):
            return


class Random(BasePlayer):
    """Will randomly choose the piece to move with."""

    def __init__(self, name=""):
        super(Random, self).__init__(name=name)
        self.name = "Random(%s)" % self.name

    def strategy(self):
        pieces = [START] + self.pieces()
        shuffle(pieces)
        for piece in pieces:
            if self.move(piece):
                return


class Even(BasePlayer):
    """Will try to distribute the moves between pieces evenly, will enter
    new piece every time the chance is given"""

    def __init__(self, name=""):
        super(Even, self).__init__(name=name)
        self.name = "Even(%s)" % self.name

    def strategy(self):
        if self.move(START):
            return
        for piece in sorted(self.pieces()):
            if self.move(piece):
                return


def make_aggressive(base):
    """Applies agressive modifier to a class"""
    class Aggressive(base):
        """Will throw out enemy's piece when given chance, otherwise acts like
        player given as `base`"""

        def __init__(self, name=""):
            super(Aggressive, self).__init__(name=name)
            self.name = "Aggressive(%s)" % self.name

        def strategy(self):
            possible_trowouts = []
            for piece in self.pieces():
                target = piece + self.die
                player = self.check(piece + self.die)
                if player not in [self, None]:
                    # Get position of enemy's piece relative to its start
                    targets_progress = player.shift_field(
                        self.unshift_field(target))
                    possible_trowouts.append((piece, targets_progress))
            for throwout in sorted(possible_trowouts, key=lambda x: x[1],
                                   reverse=True):
                if self.move(throwout[0]):
                    return
            super(Aggressive, self).strategy()

    return Aggressive


def make_cautious(base):
    """Applies cautious modifier to a class"""
    class Cautious(base):
        """Will move the piece if it takes it out of danger of throwing out"""
        def __init__(self, name=""):
            super(Cautious, self).__init__(name=name)
            self.name = "Cautious(%s)" % self.name

        def strategy(self):
            for piece in sorted(self.pieces(), reverse=True):
                if (self.is_in_danger(piece)
                        and self.is_in_danger(piece + self.die)):
                    if self.move(piece):
                        return
            super(Cautious, self).strategy()
    return Cautious


def make_finishing(base):
    """Applies finishing modifier to a class"""
    class Finishing(base):
        """Will move to finish when given the chance"""
        def __init__(self, name=""):
            super(Finishing, self).__init__(name=name)
            self.name = "Finishing(%s)" % self.name

        def strategy(self):
            for piece in sorted(self.pieces(), reverse=True):
                if piece < self._game.board_size <= piece + self.die:
                    if self.move(piece):
                        return
            super(Finishing, self).strategy()

    return Finishing

bases = [OneByOne, Even, Random]
modifiers = [make_aggressive, make_cautious, make_finishing]
