from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your password",
    database="registration_db"
)
cursor = db.cursor()

# Create users table if not exists
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    print("Users table created or already exists")

except mysql.connector.Error as err:
    print(f"Error creating table: {err}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    try:
        # Insert into database
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        cursor.execute(sql, val)
        db.commit()
        print("User registered successfully")
        return redirect(url_for('success'))  # Redirect to success page

    except mysql.connector.Error as err:
        print(f"Error inserting data into MySQL: {err}")
        return render_template('index.html', error="Registration failed. Please try again.")

@app.route('/success')
def success():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
