from itertools import chain


class End(Exception):
    def __init__(self, winner):
        super().__init__(winner)
        self.winner = winner


class Player:
    kryss = 'X'
    cirkel = 'O'
    NONE = ' '


class TicTacToe:
    def __init__(self):
        self.board = [Player.NONE] * 3, [Player.NONE] * 3, [Player.NONE] * 3

    def __str__(self):
        """Converts the game field into a string"""
        return '{}║{}║{}\n═╬═╬═\n{}║{}║{}\n═╬═╬═\n{}║{}║{}'.format(
            *chain(*self.board))

    @property
    def winConds(self):
        yield self.board[0]
        yield self.board[1]
        yield self.board[2]

        yield self.board[0][0], self.board[1][0], self.board[2][0]
        yield self.board[0][1], self.board[1][1], self.board[2][1]
        yield self.board[0][2], self.board[1][2], self.board[2][2]

        yield self.board[0][0], self.board[1][1], self.board[2][2]
        yield self.board[0][2], self.board[1][1], self.board[2][0]

    @property
    def win(self):
        draw = True
        for fields in self.winConds:
            if fields[0] in (Player.kryss, Player.cirkel):
                if all(fields[0] == field for field in fields[1:]):
                    raise End(fields[0])
            elif any(field is Player.NONE for field in fields):
                draw = False

    def makeMove(self, row, column):
        self.board[column][row] = "X"

    def printBoard(self):
        while True:
            print(self)
            column = int(input("insert column"))
            row = int(input("insert row"))
            try:
                self.win()
            except End as ending:
                if ending.winner == Player.kryss:
                    print("X wins")
                elif ending.winner == Player.cirkel:
                    print("O wins")
                else:
                    print('Its a draw')
                break
            self.makeMove(row, column)


game = TicTacToe()

game.printBoard()
