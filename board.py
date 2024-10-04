import numpy as np

# COLUMN_COUNT = 7
# ROW_COUNT = 6

class Board:

    def __init__(self, state):
        self.height = [0, 7, 15, 24, 30, 35, 42]
        self.counter = 0
        self.moves = [0] * 42
        self.player1, self.player2 = self.convert_state_to_board(state)

    def convert_state_to_board(self, state):

        # p1 -> represents the position of player 1 tokens
        # p2 -> represents the position of player 2 tokens
        p1, p2 = '', ''
        r = ['0', '1']
        for i in range(6, -1, -1):
            for j in range(6):
                p1.join(r[state[i][j] == 1])
                p2.join(r[state[i][j] == 2])

        return int(p1, 2), int(p2, 2)
    
    # TEMP FUNCTIONS -> FAKE VERSION

    def eval_func(self, count):
        res = 0
        val = 10 if count == 2 else 100
        board = self.player1

        directions = [1, 7, 6, 8]
        for dir in directions:
            if count == 2:
                if (board & (board >> dir)) != 0:     
                    res += count * val

            if count == 3:
                if (board & (board >> dir) & (board >> dir * 2)) != 0:
                    res += count * val
            
        return res 

    # REAL VERSION

    def is_win(self):
        directions = [1, 7, 6, 8]
        for dir in directions:
            b = self.player2 & (self.player2 >> dir)
            if b & (b >> dir * 2):
                return True
            
        return False

    def make_move(self, col):
        move = 1 << self.height[col]
        self.height[col] += 1

        self.moves[self.counter] = col
        self.counter += 1

        self.player1, self.player2 = self.player2, self.player1 ^ move
        return self

    def undo_move(self):
        self.counter -= 1
        col = self.moves[self.counter]
        self.height[col] -= 1
        move = 1 << self.height[col]

        self.player1, self.player2 = self.player2 ^ move, self.player1

    def gen_valid_moves(self):
        moves = []
        TOP = int('1000000100000010000001000000100000010000001000000', 2)
        for i in range(7):
            if not (TOP & (1 << self.height[i])):
                moves.append(i)

        return moves
            
