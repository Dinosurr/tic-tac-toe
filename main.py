from itertools import chain
import random
import score


class End(Exception):
    def __init__(self, winner):
        super().__init__(winner)
        self.winner = winner


class BadInput(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.error = error


class Player:
    cross = 'X'
    circle = 'O'
    NONE = ' '


class TicTacToe:
    def __init__(self):
        """Initializes field and last player"""
        self.board = [[Player.NONE] * 3, [Player.NONE] * 3, [Player.NONE] * 3]
        self.lastPlayer = Player.NONE
        self.totalturns = 0

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
    def nextPlayer(self):
        if self.lastPlayer is Player.cross:
            return Player.circle

        return Player.cross

    def win(self):
        draw = True

        for fields in self.winConds:
            if fields[0] in (Player.cross, Player.circle):
                if all(fields[0] == field for field in fields[1:]):
                    raise End(fields[0])
            elif any(field == Player.NONE for field in fields):
                draw = False
        if draw:
            raise End(Player.NONE)

    def uInput(self):
        print("Current player {}: ".format(self.nextPlayer))
        column = input("Insert column: ")
        row = input("Insert row: ")
        try:
            column, row = int(column), int(row)
        except ValueError:
            raise BadInput('Must be in single digit numbers')
        else:
            if all(0 <= i <= 2 for i in (column, row)):
                return column, row
            raise BadInput("Please only insert a number between 0 and 2")

    def makeMove(self, row, column, currentplayer):
        self.totalturns += 1
        if self.board[row][column] is Player.NONE:
            self.lastPlayer = self.board[row][column] = currentplayer
        else:
            print("Space taken, please take another")

    def computer(self):
        randCol = random.randint(0, 2)
        randRow = random.randint(0, 2)
        self.makeMove(randCol, randRow, self.nextPlayer)

    def printScore(self, winner, turns):
        with open('score.py', 'r') as f:
            if winner == Player.cross:
                currentscore = score.cross_wins
                scorestr = str(currentscore + 1)
                filedata = f.readlines()

                filedata[0] = "cross_wins = " + scorestr + '\n'

            elif winner == Player.circle:
                currentscore = score.circle_wins
                scorestr = str(currentscore + 1)
                filedata = f.readlines()

                filedata[1] = "circle_wins = " + scorestr + '\n'
            else:
                currentscore = score.draws
                scorestr = str(currentscore + 1)
                filedata = f.readlines()

                filedata[2] = "draws = " + scorestr + '\n'

            with open('score.py', 'w') as f:
                for line in filedata:
                    f.write(line)

    def stats(self, turns, winner):
        from numpy import mean
        score.all_moves.append(turns)
        numberlist = score.all_moves

        Olist = score.circle_moves
        Xlist = score.cross_moves

        avg = mean(numberlist)

        with open('score.py', 'r') as f:
            filedata = f.readlines()

            filedata[6] = "average_moves = " + str(avg) + '\n'
            filedata[11] = "all_moves = " + str(numberlist) + '\n'
            if winner == 2:
                Olist.append(turns)
                filedata[12] = "circle_moves = " + str(numberlist) + '\n'
                avgO = mean(Olist)
                filedata[4] = "average_circle_moves = " + str(avgO) + '\n'
            elif winner == 1:
                Xlist.append(turns)
                filedata[13] = "cross_moves = " + str(numberlist) + '\n'
                avgX = mean(Xlist)
                filedata[5] = "average_cross_moves = " + str(avgX) + '\n'
            with open('score.py', 'w') as f:
                for line in filedata:
                    f.write(line)

    def printBoard(self, computer):
        while True:
            winner = None
            print(self)
            try:
                self.win()
            except End as game_end:

                if game_end.winner is Player.cross:
                    print('Cross wins.')
                    winner = 1
                    self.stats(self.totalturns, winner)
                    self.printScore(game_end.winner, 1)

                elif game_end.winner is Player.circle:
                    winner = 2
                    print('Circle wins.')
                    self.printScore(game_end.winner, 1)
                    self.stats(self.totalturns, winner)

                else:
                    winner = 3
                    print('The game ended in a draw.')
                    self.printScore(game_end.winner, 1)
                    self.stats(self.totalturns, winner)
                break
            if self.nextPlayer == Player.circle and computer is True:
                self.computer()
            else:
                try:
                    column, row = self.uInput()
                except KeyboardInterrupt:
                    print("Game stopped")
                except BadInput as invalidMove:
                    print(invalidMove.error)
                else:
                    self.makeMove(row, column, self.nextPlayer)


def run(computer):
    game = TicTacToe()
    game.printBoard(computer)


while True:
    print("Want to play Tic tac toe?")
    choice = input("Y/N?").upper()
    if choice == "Y":
        pc = input("Do you want to play versus PC? Y/N").upper()
        if pc == "Y":
            run(True)
        else:
            run(False)
    else:
        print(BadInput("Exiting"))
        break
