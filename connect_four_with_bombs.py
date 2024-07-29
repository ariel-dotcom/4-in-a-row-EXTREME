import tkinter as tk
from tkinter import messagebox
import random
import copy

class ConnectFour:
    def __init__(self, root, rows=6, columns=7, difficulty=4):
        self.root = root
        self.root.title("4 in a Row")
        self.rows = rows
        self.columns = columns
        self.board = [[0] * self.columns for _ in range(self.rows)]  # Initialize the board with 0s
        self.current_player = 1  # Player 1 starts
        self.bombs = [2, 2]  # Each player has 2 bombs
        self.proximity_bombs = [2, 2]  # Each player has 2 proximity bombs
        self.proximity_mode = False  # Initially, proximity mode is off
        self.difficulty = difficulty  # Set difficulty level
        self.highlighted_column = -1  # No column is highlighted initially
        self.highlighted_cells = []  # No cells are highlighted initially

        self.cell_size = 60  # Size of each cell in the grid
        self.canvas = tk.Canvas(root, width=self.columns * self.cell_size, height=self.rows * self.cell_size, bg="blue")
        self.canvas.grid(row=3, column=0, columnspan=self.columns)

        self.turn_label = tk.Label(root, text="Player 1's Turn", bg="red", font=("Arial", 16), fg="white")
        self.turn_label.grid(row=0, column=0, columnspan=self.columns, sticky="nsew")

        self.bomb_buttons_frame = tk.Frame(root)
        self.bomb_buttons_frame.grid(row=1, column=0, columnspan=self.columns, sticky="ew")

        # Create bomb buttons for each column
        self.bomb_buttons = [
            tk.Button(self.bomb_buttons_frame, text="Bomb", command=lambda col=col: self.highlight_column_bomb(col),
                      bg="#8e3e41", fg="white", font=("Arial", 13)) for col in range(self.columns)]
        for col, button in enumerate(self.bomb_buttons):
            button.grid(row=0, column=col, padx=3, pady=5, sticky="ew")

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.grid(row=2, column=0, columnspan=self.columns, sticky="ew")

        # Create drop buttons for each column
        self.buttons = [
            tk.Button(self.buttons_frame, text="Drop", command=lambda col=col: self.drop_piece(col), bg="#3e8e41",
                      fg="white", font=("Arial", 14)) for col in range(self.columns)]
        for col, button in enumerate(self.buttons):
            button.grid(row=0, column=col, padx=1, pady=5, sticky="ew")

        # Create a button to activate proximity mode
        self.proximity_bomb_button = tk.Button(root, text="Prox Bomb", command=self.activate_proximity_mode,
                                               bg="#8e7e41", fg="white", font=("Arial", 12))
        self.proximity_bomb_button.grid(row=4, column=0, columnspan=self.columns, pady=5, sticky="ew")

        self.canvas.bind("<Button-1>", self.canvas_click_handler)

        self.root.bind("<Configure>", self.resize_handler)
        self.draw_board()

    # Handler for resizing the window
    def resize_handler(self, event):
        width = self.columns * self.cell_size
        height = self.rows * self.cell_size
        self.canvas.config(width=width, height=height)

    # Function to draw the board
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white"
                if self.board[row][col] == 1:
                    color = "red"
                elif self.board[row][col] == 2:
                    color = "yellow"
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="blue")

        if self.highlighted_column != -1:
            self.highlight_column(self.highlighted_column)
        if self.highlighted_cells:
            self.highlight_cells(self.highlighted_cells)

    # Function to highlight a column
    def highlight_column(self, col):
        for row in range(self.rows):
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=3)

    # Function to highlight specific cells
    def highlight_cells(self, cells):
        for row, col in cells:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=3)

    # Function to disable all buttons
    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED, disabledforeground=button.cget('fg'))
        for button in self.bomb_buttons:
            button.config(state=tk.DISABLED, disabledforeground=button.cget('fg'))
        self.proximity_bomb_button.config(state=tk.DISABLED, disabledforeground=self.proximity_bomb_button.cget('fg'))

    # Function to enable all buttons
    def enable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        for button in self.bomb_buttons:
            button.config(state=tk.NORMAL)
        self.proximity_bomb_button.config(state=tk.NORMAL)

    # Function to drop a piece in a column
    def drop_piece(self, col):
        if self.proximity_mode:
            return
        # Check if the column is full
        if self.board[0][col] != 0:
            messagebox.showinfo("Invalid Move", "This column is full. Please choose another column.")
            self.enable_buttons()
            return

        self.disable_buttons()
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.animate_piece_drop(row, col, self.current_player)
                self.board[row][col] = self.current_player
                self.draw_board()
                self.root.after(500, self.check_game_state, row, col)
                return

    # Function to animate the dropping of a piece
    def animate_piece_drop(self, row, col, player):
        color = "red" if player == 1 else "yellow"
        for i in range(row + 1):
            x1 = col * self.cell_size
            y1 = i * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="blue")
            self.canvas.update()
            self.canvas.after(50)
            if i < row:
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="blue")

    # Function to check the game state after a piece is dropped
    def check_game_state(self, row, col):
        if self.check_winner(row, col):
            self.highlight_winning_line(row, col)
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
        else:
            self.current_player = 3 - self.current_player
            self.update_turn_label()
            if self.current_player == 2:
                self.root.after(500, self.ai_move)
            else:
                self.enable_buttons()

    # Function to highlight a column for bomb usage
    def highlight_column_bomb(self, col):
        self.highlighted_column = col
        self.draw_board()
        self.root.after(1000, self.use_bomb, col)

    # Function to use a bomb on a column
    def use_bomb(self, col):
        if self.proximity_mode:
            return
        self.disable_buttons()
        if self.bombs[self.current_player - 1] > 0:
            for row in range(self.rows):
                self.board[row][col] = 0
            self.bombs[self.current_player - 1] -= 1
            self.current_player = 3 - self.current_player
            self.update_turn_label()
            self.highlighted_column = -1
            if self.current_player == 2:
                self.root.after(500, self.ai_move)
            else:
                self.enable_buttons()
        else:
            messagebox.showinfo("No Bombs", f"Player {self.current_player} has no bombs left!")
            self.enable_buttons()
        self.draw_board()

    # Function to activate proximity mode
    def activate_proximity_mode(self):
        if self.proximity_bombs[self.current_player - 1] > 0:
            self.proximity_mode = True
        else:
            messagebox.showinfo("No Proximity Bombs", f"Player {self.current_player} has no proximity bombs left!")

    # Handler for canvas click events
    def canvas_click_handler(self, event):
        if self.proximity_mode:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if 0 <= row < self.rows and 0 <= col < self.columns:
                self.highlight_proximity_bomb(row, col)
                self.select_proximity_bomb(row, col)

    # Function to highlight cells for proximity bomb usage
    def highlight_proximity_bomb(self, row, col):
        self.highlighted_cells = [(row + dr, col + dc) for dr in range(-1, 2) for dc in range(-1, 2) if
                                  0 <= row + dr < self.rows and 0 <= col + dc < self.columns]
        self.draw_board()

    # Function to use a proximity bomb
    def select_proximity_bomb(self, row, col):
        if not self.proximity_mode:
            return
        self.disable_buttons()
        self.clear_adjacent_pieces(row, col)
        self.proximity_bombs[self.current_player - 1] -= 1
        self.proximity_mode = False
        self.adjust_board_with_animation()
        self.highlighted_cells = []
        # Add delay before checking for a win
        self.root.after(500, self.check_board_for_winner_after_prox)

    # Function to check the board for a winner after proximity bomb usage
    def check_board_for_winner_after_prox(self):
        self.canvas.update()
        self.canvas.after(500)
        # Check for a winner for both players
        if self.check_board_for_winner():
            return
        self.current_player = 3 - self.current_player
        self.update_turn_label()
        if self.current_player == 2:
            self.root.after(500, self.ai_move)
        else:
            self.enable_buttons()

    # Function to check the entire board for a winner
    def check_board_for_winner(self):
        for col in range(self.columns):
            for row in range(self.rows):
                if self.board[row][col] != 0:
                    if self.check_winner(row, col):
                        self.highlight_winning_line(row, col)
                        messagebox.showinfo("Game Over", f"Player {self.board[row][col]} wins!")
                        self.reset_game()
                        return True
        return False

    # Function to clear adjacent pieces for proximity bomb usage
    def clear_adjacent_pieces(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.board[row][col] = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.columns:
                self.board[r][c] = 0
        self.draw_board()

    # Function to adjust the board with animation after using a proximity bomb
    def adjust_board_with_animation(self):
        for col in range(self.columns):
            empty_slots = []
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] == 0:
                    empty_slots.append(row)
                elif empty_slots:
                    empty_row = empty_slots.pop(0)
                    self.animate_piece_fall(row, empty_row, col, self.board[row][col])
                    self.board[empty_row][col] = self.board[row][col]
                    self.board[row][col] = 0
                    empty_slots.append(row)
        self.draw_board()

    # Function to animate the fall of a piece
    def animate_piece_fall(self, start_row, end_row, col, player):
        color = "red" if player == 1 else "yellow"
        for i in range(start_row, end_row + 1):
            x1 = col * self.cell_size
            y1 = i * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="blue")
            self.canvas.update()
            self.canvas.after(50)
            if i < end_row:
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="blue")

    # Function to check if a player has won
    def check_winner(self, row, col):
        def count_connected(r_step, c_step):
            r, c = row, col
            count = 0
            while 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == self.board[row][col]:
                count += 1
                r += r_step
                c += c_step
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for r_step, c_step in directions:
            if count_connected(r_step, c_step) + count_connected(-r_step, -c_step) - 1 >= 4:
                self.winning_coords = self.get_winning_coords(row, col, r_step, c_step)
                return True
        return False

    # Function to get the coordinates of the winning line
    def get_winning_coords(self, row, col, r_step, c_step):
        coords = [(row, col)]
        # Get coordinates in the positive direction
        r, c = row + r_step, col + c_step
        while 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == self.board[row][col]:
            coords.append((r, c))
            r += r_step
            c += c_step
        # Get coordinates in the negative direction
        r, c = row - r_step, col - c_step
        while 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == self.board[row][col]:
            coords.insert(0, (r, c))
            r -= r_step
            c -= c_step
        return coords

    # Function to highlight the winning line
    def highlight_winning_line(self, row, col):
        for r, c in self.winning_coords:
            x1 = c * self.cell_size
            y1 = r * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill="green", outline="blue")

    # Function to update the turn label
    def update_turn_label(self):
        self.turn_label.config(text=f"Player {self.current_player}'s Turn",
                               bg="red" if self.current_player == 1 else "yellow")

    # Function to reset the game
    def reset_game(self):
        self.board = [[0] * self.columns for _ in range(self.rows)]
        self.current_player = 1
        self.bombs = [2, 2]
        self.proximity_bombs = [2, 2]
        self.proximity_mode = False
        self.highlighted_column = -1
        self.highlighted_cells = []
        self.draw_board()
        self.update_turn_label()
        self.enable_buttons()

    # Function to make an AI move
    def ai_move(self):
        if self.current_player == 2:
            if self.difficulty == 2:
                self.easy_ai()
            elif self.difficulty == 4:
                self.moderate_ai()
            elif self.difficulty == 6:
                self.hard_ai()

    # Function for easy AI moves
    def easy_ai(self):
        if random.random() < 0.5 and self.bombs[1] > 0:
            self.highlight_column_bomb_ai()
        else:
            self.make_move_ai(2)

    # Function for moderate AI moves
    def moderate_ai(self):
        if random.random() < 0.3 and self.bombs[1] > 0:
            self.highlight_column_bomb_ai()
        else:
            self.make_move_ai(4)

    # Function for hard AI moves
    def hard_ai(self):
        if self.can_win_with_proximity_bomb():
            self.highlight_proximity_bomb_ai()
        elif random.random() < 0.2 and self.bombs[1] > 0:
            self.highlight_column_bomb_ai()
        else:
            self.make_move_ai(6)

    # Function to highlight a column for AI bomb usage
    def highlight_column_bomb_ai(self):
        col = random.randint(0, self.columns - 1)
        if any(self.board[row][col] != 0 for row in range(self.rows)):
            self.highlighted_column = col
            self.draw_board()
            self.root.after(1000, self.use_bomb_ai, col)
        else:
            self.make_move_ai(6)

    # Function for AI to use a bomb
    def use_bomb_ai(self, col):
        if self.proximity_mode:
            return
        if self.bombs[1] > 0:
            for row in range(self.rows):
                self.board[row][col] = 0
            self.bombs[1] -= 1
            self.highlighted_column = -1
        self.draw_board()
        self.root.after(500, self.check_board_for_winner_after_prox)

    # Function for AI to highlight proximity bomb
    def highlight_proximity_bomb_ai(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.proximity_bombs[1] > 0 and any(
                        self.board[row + dr][col + dc] != 0 for dr in range(-1, 2) for dc in range(-1, 2) if
                        0 <= row + dr < self.rows and 0 <= col + dc < self.columns):
                    temp_board = copy.deepcopy(self.board)
                    self.clear_adjacent_pieces_for_check(temp_board, row, col)
                    if self.check_for_ai_win(temp_board):
                        self.highlight_proximity_bomb(row, col)
                        self.root.after(1000, self.select_proximity_bomb_ai, row, col)
                        return
        self.make_move_ai(6)

    # Function for AI to select proximity bomb
    def select_proximity_bomb_ai(self, row, col):
        self.clear_adjacent_pieces(row, col)
        self.proximity_bombs[1] -= 1
        self.adjust_board_with_animation()
        self.highlighted_cells = []
        # Add delay before checking for a win
        self.root.after(500, self.check_board_for_winner_after_prox)

    # Function to clear adjacent pieces for checking
    def clear_adjacent_pieces_for_check(self, board, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        board[row][col] = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.columns:
                board[r][c] = 0

    # Function to check if AI can win with a proximity bomb
    def can_win_with_proximity_bomb(self):
        for row in range(self.rows):
            for col in range(self.columns):
                temp_board = copy.deepcopy(self.board)
                self.clear_adjacent_pieces_for_check(temp_board, row, col)
                if self.check_for_ai_win(temp_board):
                    return True
        return False

    # Function to check if AI can win
    def check_for_ai_win(self, board):
        for col in range(self.columns):
            for row in range(self.rows):
                if board[row][col] == 0:
                    continue
                if self.check_winner_with_board(board, row, col, 2):
                    return True
        return False

    # Function to check if a player has won with a given board
    def check_winner_with_board(self, board, row, col, player):
        def count_connected_with_board(board, r_step, c_step):
            r, c = row, col
            count = 0
            while 0 <= r < self.rows and 0 <= c < self.columns and board[r][c] == player:
                count += 1
                r += r_step
                c += c_step
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for r_step, c_step in directions:
            if count_connected_with_board(board, r_step, c_step) + count_connected_with_board(board, -r_step,
                                                                                              -c_step) - 1 >= 4:
                return True
        return False

    # Function for AI to make a move using alpha-beta pruning
    def make_move_ai(self, depth):
        _, col = self.alpha_beta(self.board, depth, float('-inf'), float('inf'), True)
        if col is not None:
            self.drop_piece(col)

    # Alpha-beta pruning algorithm
    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        valid_moves = [col for col in range(self.columns) if board[0][col] == 0]
        if depth == 0 or not valid_moves:
            return self.evaluate_board(board), None
        if maximizing_player:
            max_eval = float('-inf')
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                self.make_move(temp_board, col, 2)
                eval, _ = self.alpha_beta(temp_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_col = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_col
        else:
            min_eval = float('inf')
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                self.make_move(temp_board, col, 1)
                eval, _ = self.alpha_beta(temp_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_col = col
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_col

    # Function to make a move on the board
    def make_move(self, board, col, player):
        for row in range(self.rows - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = player
                break

    # Function to evaluate the board
    def evaluate_board(self, board):
        score = 0

        # Score center column
        center_array = [int(board[row][self.columns // 2]) for row in range(self.rows)]
        center_count = center_array.count(2)
        score += center_count * 3

        # Score horizontal, vertical, and diagonal lines
        for row in range(self.rows):
            for col in range(self.columns):
                if board[row][col] == 2:
                    score += self.score_position(board, row, col, 2)
                elif board[row][col] == 1:
                    score -= self.score_position(board, row, col, 1)

        return score

    # Function to score a position
    def score_position(self, board, row, col, player):
        score = 0
        opponent = 1 if player == 2 else 2

        # Scoring directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for direction in directions:
            score += self.score_line(board, row, col, player, direction)

        return score

    # Function to score a line
    def score_line(self, board, row, col, player, direction):
        score = 0
        line = []
        for i in range(-3, 4):
            r = row + i * direction[0]
            c = col + i * direction[1]
            if 0 <= r < self.rows and 0 <= c < self.columns:
                line.append(board[r][c])
            else:
                line.append(None)

        # Check line for scoring
        for i in range(len(line) - 3):
            window = line[i:i + 4]
            score += self.evaluate_window(window, player)

        return score

    # Function to evaluate a window of 4 cells
    def evaluate_window(self, window, player):
        score = 0
        opponent = 1 if player == 2 else 2

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 5

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 80

        return score


# Function to show the difficulty menu
def show_difficulty_menu():
    difficulty_window = tk.Tk()
    difficulty_window.title("Select Difficulty Level")

    tk.Label(difficulty_window, text="Select Difficulty Level:", font=("Arial", 14)).pack(pady=5)

    tk.Button(difficulty_window, text="Beginner", command=lambda: start_game(difficulty_window, 2), bg="lightgreen",
              font=("Arial", 14)).pack(pady=5)
    tk.Button(difficulty_window, text="Moderate", command=lambda: start_game(difficulty_window, 4), bg="lightblue",
              font=("Arial", 14)).pack(pady=5)
    tk.Button(difficulty_window, text="Hard", command=lambda: start_game(difficulty_window, 6), bg="red",
              font=("Arial", 14)).pack(pady=5)

    difficulty_window.mainloop()


# Function to start the game
def start_game(difficulty_window, difficulty):
    difficulty_window.destroy()
    root = tk.Tk()
    game = ConnectFour(root, rows=6, columns=7, difficulty=difficulty)
    root.mainloop()


if __name__ == "__main__":
    show_difficulty_menu()
