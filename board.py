class Board:
    sachovnice = []
    n = 0

    def __init__(self):
        self.cnt = 0

    def gensachovnicu(self, n):
        self.n = n
        for i in range(n):
            Board.sachovnice.append([])
            for j in range(n):
                if (j < ((n - 1)/2 - 1) or j > ((n - 1)/2 + 1)) and (i < ((n - 1)/2 - 1) or i > ((n - 1)/2 + 1)):
                    self.sachovnice[i].append(' ')
                elif j == i == (n-1)/2:
                    self.sachovnice[i].append('X')
                elif (i == (n - 1)/2 or j == (n - 1)/2) and j != 0 and j != n - 1 and i != 0 and i != n - 1:
                    self.sachovnice[i].append('D')
                else:
                    self.sachovnice[i].append('*')

    def tlacsachovnicu(self):
        for radek in self.sachovnice:
            print(' '.join(radek))


def main():
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
    print(chr(27) + "[2J")
    b = Board()
    b.gensachovnicu(13)
    b.tlacsachovnicu()


main()