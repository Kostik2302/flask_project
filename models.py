from flask_login import UserMixin
from start import manager, db




class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tag', backref='tags', lazy=True)

    def __repr__(self):
        return f'<Tag {self.name}>'


post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    events = db.relationship('Event', backref='post')

    def repr(self):
        return f'<Post {self.title}>'
    
    @classmethod
    def alphabet_sort(cls):
        return cls.query.order_by(cls.title.asc())


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    members_max = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    events_id = db.relationship('Event_members', backref='event', lazy=True)

    @classmethod
    def latest_first(cls):
        return cls.query.order_by(cls.date)

class Event_members(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    member_id = db.Column(db.String(128), db.ForeignKey('user.id'), primary_key=True)

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    users_id = db.relationship('Event_members', backref='user', lazy=True)


@manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
