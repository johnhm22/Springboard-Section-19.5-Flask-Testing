from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'madeup-password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


from boggle import Boggle

# variable defined and used to call methods on boggle.py
boggle_game = Boggle()


@app.route('/')
# Renders start.html which displays board with numbers along with current highest score and number of games played
def display_board():
    board = boggle_game.make_board()
    session['board'] = board
    highest_score = session.get("highest_score", 0)
    games_played = session.get("games_played", 0)

    return render_template('start.html',
    board = board,
    highest_score = highest_score,
    games_played = games_played
    )



@app.route('/check-word')
# checks word in words.txt file, passing selected word in url. Returns result in json format to function in board.js that called API route
def analyse_guess():
    board = session['board']
    word = request.args['word']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({"result": result})    



@app.route('/save-score', methods=["POST"])
# called when allocated time for each game is completed; receives score for game and updates highest score in session if score > current highest score. Also increases games_played by one and saves in session. Returns info to function in board.js that called API route
def save_score():
    score = request.json["score"]
    games_played = session.get("games_played", 0)
    highest_score = session.get("highest_score", 0)

    session['games_played'] = games_played + 1
    session['highest_score'] = max(highest_score, score)
    info = {"games_played": session['games_played'], "highest_score": session['highest_score']}

    return jsonify(info)



