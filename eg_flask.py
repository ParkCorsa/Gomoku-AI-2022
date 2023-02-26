from flask import Flask, render_template, request
from datetime import timedelta

#需要传入__name__ 为了确定资源所在路径
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

global map
map = [[0 for i in range(15)] for j in range(15)]
# #flask中定义路由是通过装饰器来实现的，访问路由会自动调用路由下跟的方法，并将执行结果返回

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/replay',methods=["POST"])
def replay():
    global map
    map = [[0 for i in range(15)] for j in range(15)]
    return {"code": 200,"msg":"成功"}


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
    #不写注释真容易看混，本少侠就勉强写一点吧
    #这里是要判断水平方向上是否满足获胜条件
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
            return {"code": 201, "msg": "黑棋获胜"}
        else:
            return {"code": 202, "msg": "白棋获胜"}

    #判断垂直方向上是否满足获胜条件
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
            return {"code": 201, "msg": "黑棋获胜"}
        else:
            return {"code": 202, "msg": "白棋获胜"}

    
    #判断pie上是否满足获胜条件
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
            return {"code": 201, "msg": "黑棋获胜"}
        else:
            return {"code": 202, "msg": "白棋获胜"}


    #判断na上是否满足获胜条件
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
            return {"code": 201, "msg": "黑棋获胜"}
        else:
            return {"code": 202, "msg": "白棋获胜"}

    return {"code": 203, "msg": "继续"}
            

    

#会运行起一个小型服务器，就会将我们的flask程序运行在一个简单的服务器上，服务器由flask提供，用于测试

if __name__ == '__main__':
	app.run()
