import datetime

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import appsecrets as ss


class AppDB():
    def getCategories(self):
        return [
            "UNKNOWN",
            "BILLS",
            "CAR",
            "CASH",
            "INCOME",
            "OTHER",
            "PHONE",
            "RENT",
            "SCHOOL",
            "SHOPPING",
            "SUPERMARKET",
            "TAX",
            "TICKETS",
            "TRANSFER",
            "UNIVERSITY",
        ]

    def insertTransactions(self, df):
        raise NotImplementedError
    def getEnergyData(self):
        raise NotImplementedError

class MockDB(AppDB):
    def insertTransactions(self, df):
        print(df)

    def getEnergyData(self):
        l=60
        data = {
            "address": [ss.energy["address"]] * l, 
            "date": pd.date_range(datetime.datetime.today(), periods=l, freq="M").tolist(),
            "electricity": [x * l * x for x in range(l)],
            "gas": [x * l * (x+5) for x in range(l)] 
        }
        return pd.DataFrame(data)

class MySQL(AppDB):
    def __init__(self):
        self.engine = create_engine(f'mysql+pymysql://{ss.db["username"]}:{ss.db["password"]}@{ss.db["host"]}:{ss.db["port"]}/{ss.db["database"]}', pool_recycle=3600) #, echo=True)

        self.Base=declarative_base(self.engine)
        class Transaction(self.Base):
            """"""
            __tablename__ = ss.db["transactions_tbl"]
            __table_args__ = {'autoload': True}
        self.Transaction=Transaction

        class Energy(self.Base):
            """"""
            __tablename__ = ss.db["energy_tbl"]
            __table_args__ = {'autoload': True}
        self.Energy=Energy


    def loadSession(self):
        """"""
        metadata = self.Base.metadata
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session


#    def getCategories(self):
#        categories = []
#        for cat in self.loadSession().query(self.Transaction.Category).distinct():
#            categories.append(cat.Category)
#        return categories

    def insertTransactions(self, df):
        dfi = df.reset_index()
        dfi = dfi.drop('index', 1)
        return dfi.to_sql(ss.db["transactions_tbl"], self.engine, if_exists='append', index=False)

    def getEnergyData(self):
        session = self.loadSession()
        qry = session.query(self.Energy).filter(self.Energy.address == ss.energy["address"]).order_by(self.Energy.date.asc())
        readings = pd.read_sql(qry.statement, self.engine)
        return readings;
