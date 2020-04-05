import random


class Player:
    def __init__(self, mode, side):
        self.mode = mode
        self.side = side

    def enemy_side(self):
        return "X" if self.side == "O" else "O"

    def win(self, board):
        straights = [board[:3], board[3:6], board[6:],
                     board[0:9:3], board[1:9:3], board[2:9:3],
                     board[0:9:4], board[2:7:2]]
        return self.side * 3 in straights

    def loose(self, board):
        straights = [board[:3], board[3:6], board[6:],
                     board[0:9:3], board[1:9:3], board[2:9:3],
                     board[0:9:4], board[2:7:2]]
        return self.enemy_side() * 3 in straights

    @staticmethod
    def blank_pos(board):
        return [i for i, el in enumerate(board) if el not in ["X", "O"]]


class HumanPlayer(Player):
    def get_move(self, board):
        wait_for_input = True
        col = None
        row = None
        while wait_for_input:
            coordinates = input("Enter the coordinates: ").strip().split()
            if len(coordinates) != 2 or not (coordinates[0].isdigit() and coordinates[1].isdigit()):
                print("You should enter numbers!")
                continue
            col = int(coordinates[0]) - 1
            row = 3 - int(coordinates[1])
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("Coordinates should be from 1 to 3!")
                continue
            if row * 3 + col not in self.blank_pos(board):
                print("This cell is occupied! Choose another one!")
                continue
            wait_for_input = False
        return [row, col]


class EasyPlayer(Player):

    def get_move(self, board):
        print('Making move level "' + self.mode + '"')
        pos = random.choice(self.blank_pos(board))
        return [pos // 3, pos % 3]


class MediumPlayer(Player):

    def get_move(self, board):
        print('Making move level "' + self.mode + '"')

        # find win situation
        for pos in self.blank_pos(board):
            new_board = "".join([self.side if i == pos else el for i, el in enumerate(board)])
            if self.win(new_board):
                return [pos // 3, pos % 3]

        # find lost situation
        for pos in self.blank_pos(board):
            new_board = "".join([self.enemy_side() if i == pos else el for i, el in enumerate(board)])
            if self.loose(new_board):
                return [pos // 3, pos % 3]

        # return random move
        pos = random.choice(self.blank_pos(board))
        return [pos // 3, pos % 3]


class HardPlayer(Player):

    def minimax(self, board, side):
        next_side = self.enemy_side() if side == self.side else self.side
        moves = []
        if self.win(board):
            return 10
        if self.loose(board):
            return -10
        if len(self.blank_pos(board)) == 0:
            return 0
        for pos in self.blank_pos(board):
            new_board = "".join([next_side if i == pos else el for i, el in enumerate(board)])
            moves.append(self.minimax(new_board, next_side))
        return min(moves) if side == self.side else max(moves)

    def get_move(self, board):

        print('Making move level "' + self.mode + '"')

        if len(self.blank_pos(board)) == 9:
            return [1, 1]

        moves = []
        for pos in self.blank_pos(board):
            new_board = "".join([self.side if i == pos else el for i, el in enumerate(board)])
            moves.append([pos, self.minimax(new_board, self.side)])

        max_score = -1000
        for move in moves:
            if move[1] > max_score:
                max_score = move[1]
        pos = random.choice([move[0] for move in moves if move[1] == max_score])
        return [pos // 3, pos % 3]


class Game:
    blank = " "

    ops = ["easy", "user", "medium", "hard"]

    @staticmethod
    def create_player(mode, side):
        if mode == "easy":
            return EasyPlayer(mode, side)
        elif mode == "medium":
            return MediumPlayer(mode, side)
        elif mode == "hard":
            return HardPlayer(mode, side)
        return HumanPlayer(mode, side)

    def __init__(self, op1, op2):
        self.player1 = self.create_player(op1, "X")
        self.player2 = self.create_player(op2, "O")
        self.board = self.blank * 9
        self.game_done = False

    def draw_board(self):
        print("-" * len(self.board))
        print("|", " ".join(self.board[:3]), "|")
        print("|", " ".join(self.board[3:6]), "|")
        print("|", " ".join(self.board[6:]), "|")
        print("-" * len(self.board))

    def get_side(self):
        return "X" if self.board.count("X") <= self.board.count("O") else "O"

    def next_move(self):
        if self.get_side() == "X":
            [row, col] = self.player1.get_move(self.board)
        else:
            [row, col] = self.player2.get_move(self.board)
        self.board = "".join([self.get_side() if i == (row * 3 + col) else n for i, n in enumerate(self.board)])

    def check_win(self):
        x_wins = self.player1.win(self.board)
        o_wins = self.player2.win(self.board)
        if x_wins:
            print("X wins")
            self.game_done = True
        elif o_wins:
            print("O wins")
            self.game_done = True
        elif self.board.count(self.blank) == 0:
            print("Draw")
            self.game_done = True


while True:
    command = input("Input command: ").strip().split()
    if len(command) == 1 and command[0] == "exit":
        break
    elif len(command) == 3 and command[0] == "start" and command[1] in Game.ops and command[2] in Game.ops:
        game = Game(command[1], command[2])
        game.draw_board()
        while not game.game_done:
            game.next_move()
            game.draw_board()
            game.check_win()
    else:
        print("Bad parameters!")
