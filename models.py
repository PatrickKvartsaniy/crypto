import datetime

import sqlalchemy as sa
from aiopg.sa import create_engine

metadata = sa.MetaData()

table = sa.Table('cryptocurrencies', metadata,
                sa.Column('name',sa.String(100)),
                sa.Column('price',sa.String(100)),
                sa.Column('date',sa.String(100)))

class Crypto():
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.date = str(datetime.date.today())

    async def save(self):
        async with create_engine(user="patrick",
                                database="crypto",
                                host="127.0.0.1",
                                password="erasmusmundus") as engine:
            async with engine.acquire() as conn:
                await conn.execute(table.insert().values(name=self.name,
                                                    price=self.price,
                                                    date=self.date))