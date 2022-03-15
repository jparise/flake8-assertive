# Copyright (c) 2018-present Jon Parise <jon@indelible.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Flake8 extension that encourages using more specific unittest assertions."""

import ast
import fnmatch
import re

__all__ = ['Checker']
__version__ = '2.1.0'


# Python 3.4 introduced `ast.NameConstant` for `None`, `True`, and `False`.
if hasattr(ast, 'NameConstant'):
    def is_constant(node, obj):
        return isinstance(node, ast.NameConstant) and node.value is obj
else:
    def is_constant(node, obj):
        return isinstance(node, ast.Name) and node.id == str(obj)


def is_function_call(node, name):
    return (isinstance(node, ast.Call) and
            isinstance(node.func, ast.Name) and
            node.func.id == name)


def is_assert_method_call(node):
    return (isinstance(node, ast.Call) and
            isinstance(node.func, ast.Attribute) and
            node.func.attr.startswith('assert'))


def args(node):
    for arg in node.args:
        yield arg
    for arg in node.keywords:
        yield arg.value


def wrap_deprecated(func, name):
    """Return a check function for a deprecated assert method call.

    If the `assertive-deprecated` option has been enabled and the wrapped
    check function doesn't yield any errors of its own, this function will
    yield an A503 error that includes the new name of the deprecated method.
    """
    def wrapper(self, node):
        for error in func(self, node):
            yield error
        else:
            yield self.error(node, 'A503', func=name, name=node.func.attr)
    return wrapper


class Checker(object):
    """Unittest assert method checker"""

    name = 'assertive'
    version = __version__
    pattern = None
    snakecase = False

    A500 = "prefer {func}() for '{op}' comparisons"
    A501 = "prefer {func}() for '{op}' expressions"
    A502 = "prefer {func}() instead of comparing to {obj}"
    A503 = "use {func}() instead of the deprecated {name}()"
    A504 = "prefer the 'msg=' kwarg for {func}() diagnostics"

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--assertive-snakecase',
            help="Use snake_case assert method names ('assert_true()')",
            action='store_true',
            default=False,
            parse_from_config=True)
        parser.add_option(
            '--assertive-test-pattern',
            help="fnmatch() pattern for identifying unittest test files",
            default=None,
            parse_from_config=True)

    @classmethod
    def parse_options(cls, options):
        cls.snakecase = options.assertive_snakecase
        cls.pattern = options.assertive_test_pattern

    def error(self, node, code, func, **kwargs):
        if self.snakecase:
            func = re.sub(r'([A-Z])', r'_\1', func).lower()
        message = code + ' ' + getattr(self, code).format(func=func, **kwargs)
        return (node.lineno, node.col_offset, message, self)

    def run(self):
        # Skip files that don't match a configured pattern.
        if self.pattern and not fnmatch.fnmatch(self.filename, self.pattern):
            return

        # Visit all of the assert method calls in the tree.
        for node in ast.walk(self.tree):
            if is_assert_method_call(node):
                name = node.func.attr.lower().replace('_', '')
                func = getattr(self, 'check_' + name, None)
                if func is not None:
                    for error in func(node):
                        yield error

    def check_assertequal(self, node):
        if any(arg for arg in args(node) if is_constant(arg, None)):
            yield self.error(node, 'A502', 'assertIsNone', obj=None)
        elif any(arg for arg in args(node) if is_constant(arg, True)):
            yield self.error(node, 'A502', 'assertTrue', obj=True)
        elif any(arg for arg in args(node) if is_constant(arg, False)):
            yield self.error(node, 'A502', 'assertFalse', obj=False)
        elif any(arg for arg in args(node) if is_function_call(arg, 'round')):
            yield self.error(node, 'A501',
                             'built-in rounding of assertAlmostEqual',
                             op='round')

    def check_assertalmostequal(self, node):
        if any(arg for arg in args(node) if is_function_call(arg, 'round')):
            yield self.error(node, 'A501',
                             'built-in rounding of assertAlmostEqual',
                             op='round')

    def check_assertnotequal(self, node):
        if any(arg for arg in args(node) if is_constant(arg, None)):
            yield self.error(node, 'A502', 'assertIsNotNone', obj=None)
        elif any(arg for arg in args(node) if is_constant(arg, True)):
            yield self.error(node, 'A502', 'assertFalse', obj=True)
        elif any(arg for arg in args(node) if is_constant(arg, False)):
            yield self.error(node, 'A502', 'assertTrue', obj=False)
        elif any(arg for arg in args(node) if is_function_call(arg, 'round')):
            yield self.error(node, 'A501',
                             'built-in rounding of assertNotAlmostEqual',
                             op='round')

    def check_assertnotalmostequal(self, node):
        if any(arg for arg in args(node) if is_function_call(arg, 'round')):
            yield self.error(node, 'A501',
                             'built-in rounding of assertNotAlmostEqual',
                             op='round')

    def check_asserttrue(self, node):
        if len(node.args) > 1:
            yield self.error(node, 'A504', 'assertTrue')
        arg = next(args(node), None)
        if arg and isinstance(arg, ast.Compare) and len(arg.ops) == 1:
            op = arg.ops[0]
            if isinstance(op, ast.In):
                yield self.error(node, 'A501', 'assertIn', op='in')
            elif isinstance(op, ast.NotIn):
                yield self.error(node, 'A501', 'assertNotIn', op='in')
            elif isinstance(op, ast.Is):
                if is_constant(arg.comparators[0], None):
                    yield self.error(node, 'A502', 'assertIsNone', obj=None)
                else:
                    yield self.error(node, 'A501', 'assertIs', op='is')
            elif isinstance(op, ast.IsNot):
                if is_constant(arg.comparators[0], None):
                    yield self.error(node, 'A502', 'assertIsNotNone', obj=None)
                else:
                    yield self.error(node, 'A501', 'assertIsNot', op='is')
            elif isinstance(op, ast.Eq):
                yield self.error(node, 'A500', 'assertEqual', op='==')
            elif isinstance(op, ast.NotEq):
                yield self.error(node, 'A500', 'assertNotEqual', op='!=')
            elif isinstance(op, ast.Lt):
                yield self.error(node, 'A500', 'assertLess', op='<')
            elif isinstance(op, ast.LtE):
                yield self.error(node, 'A500', 'assertLessEqual', op='<=')
            elif isinstance(op, ast.Gt):
                yield self.error(node, 'A500', 'assertGreater', op='>')
            elif isinstance(op, ast.GtE):
                yield self.error(node, 'A500', 'assertGreaterEqual', op='>=')
        elif is_function_call(arg, 'isinstance'):
            yield self.error(
                node, 'A501', 'assertIsInstance', op='isinstance()')

    def check_assertfalse(self, node):
        if len(node.args) > 1:
            yield self.error(node, 'A504', 'assertFalse')
        arg = next(args(node), None)
        if arg and isinstance(arg, ast.Compare) and len(arg.ops) == 1:
            op = arg.ops[0]
            if isinstance(op, ast.In):
                yield self.error(node, 'A501', 'assertNotIn', op='in')
            elif isinstance(op, ast.NotIn):
                yield self.error(node, 'A501', 'assertIn', op='in')
            elif isinstance(op, ast.Is):
                if is_constant(arg.comparators[0], None):
                    yield self.error(node, 'A502', 'assertIsNotNone', obj=None)
                else:
                    yield self.error(node, 'A501', 'assertIsNot', op='is')
            elif isinstance(op, ast.IsNot):
                if is_constant(arg.comparators[0], None):
                    yield self.error(node, 'A502', 'assertIsNone', obj=None)
                else:
                    yield self.error(node, 'A501', 'assertIs', op='is')
            elif isinstance(op, ast.Eq):
                yield self.error(node, 'A500', 'assertNotEqual', op='==')
            elif isinstance(op, ast.NotEq):
                yield self.error(node, 'A500', 'assertEqual', op='!=')
        elif is_function_call(arg, 'isinstance'):
            yield self.error(
                node, 'A501', 'assertNotIsInstance', op='isinstance()')

    check_assertequals = wrap_deprecated(
        check_assertequal,
        'assertEqual')

    check_assertnotequals = wrap_deprecated(
        check_assertnotequal,
        'assertNotEqual')

    check_assertalmostequals = wrap_deprecated(
        check_assertalmostequal,
        'assertAlmostEqual')

    check_assertnotalmostequals = wrap_deprecated(
        check_assertnotalmostequal,
        'assertNotAlmostEqual')
