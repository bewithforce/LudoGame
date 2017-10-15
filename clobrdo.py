"""This module implements the game of Ludo and checks the rules."""

from random import randint, shuffle

START = -1


class IllegalMove(Exception):
    """Base class to note illegal moves"""
    def __init__(self, message, player, game):
        self.player = player
        self.board = game.board
        super(IllegalMove, self).__init__(message, self.player, self.board)


class DidNotMove(IllegalMove):
    """Player did not move, even though moves are possible"""
    pass


class MovedMoreThanOnce(IllegalMove):
    """Player moved more than once"""
    pass


class Clobrdo(object):
    """Main class, holds the game state, checks all the rules."""

    def __init__(self, players, n_pieces=4, length=10, n_die=6):
        # Initialize players
        for i, player in enumerate(players):
            player.start = i * length
            player._game = self
            player.new_game = True
            player.finish = [False] * n_pieces
        shuffle(players)
        self.players = players

        # Initialize board
        self.board = {}
        self.board_size = length * len(players)
        self.n_pieces = n_pieces
        self.full_house = [True] * self.n_pieces

        # Initialize die
        self.n_die = n_die
        self.die = None

        # State variables
        self.moved = 0
        self.rank = []
        self.n_moves = 0

    def play(self):
        """Main loop of the game, """
        while self.players:
            for player in self.players:
                if self.n_moves > 1000:
                    pass
                self.player_move(player)
        return self.rank

    def player_move(self, player):
        """Encapsulates player strategy with sanity and other checks"""
        if player in self.rank:
            return
        self.throw(new=player.new_game)
        self.moved = 0
        possible = self.n_moves_possible(player)
        if possible == 0:
            player.moves_stalled += 1

        player.strategy()

        if not self.moved and possible:
            raise DidNotMove(
                "Player did not move, even though moves are possible", player,
                self)

        if self.moved > 1:
            raise MovedMoreThanOnce("Player moved more than once", player,
                                    self)

        if player.finish == self.full_house:
            self.rank.append(player)
            self.players.remove(player)

        if self.die == self.n_die:
            player.new_game = False
            self.player_move(player)

    def throw(self, new=False):
        """Updates die state"""
        if new:
            # 3 throws at the start of the game
            throws = [randint(1, self.n_die) for _ in range(3)]
            if self.n_die in throws:
                self.die = self.n_die
            else:
                self.die = throws[2]
        else:
            self.die = randint(1, self.n_die)
        self.n_moves += 1

    def n_moves_possible(self, player):
        """Returns number of moves possible for a player."""
        moves_possible = 0
        for piece in player.pieces():
            if self.move_possible(player, piece):
                moves_possible += 1
            # Check for possible entering
            if len(player.pieces()) < self.n_pieces and self.die == self.n_die:
                moves_possible += 1
        return moves_possible

    def positions(self, player, field_from):
        """Determines whether the player is comming to/from board/finish"""
        absolute_from = player.unshift_field(field_from)

        from_board = (field_from < self.board_size
                      and self.board.get(absolute_from) == player)
        from_finish = (field_from >= self.board_size
                       and player.finish[field_from - self.board_size])

        field_to = field_from + self.die
        absolute_to = player.unshift_field(field_to)
        finish_border = self.board_size + self.n_pieces
        to_finish = (self.board_size <= field_to < finish_border
                     and not player.finish[field_to - self.board_size])
        to_board = (field_to < self.board_size
                    and self.board.get(absolute_to) != player)

        return (absolute_from, from_board, from_finish, absolute_to, to_board,
                to_finish)

    def move_possible(self, player, field_from):
        """Checks if move from field is valid or not.
        Expects arguments relative to player in question"""

        if field_from == START and self.die == self.n_die:
            if (len(player.pieces()) < self.n_pieces
                    and self.board.get(player.start) != player):
                return True

        _, from_board, from_finish, _, to_board, to_finish = self.positions(
            player, field_from)

        if (from_board or from_finish) and (to_finish or to_board):
            return True

        return False

    def move(self, player, field_from):
        """Expects arguments relative to player in question"""
        if self.move_possible(player, field_from):
            abs_from, from_board, from_finish, abs_to, to_board, to_finish =\
                self.positions(player, field_from)

            if from_board:
                self.board.pop(abs_from)
            if from_finish:
                player.finish[field_from - self.board_size] = False
            if to_board:
                self.board[abs_to] = player
            if to_finish:
                player.finish[field_from + self.die - self.board_size] = True

            self.moved += 1

        else:
            raise IllegalMove(
                "This piece can not make this step or belongs to someone else",
                player, self)
