import math

# COLUMN_COUNT = 7
# ROW_COUNT = 6

class Board:

    def __init__(self, state):
        self.height = [0, 7, 14, 21, 28, 35, 42]
        self.counter = 0
        self.moves = [0] * 42
        self.player1, self.player2 = self.convert_state_to_board(state)

    def convert_state_to_board(self, state):
        # p1 -> represents the position of player 1 tokens
        # p2 -> represents the position of player 2 tokens
        p1, p2 = '', ''
        # start to encode into bitboard from bottom row, 1st place on the left  
        for j in range(7):
            for i in range(6, -1, -1):
                if i == 6:
                    p1 = '0' + p1
                    p2 = '0' + p2
                    continue

                if state[i][j] == 1:
                    p1 = '1' + p1
                    p2 = '0' + p2
                    self.height[j] += 1
                    self.counter += 1

                elif state[i][j] == 2:
                    p1 = '0' + p1
                    p2 = '1' + p2
                    self.height[j] += 1
                    self.counter += 1
                
                else:
                    p1 = '0' + p1
                    p2 = '0' + p2
                
        if self.counter & 1:
            p1, p2 = p2, p1

        p1 = p1[:len(p1)-1]
        p2 = p2[:len(p2)-1]
        p1 = '0' + p1
        p2 = '0' + p2

        return int(p1, 2), int(p2, 2)
    
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
    
    def bits_to_cols(self, b):
        cols = set()
        while b:
            lsb = b & -b
            indx = lsb.bit_length() - 1
            c = indx // 7
            cols.add(c)
            b &= b - 1
        return cols
    
    def possible(self):
        return (self.player1 | self.player2) ^ ((self.player1 | self.player2) + self.bottom_mask)

    def compute_winning_positions(self):
        empty = ~(self.player1 | self.player2)
        r = 0

        # Vertical
        m = self.player2 & (self.player2 << 1) & (self.player2 << 2)
        r |= (m << 3) & empty

        # Horizontal
        m = self.player2 & (self.player2 << 7)
        r |= ((m & (self.player2 << 14)) << 21) & empty
        r |= ((m & (self.player2 >> 7)) << 7) & empty
        m = self.player2 & (self.player2 >> 7)
        r |= ((m & (self.player2 >> 14)) >> 21) & empty
        r |= ((m & (self.player2 << 7)) >> 7) & empty

        # Diagonal /
        m = self.player2 & (self.player2 << 6)
        r |= ((m & (self.player2 << 12)) << 18) & empty
        r |= ((m & (self.player2 >> 6)) << 6) & empty
        m = self.player2 & (self.player2 >> 6)
        r |= ((m & (self.player2 >> 12)) >> 18) & empty
        r |= ((m & (self.player2 << 6)) >> 6) & empty

        # Diagonal \
        m = self.player2 & (self.player2 << 8)
        r |= ((m & (self.player2 << 16)) << 24) & empty
        r |= ((m & (self.player2 >> 8)) << 8) & empty
        m = self.player2 & (self.player2 >> 8)
        r |= ((m & (self.player2 >> 16)) >> 24) & empty
        r |= ((m & (self.player2 << 8)) >> 8) & empty

        return r

    def non_losing_moves(self):
        possible = self.possible()
        opp_win = self.compute_winning_positions()
        forced = possible & opp_win

        if forced:
            if forced & (forced - 1):
                return 0
            else:
                possible = forced

        else:
            possible &= ~(opp_win >> 1)

        return possible

    def print_bitboard_p1(self):
        top_level = [6, 13, 20, 27, 34, 41, 48]
        p_board = [[0] * 7 for _ in range(6)]
        str_board = str(bin(self.player1))[2:]
        pad_zeros = 48 - len(str_board)
        str_board = pad_zeros * '0' + str_board
        print(str_board)

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

    def print_bitboard_p2(self):
        top_level = [6, 13, 20, 27, 34, 41, 48] 
        p_board = [[0] * 7 for _ in range(6)]
        str_board = str(bin(self.player2))[2:]
        pad_zeros = 48 - len(str_board)
        str_board = pad_zeros * '0' + str_board
        print(str_board)

        for i in range(42):
            if (i % 7) in top_level:
                continue
            
            else:
                r = i // 7
                c = i % 7
                p_board[c][r] = str_board[i]

        for row in p_board:
            row.reverse()

        print(*p_board, sep="\n")
    
