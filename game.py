from random import randint
import msvcrt as m
import sys


def get_number():
    return randint(1, 6)


class Board:
    board = []
    n = 0

    def __init__(self):
        self.cnt = 0

    def fill_board(self):
        self.board = []
        for i in range(self.n):
            self.board.append([])
            for j in range(self.n):
                if (j < ((self.n - 1) / 2 - 1) or j > ((self.n - 1) / 2 + 1)) and (
                        i < ((self.n - 1) / 2 - 1) or i > ((self.n - 1) / 2 + 1)):
                    self.board[i].append(' ')
                elif j == i == (self.n - 1) / 2:
                    self.board[i].append('X')
                elif (i == (self.n - 1) / 2 or j == (self.n - 1) / 2) \
                        and j != 0 and j != self.n - 1 and i != 0 and i != self.n - 1:
                    self.board[i].append('D')
                else:
                    self.board[i].append('*')

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
        self.fill_board()


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

    def __init__(self, x=None, y=None):
        if x is not None and y is not None:
            self.coordinates = Coordinates(x, y)
        self.cnt = 0


class Player:
    chipsOnBoard = []
    chipsInHand = []
    coordinates = None
    enable = True

    def __init__(self, x=None, y=None):
        for i in range(4):
            self.chipsInHand.append(Chip(-1, -1))
        if x is not None and y is not None:
            self.coordinates = Coordinates(x, y)
        self.cnt = 0


class Game:
    board = Board()
    player1 = None
    player2 = None

    def __init__(self):
        self.board.build_board()
        self.player1 = Player(0, (self.board.n + 1) / 2)
        self.player2 = Player(self.board.n - 1, (self.board.n - 1)/2 - 1)
#        self.show()
        self.cnt = 0

    def play(self):
        roll = get_number()
        print('first player\'s move: \ndice number = %r' % roll)
        self.move_player(self.player1, 6)
#        self.show()
        self.move_player(self.player1, roll)
        self.show()

    def show(self):
        i = 0
        self.board.fill_board()
        for chip in self.player1.chipsOnBoard:
            i += 1
            print chip.coordinates.x, chip.coordinates.y
            self.board.board[chip.coordinates.x][chip.coordinates.y] = '\33[31m%r\033[0m' % i
        i = 0
        for chip in self.player2.chipsOnBoard:
            i += 1
            self.board.board[chip.coordinates.x][chip.coordinates.y] = '\33[34m%r\033[0m' % i
        for row in self.board.board:
            print (' '.join(row))

    def move_chip(self, chip, n):
        while n != 0:
            if chip.coordinates.y <= (self.board.n - 1) / 2 and chip.coordinates.x <= (self.board.n - 1) / 2:
                if chip.coordinates.y == chip.coordinates.x:
                    n -= 1
                    chip.coordinates.x -= 1
                elif chip.coordinates.x == (self.board.n - 1) / 2:
                    n -= 1
                    chip.coordinates.x -= 1
                elif chip.coordinates.x == (self.board.n - 1) / 2 - 1:
                    chip.coordinates.y += 1
                    n -= 1
                elif chip.coordinates.y == (self.board.n - 1) / 2 - 1:
                    if chip.coordinates.x == 0:
                        chip.coordinates.y += 1
                        n -= 1
                    else:
                        chip.coordinates.y += 1
                        n -= 1
            elif chip.coordinates.y > (self.board.n - 1) / 2 > chip.coordinates.x:
                if self.board.n - 1 - chip.coordinates.x == chip.coordinates.y:
                    n -= 1
                    chip.coordinates.y += 1
                elif chip.coordinates.x == (self.board.n + 1) / 2:
                    chip.coordinates.y += 1
                    n -= 1
                else:
                    if chip.coordinates.x == self.board.n - 1:
                        n -= 1
                        chip.coordinates.y += 1
                    else:
                        chip.coordinates.x += 1
                        n -= 1
            elif chip.coordinates.y < (self.board.n - 1) / 2 < chip.coordinates.x:
                if self.board.n - 1 - chip.coordinates.y == chip.coordinates.x:
                    n -= 1
                    chip.coordinates.y -= 1
                elif chip.coordinates.y == (self.board.n - 1) / 2 - 1:
                    chip.coordinates.x -= 1
                    n -= 1
                else:
                    if chip.coordinates.y == 0:
                        n -= 1
                        chip.coordinates.x -= 1
                    else:
                        chip.coordinates.y -= 1
                        n -= 1
            else:
                if chip.coordinates.y == chip.coordinates.x:
                    n -= 1
                    chip.coordinates.x += 1
                elif chip.coordinates.y == self.board.n - 1:
                    if chip.coordinates.x == (self.board.n - 1) / 2:
                        n -= 1
                        chip.coordinates.x += 1
                    else:
                        chip.coordinates.y += 1
                        n -= 1
                elif chip.coordinates.y == (self.board.n - 1) / 2 - 1:
                    chip.coordinates.y += 1
                    n -= 1
                elif chip.coordinates.x == 0:
                    chip.coordinates.y += 1
                    n -= 1
                else:
                    chip.coordinates.x -= 1
                    n -= 1

    def move_player(self, player, n):
        if n < 6 and len(player.chipsOnBoard) == 0:
            print "you miss a turn"
            return
        elif n == 6 and len(player.chipsOnBoard) == 0:
            temp = 0
            for chip in self.player1.chipsOnBoard:
                if (chip.coordinates.x == player.coordinates.x and
                        chip.coordinates.y == player.coordinates.y):
                    temp += 1
                    break
            for chip in self.player2.chipsOnBoard:
                if (chip.coordinates.x == player.coordinates.x and
                        chip.coordinates.y == player.coordinates.y):
                    temp += 1
                    break
            if temp == 0:
                certain_chip = player.chipsInHand[0]
                certain_chip.coordinates = Coordinates(player.coordinates.x, player.coordinates.y)
                print certain_chip.coordinates.x, certain_chip.coordinates.y
                player.chipsOnBoard.append(certain_chip)
                player.chipsInHand.remove(certain_chip)
                return
            else:
                print "you miss a turn"
                return
        elif n == 6 and len(player.chipsOnBoard) != 4:
            temp = 0
            for chip in self.player1.chipsOnBoard:
                if (chip.coordinates.x == player.coordinates.x and
                        chip.coordinates.y == player.coordinates.y):
                    temp += 1
                    break
            for chip in self.player2.chipsOnBoard:
                if (chip.coordinates.x == player.coordinates.x and
                        chip.coordinates.y == player.coordinates.y):
                    temp += 1
                    break
            if temp == 0:
                choice = raw_input("put another chips on board?[Y/n]")
                if choice == "Y":
                    certain_chip = player.chipsInHand[0]
                    certain_chip.coordinates = Coordinates(player.coordinates.x, player.coordinates.y)
                    player.chipsOnBoard.append(certain_chip)
                    player.chipsInHand.remove(certain_chip)
                    return
        if len(player.chipsOnBoard) > 1:
            choice = raw_input("what chips to move?")
            try:
                choice = int(choice)
            except ValueError:
                print("not a number, restart program")
                sys.exit()
        else:
            choice = 0
        self.move_chip(player.chipsOnBoard[choice], n)


def main():
    game = Game()
    game.play()


main()
