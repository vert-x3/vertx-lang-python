from __future__ import unicode_literals, print_function, absolute_import

import json
import collections
import operator
from functools import partial, wraps
from contextlib import contextmanager

from py4j.java_gateway import is_instance_of
from py4j.java_collections import MapConverter, ListConverter, SetConverter, JavaMap

from .compat import reduce, iteritems

java_gateway = None
jvm = None
jvertx = None

class VertxException(Exception):
    pass

class AdaptingMap(JavaMap):
    def __init__(self, map, java_converter, python_converter):
        JavaMap.__init__(self, map._target_id, map._gateway_client)
        self.java_converter = java_converter
        self.python_converter = python_converter

    def __setitem__(self, key, value):
        return JavaMap.__setitem__(self, key, self.python_converter(value))

    def __getitem__(self, key):
        return self.java_converter(JavaMap.__getitem__(self, key))

    def to_python(self):
        """ Convert to a normal python dict. """
        return {k: self.java_converter(v) for k,v in iteritems(self)}


class FrozenEncoder(json.JSONEncoder):
    ''' JSON encode capable of handling sets and frozen sets. '''
    def default(self, obj):
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        return json.JSONEncoder(self, obj)

def parse_array(old_parse_array, *args, **kwargs):
    values, end = old_parse_array(*args, **kwargs)
    return frozenset(values), end

class FrozenDecoder(json.JSONDecoder):
    ''' Decoder that will use frozensets insteadof lists for JSON arrays. '''
    def __init__(self, *args, **kwargs):
        super(FrozenDecoder, self).__init__(*args, **kwargs)
        old_parse_array = self.parse_array
        self.parse_array = partial(parse_array, old_parse_array)
        self.scan_once = json.scanner.py_make_scanner(self)


class frozendict(dict, collections.Mapping):
    ''' Hashable dict.
    
    This isn't truly frozen (immutable), but it can be placed
    into a set.
    
    '''
    def __init__(self, *args, **kwargs):
        self.__hash = None
        self.update(*args, **kwargs)

    def copy(self, **add_or_replace):
        return frozendict(self, **add_or_replace)

    def __repr__(self):
        return '<frozendict %s>' % repr(super(frozendict, self).__repr__())

    def __hash__(self):
        if self.__hash is None:
            self.__hash = reduce(operator.xor, map(hash, iteritems(self)), 0)
        return self.__hash


@contextmanager
def handle_vertx_shutdown(on_error_only=False):
    """ Protect calls to the Java Gateway.
    
    This decorate ensures the properly cleanup is done if a call
    to the Java Gateway throws an exception. Failure to do so can
    leave the program in a hung state, because the Py4J callback
    server thread will keep running in the background, preventing
    the interpreter from exiting.
    
    """
    shutdown_called = False
    try:
        yield
    except Exception:
        vertx_shutdown()
        shutdown_called = True
        raise
    finally:
        if not on_error_only and not shutdown_called:
            vertx_shutdown()

def vertx_shutdown():
    ''' Shut down py4j.
    
    This has to be called prior to exiting after calling vertx_init(),
    or the program will likely hang forever. This is because py4j starts
    a callback server in a non-daemon background thread, which will keep
    the program from exiting when the main thread completes.
    
    '''
    global java_gateway
    global jvm
    global jvertx
    java_gateway.close()
    jvm = None
    jvertx = None
    java_gateway = None

def vertx_init():
    """Initializes the Vert.x connection."""
    global java_gateway
    global jvm
    global jvertx

    if not hasattr(__builtins__, 'jvm') and not all([jvm, jvertx, java_gateway]):
        import sys
        try:
            port = sys.argv[1]
        except IndexError:
            raise RuntimeError("Failed to connect to Vert.x")
        try:
            from py4j.java_gateway import JavaGateway, GatewayClient
            proxy_port = int(sys.argv[2])
            java_gateway = JavaGateway(GatewayClient(port=int(port)), 
                                             start_callback_server=True,
                                             eager_load=True,
                                             python_proxy_port=proxy_port)
            jvm = java_gateway.jvm
            jvertx = java_gateway.entry_point.getVertx()
        except ImportError:
            raise RuntimeError("Failed to connect to Vert.x. Py4J must be on your PYTHONPATH")

def convert_char_to_java(ch):
    if isinstance(ch, int):
        return chr(ch)
    else:
        if len(ch) > 1:
            raise ValueError("{} is not a valid character".format(ch))
    return ch

def convert_short_to_java(x):
    return jvm.java.lang.Short(x)

def convert_long_to_java(x):
    return jvm.java.lang.Long(x)

def convert_byte_to_java(x):
    return jvm.java.lang.Byte(x)

def convert_double_to_java(x):
    return jvm.java.lang.Double(x)

def convert_float_to_java(x):
    return jvm.java.lang.Float(x)

def convert_boolean_to_java(x):
    return bool(x)

def json_to_python(obj, hashable=False):
    """ Converts a Java JSON object to Python dict or list. 
    
    hashable kwarg indicates if the returns dict needs to be
    hashable (and therefore able to be put into a set).
    
    """
    object_hook = frozendict if hashable else dict
    cls = FrozenDecoder if hashable else json.JSONDecoder
    d = json.loads(obj.encode(), object_hook=object_hook, cls=cls) if obj is not None else None
    return d

def list_to_json(obj):
    """Converts a Python list to Java JsonArray"""
    return jvm.io.vertx.core.json.JsonArray(json.dumps(obj, cls=FrozenEncoder)) if obj is not None else None

def dict_to_json(obj):
    """Converts a Python dictionary to Java JsonObject"""
    return jvm.io.vertx.core.json.JsonObject(json.dumps(obj, cls=FrozenEncoder)) if obj is not None else None

def python_to_java(obj):
    """Converts an arbitrary Python object to Java"""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return dict_to_json(obj)
    elif isinstance(obj, list):
        return list_to_json(obj)
    return obj

def python_map_to_java(obj):
    return MapConverter().convert(obj, java_gateway._gateway_client) if obj else obj

def python_set_to_java(obj):
    return SetConverter().convert(obj, java_gateway._gateway_client) if obj else obj

def python_list_to_java(obj):
    return ListConverter().convert(obj, java_gateway._gateway_client) if obj else obj

def data_object_to_json(obj, hashable=False):
    if obj is None:
        return None
    return java_to_python(obj.toJson(), hashable=hashable)

def handle_none(obj, type_):
    return type_(obj) if obj is not None else obj

def java_map_to_python(obj, java_converter, python_converter):
    ''' Returns a dict-like object that also updates the corresponding java map. 
    
    Returns an object that inherits from the py4j.java_collection.JavaMap, 
    but also supports converting Python objects inserted into the correct 
    java object, as well as supporting converting Java objects retrieved 
    from the map into the correct python object.
    
    '''
    if obj is None:
        return None
    return AdaptingMap(obj, java_converter, python_converter)

def java_to_python(obj, hashable=False):
    """Converts an arbitrary Java object to Python"""
    try:
        if obj is None:
            return None
        elif (is_instance_of(java_gateway, obj, jvm.io.vertx.core.json.JsonObject) or 
              is_instance_of(java_gateway, obj, jvm.io.vertx.core.json.JsonArray)):
            return json_to_python(obj, hashable=hashable)
        else:
            return obj
    except AttributeError:
        return obj


def cached(func):
    ''' Decorator for methods that need to cache results. '''
    dct = dict(cached_ret=None)
    @wraps(func)
    def inner(*args, **kwargs):
        if dct['cached_ret'] is None:
            dct['cached_ret'] = func(*args, **kwargs)
        return dct['cached_ret']
    return inner

