from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ---------- GAME STATE ----------
board = [""] * 9
current_player = "X"
mode = "ai"  # ai or multiplayer

scores = {
    "X": 0,
    "O": 0,
    "draw": 0
}

# ---------- FUNCTIONS ----------
def check_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for i,j,k in wins:
        if b[i] == b[j] == b[k] and b[i] != "":
            return b[i]
    if "" not in b:
        return "Draw"
    return None

def ai_move():
    available = [i for i in range(9) if board[i] == ""]
    return random.choice(available) if available else None

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global board, current_player, mode

    data = request.json
    mode = data.get("mode", "ai")

    board = [""] * 9

    if mode == "ai":
        current_player = "O"
        ai = ai_move()
        if ai is not None:
            board[ai] = "O"
            current_player = "X"
    else:
        current_player = "X"

    return jsonify({"board": board, "scores": scores})

@app.route("/move", methods=["POST"])
def move():
    global current_player, board, scores

    data = request.json
    pos = data.get("move")

    if board[pos] == "":
        board[pos] = current_player

        winner = check_winner(board)

        if not winner:
            if mode == "ai":
                current_player = "O"
                ai = ai_move()
                if ai is not None:
                    board[ai] = "O"
                current_player = "X"
                winner = check_winner(board)
            else:
                current_player = "O" if current_player == "X" else "X"

        if winner:
            if winner == "Draw":
                scores["draw"] += 1
            else:
                scores[winner] += 1

        return jsonify({
            "board": board,
            "winner": winner,
            "current": current_player,
            "scores": scores
        })

    return jsonify({"error": "Invalid move"})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
