import tkinter as tk
from tkinter import messagebox

e = ' '
x = 'X'
o = 'O'


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.board = [[e, e, e],
                      [e, e, e],
                      [e, e, e]]

        self.buttons = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('normal', 20), width=6, height=3,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.game()

    def show_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.board[i][j]

    def on_button_click(self, row, col):
        if self.board[row][col] == e:
            self.board[row][col] = x
            self.show_board()
            result, winner = self.check_winner()
            if result:
                self.end_game(winner)
            else:
                self.ai_move()
                result, winner = self.check_winner()
                if result:
                    self.end_game(winner)
        else:
            messagebox.showinfo(
                "Invalid Move", "Cell already occupied. Try again.")

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == e:
                    return False
        return True

    def check_winner(self):
        # Check rows
        for row in self.board:
            if all(cell == row[0] and cell != e for cell in row):
                return True, row[0]

        # Check columns
        for col in range(3):
            if all(self.board[row][col] == self.board[0][col] and self.board[row][col] != e for row in range(3)):
                return True, self.board[0][col]

        # Check diagonals
        if all(self.board[i][i] == self.board[0][0] and self.board[i][i] != e for i in range(3)):
            return True, self.board[0][0]

        if (self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != e):
            return True, self.board[0][2]

        return False, None

    def ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == e:
                    self.board[i][j] = o
                    score = self.minimax(0, False)
                    self.board[i][j] = e

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.board[best_move[0]][best_move[1]] = o
            self.show_board()

    def minimax(self, depth, is_maximizing):
        result, winner = self.check_winner()
        if result:
            return 1 if winner == o else -1
        elif self.full_board():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == e:
                        self.board[i][j] = o
                        eval = self.minimax(depth + 1, False)
                        self.board[i][j] = e
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == e:
                        self.board[i][j] = x
                        eval = self.minimax(depth + 1, True)
                        self.board[i][j] = e
                        min_eval = min(min_eval, eval)
            return min_eval

    def end_game(self, winner):
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie.")

    def game(self):
        self.show_board()
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
