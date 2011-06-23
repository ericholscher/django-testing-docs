Measuring Coverage
-------------------

After you've written some tests for your Django app, and gotten them all to
pass, you may wonder "Do I have enough tests? Am I missing anything?" One way to
help yourself answer that question is to measure the **coverage** of your
tests--that is, how thoroughly your tests exercise the application's code.

Perhaps the most popular tool for measuring coverage in Python is simply called
coverage_. While your tests are running, it keeps track of which lines of
application code are executed, which ones are skipped (like comments), and which
ones are never reached. At the end, it spits out a report that indicates which
lines of code were not executed--this points directly to holes in your test
coverage.

The nose_ testing tool integrates nicely with coverage_, and django-nose_ ties
it all into Django. This chapter will give an overview of how to get it working.


Configure django-nose
~~~~~~~~~~~~~~~~~~~~~~~~

The first thing to do is install django-nose_ using ``pip``::

    $ pip install django-nose

Then make these additions to your project's ``settings.py``::

    INSTALLED_APPS = (
        # ...
        'django_nose',
    )

    # Use nose to run all tests
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    # Tell nose to measure coverage on the 'foo' and 'bar' apps
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=foo,bar',
    ]

Here, we're setting a couple of command-line arguments to be included every time
we run ``python manage.py test``. The ``--with-coverage`` option says we want a
coverage report, and the ``--cover-package`` option lists all of the modules we
are hoping to cover (these are the names of your Django apps). For a complete
list of other available options, run ``python manage.py help test``.


Coverage reports
~~~~~~~~~~~~~~~~~~

When running test cases with coverage enabled, a report is printed at the end
looking something like this::

    Name               Stmts   Miss  Cover   Missing
    ------------------------------------------------
    foo.models            30      5    85%   10-12, 16, 19
    bar.models            10      1    90%   4
    ------------------------------------------------
    TOTAL                 40      6    87%

This says the ``foo.models`` module has 30 lines of executable code, and 5 of
those lines were not evaluated during testing. The specific lines that aren't
covered are listed at the end.

Why would certain lines not be executed? Perhaps those lines define a function
that was never called, which means we need to add some tests for that function.
Maybe those lines are inside an ``if / else`` block that only executed the
``if`` part, so we need to add tests for the ``else`` part also. It could be an
exception handler that never encountered an exception, in which case we could
add tests that purposely cause that exception (and verify that the correct
exception was raised).

Try adding the ``--cover-html`` option to your ``NOSE_ARGS`` if you'd like a
nice HTML report that highlights the missing lines in your source code.


Unreachable code
~~~~~~~~~~~~~~~~~~

It's possible (though rare) that some lines of code are missed because they are
simply unreachable. For example, the line inside this ``if`` statement can never
be executed::

    if 2 + 2 == 5:
        print("Unusually large value of 2")

Or, have you ever seen code like this?::

    try:
        do_something(x)
    # This should never happen, but just in case
    except SomeError:
        do_something_else(x)

With sufficient testing and coverage analysis, you can determine with
near-certainty whether "This should never happen" is a true statement. If there
is no possible way for ``do_something(x)`` to raise ``SomeError``, then there's
no reason to keep the extra code around.


Further reading
~~~~~~~~~~~~~~~~~~~

So far, what you're getting out of this is **statement coverage**, which is the
most basic kind of code coverage, and also arguably the weakest. It only tells
you which lines of code were evaluated, but it does not tell you anything about
all the possible ways that each of those lines could be evaluated. Those
alternatives can be measured using **branch** and **condition** coverage, which is
beyond the scope of this example.

Statement coverage is a good first step, and can point you towards obvious gaps
in your test suite. It may be insufficient in the long run, but it's the easiest
place to start if you've never measured coverage before.

See `What is Wrong with Statement Coverage`_ for more insight, and refer to
`Test coverage analysis`_ for a Python-specific introduction to more detailed
coverage techniques.


.. _coverage: http://nedbatchelder.com/code/coverage/beta/
.. _nose: http://code.google.com/p/python-nose/
.. _django-nose: http://pypi.python.org/pypi/django-nose
.. _What is Wrong with Statement Coverage: http://www.bullseye.com/statementCoverage.html
.. _Test coverage analysis: http://lautaportti.wordpress.com/2011/05/07/test-coverage-analysis/

