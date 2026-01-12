import tkinter as tk
from tkinter import messagebox, simpledialog

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Tournament Mode")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f4")

        self.human = "X"
        self.ai = "O"

        # Player name
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:")
        if not self.player_name:
            self.player_name = "Player"

        # 🔹 Custom rounds
        self.total_rounds = simpledialog.askinteger(
            "Rounds",
            "How many rounds do you want to play?",
            minvalue=1,
            maxvalue=50
        )
        if not self.total_rounds:
            self.total_rounds = 5  # default

        self.current_round = 1

        self.ai_name = "Computer (AI)"

        self.human_score = 0
        self.ai_score = 0
        self.draws = 0

        self.current_player = self.human
        self.board = [" " for _ in range(9)]
        self.buttons = []

        self.create_scoreboard()
        self.create_buttons()

    # ---------- UI ----------
    def create_scoreboard(self):
        self.score_label = tk.Label(
            self.root,
            text=self.get_score_text(),
            font=("Arial", 12, "bold"),
            bg="#f4f4f4"
        )
        self.score_label.grid(row=0, column=0, columnspan=3, pady=10)

    def get_score_text(self):
        return (
            f"Round {self.current_round}/{self.total_rounds}   |   "
            f"{self.player_name} (X): {self.human_score}   |   "
            f"{self.ai_name} (O): {self.ai_score}   |   "
            f"Draws: {self.draws}"
        )

    def update_scoreboard(self):
        self.score_label.config(text=self.get_score_text())

    def create_buttons(self):
        for i in range(9):
            btn = tk.Button(
                self.root,
                text=" ",
                font=("Arial", 26, "bold"),
                width=5,
                height=2,
                bg="white",
                command=lambda i=i: self.human_move(i)
            )
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    # ---------- Game ----------
    def human_move(self, index):
        if self.board[index] == " " and self.current_player == self.human:
            self.make_move(index, self.human)
            if not self.check_game_over(self.human):
                self.root.after(200, self.ai_move)

    def ai_move(self):
        move = self.get_best_move()
        self.make_move(move, self.ai)
        self.check_game_over(self.ai)

    def make_move(self, index, player):
        self.board[index] = player
        color = "#1e90ff" if player == self.human else "#e63946"
        self.buttons[index].config(text=player, fg=color)
        self.current_player = self.human if player == self.ai else self.ai

    # ---------- Round End ----------
    def check_game_over(self, player):
        if self.get_winner(player):
            if player == self.human:
                self.human_score += 1
                winner = self.player_name
            else:
                self.ai_score += 1
                winner = self.ai_name

            self.end_round(f"{winner} wins this round!")
            return True

        if " " not in self.board:
            self.draws += 1
            self.end_round("This round is a Draw!")
            return True

        return False

    def end_round(self, msg):
        messagebox.showinfo("Round Over", msg)
        self.current_round += 1

        if self.current_round > self.total_rounds:
            self.show_final_result()
        else:
            self.reset_board()
            self.update_scoreboard()

    def show_final_result(self):
        if self.human_score > self.ai_score:
            result = f"🏆 {self.player_name} wins the tournament!"
        elif self.ai_score > self.human_score:
            result = "🤖 Computer wins the tournament!"
        else:
            result = "🤝 Tournament Draw!"

        messagebox.showinfo("Game Over", result)
        self.root.destroy()

    def reset_board(self):
        self.board = [" " for _ in range(9)]
        self.current_player = self.human
        for btn in self.buttons:
            btn.config(text=" ", bg="white")

    # ---------- Win Check ----------
    def get_winner(self, player):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in wins)

    # ---------- MINIMAX ----------
    def minimax(self, board, is_max):
        if self.static_win(board, self.ai):
            return 1
        if self.static_win(board, self.human):
            return -1
        if " " not in board:
            return 0

        if is_max:
            best = -100
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.ai
                    best = max(best, self.minimax(board, False))
                    board[i] = " "
            return best
        else:
            best = 100
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.human
                    best = min(best, self.minimax(board, True))
                    board[i] = " "
            return best

    def get_best_move(self):
        best_score = -100
        move = 0
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.ai
                score = self.minimax(self.board, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def static_win(self, board, player):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(board[i] == player for i in combo) for combo in wins)

# Run App
root = tk.Tk()
TicTacToeAI(root)
root.mainloop()
