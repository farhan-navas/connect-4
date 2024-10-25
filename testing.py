from board import Board

arr1 = [
    [0,0,0,0,0,0,0],  # Row 0 (Top)
    [0,0,0,0,0,0,0],  # Row 1
    [0,0,0,0,0,0,0],  # Row 2
    [0,0,2,2,2,0,0],  # Row 3
    [0,0,1,2,1,0,0],  # Row 4
    [0,2,1,1,1,0,0],  # Row 5 (Bottom)
]

arr2 = [[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,2,0,0,0],
        [1,0,0,2,2,2,0],
        [1,1,0,2,1,1,0],
        ]

b = Board(arr2)
print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
# b.print_bitboard(b.player1)
# b.print_bitboard(b.player2)
print(b.height)
print("valid moves: ", b.gen_valid_moves())
print("non-losing moves: ", b.non_losing_moves())

# b = Board(arr1)
# print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
# print("valid moves: ", b.gen_valid_moves())
# print("non-losing moves: ", b.non_losing_moves())

# b = Board(empty)
# # print(b.player1, b.player2)
# print(b.height)
# print(b.gen_valid_moves())