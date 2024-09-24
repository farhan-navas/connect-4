import numpy as np
COLUMN_COUNT = 7
ROW_COUNT = 6

def convert_state_to_board(state, player):
    board = state

    # pos -> represents board position positioning of player tokens
    # ovr -> represents the position of both players
    pos, ovr = '', ''
    for i in range(ROW_COUNT, -1, -1):
        pos += '0'
        ovr += '0'
        for j in range(ROW_COUNT):
            ovr += '1' if state[i][j] != 0 else '0'
            pos += '1' if state[i][j] == player else '0'

    return int(pos, 2), int(ovr, 2)

def is_win(board):
    m = board & (board >> COLUMN_COUNT)
    if m & (m >> COLUMN_COUNT * 2):
        return True
    
    m = board & (board >> 6)
    if m & (m >> 12):
        return True
    
    m = board & (board >> 8)
    if m & (m >> 16):
        return True
    
    m = board & (board >> 1)
    if m & (m >> 2):
        return True
    
    return False

def make_move(pos, ovr, col):
    new_pos = pos ^ ovr
    new_ovr = ovr | (ovr +(1 << (col * COLUMN_COUNT)))
    return new_pos, new_ovr

