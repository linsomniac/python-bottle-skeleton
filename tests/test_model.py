#!/usr/bin/env python
#
#  Test of the database model.
#
#  See the sections marked with "XXX" to customize for your application.
#  Or remove this file and references to "model" if you aren't using a
#  database.
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

import sys
sys.path.append('..')
sys.path.append('../lib')
import model

import unittest

from bottledbwrap import dbwrap


class TestModel(unittest.TestCase):
	@classmethod
	def setUp(self):
		dbwrap.connect(connect='sqlite:///:memory:')
		dbwrap.Base.metadata.create_all()

		db = dbwrap.session()
		model.create_sample_data()
		self.db = db

	@classmethod
	def tearDown(self):
		self.db.close()

	def testModelInteraction(self):
		db = self.db

		self.assertEqual(len(list(db.query(model.User))), 3)

		self.assertFalse(model.user_by_name('cray'))
		self.assertTrue(model.user_by_name('sean'))


if __name__ == '__main__':
	print unittest.main()
