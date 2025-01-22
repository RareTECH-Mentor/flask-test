from flask import Flask, jsonify
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
