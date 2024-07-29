
# **Connect Four with Bombs and AI**

## **Description**

This is a Python implementation of the classic Connect Four game with additional features such as bombs and AI opponents. The game allows two players to drop pieces into a vertical grid and aims to connect four pieces in a row vertically, horizontally, or diagonally. Players can use bombs to clear columns and proximity bombs to clear adjacent cells. The AI opponent uses different difficulty levels based on the Alpha-Beta Pruning algorithm.

## **Features**

- **Standard Connect Four Gameplay**: Two players take turns to drop pieces into the grid.
- **Bombs**: Each player has 2 bombs to clear a column of pieces.
- **Proximity Bombs**:For beginner and moderate each player has 0 proximity bombs for hard level each player has 2 to clear adjacent cells.
- **AI Opponent**: The game features an AI opponent with three difficulty levels:
  - Beginner
  - Moderate
  - Hard
- **Animated Piece Drops**: Visual animation for piece drops and bomb effects.

## **Installation**

1. Make sure you have Python installed on your system.
2. Install the Tkinter library if it's not already installed:
   ```sh
   pip install python-tk
   ```
3. Download the game script.

## **How to Play**

1. Run the game script:
   ```sh
   python connect_four_with_bombs.py
   ```
2. A window will pop up asking you to select the difficulty level.
3. Select the difficulty level:
   - Beginner
   - Moderate
   - Hard
4. The main game window will appear with a 6x7 grid.
5. Player 1 (red) starts the game. Use the "Drop" buttons at the top to drop pieces into the columns.
6. To use a bomb, click the "Bomb" button under the desired column.
7. To use a proximity bomb, click the "Prox Bomb" button, then click on the grid to select the target cell.
8. The AI will make moves based on the selected difficulty level.
9. The game ends when one player connects four pieces in a row.

## **Files**

- `connect_four_with_bombs.py`: The main script to run the game.

## **Code Overview**

The main class `ConnectFour` handles the game logic, including:

- **Initialization**: Sets up the game board, canvas, and buttons.
- **Drawing the Board**: Draws the game board and pieces.
- **Piece Drop**: Handles dropping pieces into columns and checking for wins.
- **Bomb Usage**: Handles the logic for standard bombs and proximity bombs.
- **AI Logic**: Implements the AI opponent using Alpha-Beta Pruning.

### **Main Functions**

- `draw_board()`: Draws the game board on the canvas.
- `drop_piece(col)`: Drops a piece into the specified column.
- `check_winner(row, col)`: Checks if the current player has won the game.
- `use_bomb(col)`: Uses a bomb to clear the specified column.
- `activate_proximity_mode()`: Activates proximity bomb mode.
- `highlight_proximity_bomb(row, col)`: Highlights the cells affected by the proximity bomb.
- `select_proximity_bomb(row, col)`: Clears the cells affected by the proximity bomb.
- `ai_move()`: Handles the AI move based on the difficulty level.
- `alpha_beta(board, depth, alpha, beta, maximizing_player)`: Alpha-Beta Pruning algorithm for AI decision-making.
- `evaluate_board(board)`: Evaluates the game board for the AI.

### **Entry Point**

The game starts by showing the difficulty menu and then initializes the main game window:
```python
if __name__ == "__main__":
    show_difficulty_menu()
```

## **License**

This project is open-source and available under the MIT License.
