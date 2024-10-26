import math
import numpy as np

# COLUMN_COUNT = 7
# ROW_COUNT = 6

class Board:

    def __init__(self, state):
        self.height = [0, 7, 14, 21, 28, 35, 42]
        self.counter = 0
        self.moves = [0] * 42
        self.player1, self.player2 = self.convert_state_to_board(state)
        self.bottom_mask = 0b1000000100000010000001000000100000010000001
        self.board_mask =  0b0111111011111101111110111111011111101111110111111

    def convert_state_to_board(self, state):
        # p1 -> represents the position of player 1 tokens
        # p2 -> represents the position of player 2 tokens
        p1, p2 = 0, 0
        # reverse board such that bottom layer is now row 0, and then encode into bitboard
        state = np.flip(state, axis=0)
        for r in range(6):
            for c in range(7):
                bit_idx = c * 7 + r
                if state[r][c] == 1:
                    p1 |= 1 << bit_idx
                    self.height[c] += 1
                    self.counter += 1
                elif state[r][c] == 2:
                    p2 |= 1 << bit_idx
                    self.height[c] += 1 
                    self.counter += 1

        if self.counter & 1:
            p1, p2 = p2, p1

        return p1, p2

    # TEMP FUNCTIONS

    def eval_func(self):
        directions = [1, 7, 6, 8]

        def count_nums(board, num):
            score = 0
            for dir in directions:
                b = board
                for i in range(num - 1):
                    b = b & (b >> dir * (i+1)) 
                    score += bin(b).count('1')

            return score

        agent_score = count_nums(self.player1, 2) + count_nums(self.player1, 3) * 4 
        opp_score = count_nums(self.player2, 2) + count_nums(self.player2, 3) * 4

        return math.tanh(agent_score - opp_score)

    # REAL VERSION

    # CHECK which is_win function is more efficient
    # def is_win(self):
    #     b = self.player2
    #     if b & (b >> 1) & (b >> 2) & (b >> 3):
    #         return True
    #     if b & (b >> 7) & (b >> 14) & (b >> 21):
    #         return True
    #     if b & (b >> 6) & (b >> 12) & (b >> 18):
    #         return True
    #     if b & (b >> 8) & (b >> 16) & (b >> 24):
    #         return True
    #     return False

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
            if ((TOP & (1 << self.height[i])) == 0):
                moves.append(i)

        moves.sort(key=lambda x: abs(x - 3))
        return moves
    
    def bits_to_moves(self, b):
        moves = []
        for c in range(7):
            if self.height[c] >= (c * 7) + 6:
                continue
            idx = self.height[c]
            if b & (1 << idx):
                moves.append(c)

        return moves
    
    def possible(self):
        # returns a board of all current moves played + all next moves playable
        return (self.player1 | self.player2) ^ ((self.player1 | self.player2) + self.bottom_mask)

    def compute_winning_positions(self, b):
        w = (b << 1) & (b << 2) & (b << 3)

        # horizontal
        curr = (b << 7) & (b << 14)
        w |= curr & (b << 21)
        w |= curr & (b >> 7)
        curr >>= 21
        w |= curr & (b << 7)
        w |= curr & (b >> 21)

        # diagonal 1
        curr = (b << 6) & (b << 12)
        w |= curr & (b << 18)
        w |= curr & (b >> 6)
        curr >>= 18
        w |= curr & (b << 6)
        w |= curr & (b >> 18)

        # diagonal 2
        curr = (b << 8) & (b << 16)
        w |= curr & (b << 24)
        w |= curr & (b >> 8)
        curr >>= 24
        w |= curr & (b << 8)
        w |= curr & (b >> 24)
        # print("w")
        # self.print_bitboard(w)

        return w & self.board_mask

    def non_losing_moves(self):
        possible = self.possible()
        opp_win = self.compute_winning_positions(self.player2)

        next_possible = possible ^ (self.player1 | self.player2)
        forced = next_possible & opp_win

        if forced:
            if forced & (forced - 1):
                return []
            else:
                possible = forced
                moves = []
                for col in range(7):
                    for row in range(7):
                        b = 1 << (col * 7 + row)
                        if b & possible:
                            moves.append(col)
                return moves

        else:
            next_possible &= ~(opp_win >> 1)

        valid_moves = self.bits_to_moves(next_possible)
        valid_moves.sort(key=lambda x: abs(x - 3))

        scored_moves = []
        for idx, move in enumerate(valid_moves):
            score = self.move_score(move)
            scored_moves.append((move, score, idx))

        scored_moves.sort(key=lambda x: (-x[1], x[2]))
        sorted_moves = [move for move, score, idx in scored_moves]
        return sorted_moves
    
    def pop_count(self, b):
        return bin(b).count('1')
    
    def move_score(self, move):
        self.make_move(move)
        curr_win = self.compute_winning_positions(self.player1)
        win = (curr_win ^ self.player2) & curr_win
        self.undo_move()
        return self.pop_count(win)

    def print_bitboard(self, b):
        print(bin(b))
        top_level = [6, 13, 20, 27, 34, 41, 48]
        p_board = [[0] * 7 for _ in range(6)]
        str_board = str(bin(b))[2:]
        pad_zeros = 48 - len(str_board)
        str_board = pad_zeros * '0' + str_board
        print("board in binary: ", str_board)

        for i in range(48):
            if (i % 7) in top_level:
                continue
            
            else:
                r = i // 7
                c = i % 7
                p_board[c][r] = str_board[i]
        
        for row in p_board:
            row.reverse()

        print(*p_board, sep="\n")
    
