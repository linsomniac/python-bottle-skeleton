#!/usr/bin/env python
#
#  Copyright (c) 2013, Sean Reifschneider, tummy.com, ltd.
#  All Rights Reserved.

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
