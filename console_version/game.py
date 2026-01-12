from console_version.board import print_board, reset_board
from input_utils import get_valid_move

def check_winner(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_draw(board):
    return " " not in board

def play_game():
    board = reset_board()
    current_player = "X"

    print("\n🎮 Tic Tac Toe Started")

    while True:
        print_board(board)
        move = get_valid_move(current_player, board)
        board[move] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"🏆 Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("🤝 It's a Draw!")
            break

        current_player = "O" if current_player == "X" else "X"
