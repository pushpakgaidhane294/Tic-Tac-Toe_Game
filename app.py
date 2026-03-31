import streamlit as st
import numpy as np
import random
import pickle
import os

# Q-table
Q = {}

# Hyperparameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

# Initialize board
def init_board():
    return [" " for _ in range(9)]

# Convert board to string (state)
def get_state(board):
    return "".join(board)

# Available moves
def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]

# Check winner
def check_winner(board):
    win_states = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for state in win_states:
        if board[state[0]] == board[state[1]] == board[state[2]] != " ":
            return board[state[0]]
    if " " not in board:
        return "Draw"
    return None

# Choose action
def choose_action(state, moves):
    if random.uniform(0,1) < epsilon:
        return random.choice(moves)
    qs = [Q.get((state, a), 0) for a in moves]
    return moves[np.argmax(qs)]

# Update Q-value
def update_q(state, action, reward, next_state, next_moves):
    old_q = Q.get((state, action), 0)
    future_q = max([Q.get((next_state, a), 0) for a in next_moves], default=0)
    Q[(state, action)] = old_q + alpha * (reward + gamma * future_q - old_q)

# Train agent
def train(episodes=5000):
    global Q
    for _ in range(episodes):
        board = init_board()
        state = get_state(board)

        while True:
            moves = available_moves(board)
            action = choose_action(state, moves)
            board[action] = "X"

            winner = check_winner(board)
            next_state = get_state(board)

            if winner:
                reward = 1 if winner == "X" else 0
                update_q(state, action, reward, next_state, [])
                break

            # Opponent random move
            opp_move = random.choice(available_moves(board))
            board[opp_move] = "O"

            winner = check_winner(board)
            next_state2 = get_state(board)

            if winner:
                reward = -1 if winner == "O" else 0
                update_q(state, action, reward, next_state2, [])
                break

            next_moves = available_moves(board)
            update_q(state, action, 0, next_state2, next_moves)

            state = next_state2

    # Save Q-table
    with open("q_table.pkl", "wb") as f:
        pickle.dump(Q, f)

# Load Q-table
def load_q():
    global Q
    if os.path.exists("q_table.pkl"):
        with open("q_table.pkl", "rb") as f:
            Q = pickle.load(f)

# AI move
def ai_move(board):
    state = get_state(board)
    moves = available_moves(board)
    qs = [Q.get((state, a), 0) for a in moves]
    return moves[np.argmax(qs)]

# Streamlit UI
st.title("🤖 Tic-Tac-Toe RL Agent")

if "board" not in st.session_state:
    st.session_state.board = init_board()

load_q()

# Train button
if st.button("Train AI"):
    train(5000)
    st.success("Training Complete!")

# Display board
cols = st.columns(3)
for i in range(9):
    if cols[i%3].button(st.session_state.board[i], key=i):
        if st.session_state.board[i] == " ":
            st.session_state.board[i] = "X"

            winner = check_winner(st.session_state.board)
            if not winner:
                ai = ai_move(st.session_state.board)
                st.session_state.board[ai] = "O"

            winner = check_winner(st.session_state.board)
            if winner:
                st.write(f"🏆 Result: {winner}")

# Reset button
if st.button("Reset Game"):
    st.session_state.board = init_board()
