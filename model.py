#!/usr/bin/env python
#
#  Copyright (c) 2013, Sean Reifschneider, tummy.com, ltd.
#  All Rights Reserved.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import event, Column, Integer, String, ForeignKey
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import Pool

def initdb():
    '''Initialize the database structure.'''
    from bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()

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


#  XXX Your model goes here
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    name = Column(String(length=20), nullable=False)
    full_name = Column(String(length=60), nullable=False)
    email_address = Column(String(length=60), nullable=False)

def user_by_name(name):
    from bottledbwrap import dbwrap
    db = dbwrap.session()
    user = db.query(User).filter_by(name=name).first()
    return user


#  XXX Some sample data for testing the site
def create_sample_data():
    from bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    db = dbwrap.session()

    sean = User(
            full_name='Sean Reifschneider', name='sean',
            email_address='jafo@example.com')
    db.add(sean)
    evi = User(
            full_name='Evi Nemeth', name='evi',
            email_address='evi@example.com')
    db.add(evi)
    dmr = User(
            full_name='Dennis Ritchie', name='dmr',
            email_address='dmr@example.com')
    db.add(dmr)

    db.commit()
