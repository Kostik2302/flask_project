from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from models import Category, Tag, Post, Event, User, Event_members
from start import app, db

@app.route('/')
def home():
    return render_template('main.html')


@app.route('/user/<username>')
def user_profile(username):
    return f"Это профиль пользователя {username}"


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    # проверка логина и пароля
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if next_page == None:
                return redirect(url_for('home'))

            return redirect(next_page)
        else:
            flash('Логин или пароль некорректно заполнены')
    else:
        flash('Заполните оба поля')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйства, заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


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
@login_required
def events():
    events = Event.latest_first().all()
    datetime_now = datetime.now()
    for event in events:
        if event.date < datetime_now:
            db.session.delete(event)
    events = Event.latest_first().all()
    events_members = [i.event_id for i in Event_members.query.all()]
    user_id = current_user.id
    user_events = [i.event_id for i in Event_members.query.filter(Event_members.member_id == user_id).all()]
    return render_template('events.html', events=events, user_events=user_events, events_members=events_members)

@app.route('/events/delete', methods=['POST'])
def sign_out():
    event_id_to_delete = request.form.get('event_id_to_delete')
    db.session.query(Event_members).filter(Event_members.event_id == event_id_to_delete, Event_members.member_id == current_user.id).delete()
    db.session.commit()
    return redirect('/events')

@app.route('/events/add', methods=['POST'])
def sign_up():
    event_id_to_add = request.form.get('event_id_to_add')
    db.session.add(Event_members(event_id = event_id_to_add, member_id = current_user.id))
    db.session.commit()
    return redirect('/events')





