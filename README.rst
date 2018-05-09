=================================
Flake8 Unittest Assertion Checker
=================================

|Build Status| |PyPI Version| |Python Versions|

``flake8-assertive`` is a `Flake8 <http://flake8.pycqa.org/>`_ extension that
encourages using more specific `unittest`_ assertions beyond just the typical
``assertEqual(a, b)`` and ``assertTrue(x)`` methods. The alternate methods
suggested by this extension perform more precise checks and provide better
failure messages than the generic methods.

+---------------------------------------+-----------------------------------+
| Original                              | Suggestion                        |
+=======================================+===================================+
| ``assertEqual(a, None)``              | ``assertIsNone(a)``               |
+---------------------------------------+-----------------------------------+
| ``assertNotEqual(a, None)``           | ``assertIsNotNone(a)``            |
+---------------------------------------+-----------------------------------+
| ``assertEqual(a, True)``              | ``assertTrue(a)``                 |
+---------------------------------------+-----------------------------------+
| ``assertEqual(a, False)``             | ``assertFalse(a)``                |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a is b)``                | ``assertIs(a, b)``                |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a is not b)``            | ``assertIsNot(a, b)``             |
+---------------------------------------+-----------------------------------+
| ``assertFalse(a is b)``               | ``assertNotIs(a, b)``             |
+---------------------------------------+-----------------------------------+
| ``assertFalse(a is not b)``           | ``assertIs(a, b)``                |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a in b)``                | ``assertIn(a, b)``                |
+---------------------------------------+-----------------------------------+
| ``assertFalse(a in b)``               | ``assertNotIn(a, b)``             |
+---------------------------------------+-----------------------------------+
| ``assertTrue(isinstance(obj, cls))``  | ``assertIsInstance(obj, cls)``    |
+---------------------------------------+-----------------------------------+
| ``assertFalse(isinstance(obj, cls))`` | ``assertNotIsInstance(obj, cls)`` |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a == b)``                | ``assertEqual(a, b)``             |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a != b)``                | ``assertNotEqual(a, b)``          |
+---------------------------------------+-----------------------------------+
| ``assertFalse(a == b)``               | ``assertNotEqual(a, b)``          |
+---------------------------------------+-----------------------------------+
| ``assertFalse(a != b)``               | ``assertEqual(a, b)``             |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a < b)``                 | ``assertLess(a, b)``              |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a <= b)``                | ``assertLessEqual(a, b)``         |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a > b)``                 | ``assertGreater(a, b)``           |
+---------------------------------------+-----------------------------------+
| ``assertTrue(a >= b)``                | ``assertGreaterEqual(a, b)``      |
+---------------------------------------+-----------------------------------+


Installation
------------

Install from PyPI using ``pip``:

.. code-block:: sh

    $ pip install flake8-assertive

The extension will be activated automatically by ``flake8``. You can verify
that it has been loaded by inspecting the ``flake8 --version`` string.

.. code-block:: sh

    $ flake8 --version
    3.5.0 (assertive: 0.1.0, ...) CPython 2.7.15 on Darwin


Error Codes
-----------

This extension adds three new `error codes`_ (using the ``A50`` prefix):

- ``A500``: prefer *{func}* for '*{op}*' comparisons
- ``A501``: prefer *{func}* for '*{op}*' expressions
- ``A502``: prefer *{func}* when checking '*{obj}*'

.. _error codes: http://flake8.pycqa.org/en/latest/user/error-codes.html
.. _unittest: https://docs.python.org/library/unittest.html

.. |Build Status| image::  https://img.shields.io/travis/jparise/flake8-assertive.svg
   :target: https://travis-ci.org/jparise/flake8-assertive
.. |PyPI Version| image:: https://img.shields.io/pypi/v/flake8-assertive.svg
   :target: https://pypi.python.org/pypi/flake8-assertive
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flake8-assertive.svg
   :target: https://pypi.python.org/pypi/flake8-assertive
