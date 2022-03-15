Changes
=======

2.1.0 (2022-03-15)
------------------

* Suggest using an explicit `msg` keyword argument with ``assertTrue()`` and
  ``assertFalse()`` to avoid accidental two-argument misuse. This is controlled
  by a new error code: ``A504``

2.0.0 (2021-12-30)
------------------

* Drop support for Python 2.7 and 3.6, and add 3.10.
* Drop support for flake8 2.x versions.

1.3.0 (2020-10-12)
------------------

* Drop Python version 3.5 support and add version 3.9.

1.2.1 (2019-12-08)
------------------

* Support keyword arguments in assert method calls.

1.2.0 (2019-12-05)
------------------

* Suggest the preferred names for deprecated methods, such as
  ``assertEqual()`` instead of ``assertEquals()``.

1.1.0 (2019-06-26)
------------------

* Suggest ``assertAlmostEqual(a, b, x)`` for ``round()`` expressions like in
  ``assertEqual(a, round(b, x))`` and ``assertAlmostEqual(a, round(b, x))``
  (and similar for ``assertNotEqual()`` and ``assertNotAlmostEqual()``.
* Recognize ``assertAmostEquals()`` and ``assertNotAlmostEquals()`` as aliases
  for ``assertAlmostEqual()`` and ``assertNotAlmostEqual()``.
* Drop Python 3.4 as a supported version since it has been officially retired.

1.0.1 (2018-07-03)
------------------

* Don't make suggestions for assertions containing multiple comparison
  operations (e.g. ``assertTrue(a == b == c)``).

1.0.0 (2018-06-04)
------------------

* Suggest ``assertIsNone(a)`` for ``assertTrue(a is None)``, etc.
* Recognize ``assertEquals()`` and ``assertNotEquals()`` as aliases for
  ``assertEqual()`` and ``assertNotEqual()``.

0.9.0 (2018-05-14)
------------------

* Initial beta release
