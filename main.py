import json
import settings

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = f'postgresql://{settings.login}:{settings.pwd}@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Наполняем данными
with open('fixtures/tests_data.json') as f:
    for record in json.load(f):
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

# SELECT *
# FROM publisher as p LEFT JOIN book as b ON(p.id = b.id_publisher)
# LEFT JOIN stock as st ON(b.id = st.id_book)
# LEFT JOIN shop as sh ON(sh.id = st.id_shop)
# LEFT JOIN sale as sl ON(sl.id_stock = st.id)
# WHERE p.name = ''

autors = input('Введите имя автора')
result = session.query(Publisher).\
    join(Book).\
    join(Stock).\
    join(Shop).\
    join(Sale).\
    filter(Publisher.name == autors).all()

for c in result:
    # название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
    print(c)

session.close()
