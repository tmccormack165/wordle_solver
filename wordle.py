from flask import Flask, render_template, jsonify, request, redirect, url_for
import pickle
app = Flask(__name__)


n_row = 6
n_col = 5
grid = [['']*n_col for i in range(n_row)]
color_grid = [['white']*n_col for i in range(n_row)]

yellow = '#FFF2AE'
orange = '#FDCDAC'
green = '#B3E2CD'
grey = '#CCCCCC'

answer_entered = False

word_len = 5

vocab_df = pickle.load(open('vocab_df.pickle', 'rb'))



@app.route("/", methods=['POST', 'GET'])
def home(): 
    return render_template('bubble.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)


def filter_vocab(grey, yellow, green, vocab_df):
    '''Filters the current set of potential answers given the insight from the current guess
    Parameters:
        grey (list): a list of letters non existent in the answer
        yellow (list): a list of letters at the wrong index
        green (list): a list of letters at the correct index
    Return:
        vocab_df (pd.DataFrame): a dataframe recording the potential answers
    '''

    # filter out words that have grey letters
    for i in range(len(grey)):
        vocab_df = vocab_df[~vocab_df.Word.str.contains(grey[i])]

    # filter out words that do not have yellow letters
    for i in range(len(yellow)):
        vocab_df = vocab_df[vocab_df.Word.str.contains(yellow[i])]
    
    # filter out words that do not have a correct index for a green letter
    for i in range(len(green)):
        c = green[i][0]
        index = green[i][1]
        if(index == 0):
            regex_query = fr'^{c}.*'
        else:
            regex_query = fr'.{{{index}}}{c}'

        vocab_df = vocab_df[vocab_df.Word.str.contains(regex_query, regex=True)]
    
    return vocab_df


def check_answer(guess, answer, vocab_df):
    '''Check if the algorithm has guessed the answer, and filter the potential answers if the answer remains unknown
    Parameters:
        - guess (str): the current best guess
        - answer (str): the true answer
        - vocab_df (pd.DataFrame): a dataframe recording the current potential answers
    Return:
        - vocab_df (pd.DataFrame): the filtered data frame holding the updated potential answers
    
    '''
    green_chars = []
    yellow_chars = []
    grey_chars = []

    for i in range(len(guess)):
        c = guess[i]
        if(c == answer[i]):
            green_chars.append((c,i))
        elif(c in answer):
            yellow_chars.append(c)
        else:
            grey_chars.append(c)

    print(f'Green: {green_chars}')
    print(f'Yellow: {yellow_chars}')
    print(f'Grey: {grey_chars}')
    print('----------------------------------------')
    vocab_df = filter_vocab(grey_chars, yellow_chars, green_chars, vocab_df)
    guess_data = {'grey':grey_chars, 'yellow':yellow_chars, 'green':green_chars}
    return vocab_df, guess_data




def run(n, answer, vocab_df):
    '''Generates n guesses for the user's answer, and exits if the answer is found

    Args:
        n (int): the number of guesses that the computer has (wordle gives six guesses)
        answer (str): the answer entered by the user
    Return:
        void
    '''

    for i in range(n):
        if(i == 0):
            guess = 'audio'
        else:
            guess = vocab_df.Word.values[0]

        print(f'GUESS: {guess}')

        # assert guess is valid
        guess_len = len(guess)
        assert guess_len == word_len

        # add the guess to the grid to display on the frontend
        for j in range(guess_len):
            grid[i][j] = guess[j]

        if(answer == guess):
            print(f'Computer Wins')
        else:
            vocab_df, guess_data = check_answer(guess, answer, vocab_df)
            guess_data['green'] = [x[0] for x in guess_data['green']]
            print(f'GUESS DATA: {guess_data}')
            for j in range(guess_len):
                gchar = guess[j]
                if(gchar in guess_data['green']):
                    color_grid[i][j] = green
                elif(gchar in guess_data['yellow']):
                    color_grid[i][j] = yellow
                else:
                    color_grid[i][j] = grey

            
        
        #break



@app.route("/game", methods=['POST', 'GET'])
def game():
    global answer_entered
    global vocab_df
    if(answer_entered == False):
        answer_entered = True
    else:
        if(request.method == 'POST'):
            print(f'POST REQUEST')
            answer_entered = True
            answer = request.form['ans']
            print(f'ANSWER: {answer}')
            #print(f'vdf: {vocab_df.head()}')
            run(n_row, answer, vocab_df)



    
    return render_template('index.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)





if __name__ == '__main__':
    app.run(debug=True)