=================================
Flake8 Unittest Assertion Checker
=================================

|PyPI Version| |Python Versions|

``flake8-assertive`` is a `Flake8 <https://flake8.pycqa.org/>`_ extension that
encourages using richer, more specific `unittest`_ assertions beyond just the
typical ``assertEqual(a, b)`` and ``assertTrue(x)`` methods. The suggested
methods perform more precise checks and provide better failure messages than
the generic methods.

+------------------------------------------+-----------------------------------+------+
| Original                                 | Suggestion                        | Code |
+==========================================+===================================+======+
| ``assertTrue(a == b)``                   | ``assertEqual(a, b)``             | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a != b)``                   | ``assertNotEqual(a, b)``          | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a == b)``                  | ``assertNotEqual(a, b)``          | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a != b)``                  | ``assertEqual(a, b)``             | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a < b)``                    | ``assertLess(a, b)``              | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a <= b)``                   | ``assertLessEqual(a, b)``         | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a > b)``                    | ``assertGreater(a, b)``           | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a >= b)``                   | ``assertGreaterEqual(a, b)``      | A500 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a is b)``                   | ``assertIs(a, b)``                | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a is not b)``               | ``assertIsNot(a, b)``             | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a is b)``                  | ``assertNotIs(a, b)``             | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a is not b)``              | ``assertIs(a, b)``                | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a in b)``                   | ``assertIn(a, b)``                | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a not in b)``               | ``assertNotIn(a, b)``             | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a in b)``                  | ``assertNotIn(a, b)``             | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(isinstance(a, b))``         | ``assertIsInstance(a, b)``        | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(isinstance(a, b))``        | ``assertNotIsInstance(a, b)``     | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertEqual(a, round(b, x))``          | ``assertAlmostEqual(a, b, x)``    | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertAlmostEqual(a, round(b, x))``    | ``assertAlmostEqual(a, b, x)``    | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertNotEqual(a, round(b, x))``       | ``assertNotAlmostEqual(a, b, x)`` | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertNotAlmostEqual(a, round(b, x))`` | ``assertNotAlmostEqual(a, b, x)`` | A501 |
+------------------------------------------+-----------------------------------+------+
| ``assertEqual(a, None)``                 | ``assertIsNone(a)``               | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertNotEqual(a, None)``              | ``assertIsNotNone(a)``            | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a is None)``                | ``assertIsNone(a)``               | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a is not None)``            | ``assertIsNotNone(a)``            | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a is None)``               | ``assertIsNotNone(a)``            | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a is not None)``           | ``assertIsNone(a)``               | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertEqual(a, True)``                 | ``assertTrue(a)``                 | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertEqual(a, False)``                | ``assertFalse(a)``                | A502 |
+------------------------------------------+-----------------------------------+------+
| ``assertEquals(a, b)``                   | ``assertEqual(a, b)``             | A503 |
+------------------------------------------+-----------------------------------+------+
| ``assertNotEquals(a, b)``                | ``assertNotEqual(a, b)``          | A503 |
+------------------------------------------+-----------------------------------+------+
| ``assertAlmostEquals(a, b, x)``          | ``assertAlmostEqual(a, b, x)``    | A503 |
+------------------------------------------+-----------------------------------+------+
| ``assertNotAlmostEquals(a, b, x)``       | ``assertNotAlmostEqual(a, b, x)`` | A503 |
+------------------------------------------+-----------------------------------+------+
| ``assertTrue(a, b)``                     | ``assertTrue(a, msg=b)``          | A504 |
+------------------------------------------+-----------------------------------+------+
| ``assertFalse(a, b)``                    | ``assertFalse(a, msg=b)``         | A504 |
+------------------------------------------+-----------------------------------+------+

Note that some suggestions are normalized forms of the original, such as when
a double-negative is used (``assertFalse(a != b)`` → ``assertEqual(a, b)``).
There aren't suggestions for things like ``assertFalse(a > b)``, which may or
may not be equivalent to ``assertLessEqual(a, b)``.


Installation
------------

Install from PyPI using ``pip``:

.. code-block:: sh

    $ pip install flake8-assertive

The extension will be activated automatically by ``flake8``. You can verify
that it has been loaded by inspecting the ``flake8 --version`` string.

.. code-block:: sh

    $ flake8 --version
    4.0.1 (assertive: 2.1.0, ...) CPython 3.9.10 on Darwin


Error Codes
-----------

This extension adds three new `error codes`__ (using the ``A50`` prefix):

- ``A500``: prefer *{func}* for '*{op}*' comparisons
- ``A501``: prefer *{func}* for '*{op}*' expressions
- ``A502``: prefer *{func}* instead of comparing to *{obj}*
- ``A503``: use *{func}* instead of the deprecated *{name}*
- ``A504``: prefer the 'msg=' kwarg for *{func}* diagnostics

.. __: https://flake8.pycqa.org/en/latest/user/error-codes.html

Configuration
-------------

Configuration values are specified in the ``[flake8]`` section of your `config
file`_ or as command line arguments (e.g. ``--assertive-snakecase``).

- ``assertive-snakecase``: suggest snake_case assert method names
  (e.g. ``assert_true()``) instead of the standard names (e.g. ``assertTrue()``)
- ``assertive-test-pattern``: `fnmatch`_ pattern for identifying unittest test
  files (and all other files will be skipped)

.. _fnmatch: https://docs.python.org/library/fnmatch.html
.. _unittest: https://docs.python.org/library/unittest.html
.. _config file: https://flake8.pycqa.org/en/latest/user/configuration.html

Caveats
-------

There are some specific cases when the suggestion might not match the intent
of the original.

Testing the equality operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``assertEqual()`` won't use the ``==`` operator if the comparison has been
delegated to a `type-specific equalilty function`__. By default, this is the
case for strings, sequences, lists, tuples, sets, and dicts.

.. __: https://docs.python.org/3/library/unittest.html#unittest.TestCase.addTypeEqualityFunc

If your intent is to specifically test the ``==`` operator, consider writing
the assertion like this instead:

.. code-block:: python

    assertIs(a == b, True)

This approach has the benefit of verifying that the type's ``__eq__``
implementation returns a boolean value. Unfortunately, it also has the
downside of reporting the result of ``a == b`` on failure instead of the
values of ``a`` and ``b``.

Suggested by: `Serhiy Storchaka <https://twitter.com/SerhiyStorchaka>`_

.. |PyPI Version| image:: https://img.shields.io/pypi/v/flake8-assertive.svg
   :target: https://pypi.python.org/pypi/flake8-assertive
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flake8-assertive.svg
   :target: https://pypi.python.org/pypi/flake8-assertive
