import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

DATABASE = 'database/foRtReSS.db'
SECRET_KEY = 'development.key'

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
@app.route('/home')
def home():
    return forts()

@app.route('/forts')
def forts():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('forts.html', entries=entries)

@app.route('/addfort', methods=['POST'])
def addfort():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('forts'))
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users order by id desc')
        entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        length = len(entries)
        for i in range (0, length + 1):
            try:
                if entries[i]['username'] == request.form['username']:
                    break
            except IndexError:
                i += 1
                break

        if i > length:
            error = 'Invalid username'
        else:
            if request.form['password'] != entries[i]['password']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['logged_user'] = request.form['username']
                flash('You were logged in')
                return redirect(url_for('home'))
    return render_template('signin.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '':
            error = "Empty username field"
        elif request.form['password'] == '':
            error = "Empty password field"
        elif request.form['password'] != request.form['repassword']:
            error = "Passwords does not match"
        else:
            g.db.execute('insert into users (username, password) values (?, ?)',
                 [request.form['username'], request.form['password']])
            g.db.commit()
            session['logged_in'] = True
            session['logged_user'] = request.form['username']
            flash('New account created')
            return redirect(url_for('home'))
    return render_template('signup.html', error=error)

@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/update', methods=['POST'])
def update():
    return redirect(url_for('profile'))

@app.route('/changepass', methods=['POST'])
def changepass():
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True, ssl_context=('certificate/server.crt', 'certificate/server.key'))
