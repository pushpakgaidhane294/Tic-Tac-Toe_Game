import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
.cell {
    height: 80px;
    width: 80px;
    font-size: 30px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- INIT ----------
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.turn = "X"
    st.session_state.winner = None

# ---------- FUNCTIONS ----------
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for i,j,k in wins:
        if board[i] == board[j] == board[k] and board[i] != "":
            return board[i]
    if "" not in board:
        return "Draw"
    return None

def ai_move():
    available = [i for i in range(9) if st.session_state.board[i] == ""]
    return random.choice(available) if available else None

# ---------- TITLE ----------
st.title("🎮 Tic Tac Toe (AI)")

st.write("### You: ❌   |   AI: ⭕")

# ---------- BOARD ----------
cols = st.columns(3)

for i in range(9):
    with cols[i % 3]:
        if st.button(st.session_state.board[i] or " ", key=i):
            if not st.session_state.game_over and st.session_state.board[i] == "":
                
                # Player move
                st.session_state.board[i] = "X"
                result = check_winner(st.session_state.board)

                if result:
                    st.session_state.game_over = True
                    st.session_state.winner = result
                else:
                    # AI move
                    ai_index = ai_move()
                    if ai_index is not None:
                        st.session_state.board[ai_index] = "O"
                    
                    result = check_winner(st.session_state.board)
                    if result:
                        st.session_state.game_over = True
                        st.session_state.winner = result

# ---------- RESULT ----------
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.warning("It's a Draw 🤝")
    else:
        st.success(f"Winner: {st.session_state.winner}")

# ---------- RESTART ----------
if st.button("🔄 Restart Game"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.winner = None
