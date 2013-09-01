Python Bottle Skeleton
======================

This is a skeleton web application using the bottle framework.

While bottle is an extremely simple framework, there are many things that you
probably will need to figure out if developing even fairly simple websites
using it.  This provides many examples to get you started quickly with bottle.

It includes examples of things you need to create a web application
using bottle:

  * Form processing.

  * SQLAlchemy for Database.

  * Testing.

  * WSGI interface to Apache and standalone test server.

  * Templating including standard site page template.

Usage
-----

To try out:

  * Install python-sqlalchemy python-sqlalchemy-ext python-wtforms

  * Run: `DBCREDENTIALSTR=sqlite:///:memory: PYTHONPATH=lib python app-controller test-server`

  * In a browser go to http://127.0.0.1:8080/

To use:

  * Check out repository.

  * For Database: Install SQLAlchemy (Ubuntu: `sudo apt-get install
    python-sqlalchemy python-sqlalchemy-ext`).

  * For Forms: Install WTForms (Ubuntu: `sudo apt-get install python-wtforms`).

  * Modify "website.py" to create your routes and code associated with
    them.

Setting up Apache:

  * Install mod\_wsgi and Apache (Ubuntu:`sudo apt-get install
    libapache2-mod-wsgi`).

  * Rename "conf/application.conf", update places where it has "XXX", and put
    it on your Apache config directory ("/etc/apache2/sites-enabled",
    "/etc/httpd/conf.d").

Structure of Project
--------------------

There are the following components to the project:

  * `app-controller`: This is a both a WSGI app and a shell script.  It can
    be used as your WSGI application, but it also can be run with:

      * "test-server" to start a stand-alone server.

      * "initdb" to load your base database schema,

      * "load-test-data" to to populate any test data you have defined in your
        model.

  * `model.py`: Your database model definition, via SQLAlchemy.

  * `website.py`: The website controller code.  This is where most of the site
    programming happens, this includes the URL routing, form processing, and
    other code for the site.

  * `static`: Any files put in here are served as static content, such as your
    favicon.  You need to define routes to these static files in `website.py`

  * `views`: These are your website pages.  There is a site template in
    `layout.html`, and an example of form processing in `user-new.html`.

  * `lib`: Library files used by the site.

    * `bottle.py`: This is a version of bottle that I used to develop this
      skeleton, mostly as a "batteries included" move.  You may want to pick
      up a newer copy, but this skeleton is tested against the version here.

    * `bottledbwrap.py`: See below in the "About bottledbwrap" section.

About bottledbwrap
------------------

This is a library I've developed over the years for some of my database
applications.  It's mostly a thin layer on top of SQLAlchemy that can
pull database credentials from one of several files, or some environment
variables.

Largely it's about storing database credentials outside of your project, so
they don't get checked in to your version control or published on github.

You can provide database credentials in the following ways:

  * In a file called "dbcredentials" in the current directory or the "conf"
    sub-directory.

  * In the file specified by the environment variable "DBCREDENTIALS".

  * Directly in the environment variable "DBCREDENTIALSSTR".
