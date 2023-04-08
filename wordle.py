from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)


n_row = 6
n_col = 5
grid = [['']*n_col for i in range(n_row)]
color_grid = [['white']*n_col for i in range(n_row)]

yellow = '#FFF2AE'
orange = '#FDCDAC'
green = '#B3E2CD'
grey = '#CCCCCC'




@app.route("/", methods=['POST', 'GET'])
def home(): 
    return render_template('bubble.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)


@app.route("/game", methods=['POST', 'GET'])
def game():
    if(request.method == 'POST'):
        answer = request.form['ans']
        print(f'ANSWER: {answer}')

    
    return render_template('index.html', grid=grid, n_col=n_col,  
                           n_row=n_row, color_grid=color_grid)





if __name__ == '__main__':
    app.run(debug=True)