from board import Board


empty = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         ]

arr1 = [[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,1,2,2,2,0],
        [0,1,1,2,1,1,2],
        ]

arr2 = [[0,0,0,2,0,0,0],
        [0,0,0,2,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,2,2,0,0],
        [0,0,1,2,1,1,0],
        ]

b = Board(arr1)
print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
print(b.gen_valid_moves())
b.print_bitboard_p1()
b.print_bitboard_p2()

# b = Board(arr2)
# print(f"player 1: {b.player1}, player 2: {b.player2}, height: {b.height}, counter: {b.counter}")
# print(b.height)
# b.print_bitboard_p1()
# b.print_bitboard_p2()

# b = Board(empty)
# # print(b.player1, b.player2)
# print(b.height)
# print(b.gen_valid_moves())
# # b.print_bitboard_p1()
# # b.print_bitboard_p2()