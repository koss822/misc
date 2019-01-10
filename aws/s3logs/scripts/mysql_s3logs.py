#!/usr/bin/env python3

# /usr/local/s3logs/mysql_s3logs.py

import sqlalchemy, base, hashlib
from sqlalchemy.ext.declarative import *
from sqlalchemy import Column, Integer, String, DateTime

mysql_user = 'MYSQL_USER'
mysql_db = 'MYSQL_DB'
mysql_pass = 'MYSQL_PASS'

Base = declarative_base()


class s3logs(Base):
    __tablename__ = 'logs'
    id = Column(String, primary_key=True)
    repository = Column(String)
    date = Column(DateTime)
    ip = Column(String)
    item = Column(String)
    referer = Column(String)
    agent = Column(String)

    def __init__(self, id, repository, date, ip, item, referer, agent):
        self.id = id
        self.repository = repository
        self.date = date
        self.ip = ip
        self.item = item
        self.referer = referer
        self.agent = agent

def insert(id, repository, date, ip, item, referer, agent):
    engine = sqlalchemy.create_engine('mysql://%s:%s@localhost/%s' % (mysql_user, mysql_pass, mysql_db))
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    session.add(s3logs(id, repository, date, ip, item, referer, agent))
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
