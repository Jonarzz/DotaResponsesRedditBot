"""Module to test the bot and parser. All test should be placed in `tests` folder and python filename should start with
`test_`.
"""
import sys
import unittest

__author__ = 'MePsyDuck'

suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
result = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
sys.exit(result)
