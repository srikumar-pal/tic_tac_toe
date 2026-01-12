def get_valid_move(player, board):
    while True:
        try:
            move = int(input(f"Player {player}, choose position (1-9): "))
            if move < 1 or move > 9:
                print("❌ Choose between 1 and 9.")
                continue
            if board[move - 1] != " ":
                print("❌ Position already taken.")
                continue
            return move - 1
        except ValueError:
            print("❌ Please enter a number.")
