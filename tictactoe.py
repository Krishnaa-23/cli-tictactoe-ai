#!/usr/bin/env python3
"""
CLI Tic-Tac-Toe with unbeatable Minimax AI (alpha-beta pruning).
Save as tictactoe.py and run: python tictactoe.py
"""

from typing import List, Optional, Tuple
import math
import random

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  
    (0, 4, 8), (2, 4, 6)              
]

def fresh_board() -> List[str]:
    return [" "] * 9

def print_board(board: List[str]) -> None:
    """Prints the board with indices for empty squares to guide input."""
    def cell_repr(i):
        return board[i] if board[i] != " " else str(i+1)
    row_sep = "\n---+---+---\n"
    rows = []
    for r in range(3):
        idx = 3*r
        rows.append(f" {cell_repr(idx)} | {cell_repr(idx+1)} | {cell_repr(idx+2)} ")
    print("\n" + row_sep.join(rows) + "\n")

def check_winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if there's a winner, 'D' for draw, or None if game ongoing."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "D"  # draw
    return None

def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == " "]

def other(player: str) -> str:
    return "O" if player == "X" else "X"

def minimax(board: List[str], player: str, maximizing_player: str,
            alpha: float = -math.inf, beta: float = math.inf) -> Tuple[float, Optional[int]]:
    """
    Returns (score, move_index).
    score: +1 for maximizing_player win, -1 for loss, 0 for draw.
    maximizing_player: the AI's symbol (so score is from AI perspective).
    'player' is the current player to move.
    """
    winner = check_winner(board)
    if winner is not None:
        if winner == "D":
            return 0, None
        return (1 if winner == maximizing_player else -1), None

    moves = available_moves(board)
    best_move: Optional[int] = None

    if player == maximizing_player:
        value = -math.inf
        for m in moves:
            board[m] = player
            score, _ = minimax(board, other(player), maximizing_player, alpha, beta)
            board[m] = " "
            if score > value:
                value = score
                best_move = m
            alpha = max(alpha, value)
            if alpha >= beta:
                break  
        return value, best_move
    else:
        value = math.inf
        for m in moves:
            board[m] = player
            score, _ = minimax(board, other(player), maximizing_player, alpha, beta)
            board[m] = " "
            if score < value:
                value = score
                best_move = m
            beta = min(beta, value)
            if alpha >= beta:
                break  
        return value, best_move

def best_move_for_ai(board: List[str], ai_symbol: str) -> int:
    """Return index (0..8) of best move for the AI. If multiple best moves, pick randomly among them."""
    moves = available_moves(board)
    best_score = -math.inf
    best_moves: List[int] = []
    for m in moves:
        board[m] = ai_symbol
        score, _ = minimax(board, other(ai_symbol), ai_symbol)
        board[m] = " "
        if score > best_score:
            best_score = score
            best_moves = [m]
        elif score == best_score:
            best_moves.append(m)
    return random.choice(best_moves)

def human_turn(board: List[str], symbol: str) -> None:
    """Prompts user for a move and updates board in place."""
    moves = available_moves(board)
    while True:
        try:
            user = input(f"Player {symbol}, enter your move (1-9): ").strip()
            if user.lower() in ("q", "quit", "exit"):
                print("Exiting game.")
                exit(0)
            idx = int(user) - 1
            if idx not in range(9):
                print("Invalid cell number. Choose 1-9.")
                continue
            if board[idx] != " ":
                print("Cell already taken. Pick another.")
                continue
            board[idx] = symbol
            break
        except ValueError:
            print("Please enter a number 1-9 (or 'q' to quit).")

def choose_symbol() -> Tuple[str, str]:
    """Allow human to choose symbol. Returns (human_symbol, ai_symbol)."""
    while True:
        s = input("Choose your symbol (X/O). X goes first. [Default X]: ").strip().upper()
        if s == "":
            s = "X"
        if s in ("X", "O"):
            human = s
            ai = other(human)
            return human, ai
        print("Invalid choice; enter X or O.")

def choose_mode() -> str:
    while True:
        print("Select mode:\n1) Human vs AI\n2) Human vs Human")
        ch = input("Choice [1]: ").strip()
        if ch == "" or ch == "1":
            return "hva"
        if ch == "2":
            return "hvh"
        print("Invalid. Enter 1 or 2.")

def choose_first(human_symbol: str) -> str:
    """Ask who goes first when human vs ai."""
    while True:
        ch = input("Who goes first? (H)uman or (A)I. [Default: whoever is X]: ").strip().lower()
        if ch == "":
            # default: X starts
            return "human" if human_symbol == "X" else "ai"
        if ch in ("h", "human"):
            return "human"
        if ch in ("a", "ai"):
            return "ai"
        print("Enter H for human or A for AI.")

def play():
    print("=== Tic-Tac-Toe (CLI) with Unbeatable AI ===")
    mode = choose_mode()
    board = fresh_board()

    if mode == "hvh":
        # Human vs Human loop
        current = "X"  # X always starts
        while True:
            print_board(board)
            human_turn(board, current)
            winner = check_winner(board)
            if winner:
                print_board(board)
                if winner == "D":
                    print("It's a draw!")
                else:
                    print(f"Player {winner} wins!")
                break
            current = other(current)
        return

    # Human vs AI mode
    human_symbol, ai_symbol = choose_symbol()
    first = choose_first(human_symbol)
    current = "X"  # X goes first by convention
    # Map who actually moves when current == 'X' or 'O'
    while True:
        player_type = None  # "human" or "ai"
        if current == human_symbol:
            player_type = "human"
        else:
            player_type = "ai"

        print_board(board)

        if player_type == "human":
            human_turn(board, current)
        else:
            print(f"AI ({ai_symbol}) is thinking...")
            move = best_move_for_ai(board, ai_symbol)
            board[move] = ai_symbol
            print(f"AI played in cell {move+1}.")

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "D":
                print("It's a draw!")
            else:
                print(f"{'AI' if winner==ai_symbol else 'Player'} ({winner}) wins!")
            break

        current = other(current)


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
