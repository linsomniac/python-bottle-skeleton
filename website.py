#!/usr/bin/env python
#
#  Copyright (c) 2013, Sean Reifschneider, tummy.com, ltd.
#  All Rights Reserved.

from bottledbwrap import dbwrap
import model
from bottle import (view, debug, TEMPLATE_PATH, Bottle, static_file, request,
        redirect)
from wtforms import (Form, TextField, DateTimeField, SelectField,
        PasswordField, validators)


def web_interface():
    app = Bottle()
    debug(True)
    TEMPLATE_PATH.insert(0, '/path-to/views')

    routes(app)

    return app


#  Form validation example
class NewUserFormProcessor(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    full_name = TextField('Full Name', [validators.Length(min=4, max=60)])
    email_address = TextField(
            'Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField(
            'New Password',
            [validators.Required(),
                validators.EqualTo('confirm',
                    message='Passwords must match')
            ])
    confirm = PasswordField('Repeat Password')

def routes(app):
    #  XXX Define application routes in this class
    @app.route('/<path:re:favicon.ico>')
    @app.route('/static/<path:path>')
    def static(path):
        'Serve static content.'
        return static_file(path, root='static/')

    @app.route('/', name='index')
    @view('index')
    def index():
        'A simple form that shows the date'

        import datetime

        now = datetime.datetime.now()

        return dict(locals().items() + [('app', app)])

    @app.route('/users', name='user_list')
    @view('users')
    def user_list():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.name)

        return dict(locals().items() + [('app', app)])

    @app.route('/users/<username>', name='user')
    @view('user')
    def user_info(username):
        'A simple page from a dabase.'

        user = model.user_by_name(username)

        return dict(locals().items() + [('app', app)])

    @app.route('/form')
    @view('form')
    def static_form():
        'A simple form processing example'

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.name.data)

        return dict(locals().items() + [('app', app)])

    @app.get('/new-user', name='user_new')
    @app.post('/new-user')
    @view('user-new')
    def new_user():
        'A sample of interacting with a form and a database.'

        form = NewUserFormProcessor(request.forms.decode())

        if request.method == 'POST' and form.validate():
            db = dbwrap.session()

            sean = model.User(
                    full_name=form.full_name.data, name=form.name.data,
                    email_address=form.email_address.data)
            db.add(sean)
            db.commit()

            redirect(app.get_url('user', username=form.name.data))

        return dict(locals().items() + [('app', app)])
