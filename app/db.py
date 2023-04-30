from datetime import date, datetime, timedelta
import random

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import appsecrets as ss
from log import log

class AppDB():
    def getCategories(self):
        return ss.transactions["categories"]
    def getNonExpenseCategories(self):
        return ss.transactions["non_expense_categories"]
        
    def getTransactions(self):
        raise NotImplementedError
    def insertTransactions(self, df):
        raise NotImplementedError
    def getEnergyData(self):
        raise NotImplementedError
    def lastEnergyEntry(self):
        raise NotImplementedError
    def addEnergyEntry(self, entry):
        raise NotImplementedError
    def getCategoryRegexes(self):
        raise NotImplementedError


class MockDB(AppDB):

    def __init__(self):
        self.mock_months=60
        l = self.mock_months

        self.seed=1234
        random.seed(self.seed)

        ed = {
            "address": [ss.energy["address"]] * l, 
            "date": pd.date_range(date.today() - timedelta(days=(l+1) * 30), periods=l, freq="M").tolist(),
            "electricity": [x * l * x for x in range(l)],
            "gas": [x * l * (x+5) for x in range(l)] 
        }

        categs = {
            "id": range(2),
            "regex": ["foo.*", "bar.*"],
            "category": ["foo", "bar"]
        }

        self.categRegexes =  pd.DataFrame(categs)

        self.edata = pd.DataFrame(ed)
        log.debug(self.edata.head())
        log.debug(self.edata.tail())

        td = [self.randomTransaction(i) for i in range(self.mock_months * 24 * 30)]
        self.tdata = pd.DataFrame(td)
        log.debug(self.tdata.head())
        log.debug(self.tdata.tail())

    def randomTValue(self, category):
        if category == "UNKNOWN" or category == "TRANSFER":
            return 0;
        elif category == "INCOME":
            return 6000;
        else:
            return random.randrange(-1000, -10)

    def randomTransaction(self, i):
        categories = [c for c in self.getCategories() if c != "UNKNOWN" and c != "TRANSFER"]
        cat = categories[random.randrange(0,len(categories))]
        accounts = ["101010-00001234", "101010-00005678", "101010-00009101"]
        acct = accounts[random.randrange(0,len(accounts))]
        return {
            "id": i,
            "Date": (
                datetime.today() - timedelta(hours=self.mock_months * 24 * 30 - i)
            ).date(),
            "Description": "{}:{}".format(i, cat),
            "Value": self.randomTValue(cat),
            "Balance": 0,
            "Account Name": "someAccount",
            "Account Number": acct,
            "Category": cat
        }

    def getTransactions(self):
        return self.tdata
    
    def insertTransactions(self, df):
        log.debug(df)

    def getEnergyData(self):
        return self.edata

    def lastEnergyEntry(self):
        return self.edata.iloc[-1].to_dict()

    def addEnergyEntry(self, entry):
        log.debug(entry)
        self.edata = pd.concat(
            [self.edata, pd.DataFrame.from_dict([entry])], 
            ignore_index=True
        )
        log.debug(self.edata.tail())

    def getCategoryRegexes(self):
        return self.categRegexes;


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

        class CategoryRegex(self.Base):
            """"""
            __tablename__ = ss.db["categories_tbl"]
            __table_args__ = {'autoload': True}
        self.CategoryRegex=CategoryRegex

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

    def getTransactions(self):
        session = self.loadSession()
        qry = session.query(self.Transaction)
        trans = pd.read_sql(qry.statement, con=self.engine, parse_dates=['Date'])
        log.debug(trans.head())
        log.debug(trans.tail())
        return trans;

    def insertTransactions(self, df):
        dfi = df.reset_index()
        dfi = dfi.drop('index', 1)
        return dfi.to_sql(ss.db["transactions_tbl"], self.engine, if_exists='append', index=False)

    def getEnergyData(self):
        session = self.loadSession()
        qry = session.query(self.Energy).filter(self.Energy.address == ss.energy["address"]).order_by(self.Energy.date.asc())
        readings = pd.read_sql(qry.statement, con=self.engine, parse_dates=['date'])
        return readings;

    def lastEnergyEntry(self):
        session = self.loadSession()
        qry = session.query(self.Energy).filter(self.Energy.address == ss.energy["address"]).order_by(self.Energy.date.desc()).first()
        return vars(qry);

    def addEnergyEntry(self, entry):
        eentry = self.Energy(**entry)
        session = self.loadSession()
        session.add(eentry)
        session.commit()

    def getCategoryRegexes(self):
        session = self.loadSession()
        qry = session.query(self.CategoryRegex).order_by(self.CategoryRegex.corder.asc())
        cats = pd.read_sql(qry.statement, con=self.engine)
        log.debug(cats.head())
        log.debug(cats.tail())
        return cats;
