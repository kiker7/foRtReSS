import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

DATABASE = 'database/foRtReSS.db'
DEBUG = True
SECRET_KEY = 'development.key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['repassword']:
            error = "Different passwords"
        else:
            # tutaj do request.form['password'] zhashowac 2 razy sha256 i wpisac poniżej
            g.db.execute('insert into users (username, password) values (?, ?)',
                 [request.form['username'], request.form['password']])
            g.db.commit()
            session['logged_in'] = True
            flash('New account created')
            return redirect(url_for('show_entries'))
    return render_template('create.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users order by id desc')
        entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        length = len(entries[0])
        for i in range (0, length - 1):
            if entries[i]['username'] == request.form['username']:
                break
        
        if i == 2:
            error = 'Invalid username'
        else:
            if request.form['password'] != entries[i]['password']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/database', methods=['GET'])
def database():
    cur = g.db.execute('select id, username, password from users order by id desc')
    users = [dict(id=row[0], username=row[1], password=row[2]) for row in cur.fetchall()]
    return render_template('database.html',users=users)

@app.route('/delete', methods=['POST'])
def delete():
    g.db.execute('delete from users where id = ?',request.form['userid']) 
    g.db.commit()
    return redirect(url_for('database'))

if __name__ == '__main__':
    app.run()
