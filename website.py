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
    username = TextField('Username', [validators.Length(min=4, max=25)])
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

    @app.route('/')
    @view('index')
    def index():
        'A simple form that shows the date'

        import datetime

        date = datetime.datetime.now()

        return locals()

    @app.route('/users')
    @view('users')
    def index():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.username)

        return locals()

    @app.route('/form')
    @view('form')
    def static_form():
        'A simple form processing example'

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.username.data)
        return locals()

    @app.route('/database_form')
    @view('form')
    def database_form():
        'A sample of interacting with a form and a dabase.'

        db = dbwrap.session()

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.username.data)
        return locals()
