import math
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
from board import Board
import time
import numpy as np

def get_tt_entry(value, UB=False, LB=False):
    return {'value': value, 'UB': UB, 'LB': LB}       

class AIAgent(object):
    def __init__(self, player_id=1):
        self.player_id = player_id

    def make_move(self, state):
        # start_time = time.time()
        bitboard = Board(state)

        # CURRENTLY, max depth we can do on coursemology is 7, optimize!!
        best_move, res = self.negamax(bitboard, 8)

        # print("num of items: ", len(self.transposition_table))
        # print("Time taken: ", (time.time() - start_time), " seconds")
        print(f"best move here is {best_move}, value is {res}")

        # return best_move
        return (best_move, res)
    
    def negamax(self, bitboard: Board, depth, alpha=-math.inf, beta=math.inf):
        alpha_orig = alpha
        entry = bitboard.transposition_table[bitboard.getKey()] if\
            bitboard.getKey() in bitboard.transposition_table else None
        
        if entry:
            if entry['LB']:
                alpha = max(alpha, entry['value'])
            elif entry['UB']:
                beta = min(beta, entry['value'])
            else:
                return (None, entry['value'])
            if alpha >= beta:
                return (None, entry['value'])

        # is_win() checks if the opponent player wins
        if bitboard.is_win():
            return (None, -1)
        
        # all board spaces have been filled up, and not opp is_win so it is a draw
        if bitboard.counter == 42:
            return (None, 0)

        # reached max depth, calculate eval score which ranges from -1 to +1
        if depth == 0:
            score = bitboard.eval_func()
            return (None, score)
        
        best_move = None
        value = -1
        
        # valid_moves = bitboard.gen_valid_moves()
        non_losing = bitboard.non_losing_moves()
        valid_moves = non_losing + [move for move in bitboard.gen_valid_moves() if move not in non_losing]

        for move in valid_moves:
            bitboard.make_move(move)
            _, res = self.negamax(bitboard, depth - 1, -beta, -alpha)
            res *= -1
            bitboard.undo_move()
            if res > value:
                value = res
                best_move = move
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        if value <= alpha_orig:
            bitboard.transposition_table[bitboard.getKey()] = get_tt_entry(value, UB=True)
        elif value >= beta:
            bitboard.transposition_table[bitboard.getKey()] = get_tt_entry(value, LB=True)
        else:
            bitboard.transposition_table[bitboard.getKey()] = get_tt_entry(value)

        return (best_move, value)

def create_empty_numpy_board():
    return np.zeros((6, 7))
  
def conv_to_board(filename):
    f = open(filename, "r")
    
    test_boards = []
    player_ids = []
    outcomes = []
    players = [1, 2]

    line = f.readline()
    while line:
        pos, score = line.strip().split()
        counter = 0
        b = create_empty_numpy_board()
        height = [5, 5, 5, 5, 5, 5, 5]
        for char in pos:
            c = int(char) - 1
            curr_player = counter & 1
            row = height[c]
            b[row][c] = players[curr_player]
            height[c] -= 1
            counter += 1

        test_boards.append(b)
        outcomes.append(score)
        player_ids.append(counter & 1)
        line = f.readline()

    return test_boards, player_ids, outcomes

test_boards, player_ids, outcomes = conv_to_board("./tests/Test_L3_R1")

moves = []
results = []
times = []
for i in range(len(test_boards)):
    start = time.time()
    agent = AIAgent(player_ids[i])
    best_move, res = agent.make_move(test_boards[i])
    moves.append(best_move)
    res = -1 if res < 0 else 1 if res > 0 else 0
    results.append(res)
    times.append(time.time() - start)

for i in range(1000):
    outcome = int(outcomes[i])
    outcome = -1 if outcome < 0 else 1 if outcome > 0 else 0
    if results[i] != outcome:
        print(f"test {i} error")
        print(test_boards[i])
        print(f"outcome supp to be {outcome}, res is {results[i]}, move played {moves[i]}")

# print("testing results: ", results)
# print("correct outcomes: ", outcomes)
print(max(times))
    