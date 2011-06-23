Serializers and Deserializers
------------------------------

The ``manage.py dumpdata`` or ``manage.py loaddata`` commands can translate the
contents of your database into YAML, XML, or some other format using a
**serializer**. There may come a time when the built-in serializers do not meet
your needs, and you find yourself writing a custom serializer (and probably a
custom **deserializer** too). How can you go about testing these?

There are two basic scenarios:

    Serialization
        Dump database objects to whatever format you want ``dumpdata`` to output
    Deserialization
        Loading database objects from your custom format, like ``loaddata`` does

You could test each of these separately, or you could do a full round-trip test
that mimics ``dumpdata`` followed by ``loaddata``. We'll test them separately in
this example. We won't be testing the ``manage.py`` command itself; this is
strictly a unit test on the custom serializer and/or deserializer.

There are many different levels of detail you could get into; we'll cover only a
very simple scenario, involving a single model with a single string field. A
more comprehensive test would include multiple models, relationships between and
within models, and a wide variety of model field types and data. This example
covers only a single model, with a single string field; it's intended only to
give you a basic starting point. It's up to you how rigorously you want to test
your serializer and deserializer.


What we're testing
~~~~~~~~~~~~~~~~~~~~~~~~~

If you've written your own serializer, you've probably added something like this
to your ``settings.py``::

    SERIALIZATION_MODULES = {
        'yaml': 'myapp.custom_yaml',
    }

In this example, we're using a customized YAML serializer. Anytime Django needs
to dump or load ``yaml`` format, it'll use ``myapp/custom_yaml.py`` to do it.

This example serializer uses a slightly different structure than Django's
built-in YAML serializer. It's designed to be significantly less verbose, while
still capturing all the relevant data. You may be familiar with Django's usual
YAML output, which looks something like this::

    - fields: {name: green}
      model: myapp.color
      pk: 1
    - fields: {name: blue}
      model: myapp.color
      pk: 2
    - fields: {name: red}
      model: myapp.color
      pk: 3
    - fields: {name: squishy}
      model: myapp.texture
      pk: 1
    - fields: {name: crumbly}
      model: myapp.texture
      pk: 2

This serializer uses a more condensed format::

    myapp.color:
      1: {name: green}
      2: {name: blue}
      3: {name: red}
    myapp.texture:
      1: {name: squishy}
      2: {name: crumbly}

We won't go into the details of the serializer itself; all we're concerned with
here is how make sure it produces correct output, and that the corresponding
deserializer loads it correctly afterwards.


Test the serializer
~~~~~~~~~~~~~~~~~~~~~~~~~

To test the serializer, we will create some model instances, then serialize them
and make sure the output is correct. The ``django.core.serializers`` module
defines a ``serialize`` function that takes the name of the format you want to
serialize, along with a ``QuerySet`` of objects to serialize, and returns a
string of serialized data. That's what we'll use in our test::

    from django.test import TestCase
    from django.core import serializers
    from myapp.models import Color

    class YamlSerializerTest (TestCase):
        def test_serializer(self):
            # Stuff to serialize
            Color(name='green').save()
            Color(name='blue').save()
            Color(name='red').save()

            # Expected output
            expect_yaml = \
                'myapp.color:\n' \
                '  1: {name: green}\n' \
                '  2: {name: blue}\n' \
                '  3: {name: red}\n'

            # Do the serialization
            actual_yaml = serializers.serialize('yaml', Color.objects.all())

            # Did it work?
            self.assertEqual(actual_yaml, expect_yaml)

Notice that we pass ``'yaml'`` as the first argument to ``serialize``;
ordinarily this would use the default YAML serializer, but since we've
overridden that in ``SERIALIZATION_MODULES``, it'll use our custom one instead.

Since we're working with standard YAML, another way to verify the result is to
parse it using ``yaml.load``, and check that the resulting Python data structure
(in this case, a ``dict``) matches expectations::

    class YamlSerializerTest (TestCase):
        def test_serializer(self):
            # ...

            self.assertEqual(
                yaml.load(actual_yaml), {
                    'myapp.color': {
                        1: {'name': 'green'},
                        2: {'name': 'blue'},
                        3: {'name': 'red'},
                    }
                }
            )

Of course, if you're serializing to your own made-up custom format, you may not
have a standalone parser for that format so readily available. In that case, you
may simply choose to rely on your deserializer tests to ensure that the output
is parsed correctly.


Test the deserializer
~~~~~~~~~~~~~~~~~~~~~~~~~

Unless your serializer is designed for one-way conversion, you'll want to
include some tests for your deserializer as well. Starting with the serialized
text output, we'll make sure that it gets loaded into the database and correctly
builds the original models.

The ``django.core.serializers`` module includes a counterpart to the
``serialize`` function called (you guessed it) ``deserialize``. This function
accepts a format (like ``yaml``), along with a chunk of text to deserialize.
It returns a generator that yields each of the objects as they are parsed. We'll
convert these into a list, then verify that the deserialized objects have the
correct values in their fields::

    class YamlSerializerTest (TestCase):
        def test_deserializer(self):
            # Input text
            input_yaml = \
                'myapp.color:\n' \
                '  1: {name: green}\n' \
                '  2: {name: blue}\n' \
                '  3: {name: red}\n'

            # Deserialize into a list of objects
            objects = list(serializers.deserialize('yaml', input_yaml))

            # Were three objects deserialized?
            self.assertEqual(len(objects), 3)

            # Did the objects deserialize correctly?
            self.assertEqual(objects[0].object.name, 'green')
            self.assertEqual(objects[1].object.name, 'blue')
            self.assertEqual(objects[2].object.name, 'red')

Perhaps this isn't the most elegant way to do it, but it gets the job done.


References
~~~~~~~~~~~~

Several custom serializers are available on djangosnippets.org_, including json_
and csv_ serializers. The `slightly better YAML serializer`_ was used as the
basis for the examples above. For a much more thorough serializer test suite,
please consult Django's `regression tests`_.

.. _djangosnippets.org: http://djangosnippets.org/
.. _json: http://djangosnippets.org/snippets/1162/
.. _csv: http://djangosnippets.org/snippets/2240/
.. _slightly better YAML serializer: http://djangosnippets.org/snippets/2461/
.. _regression tests: https://github.com/django/django/blob/master/tests/regressiontests/serializers_regress/tests.py

