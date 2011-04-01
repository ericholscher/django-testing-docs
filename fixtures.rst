
Introduction to Python/Django tests: Fixtures
---------------------------------------------

In the first two posts of this `series`_, we talked about how to get the
basic infrastructure for your tests up and running. You should have a file
with doc tests and one with unit tests. They should be linked into your
django project with an ``__init__.py`` file. If you were feeling adventurous
you may have even added some real content to them. Today we're going to start
going down the road of getting some data into your tests.

This post will cover fixtures. Fixtures are how you create a state for your
database in your tests. This will be my first post in the comparison between
unit tests and doc tests. I will focus on fixtures, but some other
differences between the two may become relevant throughout the post, and I
will address them in turn.


How to create a fixture
~~~~~~~~~~~~~~~~~~~~~~~

Fixtures can go into a couple places, but generally it is a good idea to put
them in your applications ``fixtures/`` directory. This makes all of your
test data self contained inside your app, so it can be run when it is
distributed. The loaddata command discussed further down specifies where
fixtures can be placed to be loaded, if you're curious.

Before we go about trying to figure out how to use fixtures, we need to know
how to make them. Django's docs on this are pretty good. Basically if you
have an app that has data in the database, you can use the ``./manage.py
dumpdata <app>`` `command`_ to create a fixture from the current data in the
database. It's handy to note that you can use the ``--format`` tag to specify
the output format, and the ``--indent`` command to make the output prettier.
My preferred command is::

    #This assumes you are at the project level, right above your app.
     #and that APP/fixtures/ exists
     ./manage.py dumpdata APP --format=yaml --indent=4 >
     APP/fixtures/APP.yaml



This makes for a really nice, readable fixture, so if you need to edit it
later you can. Go ahead and run this command in your project directory,
substituting your app in the appropriate places. Open the fixture if you want
and take a peak inside. It should be a nice readable version of your
database, serialized into Yaml. **Note**: If you don't have PyYAML installed,
it will say that your serialization format isn't valid, ``sudo apt-get
install python-yaml`` gets you the package on Ubuntu. If not, you can remove
the format option and it will default to JSON.


Testing your fixtures (how meta of us!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django also comes with a really neat tool to be able to test and update
fixtures. The `testserver command`_ allows you to run the development server,
passing a fixture to load before it launches. This allows you to run your
code base against the fixture that you have, in a browser.

This seems really nice, but the killer feature of this command is that it
keeps the database around after you kill the development server. This means
that you can load up a fixture, edit it in the admin or frontend, and then
kill the server; then run dumpdata against that database and get your updated
fixture back out. Pretty neat! Note, your normal database name will be
prefixed with ``test_``, so it doesn't overwrite your normal DB. This is the
one you want to get data out of. (You may have to define it in your
``settings.py`` file to get dumpdata to use it. This seems like a little bit
of a hack, and maybe something could be done to make this easier.)


Fixtures in Doc tests
~~~~~~~~~~~~~~~~~~~~~

In what will become a recurring trend, doing fixtures in doc tests is a hack.
Doc tests are made to be a simple answer to a relatively simple problem, and
fixtures aren't a huge deal for them. So a lot of the functionality that we
get for free with unit tests, has to be hacked into doc tests. I will just
show how to do the basic things, because implementing anything beyond that
isn't very useful for any of us.::

    >>> from django.core.management import call_command
    >>> call_command("loaddata", "' + 'fixturefile.json' + '",
    verbosity=0)



In this snippet you are basically calling it the way it is called within
Django. Normally when you are using loaddata, you would be calling it as
``./manage.py loaddata FIXTURE``. Note that the `loaddata docs`_ talk about
how to use loaddata normally. There are a couple of downsides to this method;
The test is very fragile, if the fixture breaks, all of your tests fail.
Also, you can really only call one fixture at a time because there is no
setUp and tearDown that will make sure your environment is the same for every
test. Doing things this way just makes writing tests a whole lot harder. It
is indeed a hack, and one that shouldn't really be used unless you have a
very good reason.

Generally in doc tests, you would create your content as if you were on the
command line. This shows how doc tests are generally limited in their scope.
You go ahead and create the objects that you care about in the test
explicitly, and then run your tests against them. A simple example::

    >>> from mine.models import Site
    >>> s = Site.objects.create(url='http://google.com', query='test',
    title='test', content='lots of stuff')

    >>> s.query
    'test'
    >>> s.save()
    >>> pk_site = s.pk
    >>> Site.objects.get(pk=pk_site)
    <Site: test>
    >>> Site.objects.get(pk=pk_site).delete()


This tests creating, retrieving and deleting an object. Not a lot of
functionality, but if anything inside of the model saving code breaks you
will know about it.


Django's Testcase
~~~~~~~~~~~~~~~~~

The fixture story in unit tests is much better, as you would expect. However,
before we go into how unit tests use fixtures, there is something that I need
to explain. Because of the fact that unit tests are classes, they can be
subclassed just like any other Python class. This means that Django has
provided it's own Testcase class that we can inherit from and get some nice
extra Django functionality. The `official docs`_ has it really well
documented.

You'll notice that Django's Testcase has a section for the Test Client and
URLConf configuration. We can safely skip those for the moment because they
are geared towards testing views. The relevant sections for us at the moment
are Fixture loading and Assertions. I recommend that you actually read
the entire testing doc, it isn't that long, and is packed full of useful
information. However, knowing about all of the assertions that are available
to you will make testing a little bit easier.


Fixtures in Unit Tests
~~~~~~~~~~~~~~~~~~~~~~

The big thing that the Django Testcase does for you in regards to fixtures is
that it maintains a consistent state for all of your tests. Before each test
is run, the database is flushed: returning it to a pristine state (like after
your first syncdb). Then your fixture gets loaded into the DB, then setUp()
is called, then your test is run, then tearDown() is called. Keeping your
tests insulated from each other is incredibly important when you are trying
to make a good test suite. Having tests altering each others data, or having
tests that depend on another test altering data are inherently fragile.

Now lets talk about how you're actually going to use these fixtures. We're
going to go ahead and recreate the simple doc test above. It simply loads up
a Site object into the database, checks for some data in it, then deletes it.
The fixture handling will handle all of the loading and deleting for us, so
all we need to worry about is testing our logic! This makes the test a lot
easier to read, and makes its intention a lot clearer.::

    from django.test import TestCase
    from mine.models import Site

    class SiteTests(TestCase):
        #This is the fixture:
        #-   fields: {content: lots of stuff, query: test, title:
        test, url: 'http://google.com'}
        #model: mine.site
        #pk: 1
        fixtures = ['mine']

        def testFluffyAnimals(self):
            s = Site.objects.get(pk=1)
            self.assertEquals(s.query, 'test')
            s.query = 'who cares'
            s.save()


As you can see, this test is a lot simpler than the above one. It is also
neat that we can edit the object and save it, and it doesn't matter. No other
tests (if they existed) would be affected by this change. Notice that in my
fixtures list, I only had mine and not mine.yaml or mine.json. If you don't
add a file extension to your fixture, it will search for all fixtures with
that name, of any extension. You can define an extension if you only want it
to search for those types of files.

I hope that you can see already how unit tests give you a lot more value when
working with fixtures than doc tests. Having all of the loading, unloading,
and flushing handled for you means that it will be done correctly. Once you
get a moderately complicated testing scheme, trying to handle that all
yourself inside of a doc test will lead to fragile and buggy code.




.. _series: /tag/testing-series/
.. _command: http://docs.djangoproject.com/en/dev/ref/django-
    admin/#dumpdata
.. _testserver command: http://docs.djangoproject.com/en/dev/ref/django-
    admin/#testserver-fixture-fixture
.. _loaddata docs: http://docs.djangoproject.com/en/dev/ref/django-admin
    /#loaddata-fixture-fixture
.. _official docs: http://docs.djangoproject.com/en/dev/topics/testing/?f
    rom=olddocs#testcase
