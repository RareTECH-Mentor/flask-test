from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/test')
def test():
    return "test"

@app.route('/main/<username>')
def main(username):
    return "こんにちは" + username + "さん！"

@app.route('/checknum',methods=['POST'])
def checknum():
    num = int(request.form.get('num'))
    if num % 2 == 0:
        return "偶数です"
    else:
        return "奇数です" 

if __name__ == '__main__':
    app.run(debug=True)
