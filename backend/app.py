from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection parameters
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    surname = request.form.get('surname')
    age = request.form.get('age')
    
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, surname, age) VALUES (%s, %s, %s)", (name, surname, age))
    conn.commit()

    cursor.close()
    conn.close()
    return 'Data submitted successfully!'

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/crash')
def crash():
    # Deliberately crash the application
    raise RuntimeError('Deliberate crash!')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
