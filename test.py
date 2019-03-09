import unittest

suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
