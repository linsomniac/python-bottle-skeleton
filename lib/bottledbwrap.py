#!/usr/bin/env python
#
#  See the README.md for more information
#
#  Written by Sean Reifschneider <jafo@jafo.ca>, 2013
#
#  Part of the python-bottle-skeleton project at:
#
#      https://github.com/linsomniac/python-bottle-skeleton
#
#  I hereby place this work, python-bottle-wrapper, into the public domain.

'''Database connection wrapper for python-bottle-skeleton.
'''

from model import Base


class DbWrapper:
    '''Wrapper around SQLAlchemy and model.  For example:

        dbwrap = DbWrapper()
        session = dbwrap.session()
        session.add(Metadata())
        session.commit()

    Or:

        dbwrap = DbWrapper()
        session = dbwrap.connect(connect='sqlite:///:memory:', echo=True)
        session.add(Metadata())
        session.commit()
        session2 = dbwrap.session()   # uses connection from above
        session2.add(Host([...]))
        session2.commit()
    '''

    def __init__(self):
        self.close()

    def session(self):
        '''Get a session handle.
        This returns a new Session() handle, calling `connect()` if it has
        not previously been called.  Note: The `connect()` method also
        returns a Session(), for convenience.  `connect()` will always make
        a new SQL connection from the ground up.  Call `session()` if you
        do not need to specify connection options.

        :rtype: SQLAlchemy Session() instance.
        '''

        if not self.Sessions:
            self.connect()

        return self.Sessions()

    def connect(self, path_list=None, connect=None, echo=False):
        '''Create a session to the database.
        The database connect string is read from a configuration file, and
        a SQLAlchemy Session() to that database is returned.

        :param list path_list: (Default None)  A list of file names to check
        for the database connect string.  If `path_list` is `None`, then a
        standard list of paths is used.  If DBCREDENTIALS environment
        variable is set, that is used for the credentials file.  If
        DBCREDENTIALSTR is set, that string is used to connect to the
        database.

        The `path_list` is walked, stopping when the listed file exists,
        and that is loaded as Python code.  Any files after the first
        existing file are ignored.

        :param str connect: (Default None)  If a string, the `path_list`
        will be ignored and this string will be used as the connect string.

        :param bool echo: (Default False)  Are database commands echoed
        to stdout?

        :rtype: SQLAlchemy Session() instance.
        '''
        import os
        import sys

        if self.Sessions:
            return

        if path_list is None:
            if 'DBCREDENTIALS' in os.environ:
                path_list = [
                        os.path.expanduser(os.environ['DBCREDENTIALS'])]
            else:
                path_list = (
                        [
                            'conf/dbcredentials',
                            'dbcredentials',
                        ])

        if not connect and os.environ.get('DBCREDENTIALSTR'):
            connect = os.environ.get('DBCREDENTIALSTR')

        if connect is None:
            namespace = {}
            for path in path_list:
                if not os.path.exists(path):
                    continue
                execfile(path, {}, namespace)
                break
            else:
                sys.stderr.write(
                        'ERROR: Unable to find "dbcredentials" file.\n')
                sys.stderr.write('Tried: "%s"\n' % repr(path_list))
                sys.exit(1)
            if not 'connect' in namespace:
                sys.stderr.write(
                        'ERROR: Could not find "connect" value in "%s"\n' % path)
                sys.exit(1)
            connect = namespace['connect']

        from sqlalchemy import engine_from_config

        self.engine = engine_from_config(
                {
                    'echo': echo,
                    'max_overflow': 100,
                    'pool_size': 5,
                }, url=connect)

        self.Base = Base        # Base is from model
        self.Base.metadata.bind = self.engine

        from sqlalchemy.orm import sessionmaker
        self.Sessions = sessionmaker(bind=self.engine)

        return self.Sessions()

    def close(self):
        '''Clean up database object, return to brand-new state.

        :rtype: None
        '''
        self.engine = None
        self.Base = None
        self.Sessions = None


dbwrap = DbWrapper()
