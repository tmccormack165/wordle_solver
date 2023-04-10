from flask import Flask, render_template, jsonify, request, redirect, url_for
import pickle
app = Flask(__name__)


n_row = 6
n_col = 5
grid = [['']*n_col for i in range(n_row)]
color_grid = [['white']*n_col for i in range(n_row)]
vocab_df = pickle.load(open('vocab_df.pickle', 'rb'))


yellow = '#FFF2AE'
orange = '#FDCDAC'
green = '#B3E2CD'
grey = '#CCCCCC'

answer_entered = False

word_len = 5




@app.route("/", methods=['POST', 'GET'])
def home(): 
    return render_template('bubble.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)


def run(n):
    '''Generates n guesses for the user's answer, and exits if the answer is found

    Args:
        n (int): the number of guesses that the computer has (wordle gives six guesses)
    Return:
        void
    '''

    for i in range(n):
        if(i == 0):
            guess = 'audio'
        else:
            guess = vocab_df.Word.values[0]

        print(f'GUESS: {guess}')
        #update grid
        guess_len = len(guess)
        assert guess_len == word_len

        for j in range(guess_len):
            grid[i][j] = guess[j]

        break



@app.route("/game", methods=['POST', 'GET'])
def game():
    if(request.method == 'POST'):
        answer_entered = True
        answer = request.form['ans']
        print(f'ANSWER: {answer}')
        print(f'vdf: {vocab_df.head()}')
        run(n_row)



    
    return render_template('index.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)





if __name__ == '__main__':
    app.run(debug=True)