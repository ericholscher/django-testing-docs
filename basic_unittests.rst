.. _basic_unittests:

Introduction to Python/Django testing: Basic Unit Tests
-------------------------------------------------------


Last post we talked about how to set up and use doc tests inside of Django.
Today, in the second post of the series, we'll be talking about how to use
the other testing framework that comes with Python, unittest. unittest is a
xUnit type of testing system (JUnit from the Java world is another example)
implemented in Python. It is a much more robust solution for testing than Doc
tests, and allows for a lot more organization of code. We'll get into that in
the next post in the series, comparing unit and doc tests.

So we're going to assume that you are picking up after the previous post in
this series. If so, you should have a basic tests directory, with an
``__init__.py`` and a ``doctst.py`` file inside of it. Today we are going to
write some very basic unit tests, and figure out how to wire those into your
existing test suite.


Writing your first unit test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Making a unit test is a lot like making a Python class. As per usual, the
`Django docs`_ have lots of great information and examples. They will show
you how to do some easy stuff with your Django models. This tutorial will
mostly be about how to use unit tests inside Django, regardless of the data
at hand. So let's start with a very basic unit test.::

    import unittest

    class TestBasic(unittest.TestCase):
        "Basic tests"

        def test_basic(self):
            a = 1
            self.assertEqual(1, a)

        def test_basic_2(self):
            a = 1
            assert a == 1


This is a very basic unit test. You will notice it is just a normal
Python class. You create a class that inherits from unittest.TestCase. This
tells unittest that it is a test file. Then you simply go in and define some
functions (Note: they need to start with test so that unittest will run
them), in which you assert some conditions which are true. This allows you a
lot more flexibility in the tests.

Now if you try to run these tests, you will again not see them showing
up in your output! You need to go into your ``__init__.py`` in your tests
directory. It should now look like the following (assuming you followed part
1 of this series)::

    from unittst import *

    import doctst

    __test__ = {
        'Doctest': doctst
        }



Unit tests are a lot easier to import than doctests. You simply do a ``from
<filename> import <testnames>``. I named my unit test file ``unittst.py``,
and Python will import that from the current directory. You are importing the
test classes that you defined in your file. So I could have as easily put
``from unittest import TestBasic`` and it would work. Using the ``import *``
syntax allows us to add more tests to the file later and not have to edit it.

You can go ahead and run your tests, and see if they're being properly
imported.::

    [eric@Odin:~/EH]$ ./manage.py test mine
    Creating test database...
    Creating table auth_permission
    [Database stuff removed]
    ...
    Ran 3 tests in 0.004s

    OK


Awesome!


A couple neat features
~~~~~~~~~~~~~~~~~~~~~~

There are some neat things you can do with basic unit tests. Below I'll show
an addition to the above file, which is another test class, with a bit more
functionality.::

    class TestBasic2(unittest.TestCase):
        "Show setup and teardown"

        def setUp(self):
            self.a = 1

        def tearDown(self):
            del self.a

        def test_basic1(self):
            "Basic with setup"

            self.assertNotEqual(self.a, 2)

        def test_basic2(self):
            "Basic2 with setup"
            assert self.a != 2

        def test_fail(self):
            "This test should fail"
            assert self.a == 2


Here you see that you can define a docstring for the tests. These are used
when you are running the tests, so you have a human readable name. You'll
also notice that I've used some more assertions. The `Python docs`_ have a
full list of assertions that you can make. The ``setUp`` and ``tearDown``
methods are run before and after every test respectively. This allows you to
set up a basic context or environment inside of each of your tests. This also
insures that each of your tests do not edit the data that other tests depend
on. This is a basic tenet of testing, that each test should stand alone, and
not affect the others.

This also seems like a good time to explicitly say that all of your test
classes and files should start with test! If not, they will not be run! If
you have a test not running and everything else looks right, this is probably
your problem. Also note that they cannot be named the same thing! These will
overwrite one another with the last one being imported into the file running.
It is generally a good practice to name your tests something that is certain
to be unique. I generally tend to follow whatever naming convention I've used
for my named url patterns.

When you go ahead and run your tests, you should see one that fails (the last
one).::

    [eric@Odin:~/EH]$ ./manage.py test mine
    Creating test database...
    Creating table auth_permission
    [Database stuff removed]
    ....F.
    =====================================================
    FAIL: This test should fail
    Traceback (most recent call last):
      File "/home/eric/Python/EH/mine/tests/unittst.py", line 35, in
      test_fail
        assert self.a == 2
    AssertionError

    Ran 6 tests in 0.003s

    FAILED (failures=1)


You can see the value of unit tests here. Each test is run seperately, so you
get a nice human readable error message when it breaks. You can go ahead and
make that test pass (``self.assertFalse(self.a == 2)``). You get an OK from
your tests, and we can go on our merry way.

Now you can see for yourself that there are a lot of differences between Doc
tests and unit tests. They each serve their own purpose, and in the next post
in this series I will talk about when you should use each. Unit tests require
a little bit more up front effort; you can't just paste something out of your
Python shell and have it work. However, they give you a lot more flexibility.


.. _Django docs: http://docs.djangoproject.com/en/dev/topics/testing
    /#writing-unit-tests
.. _Python docs: http://docs.python.org/library/unittest.html#id1
