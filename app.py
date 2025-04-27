from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # needed for session management

posts = []  # this will hold our blog posts for now

# Dummy user credentials (for now)
USERNAME = 'admin'
PASSWORD = 'rohith'

# Home Page
@app.route('/')
def home():
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
        posts.append({'title': title, 'content': content})
        return redirect(url_for('home'))
    return render_template('create.html')

# Edit Post
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if not session.get('logged_in'):
        flash("Please log in to edit a post!")
        return redirect(url_for('login'))
    post = posts[index]
    if request.method == 'POST':
        posts[index]['title'] = request.form['title']
        posts[index]['content'] = request.form['content']
        return redirect(url_for('home'))
    return render_template('edit.html', post=post, index=index)

# Delete Post
@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if not session.get('logged_in'):
        flash("Please log in to delete a post!")
        return redirect(url_for('login'))
    posts.pop(index)
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
