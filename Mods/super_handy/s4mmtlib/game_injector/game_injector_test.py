from game_injector import GameInjector
import unittest

class TestGameInjector(unittest.TestCase):
    def test_call_counts(self):
        injector = GameInjector()

        test_obj = TestObject()
        injector.wrap_function(test_obj, 'do_something', observe_key='test_inject')

        start_count = 0
        def increase_start_count(obs, val):
            nonlocal start_count
            start_count += 1

        end_count = 0
        def increase_end_count(obs, val):
            nonlocal end_count
            end_count += 1

        injector.before('test_inject', increase_start_count)
        injector.after('test_inject', increase_end_count)

        test_obj.do_something()
        test_obj.do_something()
        test_obj.do_something()

        self.assertEqual(start_count, 3)
        self.assertEqual(end_count, 3)

class TestObject:
    def __init__(self):
        self.some_val = 20

    def do_something(self):
        return self.some_val


if __name__ == '__main__':
    unittest.main()
