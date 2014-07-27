import inspect
from itertools import chain


DELEGATE_STR = 'Delegate(args={args}, return_value={return_value})'


class DelegateMetaclass(type):

    def __str__(cls):
        return DELEGATE_STR.format(args=', '.join(map(str, cls.args)),
                                   return_value=cls.return_value)


class BaseDelegate(object):

    __metaclass__ = DelegateMetaclass

    def __init__(self, *implementations):
        for implementation in implementations:
            if not hasattr(implementation, '__call__'):
                raise ValueError('Implementation is not callable')

            args_spec = inspect.getargspec(implementation)
            if len(args_spec.args) != len(self.__class__.args):
                raise ValueError(
                    'Wrong number of arguments: '
                    '{} != {}'.format(len(args_spec.args),
                                      len(self.__class__.args))
                )

        self.implementations = implementations

    def __call__(self, *args, **kwargs):
        for implementation in self.implementations:
            for i, argument in enumerate(chain(args, kwargs.values())):
                if not isinstance(argument, self.args[i]):
                    raise ValueError(
                        'Wrong argument type: '
                        '{} != {}'.format(argument.__class__, self.args[i])
                    )

            return_value = implementation(*args, **kwargs)

            if not isinstance(return_value, self.return_value):
                raise ValueError(
                    'Wrong return_value type: '
                    '{} != {}'.format(return_value.__class__,
                                      self.return_value)
                )

        return return_value

    def __add__(self, other):
        DelegateType = self.__class__
        assert DelegateType == other.__class__, ('Only can add Delegates '
                                                 'of the same type')
        return self.__class__(
            *(self.implementations + other.implementations)
        )


class Delegate(type):

    def __new__(cls, args, return_value=None):
        return type(
            DELEGATE_STR.format(args=', '.join(map(str, args)),
                                return_value=return_value),
            (BaseDelegate,),
            {
                'args': args,
                'return_value': return_value
            }
        )
