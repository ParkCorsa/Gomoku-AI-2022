from flask import Flask, jsonify, render_template, request
from datetime import timedelta

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

global map
map = [[0 for i in range(15)] for j in range(15)]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/replay',methods=["POST"])
def replay():
    global map
    map = [[0 for i in range(15)] for j in range(15)]
    return jsonify({"code": 200,"msg":"成功"})


@app.route('/yes',methods=["POST"])
def yes():
    print('this is yes ')
    t = int(request.form['t'])
    print(t)
    tmprow = request.form['row']
    print(tmprow)
    tmpcol = request.form['col']
    print(tmpcol)
    row = int(tmprow)
    col = int(tmpcol)
    total = 1

    map[int(row)][int(col)] = t
    chessboard = map
    print(chessboard)
    print('this is yes ')
    print(t)
    print(tmprow)
    print(tmpcol)

    #horizontal
    while col - 1 > 0 and chessboard[row][col - 1] == t:
        total = total + 1
        col = col - 1

    row = int(tmprow)
    col = int(tmpcol)
    while col + 1 < 15 and chessboard[row][col + 1] == t:
        total = total + 1
        col = col + 1
    
    if total >= 5:
        if t == 1:
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            return jsonify({"code": 202, "msg": "白棋获胜"})

    #vertical
    row = int(tmprow)
    col = int(tmpcol)
    while row - 1 > 0 and chessboard[row - 1][col] == t:
        total = total + 1
        row = row - 1

    row = int(tmprow)
    col = int(tmpcol)
    while row + 1 < 15 and chessboard[row + 1][col] == t:
        total = total + 1
        row = row + 1
    
    if total >= 5:
        if t == 1:
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            return jsonify({"code": 202, "msg": "白棋获胜"})

    #other 2 cases
    row = int(tmprow)
    col = int(tmpcol)
    while row - 1 > 0 and col + 1 < 15 and chessboard[row - 1][col + 1] == t:
        total = total + 1
        row = row - 1
        col = col + 1

    row = int(tmprow)
    col = int(tmpcol)
    while row + 1 < 15 and col - 1 > 0 and chessboard[row + 1][col - 1] == t:
        total = total + 1
        row = row + 1
        col = col - 1
    
    if total >= 5:
        if t == 1:
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            return jsonify({"code": 202, "msg": "白棋获胜"})


    row = int(tmprow)
    col = int(tmpcol)
    while row - 1 > 0 and col - 1 > 0 and chessboard[row - 1][col - 1] == t:
        total = total + 1
        row = row - 1
        col = col - 1

    row = int(tmprow)
    col = int(tmpcol)
    while row + 1 < 15 and col + 1 < 15 and chessboard[row + 1][col + 1] == t:
        total = total + 1
        row = row + 1
        col = col + 1
    
    if total >= 5:
        if t == 1:
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            return jsonify({"code": 202, "msg": "白棋获胜"})

    return jsonify({"code": 203, "msg": "继续"})
            

if __name__ == '__main__':
	app.run(debug=True)

