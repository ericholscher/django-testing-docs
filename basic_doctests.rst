.. _basic_doctests:

Introduction to Python/Django testing: Basic Doctests
-----------------------------------------------------

This is the first in a series of articles that will walk
you through how to test your Django application. These posts will focus more
on how to get things done in Django, but note that a lot of the content is
applicable to pure python as well. A lot of best practices are codified into
Django's testing framework, so that we don't have to worry about them! I will
try to point them out as we are using them through, because they are good
things to know.

The currently planned structure for this series is below. Please comment if
there is something that you think is missing, or something that I shouldn't
do. This is subject to change, a lot, as well, so your feedback will help
direct it. Also note that most or all of this content is available in the
Django and Python documentation, and I will try and point there and not re-
invent the wheel. I hope that these posts will take a more practical look,
and try to point out some pit falls and other things that are useful.



Where to start
~~~~~~~~~~~~~~

I'm assuming that you already have a project that you're working on that you
would like to test. There are two different ways of putting tests inside of
your django project. You can add a tests.py file and put your tests inside of
there. You can also define a tests/ directory and put your tests in files
inside of that. For these tutorials it is assumed that the second is the way
things are done. It makes it a lot easier when you can break your tests out
into logical files.


Doctests
~~~~~~~~

These can go in two places inside your django project. You can put them in
your models.py file, in the Docstring for your modules. This is a good way to
show usage of your models, and to provide basic testing. The `official docs`_
have some great examples of this.

The other place your Doctests can go is inside your tests directory. A
doctests file is usually pretty simple. A doctest is just a large string, so
there isn't much else to put besides a string. Usually you want to use the
triple quote, multi-line string delimiter to define them. That way your " and
's inside of your doctests don't break.::

    """
    This is my worthless test.
    >>> print "wee"
    wee
    >>> print False
    False
    """



You can go ahead and put that in a file in your ``tests/`` directory, I named
it ``doctst.py``. I didn't name it doctest, because of the python module with
the same name. It's generally good to avoid possible name overlaps. My
application that I'm writing tests for is ``mine``, because it's the code for
my website. Make sure that directory has an ``__init__.py`` as well, to
signify that it is a python module.

Now here is the tricky part; go ahead and try and run your test suite. In
your project directory run ``./manage.py test APPNAME``. It will show you
that you have passed 0 tests. 0 tests? We just defined one.

You need to go into your ``__init__.py`` file and put some stuff in there.::

    import doctest
    __test__ = {
        'Doctest': doctest
    }


You are importing the doc test module and then adding it to the ``__test__``
dictionary. You have to do this because of the way that python handles
looking for doc tests. It looks for a ``__test__`` dictionary inside of your
module, and if that exists it looks through it, executing all docstrings as
doctests. For more information look at the `Python docs`_.

Now you should be able to go ahead and run the tests and see the magical
``Ran 1 test in 0.003s OK`` that all testers live for. This is little bit of
overhead really threw me off when I was trying to break my tests.py out into
the tests/ directory. Notice that the doc test runner sees all of your tests
as one single test. This is one annoying thing that the doctests do.

So now we have a test suite that is worthless, but you know how to use doc
tests. If you didn't notice, the doctest format is simply the output of your
default python shell, so when you are testing your code on the command line
and it works, you can simple copy and paste it into your tests. This makes
writing doc tests almost trivial. Note however, that they are somewhat
fragile, and shouldn't be used for everything. In the next segment, we will
talk about unit tests. Then we will compare the two and see what the use
cases are for each.

Doctest Considerations
~~~~~~~~~~~~~~~~~~~~~~

Keep in mind that when the test runner executes a doctest, it does not
process the output in any way. For instance, this doctest will fail::

    >>> {"abc": 1, "def": 2}
    {"abc": 1, "def": 2}

The reason for the failure is that the python interpreter always, when 
displaying dictionaries, converts double quotes into single quotes.
This, on the other hand, will pass::

    >>> {"abc": 1, "def": 2}
    {'abc': 1, 'def': 2}

Also, if you are using the popular python shell replacement ipython_
to aide in creating doctests, keep in mind it will not necessarily
output objects the same way as the vanilla python interactive
interpreter. Example::

    In [1]: {'key3': 'fff', 'key2': 123}
    Out[1]: {'key2': 123, 'key3': 'fff'}

The same output with the vanilla python shell::

    >>> {'key3': 'fff', 'key2': 123}
    {'key3': 'fff', 'key2': 123}

Notice the difference between the order of the keys.

.. _official docs: http://docs.djangoproject.com/en/dev/topics/testing
    /#writing-doctests
.. _Python docs: http://www.python.org/doc/2.5.2/lib/doctest-which-
    docstrings.html

.. _ipython: http://ipython.scipy.org/moin/
