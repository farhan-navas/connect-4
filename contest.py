# from game_utils import initialize, step, get_valid_col_id

# c4_board = initialize()
# print(c4_board.shape)

# print(c4_board)

# get_valid_col_id(c4_board)

# step(c4_board, col_id=2, player_id=1, in_place=True)

# print(c4_board)

# step(c4_board, col_id=2, player_id=2, in_place=True)
# step(c4_board, col_id=2, player_id=1, in_place=True)
# step(c4_board, col_id=2, player_id=2, in_place=True)
# step(c4_board, col_id=2, player_id=1, in_place=True)
# step(c4_board, col_id=2, player_id=2, in_place=True)
# print(c4_board)

# print(get_valid_col_id(c4_board))

# step(c4_board, col_id=2, player_id=1, in_place=True)

class ZeroAgent(object):
    def __init__(self, player_id=1):
        pass
    def make_move(self, state):
        return 0

# Step 1
# agent1 = ZeroAgent(player_id=1) # Yours, Player 1
# agent2 = ZeroAgent(player_id=2) # Opponent, Player 2

# # Step 2
# contest_board = initialize()

# # Step 3
# p1_board = contest_board.view()
# p1_board.flags.writeable = False
# move1 = agent1.make_move(p1_board)

# # Step 4
# step(contest_board, col_id=move1, player_id=1, in_place=True)

# from simulator import GameController, HumanAgent
# from connect_four import ConnectFour

# board = ConnectFour()
# game = GameController(board=board, agents=[HumanAgent(1), HumanAgent(2)])
# game.run()

# ## Task 1.1 Make a valid move

# import random

# class AIAgent(object):
#     """
#     A class representing an agent that plays Connect Four.
#     """
#     def __init__(self, player_id=1):
#         """Initializes the agent with the specified player ID.

#         Parameters:
#         -----------
#         player_id : int
#             The ID of the player assigned to this agent (1 or 2).
#         """
#         self.player_id = player_id
    
#     def make_move(self, state):
#         """
#         Determines and returns the next move for the agent based on the current game state.

#         Parameters:
#         -----------
#         state : np.ndarray
#             A 2D numpy array representing the current, read-only state of the game board. 
#             The board contains:
#             - 0 for an empty cell,
#             - 1 for Player 1's piece,
#             - 2 for Player 2's piece.

#         Returns:
#         --------
#         int
#             The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
#         """
#         possible_choices = get_valid_col_id(state)
        

# def test_task_1_1():
#     from utils import check_step, actions_to_board
    
#     # Test case 1
#     res1 = check_step(ConnectFour(), 1, AIAgent)
#     assert(res1 == "Pass")
 
#     # Test case 2
#     res2 = check_step(actions_to_board([0, 0, 0, 0, 0, 0]), 1, AIAgent)
#     assert(res2 == "Pass")
    
#     # Test case 3
#     res2 = check_step(actions_to_board([4, 3, 4, 5, 5, 1, 4, 4, 5, 5]), 1, AIAgent)
#     assert(res2 == "Pass")

## Task 2.1: Defeat the Baby Agent

from game_utils import initialize, step, get_valid_col_id, is_end
import math
import numpy as np
import time
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
import random

class AIAgent(object):
    def __init__(self, player_id=1):
        self.player_id = player_id
        self.agent_table = np.zeros((6, 7), dtype=int)
        self.opp_table = np.zeros((6, 7), dtype=int)
        self.transposition_table = {}

    def make_move(self, state):
        start_time = time.time()
        res, move = self.negamax(state, self.player_id, 5)
        print("--- %s seconds ---" % (time.time() - start_time))
        return move
    
    def is_win(self, state, player):
        for row in range(6):
            for col in range(7):
                if state[row][col] == 0:
                    continue
                if col + 3 < 7 and np.all(state[row, col:col+4] == player):
                    return player
                if row + 3 < 6 and np.all(state[row:row+4, col] == player):
                    return player
                if row + 3 < 6 and col + 3 < 7 and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return player
                if row + 3 < 6 and col - 3 >= 0 and state[row][col] == state[row + 1][col - 1] == state[row + 2][col - 2] == state[row + 3][col - 3]:
                    return player
        return 0

    def check_rows(self, state, player, table, count):
        val = 10 if count == 2 else 100

        for r in range(6):
            for c in range(7):
                if state[r][c] == 0 or state[r][c] != player:
                    continue
                if r + count > 6 and c + count > 7:
                    break 
                if c + count <= 7 and state[r][c] == state[r][c + count - 2] == state[r][c + count - 1] == player:
                    table[r][c] = val
                    table[r][c + count - 2] = val
                    table[r][c + count - 1] = val
                if r + count <= 6 and state[r][c] == state[r + count - 2][c] == state[r + count - 1][c] == player:
                    table[r][c] = val
                    table[r + count - 2][c] = val
                    table[r + count - 1][c] = val
                if r + count <= 6 and c + count <= 7 and state[r][c] == state[r + count - 2][c + count - 2] == state[r + count - 1][c + count - 1] == player:
                    table[r][c] = val
                    table[r + count - 2][c + count - 2] = val
                    table[r + count - 1][c + count - 1] = val
                if r + count <= 6 and c - count + 1 >= 0 and state[r][c] == state[r + count - 2][c - count + 2] == state[r + count - 1][c - count + 1] == player:
                    table[r][c] = val
                    table[r + count - 2][c - count + 2] = val
                    table[r + count - 1][c - count + 1] = val
        
        return table            

    def eval_func(self, state, player):
        # eval_table = np.array([[3, 4, 5, 7, 5, 4, 3], 
        #             [4, 6, 8, 10, 8, 6, 4],
        #             [5, 8, 11, 13, 11, 8, 5],
        #             [5, 8, 11, 13, 11, 8, 5],
        #             [4, 6, 8, 10, 8, 6, 4],
        #             [3, 4, 5, 7, 5, 4, 3]])
        
        # self.agent_table.fill(0)
        # self.opp_table.fill(0)
        # opp_player = 3 - player

        # self.agent_table = self.check_rows(state, player, self.agent_table, 2)    
        # self.agent_table = self.check_rows(state, player, self.agent_table, 3)
        # self.opp_table = self.check_rows(state, opp_player, self.opp_table, 2)
        # self.opp_table = self.check_rows(state, opp_player, self.opp_table, 3)

        # agent_score = np.sum(self.agent_table * eval_table)
        # opp_score = np.sum(self.opp_table * eval_table) 

        # return agent_score - opp_score
        return random.randint(0, 100)
    
    def order_moves(self, moves):
        center = 3
        sorted_moves = sorted(moves, key=lambda x: abs(x - center))
        return sorted_moves
    
    def negamax(self, state, player, depth, alpha=-math.inf, beta=math.inf):
        key = hash(state.data.tobytes())
        if key in self.transposition_table and self.transposition_table[key]['depth'] >= depth:
            return self.transposition_table[key]['value'], self.transposition_table[key]['move']

        opp_player = 3 - player
        if self.is_win(state, player) == player:
            return 1000, None
        
        if self.is_win(state, opp_player) == opp_player:
            return -1000, None

        if depth == 0:
            score = self.eval_func(state, player)
            return score, None
        
        value = -math.inf
        valid_moves = self.order_moves(get_valid_col_id(state))
        best_move = None

        for move in valid_moves: 
            new_value, _ = self.negamax(step(state, move, opp_player, in_place=False), opp_player, depth - 1, -beta, -alpha)
            new_value *= -1
            if new_value > value:
                value = new_value
                best_move = move

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        self.transposition_table[key] = {'value': value, 'move': move, 'depth': depth}
        return value, best_move


board = ConnectFour()
game = GameController(board=board, agents=[HumanAgent(1), AIAgent(2)])
game.run()

# # Test cases
# assert(True)
# # Upload your code to Coursemology to test it against our agent.

# def test_task_2_1():
#     assert(True)
#     # Upload your code to Coursemology to test it against our agent.

# ## Task 2.2: Defeat the Base Agent

# class AIAgent(object):
#     """
#     A class representing an agent that plays Connect Four.
#     """
#     def __init__(self, player_id=1):
#         """Initializes the agent with the specified player ID.

#         Parameters:
#         -----------
#         player_id : int
#             The ID of the player assigned to this agent (1 or 2).
#         """
#         pass
#     def make_move(self, state):
#         """
#         Determines and returns the next move for the agent based on the current game state.

#         Parameters:
#         -----------
#         state : np.ndarray
#             A 2D numpy array representing the current, read-only state of the game board. 
#             The board contains:
#             - 0 for an empty cell,
#             - 1 for Player 1's piece,
#             - 2 for Player 2's piece.

#         Returns:
#         --------
#         int
#             The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
#         """
#         """ YOUR CODE HERE """
#         raise NotImplementedError
#         """ YOUR CODE END HERE """

# def test_task_2_2():
#     assert(True)
#     # Upload your code to Coursemology to test it against our agent.


# if __name__ == '__main__':
    # test_task_1_1()
    # test_task_2_1()
    # test_task_2_2()