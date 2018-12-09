from random import randint
import msvcrt as m


def get_number():
    return randint(1, 6)


class Board:
    board = []
    n = 0

    def __init__(self):
        self.cnt = 0

    def build_board(self):
        print("input odd n")
        n = input()
        try:
            n = int(n)
        except ValueError:
            print("not a number, restart program")
            return 0
        if n % 2 == 0:
            print("not odd number, restart program")
            return 1
        self.n = n
        for i in range(n):
            Board.board.append([])
            for j in range(n):
                if (j < ((n - 1)/2 - 1) or j > ((n - 1)/2 + 1)) and (i < ((n - 1)/2 - 1) or i > ((n - 1)/2 + 1)):
                    self.board[i].append(' ')
                elif j == i == (n-1)/2:
                    self.board[i].append('X')
                elif (i == (n - 1)/2 or j == (n - 1)/2) and j != 0 and j != n - 1 and i != 0 and i != n - 1:
                    self.board[i].append('D')
                else:
                    self.board[i].append('*')

    def show(self):
        for row in self.board:
            print(' '.join(row))


class Coordinates:
    x = None
    y = None

    def __init__(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y


class Chip:
    coordinates = None
    onTable = False

    def __init__(self, x=None, y=None):
        if x is not None and y is not None:
            self.coordinates = Coordinates(x, y)
        self.cnt = 0


class Player:
    chips = []
    coordinates = None

    def __init__(self, x=None, y=None):
        for i in range(4):
            self.chips.append(Chip(-1, -1))
        if x is not None and y is not None:
            self.coordinates = Coordinates(x, y)
        self.cnt = 0


class Game:
    board = Board()
    player1 = None
    player2 = None

    def __init__(self):
        self.board.build_board()
        self.player1 = Player((self.board.n + 1) / 2, 0)
        self.player2 = Player((self.board.n - 1) / 2, 0)
        self.board.show()
        self.cnt = 0

    def play(self):
        m.getch()
        return 0


def main():
    game = Game()


main()
