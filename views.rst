.. _views:

Practical Django Testing Examples: Views
----------------------------------------


This is the fourth in a series of Django testing posts. Today is the start of a
sub-series, which is practical examples. This series will be going through
each of the different kinds of tests in Django, and showing how to do them. I
will also try to point out what you want to be doing to make sure you're
getting good code coverage and following best practices.

Instead of picking some contrived models and views, I figured I would do
something a little bit more useful. I'm going to take one of my favorite open
source Django apps, and write some tests for it! Everyone loves getting
patches, and patches that are tests are a god send. So I figured that I might
as well do a tutorial and give back to the community at the same time.

So I'm going to be writing some tests for `Nathan Borror`_'s Basic `Blog`_.
It also happens to be the code that powers my blog here, with some slight
modifications. So this is a win-win-win for everyone involved, just as it
should be.

Nathan's app has some basic view testing already done on it. He was gracious
enough to allow me to publicly talk about his tests. He claims to be a
designer, and not a good coder, but I know he's great at both. So we're going
to talk about his view testing today, and then go ahead and make some Model
and Template Tag tests later.


Basic philosophy
~~~~~~~~~~~~~~~~

Usually when I go about testing a Django application, there are 3 major parts
that I test. Models, Views, and Template Tags. Templates are hard to test,
and are generally more about aesthetics than code, so I tend not to think
about actually testing Templates. This should cover most of the parts of your
application that are standard. Of course, if your project has utils, forms,
feeds, and other things like that, you can and should probably test those as
well!


Views
~~~~~

So lets go ahead and take a look to see what the tests `used to look like`_.
He has already updated the project with my new tests, so you can check them
out, and break them at your leisure.::

    """
    >>> from django.test import Client
    >>> from basic.blog.models import Post, Category
    >>> import datetime

    >>> from django.core.urlresolvers import reverse
    >>> client = Client()

    >>> response = client.get(reverse('blog_index'))
    >>> response.status_code
    200
    >>> response = client.get(reverse('blog_category_list'))
    >>> response.status_code
    200
    >>> category = Category(title='Django', slug='django')

    >>> category.save()
    >>> response = client.get(category.get_absolute_url())
    >>> response.status_code
    200

    >>> post = Post(title='My post', slug='my-post', body='Lorem ipsum
    dolor sit amet', status=2, publish=datetime.datetime.now())
    >>> post.save()
    >>> post.categories.add(category)


    >>> response = client.get(post.get_absolute_url())
    >>> response.status_code
    200
    """


Notice how he is using reverse() when referring to his URLs, this makes tests
a lot more portable, because if you change your URL Scheme, the tests will
still work. A good thing to note is that a lot of best practices that apply
to coding apply to testing too! Then the tests go on to create a Category,
save it, and then test it's view and get_absolute_url() method. This is a
really clever way of testing a view and a model function (get_absolute_url)
at the same time.

Next a post is created, and saved, then a category is added to it, the one
created above. That is all that these tests do, but it covers a really good
subsection of the code. It's always good to test if you can save your objects
because a lot of bugs are found in that operation. So for the length of the
code it is remarkably well done.

This is a pretty simple test suite at the moment. But the fact that he has
tests is better than 90% of other open source projects! I'm sure if we asked
Nathan, he would tell us that even this simple test suite helps a ton. Most
of the bugs people make break in very loud and obvious ways. Which just goes
to emphasize my point that everything should have tests, even if they're
simplistic.

So how are we going to improve this testing of views? First of all, note that
these tests are hardly touching models, and not testing any template tags;
this will be addressed later. In regard to views, these tests aren't checking
the context of the responses, they are simply checking status code. This
isn't really testing the functionality of the view, just testing if it
doesn't break. There are also some views that aren't being touched, like
search, pagination, and the date archive views. We aren't going to test
pagination because we don't have enough data to paginate. This brings me to a
meta subject, slight tangent time.


Do I test Django stuff?
~~~~~~~~~~~~~~~~~~~~~~~

So we have some Generic views in our application, should we test them? I
don't think that there is a correct answer to this question, but I have an
opinion. I think that you should test generic views, but only in the ways
that they can break based on how you define them. This doesn't look much
different than normal tests that you should be writing anyway.

For the date-based generic view for example, you are passing in a QuerySet
and DateField in the URLConf; and the parts of the date you're using in the
actual URLs. So what is the easiest way to test that all of these things are
being set correctly? Find the most specific example and test for it. So you
would test the context and response code of blog_detail page, because it has
to use the query set, the date field, and the full path for the URLs.
Assuming that your code isn't broken in some horrible way, that means that
all the other parts of the date URLs should work.


Let's write some tests
~~~~~~~~~~~~~~~~~~~~~~

So we need to add some stuff to the tests. We need to get some data into the
tests, in order to use the date-based archives, and search stuff. So we're
going to take the stuff that was previously at the bottom of the test, and
move it up to the top. Also need to add 2 posts and categories, so that we
know that our filtering functionality is working.::

    >>> category = Category(title='Django', slug='django')
    >>> category.save()

    >>> category2 = Category(title='Rails', slug='rails')
    >>> category2.save()
    >>> post = Post(title='DJ Ango', slug='dj-ang', body='Yo DJ! Turn
    that music up!', status=2, publish=datetime.datetime(2008,5,5,16,20))
    >>> post.save()

    >>> post2 = Post(title='Where my grails at?', slug='where', body='I
    Can haz Holy plez?', status=2, publish=datetime.datetime(2008,4,2,11,11))
    >>> post2.save()
    >>> post.categories.add(category)
    >>> post2.categories.add(category2)


Pretty obvious what this test is doing. If these tests were going to be much
more complicated than this, it would make a lot of sense to write a fixture
to store the data. However I'm trying to test the saving functionality (which
is technically a model thing), so it's good to make the objects inline.

So now we have our data, and we need to do something with it. Let's go ahead
and run the test suite to make sure that we haven't done anything stupid.
It's a tenet of `Test Driven Development`_ to test after every change, and
one that I picked up from that philosophy. It's really handy. I don't do it
on a really granular level like it suggests, but I try to do it after any
moderately important change.


Getting into context
~~~~~~~~~~~~~~~~~~~~

So we have the tests that were there before, and they're fine. They perform a
great function, so we should keep them around, we just need to add some stuff
to them. This is one of the reasons I really don't like doctests. Using unit
tests you can just throw an ``import pdb; pdb.set_trace()`` in your code and
it will drop you into a prompt, and you can easily use this to write new
tests. Doctests however hijack the STDOUT during the tests, so when I drop
into pdb with a ``>>> import pdb; pdb.set_trace()`` in the test, i can't see
the output, so it's hard for me to get testing information.

**Note**: You can also do this by changing your settings file database
(because otherwise these objects would be created in your real DB), running
syncdb, running ``s/>>> //`` on your test, adding a setup_test_environment()
import and call to the test, and running ``python -i testfile``, if you want.
But do you really want to do that?

Let's go poking around inside of response.context, which is a dictionary of
contexts for the response. We only care about [-1], because that is where our
context will be (except for generic views, annoying right?). So go down to
the first view, ``blog_index``, and put::

    >>> response = client.get(reverse('blog_index'))

    >>> response.context[-1]['object_list']
    [test]


In your tests. We know [test] won't match, but we just want to know what the
real output is. When you go ahead and run the tests your should find some
output like this::

    Expected:
        [test]
    Got:

        [<Post: DJ Ango>, <Post: Where my grails at?>]



So go ahead and put in the correct information in where [test] was. This is a
really annoying way of testing, and I'm going to repeat that this is why doc
tests are evil, but we're already this far, so let's push on. Writing tests
this way requires the tester to be vigilant, because you're trusting that the
code is outputting the correct value. This is kind of nice actually, because
it forces you to mentally make sure that your tests are correct, and if
you're code isn't outputting what you expect, then you've already found bugs,
just by writing the tests ;) But if you're testing code that's complex, this
method breaks down, because you don't know if the output is correct!

If you look in the context, you'll see lots of other things that we could
test for as well. Some that Django (oh so nicely) gave us, and other stuff
that is user defined. Things like pagination, results per page, and some
other stuff that we really don't care about. The object_list on the page is
really what we're after, so we can move on. Run your tests to be sure, and
lets move on.


Updating current tests
~~~~~~~~~~~~~~~~~~~~~~

Now that we have our hackjob way of getting data out of the tests, we can
move on to writing more tests. Go down to the next view test of
``blog_category_list``, and pull the old object_list trick. You should get
the following back out once you run your tests::

    Expected:
         [test]
     Got:
         [<Category: Django>, <Category: Rails>]



This looks correct, so lets go ahead and put that in the test. As you can
see, for this simple stuff, it isn't really a huge deal doing testing this
way. The test suite runs in about 3 seconds on my machine, so it's not a huge
hurdle.

Let's go ahead and do it for the category and post detail pages. When I don't
remember or don't know what variables we'll be looking for in the context, I
usually just put ``>>> request.context[-1]`` to output all of it, and see
what it is that I want. For the ``category.get_absolute_url()`` we need
``object_list`` again. For the ``post.get_absolute_url()`` we just want
``object``.::

    >>> response = client.get(category.get_absolute_url())
    >>> response.context[-1]['object_list']
    [<Post: DJ Ango>]
    >>> response.status_code
    200

    >>> response = client.get(post.get_absolute_url())
    >>> response.context[-1]['object']

    <Post: DJ Ango>
    >>> response.status_code


We can consider those views tested now.


Creating new tests
~~~~~~~~~~~~~~~~~~

So now we've improved on the tests that were already there. Let's go ahead
and write some new ones for search and the date-based views. Starting with
search, because it will be interesting. Search requires some GET requests
with the test client, which should be fun.::

    >>> response = client.get(reverse('blog_search'), {'q': 'DJ'})

    >>> response.context[-1]['object_list']
    [<Post: DJ Ango>]

    >>> response.status_code
    200
    >>> response = client.get(reverse('blog_search'), {'q': 'Holy'})

    >>> response.context[-1]['object_list']
    [<Post: Where my grails at?>]

    >>> response.status_code
    200
    >>> response = client.get(reverse('blog_search'), {'q': ''})

    >>> response.context[-1]['message']
    'Search term was too vague. Please try again.'


As you can see, we're testing to make sure that search works. We're also
testing the edge case of a blank search, and making sure this does what we
want. A blank search could return everything, nothing, or an error. The
correct output is an error, so we go ahead and check for that. Notice that
you pass GET parameters in the test client as a dictionary after the URL, and
passing them as ``?q=test`` on the URL wouldn't work. `Russ`_ is working on
fixing that, and by the time you read this, it might not be true.

Next, on to testing the generic date views. You should be in the hang of it
by now.::

    >>> response = client.get(reverse('blog_detail', args=[2008, 'apr', 2, 'where']))

    >>> response.context[-1]['object']
    <Post: Where my grails at?>

    >>> response.status_code
    200


Notice here that we're using the args on reverse, and not using get
parameters. We're passing those arguments as positional into the view. You
can also use kwargs={'year': '2008'} if you want to be more explicit. As
talked about above, I feel that this is enough of testing for the generic
views.

Wow! That was a long post. I'm glad I decided to split the testing up into
separate posts! I hope this has been enlightening for everyone, and I'm sure
that I'm doing it wrong in some places. I would love some feedback, and to
hear how you work around and solve some of the problems above. Also your
thoughts on this kind of stuff.

Nathan has graciously included `my new tests`_ in his project, if you want to
see them live, or check them out.




.. _Testing series: /tag/testing-series/
.. _Nathan Borror: http://playgroundblues.com/
.. _Blog: http://code.google.com/p/django-basic-
    apps/source/browse/trunk/blog/
.. _used to look like: http://code.google.com/p/django-basic-
    apps/source/browse/trunk/blog/tests.py?r=62
.. _Test Driven Development: http://en.wikipedia.org/wiki/Test-
    driven_development
.. _Russ: http://cecinestpasun.com/
.. _my new tests: http://code.google.com/p/django-basic-
    apps/source/browse/trunk/blog/tests.py
