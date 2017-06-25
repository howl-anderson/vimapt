import six

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

from depsolver.bundled.traitlets \
    import \
        HasTraits, TraitError
from depsolver.errors \
    import \
        DepSolverError
from depsolver.utils \
    import \
        Callable, CachedScheduler, Scheduler

class TestScheduler(unittest.TestCase):
    def test_simple(self):
        scheduler = Scheduler()
        scheduler.set_constraints("second", "first", "third")

        self.assertEqual(scheduler.order("third"), ["first", "second"])

    def test_after(self):
        scheduler = Scheduler()
        scheduler.set_constraints("second", "first")
        scheduler.set_constraints("third", "second")

        self.assertEqual(scheduler.order("third"), ["first", "second"])

    def test_before(self):
        scheduler = Scheduler()
        scheduler.set_constraints("second", before="third")
        scheduler.set_constraints("first", before="second")

        self.assertEqual(scheduler.order("third"), ["first", "second"])

    def test_cycle(self):
        scheduler = Scheduler()
        scheduler.set_constraints("second", before="third")
        scheduler.set_constraints("third", before="second")

        self.assertRaises(DepSolverError, lambda: scheduler.order("third"))

    def test_compute_priority(self):
        r_priority = dict((name, i) for i, name in \
                           enumerate(["first", "second", "third", "fourth"]))

        scheduler = Scheduler()
        scheduler.set_constraints("second", "first", "third")
        scheduler.set_constraints("third", before="fourth")

        self.assertEqual(scheduler.compute_priority(), r_priority)

class TestCachedScheduler(unittest.TestCase):
    def test_simple(self):
        r_priority = dict((name, i) for i, name in \
                           enumerate(["first", "second", "third", "fourth"]))

        scheduler = CachedScheduler()
        scheduler.set_constraints("second", "first", "third")
        scheduler.set_constraints("third", before="fourth")

        self.assertEqual(scheduler.compute_priority(), r_priority)

        self.assertFalse(scheduler.invalidated)
        scheduler.set_constraints("fifth", after="fourth")
        self.assertTrue(scheduler.invalidated)

        r_priority = dict((name, i) for i, name in \
                          enumerate(["first", "second", "third", "fourth", "fifth"]))
        self.assertEqual(scheduler.compute_priority(), r_priority)

class TestCallableTrait(unittest.TestCase):
    def test_simple(self):
        class Foo(HasTraits):
            func = Callable()

        foo = Foo()
        self.assertRaises(TraitError, lambda: Foo(func="yo"))
