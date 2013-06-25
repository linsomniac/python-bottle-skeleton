Python Bottle Skeleton
======================

This is a skeleton web application using the bottle framework.  It includes
examples of everything you need to create a web application using bottle:

    Form processing.

    SQLAlchemy for Database.

    Testing.

    WSGI interface to Apache.

Usage
-----

To use:

  * Check out repository.

  * For Database: Install SQLAlchemy (Ubuntu: "sudo apt-get install
    python-sqlalchemy python-sqlalchemy-ext").

  * For Forms: Install WTForms (Ubuntu: "sudo apt-get install python-wtforms").

  * Modify "website.py" to create your routes and code associated with
    them.

Setting up Apache:

  * Install mod_wsgi and Apache (Ubuntu:"sudo apt-get install
    libapache2-mod-wsgi").

  * Rename "conf/application.conf", update places where it has "XXX", and put
    it on your Apache config directory ("/etc/apache2/sites-enabled",
    "/etc/httpd/conf.d").
