import ast
import re
import unittest

from flake8_assertive import Checker


class TestChecks(unittest.TestCase):
    def tearDown(self):
        Checker.pattern = None
        Checker.snakecase = False

    def check(self, code, expected=None, pattern=None, filename="test.py"):
        tree = ast.parse(code, filename)
        checker = Checker(tree, filename)
        error = next(checker.run(), None)

        if expected is None:
            return self.assertIsNone(error)

        self.assertIsNotNone(error, "expected {0} error".format(expected))
        self.assertEqual(expected, error[2].split(" ")[0])
        if pattern is not None:
            self.assertRegex(error[2], re.escape(pattern))

    def test_assertequal_none(self):
        self.check("self.assertEqual(None, 1)", "A502", "assertIsNone()")
        self.check("self.assertEqual(1, None)", "A502", "assertIsNone()")

    def test_assertequal_true(self):
        self.check("self.assertEqual(True, a)", "A502", "assertTrue()")
        self.check("self.assertEqual(a, True)", "A502", "assertTrue()")

    def test_assertequal_false(self):
        self.check("self.assertEqual(False, a)", "A502", "assertFalse()")
        self.check("self.assertEqual(a, False)", "A502", "assertFalse()")

    def test_assertequal_round(self):
        self.check(
            "self.assertEqual(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertAlmostEqual()",
        )
        self.check(
            "self.assertEqual(round(a, 2), 1.01)",
            "A501",
            "built-in rounding of assertAlmostEqual()",
        )

    def test_assertnotequal_none(self):
        self.check("self.assertNotEqual(None, 1)", "A502", "assertIsNotNone()")
        self.check("self.assertNotEqual(1, None)", "A502", "assertIsNotNone()")

    def test_assertnotequal_true(self):
        self.check("self.assertNotEqual(True, a)", "A502", "assertFalse()")
        self.check("self.assertNotEqual(a, True)", "A502", "assertFalse()")

    def test_assertnotequal_false(self):
        self.check("self.assertNotEqual(False, a)", "A502", "assertTrue()")
        self.check("self.assertNotEqual(a, False)", "A502", "assertTrue()")

    def test_assertnotequal_round(self):
        self.check(
            "self.assertNotEqual(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertNotAlmostEqual()",
        )
        self.check(
            "self.assertNotEqual(round(a, 2), 1.01)",
            "A501",
            "built-in rounding of assertNotAlmostEqual()",
        )

    def test_assertequals(self):
        self.check("self.assertEquals(True, a)", "A502", "assertTrue()")

    def test_assertnotequals(self):
        self.check("self.assertNotEquals(True, a)", "A502", "assertFalse()")

    def test_assertalmostequal_round(self):
        self.check(
            "self.assertAlmostEqual(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertAlmostEqual()",
        )
        self.check(
            "self.assertAlmostEqual(round(a, 2), 1.01)",
            "A501",
            "built-in rounding of assertAlmostEqual()",
        )

    def test_assertalmostequals(self):
        self.check(
            "self.assertEquals(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertAlmostEqual()",
        )

    def test_assertnotalmostequal_round(self):
        self.check(
            "self.assertNotAlmostEqual(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertNotAlmostEqual()",
        )
        self.check(
            "self.assertNotAlmostEqual(round(a, 2), 1.01)",
            "A501",
            "built-in rounding of assertNotAlmostEqual()",
        )

    def test_assertnotalmostequals(self):
        self.check(
            "self.assertNotAlmostEquals(1.01, round(a, 2))",
            "A501",
            "built-in rounding of assertNotAlmostEqual()",
        )

    def test_asserttrue_is(self):
        self.check("self.assertTrue(True is True)", "A501", "assertIs()")
        self.check("self.assertTrue(True is not False)", "A501", "assertIsNot()")

    def test_asserttrue_is_none(self):
        self.check("self.assertTrue(a is None)", "A502", "assertIsNone()")
        self.check("self.assertTrue(a is not None)", "A502", "assertIsNotNone()")

    def test_assertfalse_is(self):
        self.check("self.assertFalse(True is False)", "A501", "assertIsNot()")
        self.check("self.assertFalse(True is not True)", "A501", "assertIs()")

    def test_assertfalse_is_none(self):
        self.check("self.assertFalse(a is None)", "A502", "assertIsNotNone()")
        self.check("self.assertFalse(a is not None)", "A502", "assertIsNone()")

    def test_asserttrue_in(self):
        self.check("self.assertTrue(1 in [1])", "A501", "assertIn()")
        self.check("self.assertTrue(1 not in [2])", "A501", "assertNotIn()")

    def test_assertfalse_in(self):
        self.check("self.assertFalse(1 in [2])", "A501", "assertNotIn()")
        self.check("self.assertFalse(1 not in [1])", "A501", "assertIn()")

    def test_asserttrue_equal(self):
        self.check("self.assertTrue(1 == 1)", "A500", "assertEqual() for '=='")
        self.check("self.assertTrue(1 != 1)", "A500", "assertNotEqual() for '!='")

    def test_asserttrue_less(self):
        self.check("self.assertTrue(0 < 1)", "A500", "assertLess() for '<'")
        self.check("self.assertTrue(0 <= 1)", "A500", "assertLessEqual() for '<='")

    def test_asserttrue_greater(self):
        self.check("self.assertTrue(1 > 0)", "A500", "assertGreater() for '>'")
        self.check("self.assertTrue(1 >= 0)", "A500", "assertGreaterEqual() for '>='")

    def test_asserttrue_isinstance(self):
        self.check(
            "self.assertTrue(isinstance(True, bool))",
            "A501",
            "assertIsInstance() for 'isinstance()'",
        )

    def test_assertfalse_isinstance(self):
        self.check(
            "self.assertFalse(isinstance(True, bool))",
            "A501",
            "assertNotIsInstance() for 'isinstance()'",
        )

    def test_assertfalse_equal(self):
        self.check("self.assertFalse(1 == 1)", "A500", "assertNotEqual() for '=='")
        self.check("self.assertFalse(1 != 0)", "A500", "assertEqual() for '!='")

    def test_keyword_args(self):
        self.check("self.assertTrue(expr=1)", expected=None)
        self.check("self.assertTrue(expr=(True is True))", expected="A501")
        self.check("self.assertEqual(first=1, second=1)", expected=None)
        self.check("self.assertEqual(first=1, second=None)", "A502")
        self.check("self.assertEqual(first=None, second=1)", "A502")
        self.check("self.assertEqual(1, second=1)", expected=None)
        self.check("self.assertEqual(None, second=1)", "A502")

    def test_multiple_comparison_ops(self):
        self.check("self.assertTrue(1 == 1 == 1)", expected=None)
        self.check("self.assertFalse(1 == 1 == 1)", expected=None)

    def test_pattern(self):
        Checker.pattern = "[a-m]*.py"
        self.check("self.assertTrue(1 == 1)", expected="A500", filename="a.py")
        self.check("self.assertTrue(1 == 1)", expected=None, filename="z.py")

    def test_snakecase(self):
        Checker.snakecase = True
        self.check("self.assert_equal(True, a)", "A502", "assert_true()")

    def test_deprecated(self):
        self.check("self.assertEquals(True, a)", "A502", "assertTrue()")
        self.check("self.assertEquals(a, b)", "A503", "assertEqual()")

    def test_asserttrue_misuse(self):
        self.check("self.assertTrue(a, 'foo')", expected="A504")
        self.check("self.assertTrue(a, msg='foo')", expected=None)

    def test_assertfalse_misuse(self):
        self.check("self.assertFalse(a, 'foo')", expected="A504")
        self.check("self.assertFalse(a, msg='foo')", expected=None)
