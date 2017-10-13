import clobrdo


class BasePlayer(object):
    def __init__(self, name=None):
        self.name = name
        self.start = None
        self.finish = []
        self.new_game = True
        self._game = None
        self.moves_stalled = 0

    @property
    def n_pieces(self):
        return self._game.n_pieces

    def strategy(self):
        """One call of function should result in one move on the board if such move is possible"""
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def die(self):
        return self._game.die

    @property
    def n_die(self):
        return self._game.n_die

    def move(self, field_from):
        try:
            self._game.move(self, field_from)
            return True
        except clobrdo.IllegalMove:
            return False

    def check(self, field):
        return self._game.board.get(self.unshift_field(field))

    def pieces(self, target_player=None):
        """Returns list of all pieces in play belonging to a target_player (if not specified return the pieces of player
        asking"""
        # TODO: Should players see to finishes of others?? Hard to implement in current state.
        if target_player is None:
            target_player = self
        pieces = [self.shift_field(item[0]) for item in self._game.board.items() if item[1] == target_player]
        if target_player == self:
            pieces += [self._game.board_size + i for i, x in enumerate(self.finish) if x]
        return pieces

    def is_in_danger(self, field):
        for f in range(field - 1, field - self.n_die, -1):
            if self.check(f) not in [None, self]:
                return True
        return False

    def enemies(self):
        return [player for player in self._game.players if player != self]

    def shift_field(self, field):
        """Player class wraps the playing board in such a way that it is seen by the strategy as indexed in terms of
        its on start and finish. This is done using shift_field and unshift_field functions."""
        return (field - self.start) % self._game.board_size

    def unshift_field(self, field):
        return (field + self.start) % self._game.board_size
