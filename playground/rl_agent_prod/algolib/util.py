from __future__ import print_function
from functools import wraps
import inspect
import sys

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def initializer(func):
  """
  Taken from https://stackoverflow.com/questions/1389180/automatically-initialize-instance-variables
  Automatically assigns the parameters.

  >>> class process:
  ...     @initializer
  ...     def __init__(self, cmd, reachable=False, user='root'):
  ...         pass
  >>> p = process('halt', True)
  >>> p.cmd, p.reachable, p.user
  ('halt', True, 'root')
  """
  names, varargs, keywords, defaults = inspect.getargspec(func)

  @wraps(func)
  def wrapper(self, *args, **kargs):
      for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
          setattr(self, name, arg)

      for name, default in zip(reversed(names), reversed(defaults)):
          if not hasattr(self, name):
              setattr(self, name, default)

      func(self, *args, **kargs)

  return wrapper
