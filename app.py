from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes (allows all origins)
CORS(app)

# MySQL Database connection details
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'Nikhil@00',  # Replace with your MySQL password
    'host': '10.92.192.3',  # Replace with your Cloud SQL instance IP
    'database': 'users_db'  # Replace with your database name
}

# Connect to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# POST /users: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User created successfully'}), 201

# GET /users: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(users), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
