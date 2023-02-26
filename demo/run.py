from flask import Flask, jsonify, render_template, request
from datetime import timedelta
import sys
import subprocess
import numpy as np

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

global turn 

turn = 1

global map
map = [[0 for i in range(15)] for j in range(15)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yes',methods=["POST"])
def yes():
    global turn
    t = int(request.form['t'])
    tmprow = request.form['row']
    tmpcol = request.form['col']
    row = int(tmprow)
    col = int(tmpcol)
    total = 1

    if row == -1 and col == -1 and turn == 3:
        for i in range(0,15):
            for j in range(0,15):
                if map[i][j] == 1 or map[i][j] == 2:
                    map[i][j] == 3 - map[i][j]
    else:
        map[int(row)][int(col)] = t
    chessboard = map

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
            turn += 1
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            turn += 1
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
            turn += 1
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            turn += 1
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
            turn += 1
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            turn += 1
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
            turn += 1
            return jsonify({"code": 201, "msg": "黑棋获胜"})
        else:
            turn += 1
            return jsonify({"code": 202, "msg": "白棋获胜"})

    turn += 1
    return jsonify({"code": 203, "msg": "继续"})

class AI:
    def __init__(self, path, id):
        self.path = path
        if path == 'human':
            self.human = 1
        else:
            self.human = 0
        self.id = id

    def send(self, message):
        value = str(message) + '\n'
        value = bytes(value, 'UTF-8')
        self.proc.stdin.write(value)
        self.proc.stdin.flush()

    def receive(self):
        return self.proc.stdout.readline().strip().decode()

    def init(self):
        if self.human == 0:
            self.proc = subprocess.Popen(self.path,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
            self.send(self.id)
            self.name = self.receive()

    def action(self, a, b):
        if self.human == 1:
            value = sys.stdin.readline().strip().split(' ')
        else:
            self.send(str(a) + ' ' + str(b))
            value = self.receive().split(' ')
        return int(value[0]), int(value[1])

class Board:
    def __init__(self):
        self.board = -np.ones((15, 15), dtype=int)

    def show(self):
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == -1:
                    sys.stdout.write('_ ')
                else:
                    sys.stdout.write(str(self.board[i][j]) + ' ')
            sys.stdout.write('\n')
    def clear(self):
            for i in range(15):
                for j in range(15):
                    self.board[i][j] = -1

    def action(self, side, turn, x, y):
        if turn == 2 and side == 1 and x == -1 and y == -1:
            self.board = np.where(self.board != -1, 1 - self.board, self.board)
        else:
            self.board[x][y] = side

    def full(self):
        return len(np.where(self.board == -1)[0]) == 0

    def check_win(self, side, turn, x, y):
        if turn == 1 and side == 1 and x == -1 and y == -1:
            return 0
        if x >= 15 or y >= 15 or self.board[x][y] != -1:
            return -1

        # 8 Directions
        dx = [1, 1, -1, -1, 0, 0, 1, -1]
        dy = [1, -1, 1, -1, 1, -1, 0, 0]
        for xx in range(0, 15):
            for yy in range(0, 15):

                for i in range(8):
                    curx, cury = xx, yy
                    flg = True
                    for _ in range(5):
                        if curx < 0 or curx >= 15 or cury < 0 or cury >= 15:
                            flg = False
                            break

                        if self.board[curx][cury] != side and (curx != x or cury != y):
                            flg = False
                            break
                        curx, cury = curx + dx[i], cury + dy[i]
                        # print(_, curx, cury, self.board[curx][cury], side)
                    if flg:
                        return 1

        return 0

def try_init(ai0, ai1):
    ai0.init()
    ai1.init()

global board
board = Board() 

AI1 = AI('human', 1)
AI0 = AI('./baseline', 0)
try_init(AI0, AI1)

@app.route('/white',methods=["POST"])
def white():
    global turn, board
    board.show()
    a = int(request.form['row'])
    b = int(request.form['col'])
    type = int(request.form['t'])
    if type == 3:
        c, d = AI0.action(a, b)
        sys.stderr.write('ai0 take action: [' + str(c) + ' ' + str(d) + ']\n')
        board.action(0, turn, c, d)
        return jsonify({"x":c, "y":d, "code": 203, "msg": "继续"})
    
    c, d = AI0.action(a, b)
    sys.stderr.write('ai0 take action: [' + str(c) + ' ' + str(d) + ']\n')
    ret = board.check_win(0, turn, c, d)
    board.action(0, turn, c, d)
    board.show()
    if ret == -1:
        turn += 1
        return jsonify({"code": 202, "msg": "白棋获胜"})
    elif ret == 1:
        turn += 1
        return jsonify({"code": 201, "msg": "黑棋获胜"})
    elif board.full():
        turn += 1
        return jsonify({"code": 200, "msg": "平局"})
    if turn == 2 and a == -1 and b == -1:
        sys.stderr.write('ai1 flips the board\n')
    else:
        sys.stderr.write('ai1 take action: [' + str(a) + ' ' + str(b) + ']\n')
    ret = board.check_win(1, turn, a, b)
    board.action(1, turn, a, b)
    if ret == -1:
        turn += 1
        return jsonify({"code": 201, "msg": "黑棋获胜"})
    elif ret == 1:
        turn += 1
        return jsonify({"code": 202, "msg": "白棋获胜"})
    elif board.full():
        turn += 1
        return jsonify({"code": 200, "msg": "平局"})

    turn += 1
    return jsonify({"x":c, "y":d, "code": 203, "msg": "继续"})

ai0 = AI('human', 0)
ai1 = AI('./baseline', 1)  
try_init(ai0, ai1)

@app.route('/black',methods=["POST"])
def black():
    global turn, board
    board.show()
    a = int(request.form['row'])
    b = int(request.form['col'])
    sys.stderr.write('ai0 take action: [' + str(a) + ' ' + str(b) + ']\n')
    ret = board.check_win(0, turn, a, b)
    board.action(0, turn, a, b)
    board.show()
    if ret == -1:
        turn += 1
        return jsonify({"code": 202, "msg": "白棋获胜"})
    elif ret == 1:
        turn += 1
        return jsonify({"code": 201, "msg": "黑棋获胜"})
    elif board.full():
        turn += 1
        return jsonify({"code": 200, "msg": "平局"})
    a, b = ai1.action(a, b)
    if turn == 2 and a == -1 and b == -1:
        sys.stderr.write('ai1 flips the board\n')
    else:
        sys.stderr.write('ai1 take action: [' + str(a) + ' ' + str(b) + ']\n')
    ret = board.check_win(1, turn, a, b)
    board.action(1, turn, a, b)
    if ret == -1:
        turn += 1
        return jsonify({"code": 201, "msg": "黑棋获胜"})
    elif ret == 1:
        turn += 1
        return jsonify({"code": 202, "msg": "白棋获胜"})
    elif board.full():
        turn += 1
        return jsonify({"code": 200, "msg": "平局"})

    turn += 1
    return jsonify({"x":a, "y":b, "code": 203, "msg": "继续"})

@app.route('/replay',methods=["POST"])
def replay():
    global map, board
    map = [[0 for i in range(15)] for j in range(15)]
    board.clear()
    AI1 = AI('human', 1)
    AI0 = AI('./baseline', 0)
    try_init(AI0, AI1)
    ai0 = AI('human', 0)
    ai1 = AI('./baseline', 1)  
    try_init(ai0,ai1)
    return jsonify({"code": 200,"msg":"成功"})

if __name__ == '__main__':
	app.run(debug=True)

