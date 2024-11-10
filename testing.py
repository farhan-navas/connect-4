from board import Board
import numpy as np
from game import AIAgent

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
    [0,1,0,0,0,0,0], 
])

arr5 = np.array([[0, 0, 0, 2, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0],
 [0, 0, 0, 2, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0],
 [0, 0, 0, 2, 1, 0, 0],
 [0, 2, 1, 1, 2, 1, 0]]
)

b = Board(arr5)
print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
b.print_bitboard(b.player1)
b.print_bitboard(b.player2)
print("counter: ", b.counter)
print(b.height)
print("valid moves: ", b.gen_valid_moves())
print("non-losing moves: ", b.non_losing_moves())

a = AIAgent(2)
a.make_move(arr5)

# test1 = [(2097152, 268451840), (2097152, 268435457), (2097152, 272629760), (2097152, 4398314946560), (2097152, 34628173824), (2097152, 268435584), (2097152, 805306368)]
# test2 = [(16512, 4432408346624), (16512, 4432674684928), (16512, 4432406249473), (16512, 4432406282240), (16512, 13228499271680), (16512, 4501125726208), (16512, 4501125726208), (16512, 4432406249728)]
# test3 = [(32768, 16512),]
# for elem in test2:
#     x = elem[0] ^ elem[1]
#     x &= b.board_mask
#     b.print_bitboard(x)


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