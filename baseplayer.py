import clobrdo


class BasePlayer(object):
    """Base class for player strategies"""
    def __init__(self, name=None):
        self.name = name
        self.start = None
        self.finish = []
        self.new_game = True
        self._game = None
        self.moves_stalled = 0

    @property
    def n_pieces(self):
        """Returns number of pieces each player has in the game"""
        return self._game.n_pieces

    def strategy(self):
        """One call of function should result in one move on the board if such
        move is possible"""
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def die(self):
        """Access to die."""
        return self._game.die

    @property
    def n_die(self):
        """Returns number of sides of the die"""
        return self._game.n_die

    def move(self, field_from):
        """Tries to move. Returns True on success."""
        try:
            self._game.move(self, field_from)
            return True
        except clobrdo.IllegalMove:
            return False

    def check(self, field):
        """Returns the player standing on field. None if empty."""
        return self._game.board.get(self.unshift_field(field))

    def pieces(self, target_player=None):
        """Returns list of all pieces in play belonging to a target_player
        (if not specified return the pieces of player asking)"""
        # TODO: Should players see to finishes of others??
        # Hard to implement in current state.
        if target_player is None:
            target_player = self
        pieces = [self.shift_field(item[0])
                  for item in self._game.board.items()
                  if item[1] == target_player]
        if target_player == self:
            pieces += [self._game.board_size + i
                       for i, x in enumerate(self.finish) if x]
        return pieces

    def is_in_danger(self, field):
        """Returns True iff the field is in danger of taking
        in the next move"""
        for possible in range(field - 1, field - self.n_die, -1):
            if self.check(possible) not in [None, self]:
                return True
        return False

    def enemies(self):
        """Returns list of positions of enenemies' pieces."""
        return [player for player in self._game.players if player != self]

    def shift_field(self, field):
        """Player class wraps the playing board in such a way that it is seen
        by the strategy as indexed in terms of its on start and finish.
        This is done using shift_field and unshift_field functions."""
        return (field - self.start) % self._game.board_size

    def unshift_field(self, field):
        return (field + self.start) % self._game.board_size
