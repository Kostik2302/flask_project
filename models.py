from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

    @classmethod
    def newest_first(cls):
        return cls.query.order_by(cls.date.desc())

