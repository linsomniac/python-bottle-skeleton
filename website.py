#!/usr/bin/env python
#
#  This implements the website logic, this is where you would do any dynamic
#  programming for the site pages and render them from templaes.
#
#  NOTE: This file will need heavy customizations.  Search for "XXX".
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

#  XXX Remove these two lines if you aren't using a database
from bottledbwrap import dbwrap
import model

from bottle import (view, TEMPLATE_PATH, Bottle, static_file, request,
        redirect, BaseTemplate, Bottle)

#  XXX Remove these lines and the next section if you aren't processing forms
from wtforms import (Form, TextField, DateTimeField, SelectField,
        PasswordField, validators)

#  XXX Form validation example
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


def build_application():
    #  XXX Define application routes in this class

    app = Bottle()

    #  Pretty much this entire function needs to be written for your

    BaseTemplate.defaults['app'] = app #  XXX Template global variable
    TEMPLATE_PATH.insert(0, 'views')   #  XXX Location of HTML templates

    #  XXX Routes to static content
    @app.route('/<path:re:favicon.ico>')
    @app.route('/static/<path:path>')
    def static(path):
        'Serve static content.'
        return static_file(path, root='static/')

    #  XXX Index page
    @app.route('/', name='index')                  #  XXX URL to page
    @view('index')                                 #  XXX Name of template
    def index():
        'A simple form that shows the date'

        import datetime

        now = datetime.datetime.now()

        #  any local variables can be used in the template
        return locals()

    #  XXX User list page
    @app.route('/users', name='user_list')        #  XXX URL to page
    @view('users')                                #  XXX Name of template
    def user_list():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.name)

        #  any local variables can be used in the template
        return locals()

    #  XXX User details dynamically-generated URL
    @app.route('/users/<username>', name='user')  #  XXX URL to page
    @view('user')                                 #  XXX Name of template
    def user_info(username):
        'A simple page from a dabase.'

        user = model.user_by_name(username)

        #  any local variables can be used in the template
        return locals()

    #  XXX A simple form example, not used on the demo site
    @app.route('/form')                           #  XXX URL to page
    @view('form')                                 #  XXX Name of template
    def static_form():
        'A simple form processing example'

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.name.data)

        #  any local variables can be used in the template
        return locals()

    #  XXX Create a new user, form processing, including GET and POST
    @app.get('/new-user', name='user_new')        #  XXX GET URL to page
    @app.post('/new-user')                        #  XXX POST URL to page
    @view('user-new')                             #  XXX Name of template
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

        #  any local variables can be used in the template
        return locals()

    #  REQUIRED: return the application handle herre
    return app
