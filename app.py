import os, logging
from datetime import datetime
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.errorhandler(500)
def general_application_error(e):
    """ General Error Hanlder
        returns 500 on invocation
    """
    return jsonify(error=str(e)), 500

@app.route('/')
def appRoot():
    person = {'name': 'Alice', 'birth-year': 1978}
    return jsonify(person)

@app.route('/healthz')
def healthcheck():
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return jsonify({"message": "Hello From  Flask App, Current Date is : {} ".format(dt_string)})

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/read')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(books)

@app.route('/init/')
def init():
    person = {'name': 'Alice', 'birth-year': 1978, 'envar': ENV1}
    return jsonify(person)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == "__main__":

    if os.getenv('ENVIRONMENT') is not None:
        app.config['environment'] = os.getenv('ENVIRONMENT')
    else:
        app.config['environment'] = "dev"

    app.run(debug=False, host='0.0.0.0', port=8080)