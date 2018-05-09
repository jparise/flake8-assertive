import ast
import re
import unittest

from flake8_assertive import Checker


def make_linter(code, path='example.py'):
    tree = ast.parse(code, path)
    return Checker(tree, path)


class TestChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Always use Python 3's `assetRegex` method name.
        if not hasattr(cls, 'assertRegex'):
            cls.assertRegex = cls.assertRegexpMatches

    def check(self, code, error=None, pattern=None):
        linter = make_linter(code)
        result = next(linter.run(), None)
        if error is None:
            return self.assertIsNone(result)

        self.assertIsNotNone(result, "expected {0} error".format(error))
        self.assertEqual(error, result[2].split(' ')[0])
        if pattern is not None:
            self.assertRegex(result[2], re.escape(pattern))

    def test_assertequal_none(self):
        self.check("self.assertEqual(None, 1)", "A502", "assertIsNone()")
        self.check("self.assertEqual(1, None)", "A502", "assertIsNone()")

    def test_assertequal_true(self):
        self.check("self.assertEqual(True, a)", "A502", "assertTrue()")
        self.check("self.assertEqual(a, True)", "A502", "assertTrue()")

    def test_assertequal_false(self):
        self.check("self.assertEqual(False, a)", "A502", "assertFalse()")
        self.check("self.assertEqual(a, False)", "A502", "assertFalse()")

    def test_assertnotequal_none(self):
        self.check("self.assertNotEqual(None, 1)", "A502", "assertIsNotNone()")
        self.check("self.assertNotEqual(1, None)", "A502", "assertIsNotNone()")

    def test_assertnotequal_true(self):
        self.check("self.assertNotEqual(True, a)", "A502", "assertFalse()")
        self.check("self.assertNotEqual(a, True)", "A502", "assertFalse()")

    def test_assertnotequal_false(self):
        self.check("self.assertNotEqual(False, a)", "A502", "assertTrue()")
        self.check("self.assertNotEqual(a, False)", "A502", "assertTrue()")

    def test_asserttrue_is(self):
        self.check("self.assertTrue(True is True)", "A501", "assertIs()")
        self.check(
            "self.assertTrue(True is not False)", "A501", "assertIsNot()")

    def test_assertfalse_is(self):
        self.check("self.assertFalse(True is False)", "A501", "assertIsNot()")
        self.check("self.assertFalse(True is not True)", "A501", "assertIs()")

    def test_asserttrue_in(self):
        self.check("self.assertTrue(1 in [1])", "A501", "assertIn()")
        self.check("self.assertTrue(1 not in [2])", "A501", "assertNotIn()")

    def test_assertfalse_in(self):
        self.check("self.assertFalse(1 in [2])", "A501", "assertNotIn()")
        self.check("self.assertFalse(1 not in [1])", "A501", "assertIn()")

    def test_asserttrue_equal(self):
        self.check("self.assertTrue(1 == 1)", "A500", "assertEqual() for '=='")
        self.check(
            "self.assertTrue(1 != 1)", "A500", "assertNotEqual() for '!='")

    def test_asserttrue_less(self):
        self.check("self.assertTrue(0 < 1)", "A500", "assertLess() for '<'")
        self.check(
            "self.assertTrue(0 <= 1)", "A500", "assertLessEqual() for '<='")

    def test_asserttrue_greater(self):
        self.check("self.assertTrue(1 > 0)", "A500", "assertGreater() for '>'")
        self.check(
            "self.assertTrue(1 >= 0)", "A500", "assertGreaterEqual() for '>='")

    def test_asserttrue_isinstance(self):
        self.check(
            "self.assertTrue(isinstance(True, bool))",
            "A501", "assertIsInstance() for 'isinstance()'")

    def test_assertfalse_isinstance(self):
        self.check(
            "self.assertFalse(isinstance(True, bool))",
            "A501", "assertNotIsInstance() for 'isinstance()'")

    def test_assertfalse_equal(self):
        self.check(
            "self.assertFalse(1 == 1)", "A500", "assertNotEqual() for '=='")
        self.check(
            "self.assertFalse(1 != 0)", "A500", "assertEqual() for '!='")
