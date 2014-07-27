from cStringIO import StringIO
import sys
from unittest import TestCase

from delegates import Delegate


class DelegatesTest(TestCase):

    def test_delegate_declaration_and_instantiation(self):
        MyDelegate = Delegate(
            args=(int, str, float),
            return_value=int
        )

        def implementing_function(a, b, random_name):
            return 314
        delegate = MyDelegate(implementing_function)
        result = delegate(42, 'foo', random_name=3.7)

        self.assertEquals(result, 314)

    def test_wrong_implementation_number_of_arguments(self):
        MyDelegate = Delegate(
            return_value=int,
            args=(int, str, float)
        )
        implementing_function = lambda: 314

        try:
            MyDelegate(implementing_function)
            self.fail()
        except ValueError as exc:
            self.assertEquals(exc.message, 'Wrong number of arguments: 0 != 3')
        except:
            self.fail()

    def test_delegate_without_return_value(self):
        MyDelegate = Delegate(
            args=(int, str, float)
        )

        self.assertEquals(
            str(MyDelegate),
            'Delegate(args=<type \'int\'>, <type \'str\'>, <type \'float\'>, '
            'return_value=None)'
        )

    def test_arguments_validation(self):
        MyDelegate = Delegate(
            return_value=int,
            args=(int, str, float)
        )
        implementing_function = lambda a, b, c: 314
        delegate = MyDelegate(implementing_function)

        try:
            delegate(1, 2, 3)
            self.fail()
        except ValueError as exc:
            self.assertEquals(exc.message, 'Wrong argument type: '
                              '<type \'int\'> != <type \'str\'>')
        except:
            self.fail()

    def test_return_value_validation(self):
        MyDelegate = Delegate(
            return_value=int,
            args=(int, str, float)
        )
        implementing_function = lambda a, b, c: 'This is a str'
        delegate = MyDelegate(implementing_function)

        try:
            delegate(1, 'b', 3.3)
            self.fail()
        except ValueError as exc:
            self.assertEquals(exc.message, 'Wrong return_value type: '
                              '<type \'str\'> != <type \'int\'>')
        except:
            self.fail()

    def test_add_two_delegates(self):
        sys.stdout = testing_stdout = StringIO()

        MyDelegate = Delegate(
            args=(int, str, float),
            return_value=int
        )

        def implementing_function1(a, b, random_name):
            print('First implementation')
            return 314
        delegate1 = MyDelegate(implementing_function1)

        def implementing_function2(a, b, random_name):
            print('Second implementation')
            return 101
        delegate2 = MyDelegate(implementing_function2)

        delegate = delegate1 + delegate2
        result = delegate(42, 'foo', random_name=3.7)

        self.assertEquals(result, 101)
        self.assertEquals(testing_stdout.getvalue(),
                          'First implementation\n'
                          'Second implementation\n')
