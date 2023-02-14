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

autors = input('Введите имя автора: ')
result = session.query(Publisher).\
    join(Book).\
    join(Stock).\
    join(Shop).\
    join(Sale).\
    filter(Publisher.name == autors)

for p in result.all():
    for b in p.book:
        for st in b.stock:
            for sl in st.sale:
                # название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
                print(f'{b.title} | {st.shop.name} | {sl.price} | {sl.date_sale}')

session.close()
