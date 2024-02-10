from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Category, Tag, Post, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/user/<username>')
def user_profile(username):
    return f"Это профиль пользователя {username}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # проверка логина и пароля
        return 'Вы вошли в систему!'
    else:
        return render_template('login.html')

@app.route('/games')
def index():
    posts = Post.alphabet_sort().all()
    return render_template('index.html', posts=posts)

@app.route('/games/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/games/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.title.asc()).all()
    return render_template('category.html', category=category, posts=posts)

@app.route('/games/tag/<int:tag_id>')
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.filter(Post.tags.any(id=tag_id)).order_by(Post.title.asc()).all()
    return render_template('tag.html', tag=tag, posts=posts)

@app.route('/events')
def events():
    events = Event.newest_first().all()
    return render_template('events.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)

