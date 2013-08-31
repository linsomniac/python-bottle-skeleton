#!/usr/bin/env python
#
#  Copyright (c) 2013, Sean Reifschneider, tummy.com, ltd.
#  All Rights Reserved.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import event, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import Pool
import datetime
from bottledbwrap import dbwrap
import model

def initdb():
    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    model.create_sample_data(dbwrap.session())

def create_sample_current_oncall():
    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    db = dbwrap.session()
    model.create_sample_data(db)

    sean = model.User(
            full_name='Sean Reifschneider', username='sean',
            email_address='jafo@example.com')
    db.add(sean)
    evi = model.User(
            full_name='Evi Nemeth', username='evi',
            email_address='evi@example.com')
    db.add(evi)
    dmr = model.User(
            full_name='Dennis Ritchie', username='dmr',
            email_address='dmr@example.com')
    db.add(dmr)

    db.commit()

@event.listens_for(Pool, 'checkout')
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    '''Ping a database connection before using it to make sure it is still
    alive.'''
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute('SELECT 1')
    except:
        # optional - dispose the whole pool instead of invalidating separately
        # connection_proxy._pool.dispose()

        # pool will try connecting again up to three times before raising.
        raise DisconnectionError()
    cursor.close()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    username = Column(String(length=20), nullable=False)
    email_address = Column(String(length=60), nullable=False)
    crypted_password = Column(String(length=200))
