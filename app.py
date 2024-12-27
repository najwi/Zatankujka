from datetime import datetime
from flask import Flask, redirect, url_for, render_template, session, request

from config import config
from sheetService import add_row, RowData

app = Flask(__name__)
app.secret_key = config['SESSION_KEY']


@app.before_request
def check_login():
    # List of routes that don't require login
    public_routes = ['login']

    if request.endpoint in public_routes:
        return

    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))


@app.route("/")
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("index.html", default_date=today)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username')
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        if data['username'] == config['USER']['LOGIN'] and data['password'] == config['USER']['PASSWORD']:
            session['username'] = data['username']
            return redirect(url_for('index'))
        else:
            return render_template("login.html", failedMsg=True)

    if request.method == 'GET':
        if 'username' not in session:
            return render_template("login.html")
        else:
            return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    odometer = request.form['odometer']
    amount = request.form['amount'].replace('.', ',')
    lpgPrice = request.form['lpgPrice'].replace('.', ',')
    pbPrice = request.form['pbPrice'].replace('.', ',')
    row_data = RowData(date, odometer, amount, lpgPrice, pbPrice)
    add_row(row_data)
    return render_template("success.html")
