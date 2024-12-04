from flask import Flask, render_template_string, request
import random

word_list = ["python", "flask", "hangman", "developer", "code"]
stages = [r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''',r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''',r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''',r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''',r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''',r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''',r'''
  +---+
  |   |
      |
      |
      |
      |
=========
''']
logo = ''' 
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/    '''


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hangman Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
        }

        .game-container {
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            width: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color:green;
            font-size:5em;
        }

        h2 {
            font-size: 1.5em;
        }

        input {
            padding: 10px;
            font-size: 1em;
            margin: 10px 0;
            width: 50px;
        }

        button {
            padding: 10px 20px;
            font-size: 1em;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }

        button:hover {
            background-color: #45a049;
        }

        
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Hangman</h1>
        <p>{{ game_data.message }}</p>

        <h2>Lives: {{ game_data.lives }}/6</h2>
        <h2>Word to guess: {{ game_data.display }}</h2>
        <h2>Word length: {{ game_data.word_length }} letters</h2>

        <form method="POST">
            <input type="text" name="guess" maxlength="1" required>
            <button type="submit">Guess</button>
        </form>

        <h3>Hangman Stage:</h3>
        <pre>{{ stages[game_data.lives] }}</pre>
    </div>
</body>
</html>
"""

app = Flask(__name__)


game_data = {
    "lives": 6,
    "chosen_word": random.choice(word_list),
    "correct_letters": [],
    "guessed_letters": [],
    "game_over": False,
    "display": "",
    "word_length": 0,
    "message": ""
}


@app.route("/", methods=["GET", "POST"])
def index():
    while game_data["game_over"]:
        game_data["lives"] = 6
        game_data["chosen_word"] = random.choice(word_list)
        game_data["correct_letters"] = []
        game_data["guessed_letters"] = []
        game_data["game_over"] = False
        game_data["display"] = ""
        game_data["word_length"] = 0
        game_data["message"] = "New Game Started!"
        return render_template_string(str(TEMPLATE), game_data=game_data, logo=logo, stages=stages)


    if not game_data["display"]:
        game_data["display"] = "_" * len(game_data["chosen_word"])
        game_data["word_length"] = len(game_data["chosen_word"])

    if request.method == "POST":
        guess = request.form.get("guess").lower()

        if guess in game_data["guessed_letters"]:
            game_data["message"] = f"You've already guessed {guess}. Try another letter."
        else:
            game_data["guessed_letters"].append(guess)

            display = ""
            for letter in game_data["chosen_word"]:
                if letter in game_data["guessed_letters"]:
                    display += letter
                else:
                    display += "_"

            game_data["display"] = display

            if guess not in game_data["chosen_word"]:
                game_data["lives"] -= 1
                if game_data["lives"] == 0:
                    game_data["game_over"] = True
                    game_data["message"] = "You lose!"
                    game_data["display"] = game_data["chosen_word"]

            elif "_" not in display:
                game_data["game_over"] = True
                game_data["message"] = "You win!"

    return render_template_string(str(TEMPLATE), game_data=game_data, logo=logo, stages=stages)


if __name__ == "__main__":
    app.run(debug=False , host='127.0.0.1')
