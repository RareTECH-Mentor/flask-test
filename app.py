from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@mysql-db/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def select_user(self):
        return {
            'id': self.id,
            'name': self.name
        }

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/test')
def test():
    return "test"

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([user.select_user() for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.select_user()), 201

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
    db.create_all()
    app.run(debug=True)
