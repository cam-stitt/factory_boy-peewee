import factory
from .compat import unittest

from factory_peewee import PeeweeModelFactory
from . import app


class StandardFactory(PeeweeModelFactory):
    class Meta:
        model = app.StandardModel
        database = app.database

    id = factory.Sequence(lambda n: n)
    foo = factory.Sequence(lambda n: 'foo%d' % n)


class NonIntegerPkFactory(PeeweeModelFactory):
    class Meta:
        model = app.NonIntegerPk
        database = app.database

    id = factory.Sequence(lambda n: 'foo%d' % n)


class PeeweePkSequenceTestCase(unittest.TestCase):
    def setUp(self):
        super(PeeweePkSequenceTestCase, self).setUp()
        StandardFactory.reset_sequence(1)
        if app.StandardModel.table_exists():
            app.StandardModel.drop_table()
        app.StandardModel.create_table()

    def test_pk_first(self):
        std = StandardFactory.build()
        self.assertEqual('foo1', std.foo)

    def test_pk_many(self):
        std1 = StandardFactory.build()
        std2 = StandardFactory.build()
        self.assertEqual('foo1', std1.foo)
        self.assertEqual('foo2', std2.foo)

    def test_pk_creation(self):
        std1 = StandardFactory.create()
        self.assertEqual('foo1', std1.foo)
        self.assertEqual(1, std1.id)

        StandardFactory.reset_sequence()
        std2 = StandardFactory.create()
        self.assertEqual('foo2', std2.foo)
        self.assertEqual(2, std2.id)

    def test_pk_force_value(self):
        std1 = StandardFactory.create(id=10)
        self.assertEqual('foo1', std1.foo)  # sequence was set before pk
        self.assertEqual(10, std1.id)

        StandardFactory.reset_sequence()
        std2 = StandardFactory.create()
        self.assertEqual('foo11', std2.foo)
        self.assertEqual(11, std2.id)


class PeeweeNonIntegerPkTestCase(unittest.TestCase):
    def setUp(self):
        super(PeeweeNonIntegerPkTestCase, self).setUp()
        NonIntegerPkFactory.reset_sequence()
        if app.NonIntegerPk.table_exists():
            app.NonIntegerPk.drop_table()
        app.NonIntegerPk.create_table()

    def test_first(self):
        nonint = NonIntegerPkFactory.build()
        self.assertEqual('foo1', nonint.id)

    def test_many(self):
        nonint1 = NonIntegerPkFactory.build()
        nonint2 = NonIntegerPkFactory.build()

        self.assertEqual('foo1', nonint1.id)
        self.assertEqual('foo2', nonint2.id)

    def test_creation(self):
        nonint1 = NonIntegerPkFactory.create()
        self.assertEqual('foo1', nonint1.id)

        NonIntegerPkFactory.reset_sequence()
        nonint2 = NonIntegerPkFactory.build()
        self.assertEqual('foo1', nonint2.id)

    def test_force_pk(self):
        nonint1 = NonIntegerPkFactory.create(id='foo100')
        self.assertEqual('foo100', nonint1.id)

        NonIntegerPkFactory.reset_sequence()
        nonint2 = NonIntegerPkFactory.create()
        self.assertEqual('foo1', nonint2.id)
