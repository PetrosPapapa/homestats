from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import appsecrets as ss


class TransactionDB():
    def getCategories(self):
        raise NotImplementedError

class MockTransactionDB(TransactionDB):
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

class MySQLTransactionDB(TransactionDB):
    def __init__(self):
        self.engine = create_engine(f'mysql+pymysql://{ss.db["username"]}:{ss.db["password"]}@{ss.db["host"]}:{ss.db["port"]}/{ss.db["database"]}', pool_recycle=3600) #, echo=True)
        self.Base=declarative_base(self.engine)
        class Transaction(self.Base):
            """"""
            __tablename__ = 'transactions'
            __table_args__ = {'autoload': True}
        self.Transaction=Transaction

    def loadSession(self):
        """"""
        metadata = self.Base.metadata
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session


    def getCategories(self):
        categories = []
        for cat in self.loadSession().query(self.Transaction.Category).distinct():
            categories.append(cat.Category)
        return categories

