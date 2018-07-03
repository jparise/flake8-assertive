Changes
=======

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
