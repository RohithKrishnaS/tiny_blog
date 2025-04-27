from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Setup the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Dummy user credentials
USERNAME = 'admin'
PASSWORD = 'rohith#@'

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

# Home Page
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# Create New Post
@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('logged_in'):
        flash("Please log in to create a post!")
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create.html')

# Edit Post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if not session.get('logged_in'):
        flash("Please log in to edit a post!")
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', post=post)

# Delete Post
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    if not session.get('logged_in'):
        flash("Please log in to delete a post!")
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            flash("You are now logged in!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.")
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

# Create database tables if not exist
with app.app_context():
    db.create_all()
