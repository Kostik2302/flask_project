from flask import Flask
from models import Post, Tag, Category, Event, db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Создаем примеры категорий
        category1 = Category(name='Семейные игры')
        category2 = Category(name='Обучение')
        category3 = Category(name='Хобби')

        # Добавляем категории в базу
        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.commit()

        # Создаем примеры тегов
        tag1 = Tag(name='Python')
        tag2 = Tag(name='JavaScript')
        tag3 = Tag(name='Кино')

        # Добавляем теги в базу
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.commit()

        # Тестовые посты
        post1 = Post(title='Монополия', 
            content='Начиная с банкира, каждый игрок по очереди бросает кости. Игру начинает игрок с наибольшим итогом. Поместите свой жетон в угол с надписью "GO", затем бросьте кости и переместите свой жетон (в направлении стрелки) на количество пробелов, указанное кубиками. После завершения игры ход переходит влево. Жетоны остаются на занятых местах и переходят к следующему ходу игрока с этой точки. Два или более токена могут находиться на одном и том же месте одновременно. В зависимости от места, которого достигнет ваш токен, вы можете получить право на покупку недвижимости или другого имущества или быть обязаны платить арендную плату, налоги, получить Шанс или Общую карту, попасть в тюрьму и т.д... Если вы бросаете дубли, вы перемещаете свой жетон, как обычно, сумму двух игральных костей, и на вас распространяются любые привилегии или штрафы, относящиеся к месту, на которое вы приземляетесь. Удерживая кости, бросьте еще раз и переместите свой жетон, как и раньше. Если вы бросаете двойники три раза подряд, немедленно переместите свой жетон на место, отмеченное "В тюрьме".',
            rules='https://translated.turbopages.org/proxy_u/en-ru.ru.29be35f4-65c775ad-202247b6-74722d776562/https/monopoly.fandom.com/wiki/Official_Rules', 
            category_id=category1.id)
        post2 = Post(title='Мафия', 
            content='Игроки сидят за одним столом. Всем раздали карты, которые поделили участников на два лагеря: мирные жители и мафия. Показывать карточки друг другу нельзя. Суть игры Мафия в противостоянии команд: горожане стремятся вычислить бандитов, а те, напротив, — убить всех мирных.', 
            rules='https://www.kp.ru/family/hobbi/kak-igrat-v-mafiju/?ysclid=lsg3b3sq8v663608895',
            category_id=category2.id)
        post3 = Post(title='10 фильмов про роботов и ИИ', 
            content='Пересмотрели все фильмы про ИИ и роботов? Эти вы точно еще не смотрели.',
            rules='https://translated.turbopages.org/proxy_u/en-ru.ru.29be35f4-65c775ad-202247b6-74722d776562/https/monopoly.fandom.com/wiki/Official_Rules',  
            category_id=category3.id)

        # Добавляем теги к постам
        post1.tags.append(tag1)
        post1.tags.append(tag2)
        post2.tags.append(tag2)
        post3.tags.append(tag3)

        # Сохраняем посты в БД
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

        # Тестовые события
        event1 = Event(name='Финал супертурнира лиги вершителей судеб мирового рынка',
            game_id=post1.id,
            date=datetime(2024, 2, 20, 15, 00),
            place='Itmo 426 кабинет на ЛОМО',
            members_max=4,
            description='Будет просто Чипи-Чапа')
        
        # Сохраняем события в БД
        db.session.add(event1)
        db.session.commit()