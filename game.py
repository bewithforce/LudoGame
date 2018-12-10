#!/usr/bin/python
from random import randint
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
        for i in list(range(self.n)):
            self.board.append([])
            for j in list(range(self.n)):
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


class Player:

    def __init__(self, x, y, n):
        self.chipsOnBoard = []
        self.chipsInHand = []
        self.chipsAtHome = []
        self.coordinates = None
        self.enable = True
        for i in list(range(n//1)):
            temp = Chip(-1, -1)
            self.chipsInHand.append(temp)
        if x is not None and y is not None:
            self.coordinates = Coordinates(x, y)


class Game:
    board = Board()
    player1 = None
    player2 = None

    def __init__(self):
        self.board.build_board()
        self.player1 = Player(0, (self.board.n + 1) / 2, (self.board.n - 3) / 2)
        self.player2 = Player(self.board.n - 1, (self.board.n - 1)/2 - 1, (self.board.n - 3) / 2)
        self.show()

    def cant_go_to_base(self, n, player):
        if n > (self.board.n - 3) / 2:
            return True
        else:
            if player.coordinates.x < player.coordinates.y:
                for chip in player.chipsAtHome:
                    if chip.coordinates.x == player.coordinates.x + n \
                            and chip.coordinates.y == player.coordinates.y - 1:
                        return True
            else:
                for chip in player.chipsAtHome:
                    if chip.coordinates.x == player.coordinates.x - n \
                            and chip.coordinates.y == player.coordinates.y + 1:
                        return True

    def play(self):
        while (len(self.player1.chipsAtHome) != (self.board.n - 3) / 2
                or len(self.player1.chipsAtHome) != (self.board.n - 3) / 2):
            roll = get_number()
            print('first player\'s move: \ndice number = %r' % roll)
            self.move_player(self.player1, roll)
            self.show()
            roll = get_number()
            print('second player\'s move: \ndice number = %r' % roll)
            self.move_player(self.player2, roll)
            self.show()
        if len(self.player1.chipsAtHome) == (self.board.n - 3) / 2:
            print("First player wins")
        else:
            print("Second player wins")

    def show(self):
        print("___________________________________________________")
        i = 0
        self.board.fill_board()
        for chip in self.player1.chipsOnBoard:
            i += 1
            self.board.board[chip.coordinates.x][chip.coordinates.y] = 'A%r' % i
        i = 0
        for chip in self.player2.chipsOnBoard:
            i += 1
            self.board.board[chip.coordinates.x][chip.coordinates.y] = 'B%r' % i
        for row in self.board.board:
            print ('  '.join(row))

    #
    def move_chip(self, chip, n, player):
        coordinates = Coordinates(chip.coordinates.x, chip.coordinates.y)
        while n != 0:
            if player.coordinates.x == 0:
                if (coordinates.y == (self.board.n - 1) / 2 and coordinates.x < (self.board.n - 1) / 2
                        and coordinates.x + n < (self.board.n - 1)/2):
                    coordinates.x += n
                    return coordinates
                elif coordinates.y == (self.board.n - 1) / 2 and coordinates.x < (self.board.n - 1) / 2:
                    return
            else:
                if (coordinates.y == (self.board.n - 1) / 2 and coordinates.x > (self.board.n - 1) / 2
                        and coordinates.x - n > (self.board.n - 1)/2):
                    coordinates.x -= n
                    return coordinates
                elif coordinates.y == (self.board.n - 1) / 2 and coordinates.x > (self.board.n - 1) / 2:
                    return

            if coordinates.x == player.coordinates.x and \
                    (coordinates.y == player.coordinates.y - 1 or coordinates.y == player.coordinates.y + 1) \
                    and self.cant_go_to_base(n, player) is True:
                return
            elif coordinates.x == player.coordinates.x and \
                    (coordinates.y == player.coordinates.y - 1 or coordinates.y == player.coordinates.y + 1):
                player.chipsAtHome.append(chip)
                if player.coordinates.x == 0:
                    return Coordinates(player.coordinates.x + n, player.coordinates.y - 1)
                else:
                    return Coordinates(player.coordinates.x - n, player.coordinates.y + 1)

            if coordinates.y <= (self.board.n - 1) / 2 and coordinates.x <= (self.board.n - 1) / 2:
                if coordinates.y == coordinates.x:
                    coordinates.x -= 1
                    n -= 1
                elif coordinates.x == (self.board.n - 1) / 2:
                    coordinates.x -= 1
                    n -= 1
                elif coordinates.x == (self.board.n - 1) / 2 - 1:
                    coordinates.y += 1
                    n -= 1
                else:
                    if coordinates.x == 0:
                        coordinates.y += 1
                        n -= 1
                    else:
                        coordinates.x -= 1
                        n -= 1
            elif coordinates.y > (self.board.n - 1) / 2 > coordinates.x:
                if self.board.n - 1 - coordinates.x == coordinates.y:
                    coordinates.y += 1
                    n -= 1
                elif coordinates.y == (self.board.n + 1) / 2:
                    coordinates.x += 1
                    n -= 1
                else:
                    if coordinates.y == self.board.n - 1:
                        coordinates.x += 1
                        n -= 1
                    else:
                        coordinates.y += 1
                        n -= 1
            elif coordinates.y < (self.board.n - 1) / 2 < coordinates.x:
                if self.board.n - 1 - coordinates.y == coordinates.x:
                    coordinates.y -= 1
                    n -= 1
                elif coordinates.y == (self.board.n - 1) / 2 - 1:
                    coordinates.x -= 1
                    n -= 1
                else:
                    if coordinates.y == 0:
                        coordinates.x -= 1
                        n -= 1
                    else:
                        coordinates.y -= 1
                        n -= 1
            else:
                if coordinates.y == coordinates.x:
                    n -= 1
                    coordinates.x += 1
                elif coordinates.x == self.board.n - 1:
                    coordinates.y -= 1
                    n -= 1
                elif coordinates.x == (self.board.n - 1) / 2:
                    coordinates.x += 1
                    n -= 1
                elif coordinates.x == (self.board.n + 1) / 2:
                    coordinates.y -= 1
                    n -= 1
                elif coordinates.y == (self.board.n + 1) / 2:
                    coordinates.x += 1
                    n -= 1
        return coordinates

    def move_player(self, player, n):
        if n < 6 and len(player.chipsOnBoard) == 0:
            print("you miss a turn")
            return
        elif n == 6 and (len(player.chipsOnBoard) - len(player.chipsAtHome)) == 0:
            if player is self.player1:
                for chip in self.player2.chipsOnBoard:
                    if (chip.coordinates.x == player.coordinates.x and
                            chip.coordinates.y == player.coordinates.y):
                        self.player2.chipsOnBoard.remove(chip)
                        self.player2.chipsInHand.append(chip)
                        break
            else:
                for chip in self.player1.chipsOnBoard:
                    if (chip.coordinates.x == player.coordinates.x and
                            chip.coordinates.y == player.coordinates.y):
                        self.player1.chipsOnBoard.remove(chip)
                        self.player1.chipsInHand.append(chip)
                        break
            certain_chip = player.chipsInHand[0]
            certain_chip.coordinates = Coordinates(player.coordinates.x, player.coordinates.y)
            player.chipsOnBoard.append(certain_chip)
            player.chipsInHand.remove(certain_chip)
            return
        elif n == 6 and len(player.chipsOnBoard) - len(player.chipsAtHome) != 0:
            if len(player.chipsInHand) > 0:
                choice = raw_input("put another chips on board?[Y/n]")
                if choice == "Y":
                    temp = 0
                    if player is self.player1:
                        for chip in self.player2.chipsOnBoard:
                            if (chip.coordinates.x == player.coordinates.x and
                                    chip.coordinates.y == player.coordinates.y):
                                self.player2.chipsOnBoard.remove(chip)
                                self.player2.chipsInHand.append(chip)
                                break
                        for chip in self.player1.chipsOnBoard:
                            if (chip.coordinates.x == player.coordinates.x and
                                    chip.coordinates.y == player.coordinates.y):
                                temp += 1
                                break
                    else:
                        for chip in self.player1.chipsOnBoard:
                            if (chip.coordinates.x == player.coordinates.x and
                                    chip.coordinates.y == player.coordinates.y):
                                self.player1.chipsOnBoard.remove(chip)
                                self.player1.chipsInHand.append(chip)
                                break
                        for chip in self.player2.chipsOnBoard:
                            if (chip.coordinates.x == player.coordinates.x and
                                    chip.coordinates.y == player.coordinates.y):
                                temp += 1
                                break
                    if temp == 0:
                        certain_chip = player.chipsInHand[0]
                        certain_chip.coordinates = Coordinates(player.coordinates.x, player.coordinates.y)
                        player.chipsOnBoard.append(certain_chip)
                        player.chipsInHand.remove(certain_chip)
                        return
        while True:
            if len(player.chipsOnBoard) > 1:
                choice = raw_input("what chips to move?")
                try:
                    choice = int(choice)
                    choice -= 1
                except ValueError:
                    print("not a number, restart program")
                    sys.exit()
            else:
                choice = 0
            if choice > (self.board.n - 3) / 2:
                print("bad choice")
                continue
            coordinates = self.move_chip(player.chipsOnBoard[choice], n, player)
            if coordinates is None:
                if len(player.chipsOnBoard) > 1:
                    for tempChip in player.chipsOnBoard:
                        if self.move_chip(tempChip, n, player) is not None:
                            print("bad choice")
                        else:
                            print("you miss a turn")
                    continue
                else:
                    print("you miss a turn")
                    break
            for chip in player.chipsOnBoard:
                if (coordinates.x == chip.coordinates.x and
                        coordinates.y == chip.coordinates.y):
                    print("bad choice")
                    continue
            for chip in self.player1.chipsOnBoard:
                if (coordinates.x == chip.coordinates.x and
                        coordinates.y == chip.coordinates.y):
                    self.player1.chipsOnBoard.remove(chip)
                    self.player1.chipsInHand.append(chip)
                    break
            for chip in self.player2.chipsOnBoard:
                if (coordinates.x == chip.coordinates.x and
                        coordinates.y == chip.coordinates.y):
                    self.player2.chipsOnBoard.remove(chip)
                    self.player2.chipsInHand.append(chip)
                    break
            player.chipsOnBoard[choice].coordinates.x = coordinates.x
            player.chipsOnBoard[choice].coordinates.y = coordinates.y
            break


def main():
    game = Game()
    game.play()


main()
