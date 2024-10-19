from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('registration.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE: Add a new user
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Registration (Name, Email, Password, DateOfBirth, PhoneNumber, Address) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['Name'], data['Email'], data['Password'], data['DateOfBirth'], 
                  data.get('PhoneNumber'), data.get('Address')))
            conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists!'}), 400

# READ: Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Registration').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

# UPDATE: Update user info by ID
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Registration 
            SET Name = ?, Email = ?, PhoneNumber = ?, Address = ?
            WHERE ID = ?
        ''', (data['Name'], data['Email'], data.get('PhoneNumber'), data.get('Address'), id))
        conn.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

# DELETE: Delete user by ID
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Registration WHERE ID = ?', (id,))
        conn.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
