from flask import Flask

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

if __name__ == '__main__':
    app.run(debug=True)
