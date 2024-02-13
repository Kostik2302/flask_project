from flask import Flask
from models import Post, Tag, Category, Event, User
from datetime import datetime
from start import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()

            # Создаем примеры категорий
            category1 = Category(name='Настольные игры')

            # Добавляем категории в базу
            db.session.add(category1)
            db.session.commit()

            # Создаем примеры тегов
            tag1 = Tag(name='Быстрая игра')

            # Добавляем теги в базу
            db.session.add(tag1)
            db.session.commit()

            # Тестовые посты
            post1 = Post(title='Дженга', 
                content='Дженга» — это увлекательная настольная игра, известная в России как «падающая башня». Принцип достаточно прост: из ровных деревянных брусков строится башня (каждый новый «этаж» делается с чередованием направления укладки), а затем игроки начинают аккуратно вытаскивать по одному бруску и ставить его на верх башни.',
                rules='https://ru.wikihow.com/играть-в-дженга', 
                category_id=category1.id)

            # Добавляем теги к постам
            post1.tags.append(tag1)

            # Сохраняем посты в БД
            db.session.add(post1)
            db.session.commit()

            # Тестовые события
            event1 = Event(name='Чисто посидеть поболтать поиграть в Дженгу',
                game_id=post1.id,
                date=datetime(2024, 5, 20, 15, 00),
                place='Коворкинг на Карповке',
                members_max=4,
                description='Ждем каждого')
            
            # Сохраняем события в БД
            db.session.add(event1)
            db.session.commit()
        except:
            print('Ашыпка')
