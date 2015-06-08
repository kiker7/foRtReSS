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

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

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
    col_cur = g.db.execute('SELECT username, color FROM users ORDER BY id DESC')
    color_tmp = [dict(username=row[0], color=row[1]) for row in col_cur.fetchall()]
    color = {}
    bgcolor = {}
    for crl in color_tmp:
        c = hex_to_rgb(crl['color'])
        d = (c[0] + 44, c[1] + 44, c[2] + 44)
        if d[0] > 255:
            d = (255, d[1], d[2])
        if d[1] > 255:
            d = (d[0], 255, d[2])
        if d[2] > 255:
            d = (d[0], d[1], 255)
        color[crl['username']] = rgb_to_hex(d)
        d = (c[0] / 2, c[1] / 2, c[2] / 2)
        bgcolor[crl['username']] = rgb_to_hex(d)
    cur = g.db.execute('SELECT author, text FROM entries ORDER BY id DESC')
    entries = [dict(author=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('forts.html', entries=entries, color=color, bgcolor=bgcolor)

@app.route('/addfort', methods=['POST'])
def addfort():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO entries (author, text) VALUES (?, ?)',
                 [session['logged_user'], request.form['text']])
    g.db.commit()
    return redirect(url_for('forts'))
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('SELECT username, password FROM users ORDER BY id DESC')
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
                return redirect(url_for('home'))
    return render_template('signin.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        exist = False
        cur = g.db.execute('SELECT username FROM users ORDER BY id DESC')
        registered = [dict(username=row[0]) for row in cur.fetchall()]
        for i in range (0, len(registered)):
            if registered[i]['username'] == request.form['username']:
                exist = True
                break
        
        if request.form['username'] == '':
            error = "Empty username field"
        elif request.form['password'] == '':
            error = "Empty password field"
        elif exist == True:
            error = "Username already exist"
        elif request.form['password'] != request.form['repassword']:
            error = "Passwords does not match"
        else:
            g.db.execute('INSERT INTO users (username, password, color) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], "#000000"])
            g.db.commit()
            session['logged_in'] = True
            session['logged_user'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('signup.html', error=error)

@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/profile')
def profile(error=None):
    cur = g.db.execute('SELECT name, surname, email, color, about FROM users WHERE username=?', [session['logged_user']])
    info = [dict(name=row[0], surname=row[1], email=row[2], color=row[3], about=row[4]) for row in cur.fetchall()]
    return render_template('profile.html', info=info, error=error)

@app.route('/update', methods=['POST'])
def update():
    g.db.execute("UPDATE users SET name=?, surname=?, email=?, color=?, about=? WHERE username=?", [request.form['fname'], request.form['lname'], request.form['email'], request.form['color'], request.form['about'], session['logged_user']])
    g.db.commit()
    return redirect(url_for('profile'))

@app.route('/changepass', methods=['POST'])
def changepass():
    error = None
    cur = g.db.execute('SELECT password FROM users WHERE username=?', [session['logged_user']])
    password = cur.fetchall()
    password = password[0][0]
    old_pass = request.form['old_pass']
    new_pass = request.form['new_pass']
    re_new_pass = request.form['re_new_pass']
    
    if password != old_pass:
        error = "Wrong old password"
    elif new_pass != re_new_pass:
        error = "New password doesn't match"
    else:
        g.db.execute("UPDATE users SET password=? WHERE username=?", [new_pass, session['logged_user']])
        g.db.commit()
    return profile(error=error)

@app.route('/database', methods=['GET'])
def database():
    cur = g.db.execute('SELECT id, username, password, name, surname, email, color, about FROM users ORDER BY id DESC')
    users = [dict(id=row[0], username=row[1], password=row[2], name=row[3], surname=row[4], email=row[5], color=row[6], about=row[7]) for row in cur.fetchall()]
    return render_template('database.html', users=users)

@app.route('/delete', methods=['POST'])
def delete():
    g.db.execute('DELETE FROM users WHERE id = ?', request.form['userid']) 
    g.db.commit()
    return redirect(url_for('database'))

@app.route('/view')
def view():
    author = request.args.get('author')
    cur = g.db.execute('SELECT name, surname, email, color, about FROM users WHERE username=?', [author])
    info = [dict(name=row[0], surname=row[1], email=row[2], color=row[3], about=row[4]) for row in cur.fetchall()]
    dur = g.db.execute('SELECT text FROM entries WHERE author=?', [author])
    forts = [dict(entry=row[0]) for row in dur.fetchall()]
    return render_template('view.html',info=info,forts=forts, author=author)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True, ssl_context=('certificate/server.crt', 'certificate/server.key'))
