from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

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
    
db_config = {
    "host": "flask-test-mysql-db-1",
    "user": "user",
    "password": "password",
    "database": "test_db"
}

@app.route('/signup',methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup',methods=['POST'])
def signup_user():
    name = request.form.get('name')
    print(name)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES(%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/users')
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@app.route('/users')
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('allusers.html',data=result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@app.route('/update',methods=['GET'])
def update():
    return render_template('update.html')

@app.route('/update',methods=['POST'])
def update_data():
    id = request.form.get('id')
    name = request.form.get('name')
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name=(%s) WHERE id=(%s)", (name,id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/users')
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/delete',methods=['GET'])
def delete():
    return render_template('delete.html')

@app.route('/delete',methods=['POST'])
def delete_data():
    id = request.form.get('id')
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=(%s)", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/users')
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/add',methods=['POST'])
def add_data():
    data = request.json
    name = data.get("name")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES(%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "success"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/get')
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"result": result})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# @app.route('/update',methods=['POST'])
# def update_data():
#     data = request.json
#     id = data.get("id")
#     name = data.get("name")
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#         cursor.execute("UPDATE users SET name=(%s) WHERE id=(%s)", (name,id))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "success"})
#     except mysql.connector.Error as err:
#         return jsonify({"error": str(err)}), 500

# @app.route('/delete',methods=['POST'])
# def delete_data():
#     data = request.json
#     id = data.get("id")
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM users WHERE id=(%s)", (id,))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "success"})
#     except mysql.connector.Error as err:
#         return jsonify({"error": str(err)}), 500

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/test')
def test():
    return "test"

# @app.route('/users')
# def get_users():
#     users = User.query.all()
#     return jsonify([user.select_user() for user in users])

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
