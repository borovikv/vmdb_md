'''
Created on Jul 19, 2013

@author: drifter
'''
import sys
from pprint import PrettyPrinter

class MyPrettyPrinter(PrettyPrinter):
    def format(self, *args, **kwargs):
        _repr, readable, recursive = PrettyPrinter.format(self, *args, **kwargs)
        if _repr:
            if _repr[0] in ('"', "'"):
                _repr = _repr.decode('string_escape')
            elif _repr[0:2] in ("u'", 'u"'):
                _repr = _repr.decode('unicode_escape')#.encode(sys.stdout.encoding)
        return _repr, readable, recursive

def mpprint(obj, stream=None, indent=1, width=80, depth=None):
    printer = MyPrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(obj)