import os
import sqlite3
import datetime

from flask import Flask, request, session, g, redirect, url_for, abort,\
    render_template, flash

# Placeholder name for now. Name as variable to be easily changable when I come
# up with something better
website_name = 'linkit'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, website_name),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SITE_SETTINGS', silent=True)


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """initializes the database."""
    init_db()
    print('Initialized the database')


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_posts():
    db = get_db()
    cur = db.execute('select title,\
                     postContents,\
                     postLink\
                     from posts\
                     order by postDate desc')
    posts = cur.fetchall()
    return render_template('show_posts.html', posts=posts)


@app.route('/add', methods=['POST'])
def add_post():
    db = get_db()
    post_id = '3x3x3z'
    post_date = str(datetime.datetime.now())
    db.execute('insert into posts (id, title, postContents, postDate)\
               values (?, ?, ?, ?)',
               [post_id, request.form['title'], request.form['text'], post_date])
    db.commit()
    flash('new post was successfully posted')
    return redirect(url_for('show_posts'))
