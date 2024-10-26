from board import Board
import numpy as np

arr1 = np.array([
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,2,2,2,0,0],  
    [0,0,1,2,1,0,0],  
    [0,2,1,1,1,0,0], 
])

arr2 = np.array([
    [0,2,0,2,2,0,0],
    [0,1,0,1,2,0,0],
    [1,2,0,2,1,0,0],
    [2,1,0,1,2,0,0],
    [1,2,0,2,1,0,1],
    [2,1,0,1,2,1,1],
])

arr3 = np.array([
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0],  
    [0,0,0,0,0,0,0], 
])

b = Board(arr2)
print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
b.print_bitboard(b.player1)
b.print_bitboard(b.player2)
print(b.height)
print("valid moves: ", b.gen_valid_moves())
print("non-losing moves: ", b.non_losing_moves())

# print(f"player 1: {nb.player1}, player 2: {nb.player2}, height: {nb.height}, counter: {nb.counter}")
# print("valid moves: ", nb.gen_valid_moves())
# print("non-losing moves: ", nb.non_losing_moves())


# b = Board(arr1)
# print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
# print("valid moves: ", b.gen_valid_moves())
# print("non-losing moves: ", b.non_losing_moves())

# b = Board(empty)
# # print(b.player1, b.player2)
# print(b.height)
# print(b.gen_valid_moves())