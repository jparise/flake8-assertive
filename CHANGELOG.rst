Changes
=======

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
