import sys
import unittest

suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
result = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
sys.exit(result)
