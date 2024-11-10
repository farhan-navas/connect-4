from moves import arr
import numpy as np
from board import Board

def create_empty_numpy_board():
    return np.zeros((6, 7))

def conv(pos):
    players = [1, 2]
    counter = 0
    b = create_empty_numpy_board()
    height = [5,5,5,5,5,5,5]
    for char in pos:
        c = int(char)
        curr_player = counter & 1
        row = height[c]
        b[row][c] = players[curr_player]
        height[c] -= 1
        counter += 1

    return b

p_data = []
for idx, s in enumerate(arr):
    p_set = set()
    # print(f"curr arr idx: {idx}")
    for elem in s:
        p_elem = conv(elem)
        bb = Board(p_elem)
        p_set.add((bb.player1, bb.player2))
        bb = None
    p_data.append(p_set)
    # print(f"curr set idx {idx} size: {len(p_set)}")

with open('p_moves.py', 'w') as f:
    f.write('processed_arr = [\n')
    for p_set in p_data:
        f.write('   {\n')
        for item in p_set:
            f.write(f'      {repr(item)}, \n')
        f.write('   },\n')
    f.write(']\n')


