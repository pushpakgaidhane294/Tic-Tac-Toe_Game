from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

board = [""] * 9
current_player = "O"  # AI starts

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player, board

    data = request.json
    human_move = data.get("move")

    if board[human_move] == "" and current_player == "X":
        board[human_move] = "X"
        current_player = "O"

    winner = check_winner(board)

    # AI turn
    if not winner and current_player == "O":
        ai = ai_move()
        if ai is not None:
            board[ai] = "O"
        current_player = "X"
        winner = check_winner(board)

    return jsonify({
        "board": board,
        "winner": winner
    })

@app.route("/start", methods=["GET"])
def start():
    global board, current_player
    board = [""] * 9
    current_player = "O"

    # AI first move
    ai = ai_move()
    if ai is not None:
        board[ai] = "O"
        current_player = "X"

    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(debug=True)
