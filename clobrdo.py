from random import randint, shuffle


START = -1


class IllegalMove(Exception):
    def __init__(self, message, player, board):
        self.player = player
        self.board = board
        super().__init__(message)


class DidNotMove(IllegalMove):
    pass


class Clobrdo:
    """Main class, holds the game state, checks all the rules."""
    def __init__(self, players, n_pieces=4, length=10, n_die=6):
        # Initialize players
        for i, player in enumerate(players):
            player.start = i * length
            player._board = self
            player.finish = [False] * n_pieces
        shuffle(players)
        self.players = players

        # Initialize board
        self.board = {}
        self.board_size = length * len(players)
        self.n_pieces = n_pieces

        # Initialize die
        self.n_die = n_die
        self.die = None

        # State variables
        self.moved = False
        self.rank = []
        self.n_moves = 0

    def play(self):
        """Main loop of the game, """
        while self.players:
            for player in self.players:
                self.player_move(player)
                if self.die == 6:
                    self.player_move(player)
                    player.new_game = False
        return self.rank

    def player_move(self, player):
        """Encapsulates player strategy with sanity and other checks"""
        if player in self.rank:
            return
        self.throw(new=player.new_game)
        self.moved = False
        possible = self.n_moves_possible(player)
        if possible == 0:
            player.moves_stalled += 1
        player.strategy()

        if not self.moved and possible:
            raise DidNotMove("Player did not move, even though moves are possible", player, self)

        if player.finish == [True] * self.n_pieces:
            self.rank.append(player)
            self.players.remove(player)

    def throw(self, new=False):
        """Updates die state"""
        if new:
            # 3 throws at the start of the game
            throws = [randint(1, self.n_die) for _ in range(3)]
            if 6 in throws:
                self.die = 6
            else:
                self.die = throws[2]
        self.die = randint(1, self.n_die)
        self.n_moves += 1

    def n_moves_possible(self, player):
        moves_possible = 0
        for piece in player.pieces():
            if self.move_possible(player, piece):
                moves_possible += 1
            # Check for possible entering
            if len(player.pieces()) < self.n_pieces and self.die == 6:
                moves_possible += 1
        return moves_possible

    def move_possible(self, player, field_from):
        """Checks if move from field is valid or not.
        Expects arguments relative to player in question"""

        # Moving piece in game
        if self.board.get(player.unshift_field(field_from)) == player:
            field_to = field_from + self.die

            # Destination in finish
            if self.board_size <= field_to < self.board_size + self.n_pieces:
                if not player.finish[field_to - self.board_size]:
                    return True
                return False

            # In "normal" fields
            if field_to < self.board_size:
                # Prevents self-throwing off
                if self.board.get(player.unshift_field(field_to)) == player:
                    return False
                return True
            else:
                return False

        # Piece entering the game
        if field_from == START and len(player.pieces()) < self.n_pieces and self.die == 6:
            return True
        return False

    def move(self, player, field_from):
        """Expects arguments relative to player in question"""
        if self.move_possible(player, field_from):
            if field_from == START:
                self.board[player.start] = player
                self.moved = True
                return
            field_to = field_from + self.die
            if field_to >= self.board_size:
                player.finish[field_to - self.board_size] = True
            else:
                self.board[player.unshift_field(field_to)] = player
            if field_from >= self.board_size:
                player.finish[field_from - self.board_size] = False
            else:
                self.board.pop(player.unshift_field(field_from))
            self.moved = True
        else:
            raise IllegalMove("This piece can not make this step or belongs to someone else", player, self)


class BasePlayer:
    def __init__(self, name=None):
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name
        self.start = None
        self.finish = []
        self.new_game = True
        self._board = None
        self.moves_stalled = 0

    @property
    def n_pieces(self):
        return self._board.n_pieces

    def strategy(self):
        """One call of function should result in one move on the board if such move is possible"""
        pass

    def __repr__(self):
        return self.__class__.__name__+"(%s)" % self.name

    def __str__(self):
        return self.__class__.__name__+"(%s)" % self.name

    def die(self):
        return self._board.die

    def move(self, field_from):
        self._board.move(self, field_from)

    def pieces(self, target_player=None):
        """Returns list of all pieces in play belonging to a target_player (if not specified return the pieces of player
        asking"""
        # TODO: Should players see to finishes of others?? Hard to implement in current state.
        if target_player is None:
            target_player = self
        pieces = [self.shift_field(item[0]) for item in self._board.board.items() if item[1] == target_player]
        if target_player == self:
            pieces += [self._board.board_size+i for i, x in enumerate(self.finish) if x]
        return pieces

    def enemies(self):
        return [player for player in self._board.players if player != self]

    def shift_field(self, field):
        """Player object wraps the playing board in such a way that it is seen by the strategy as indexed in terms of
        its on start and finish. This is done using shift_field and unshift_field functions."""
        return (field - self.start) % self._board.board_size

    def unshift_field(self, field):
        return (field + self.start) % self._board.board_size
