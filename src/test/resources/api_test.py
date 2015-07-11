from __future__ import unicode_literals, print_function, absolute_import
import sys
import unittest

from testmodel_python.testmodel.test_interface import TestInterface
from testmodel_python.testmodel.refed_interface1 import RefedInterface1
from testmodel_python.testmodel.refed_interface2 import RefedInterface2
from testmodel_python.testmodel.generic_refed_interface import GenericRefedInterface
from testmodel_python.testmodel.factory import Factory
from acme_python.pkg.my_interface import MyInterface
from acme_python.sub.sub_interface import SubInterface

from vertx_python import util
from vertx_python.util import frozendict
from vertx_python.compat import long, unicode

util.vertx_init()

with util.handle_java_error():
    jvm = util.jvm
    obj = TestInterface(jvm.io.vertx.codegen.testmodel.TestInterfaceImpl())
    refed_obj = RefedInterface1(jvm.io.vertx.codegen.testmodel.RefedInterface1Impl())
    refed_obj2 = RefedInterface1(jvm.io.vertx.codegen.testmodel.RefedInterface1Impl())

class TestAPI(unittest.TestCase):
    def testMethodWithBasicParams(self):
        obj.method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, True, 88, 'foobar')

    def testMethodWithBasicBoxedParams(self):
        obj.method_with_basic_boxed_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, True, 88)

    def testMethodWithHandlerBasicTypes(self):
        dct = dict(count=0)
        def byte_handler(b):
            self.assertEqual(type(b), int)
            self.assertEqual(123, b)
            dct['count'] += 1
        def short_handler(s):
            self.assertEqual(type(s), int)
            self.assertEqual(12345, s)
            dct['count'] += 1
        def int_handler(i):
            self.assertEqual(type(i), int)
            self.assertEqual(1234567, i)
            dct['count'] += 1
        def long_handler(l):
            self.assertEqual(type(l), long)
            self.assertEqual(1265615234, l)
            dct['count'] += 1
        def float_handler(f):
            self.assertEqual(type(f), float)
            self.assertEqual(12.345, f)
            dct['count'] += 1
        def double_handler(d):
            self.assertEqual(type(d), float)
            self.assertEqual(12.34566, d)
            dct['count'] += 1
        def boolean_handler(b):
            self.assertEqual(type(b), bool)
            self.assertTrue(b)
            dct['count'] += 1
        def char_handler(c):
            self.assertEqual(type(c), unicode)
            self.assertEqual('X', c)
            dct['count'] += 1
        def string_handler(s):
            self.assertEqual(type(s), unicode)
            self.assertEqual('quux!', s)
            dct['count'] += 1

        obj.method_with_handler_basic_types(byte_handler, short_handler, 
                                            int_handler, long_handler,
                                            float_handler, double_handler, 
                                            boolean_handler, char_handler,
                                            string_handler)
        self.assertEqual(dct['count'], 9)
              
    def testMethodWithHandlerAsyncResultBasicTypes(self):
        dct = dict(count=0)
        def byte_handler(b, err):
            self.assertEqual(type(b), int)
            self.assertEqual(123, b)
            self.assertIsNone(err)
            dct['count'] += 1
        def short_handler(s, err):
            self.assertEqual(type(s), int)
            self.assertEqual(12345, s)
            self.assertIsNone(err)
            dct['count'] += 1
        def int_handler(i, err):
            self.assertEqual(type(i), int)
            self.assertEqual(1234567, i)
            self.assertIsNone(err)
            dct['count'] += 1
        def long_handler(l, err):
            self.assertEqual(type(l), long)
            self.assertEqual(1265615234, l)
            self.assertIsNone(err)
            dct['count'] += 1
        def float_handler(f, err):
            self.assertEqual(type(f), float)
            self.assertEqual(12.345, f)
            self.assertIsNone(err)
            dct['count'] += 1
        def double_handler(d, err):
            self.assertEqual(type(d), float)
            self.assertEqual(12.34566, d)
            self.assertIsNone(err)
            dct['count'] += 1
        def boolean_handler(b, err):
            self.assertEqual(type(b), bool)
            self.assertTrue(b)
            self.assertIsNone(err)
            dct['count'] += 1
        def char_handler(c, err):
            self.assertEqual(type(c), unicode)
            self.assertEqual('X', c)
            self.assertIsNone(err)
            dct['count'] += 1
        def string_handler(s, err):
            self.assertEqual(type(s), unicode)
            self.assertEqual('quux!', s)
            self.assertIsNone(err)
            dct['count'] += 1
        obj.method_with_handler_async_result_byte(False, byte_handler)
        obj.method_with_handler_async_result_short(False, short_handler)
        obj.method_with_handler_async_result_integer(False, int_handler)
        obj.method_with_handler_async_result_long(False, long_handler)
        obj.method_with_handler_async_result_float(False, float_handler)
        obj.method_with_handler_async_result_double(False, double_handler)
        obj.method_with_handler_async_result_boolean(False, boolean_handler)
        obj.method_with_handler_async_result_character(False, char_handler)
        obj.method_with_handler_async_result_string(False, string_handler)
        self.assertEqual(dct['count'], 9)


    def testMethodWithHandlerAsyncResultBasicTypesFails(self):
        dct = dict(count=0)
        def handler(x, err):
            self.assertIsNone(x);
            self.assertIsNotNone(err);
            self.assertEqual("foobar!", err.getMessage());
            dct['count'] += 1

        obj.method_with_handler_async_result_byte(True, handler)
        obj.method_with_handler_async_result_short(True, handler)
        obj.method_with_handler_async_result_integer(True, handler)
        obj.method_with_handler_async_result_long(True, handler)
        obj.method_with_handler_async_result_float(True, handler)
        obj.method_with_handler_async_result_double(True, handler)
        obj.method_with_handler_async_result_boolean(True, handler)
        obj.method_with_handler_async_result_character(True, handler)
        obj.method_with_handler_async_result_string(True, handler)
        self.assertEqual(dct['count'], 9)

    def testMethodWithUserTypes(self):
        refed_obj.set_string('aardvarks')
        obj.method_with_user_types(refed_obj)


    def testObjectParam(self):
        obj.method_with_object_param('null', None)
        obj.method_with_object_param('string', 'wibble')
        obj.method_with_object_param('true', True)
        obj.method_with_object_param('false', False)
        obj.method_with_object_param('long', 123)
        obj.method_with_object_param('double', 123.456)
        json_obj = {"foo" : "hello", "bar" : 123}
        obj.method_with_object_param('JsonObject', json_obj)
        json_arr = ["foo", "bar", "wib"]
        obj.method_with_object_param('JsonArray', json_arr)


    def testDataObjectParam(self):
        data_object = {"foo" : "hello", "bar" : 123, "wibble" : 1.23}
        obj.method_with_data_object_param(**data_object)


    #TODO not really possible to pass a Null object w/ Python API
    #def testNullDataObjectParam(self):
        #data_object = {}
        #obj.method_with_null_data_object_param(**data_object)


    def testMethodWithHandlerDataObject(self):
        dct = dict(count=0)
        def handler(option):
            self.assertEqual("foo", option['foo'])
            self.assertEqual(123, option['bar'])
            self.assertEqual(0.0, option['wibble'])
            dct['count'] += 1
        obj.method_with_handler_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultDataObject(self):
        dct = dict(count=0)
        def handler(option, err):
            self.assertIsNone(err)
            self.assertEqual("foo", option['foo'])
            self.assertEqual(123, option['bar'])
            self.assertEqual(0.0, option['wibble'])
            dct['count'] += 1
        obj.method_with_handler_async_result_data_object(False, handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultDataObjectFails(self):
        dct = dict(count=0)
        def handler(option, err):
            self.assertIsNone(option)
            self.assertIsNotNone(err)
            self.assertEqual("foobar!", err.getMessage())
            dct['count'] += 1
        obj.method_with_handler_async_result_data_object(True, handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListAndSet(self):
        dct = dict(count=0)
        def handle_str_list(l):
            self.assertEqual(type(l), list)
            self.assertEqual("foo", l[0])
            self.assertEqual("bar", l[1])
            self.assertEqual("wibble", l[2])
            dct['count'] += 1
        def handle_int_list(l):
            self.assertEqual(type(l), list)
            self.assertEqual(5, l[0])
            self.assertEqual(12, l[1])
            self.assertEqual(100, l[2])
            dct['count'] += 1
        def handle_str_set(s):
            self.assertEqual(type(s), set)
            self.assertSetEqual(set(['foo', 'bar', 'wibble']), s)
            dct['count'] += 1
        def handle_int_set(s):
            self.assertEqual(type(s), set)
            self.assertSetEqual(set([5, 12, 100]), s)
            dct['count'] += 1

        obj.method_with_handler_list_and_set(handle_str_list, handle_int_list,
                                             handle_str_set, handle_int_set)
        self.assertEqual(dct['count'], 4)


    def testMethodWithHandlerAsyncResultListAndSet(self):
        dct = dict(count=0)
        def handle_str_list(l, err):
            self.assertIsNone(err)
            self.assertEqual(type(l), list)
            self.assertEqual("foo", l[0])
            self.assertEqual("bar", l[1])
            self.assertEqual("wibble", l[2])
            dct['count'] += 1
        def handle_int_list(l, err):
            self.assertIsNone(err)
            self.assertEqual(type(l), list)
            self.assertEqual(5, l[0])
            self.assertEqual(12, l[1])
            self.assertEqual(100, l[2])
            dct['count'] += 1
        def handle_str_set(s, err):
            self.assertIsNone(err)
            self.assertEqual(type(s), set)
            self.assertSetEqual(set(['foo', 'bar', 'wibble']), s)
            dct['count'] += 1
        def handle_int_set(s, err):
            self.assertIsNone(err)
            self.assertEqual(type(s), set)
            self.assertSetEqual(set([5, 12, 100]), s)
            dct['count'] += 1

        obj.method_with_handler_async_result_list_string(handle_str_list)
        obj.method_with_handler_async_result_list_integer(handle_int_list)
        obj.method_with_handler_async_result_set_string(handle_str_set)
        obj.method_with_handler_async_result_set_integer(handle_int_set)
        self.assertEqual(dct['count'], 4)


    def testMethodWithHandlerListVertxGen(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), RefedInterface1)
            self.assertEqual(val[0].get_string(), 'foo')
            self.assertEqual(type(val[1]), RefedInterface1)
            self.assertEqual(val[1].get_string(), 'bar')
            dct['count'] += 1
        obj.method_with_handler_list_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)

    def testMethodWithHandlerUserTypes(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), RefedInterface1)
            self.assertEqual(val.get_string(), 'echidnas')
            dct['count'] += 1
        obj.method_with_handler_user_types(handler)
        self.assertEqual(dct['count'], 1)

    def testMethodWithHandlerListAbstractVertxGen(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertIsInstance(val[0], RefedInterface2)
            self.assertEqual(val[0].get_string(), 'abstractfoo')
            self.assertIsInstance(val[1], RefedInterface2)
            self.assertEqual(val[1].get_string(), 'abstractbar')
            dct['count'] += 1

        obj.method_with_handler_list_abstract_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListVertxGen(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), RefedInterface1)
            self.assertEqual(val[0].get_string(), 'foo')
            self.assertEqual(type(val[1]), RefedInterface1)
            self.assertEqual(val[1].get_string(), 'bar')
            dct['count'] += 1
        obj.method_with_handler_async_result_list_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListAbstractVertxGen(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertIsInstance(val[0], RefedInterface2)
            self.assertEqual(val[0].get_string(), 'abstractfoo')
            self.assertIsInstance(val[1], RefedInterface2)
            self.assertEqual(val[1].get_string(), 'abstractbar')
            dct['count'] += 1

        obj.method_with_handler_async_result_list_abstract_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetVertxGen(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 2)
            for item in val:
                self.assertEqual(type(item), RefedInterface1)
            self.assertSetEqual(set([x.get_string() for x in val]), 
                                set(['foo', 'bar']))
            dct['count'] += 1
        obj.method_with_handler_set_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetAbstractVertxGen(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 2)
            for item in val:
                self.assertIsInstance(item, RefedInterface2)
            self.assertSetEqual(set([x.get_string() for x in val]), 
                                set(['abstractfoo', 'abstractbar']))
            dct['count'] += 1

        obj.method_with_handler_set_abstract_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetVertxGen(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 2)
            for item in val:
                self.assertEqual(type(item), RefedInterface1)
            self.assertSetEqual(set([x.get_string() for x in val]), 
                                set(['foo', 'bar']))
            dct['count'] += 1

        obj.method_with_handler_async_result_set_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetAbstractVertxGen(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 2)
            for item in val:
                self.assertIsInstance(item, RefedInterface2)
            self.assertSetEqual(set([x.get_string() for x in val]), 
                                set(['abstractfoo', 'abstractbar']))
            dct['count'] += 1

        obj.method_with_handler_async_result_set_abstract_vertx_gen(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), dict)
            self.assertEqual(val[0], dict(cheese='stilton'))
            self.assertEqual(type(val[1]), dict)
            self.assertEqual(val[1], dict(socks='tartan'))
            dct['count'] += 1
        obj.method_with_handler_list_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListNullJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertIsNone(val[0])
            dct['count'] += 1
        obj.method_with_handler_list_null_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListComplexJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertEqual(val[0], {'outer' : {'socks' : 'tartan'}, 'list' : ['yellow', 'blue']})
            dct['count'] += 1
        obj.method_with_handler_list_complex_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), dict)
            self.assertEqual(val[0], dict(cheese='stilton'))
            self.assertEqual(type(val[1]), dict)
            self.assertEqual(val[1], dict(socks='tartan'))
            dct['count'] += 1
        obj.method_with_handler_async_result_list_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListNullJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertIsNone(val[0])
            dct['count'] += 1
        obj.method_with_handler_async_result_list_null_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListComplexJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertEqual(val[0], {'outer' : {'socks' : 'tartan'}, 
                                      'list' : ['yellow', 'blue']})
            dct['count'] += 1
        obj.method_with_handler_async_result_list_complex_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            for elt in val:
                self.assertEqual(type(elt), frozendict)
            self.assertEqual(val, set([frozendict(cheese='stilton'), 
                                       frozendict(socks='tartan')]))
            dct['count'] += 1
        obj.method_with_handler_set_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetNullJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            for elt in val:
                self.assertIsNone(None)
            dct['count'] += 1
        obj.method_with_handler_set_null_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetComplexJsonObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            self.assertEqual(val, set([frozendict({'outer' : frozendict({'socks' : 'tartan'}),
                                                   'list' : frozenset(['yellow', 'blue'])})
                                     ])
                            )
            dct['count'] += 1
        obj.method_with_handler_set_complex_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            for elt in val:
                self.assertEqual(type(elt), frozendict)
            self.assertEqual(val, set([frozendict(cheese='stilton'), 
                                       frozendict(socks='tartan')]))
            dct['count'] += 1
        obj.method_with_handler_async_result_set_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetNullJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            for elt in val:
                self.assertIsNone(None)
            dct['count'] += 1
        obj.method_with_handler_async_result_set_null_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetComplexJsonObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            self.assertEqual(val, set([frozendict({'outer' : frozendict({'socks' : 'tartan'}),
                                                   'list' : frozenset(['yellow', 'blue'])})
                                     ])
                            )
            dct['count'] += 1
        obj.method_with_handler_async_result_set_complex_json_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), list)
            self.assertEqual(val[0], ['green', 'blue'])
            self.assertEqual(type(val[1]), list)
            self.assertEqual(val[1], ['yellow', 'purple'])
            dct['count'] += 1
        obj.method_with_handler_list_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListNullJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertIsNone(val[0])
            dct['count'] += 1
        obj.method_with_handler_list_null_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListJsonArray(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 2)
            self.assertEqual(type(val[0]), list)
            self.assertEqual(val[0], ['green', 'blue'])
            self.assertEqual(type(val[1]), list)
            self.assertEqual(val[1], ['yellow', 'purple'])
            dct['count'] += 1
        obj.method_with_handler_async_result_list_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListNullJsonArray(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(len(val), 1)
            self.assertIsNone(val[0])
            dct['count'] += 1
        obj.method_with_handler_async_result_list_null_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListComplexJsonArray(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(val, [[{'foo' : 'hello'}], [{'bar' : 'bye'}]])
            dct['count'] += 1
        obj.method_with_handler_async_result_list_complex_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            for elt in val:
                self.assertEqual(type(elt), frozenset)
            self.assertEqual(val, set([frozenset(['green', 'blue']),
                                       frozenset(['yellow', 'purple'])]))
            dct['count'] += 1
        obj.method_with_handler_set_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetNullJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            for elt in val:
                self.assertIsNone(elt)
            dct['count'] += 1
        obj.method_with_handler_set_null_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetComplexJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), set)
            self.assertEqual(val, set([frozenset([frozendict({'foo' : 'hello'})]), 
                                       frozenset([frozendict({'bar' : 'bye'})])
                                     ])
                            )
            dct['count'] += 1
        obj.method_with_handler_set_complex_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetJsonArray(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            for elt in val:
                self.assertEqual(type(elt), frozenset)
            self.assertEqual(val, set([frozenset(['purple', 'yellow']), 
                                       frozenset(['blue', 'green'])
                                     ])
                            )
            dct['count'] += 1
        obj.method_with_handler_async_result_set_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetNullJsonArray(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(len(val), 1)
            for elt in val:
                self.assertIsNone(elt)
            dct['count'] += 1
        obj.method_with_handler_async_result_set_null_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListComplexJsonArray(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(val, [[{'foo' : 'hello'}], [{'bar' : 'bye'}]])
            dct['count'] += 1
        obj.method_with_handler_list_complex_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetComplexJsonArray(self):
        dct = dict(count=0)
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), set)
            self.assertEqual(val, set([frozenset([frozendict({'foo' : 'hello'})]), 
                                       frozenset([frozendict({'bar' : 'bye'})])
                                     ])
                            )
            dct['count'] += 1
        obj.method_with_handler_async_result_set_complex_json_array(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListDataObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            for elt in val:
                self.assertEqual(type(elt), dict)
            self.assertEqual(val[0], {'foo' : 'String 1', 'bar' : 1, 'wibble' : 1.1})
            self.assertEqual(val[1], {'foo' : 'String 2', 'bar' : 2, 'wibble' : 2.2})
            dct['count'] += 1
        obj.method_with_handler_list_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerListNullDataObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(type(val), list)
            self.assertIsNone(val[0])
            dct['count'] += 1
        obj.method_with_handler_list_null_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetDataObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(val, set([frozendict({'foo' : 'String 1', 'bar' : 1, 'wibble' : 1.1}),
                                       frozendict({'foo' : 'String 2', 'bar' : 2, 'wibble' : 2.2})
                                      ])
                            )
            dct['count'] += 1
        obj.method_with_handler_set_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerSetNullDataObject(self):
        dct = dict(count=0)
        def handler(val):
            self.assertEqual(val, set([None]))
            dct['count'] += 1
        obj.method_with_handler_set_null_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListDataObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            for elt in val:
                self.assertEqual(type(elt), dict)
            self.assertEqual(val[0], {'foo' : 'String 1', 'bar' : 1, 'wibble' : 1.1})
            self.assertEqual(val[1], {'foo' : 'String 2', 'bar' : 2, 'wibble' : 2.2})
            dct['count'] += 1
        obj.method_with_handler_async_result_list_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultListNullDataObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, [None])
            dct['count'] += 1
        obj.method_with_handler_async_result_list_null_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetDataObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, set([frozendict({'foo' : 'String 1', 'bar' : 1, 'wibble' : 1.1}),
                                       frozendict({'foo' : 'String 2', 'bar' : 2, 'wibble' : 2.2})
                                      ])
                            )
            dct['count'] += 1
        obj.method_with_handler_async_result_set_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultSetNullDataObject(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, set([None]))
            dct['count'] += 1
        obj.method_with_handler_async_result_set_null_data_object(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultUserTypes(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), RefedInterface1)
            self.assertEqual(val.get_string(), 'cheetahs')
            dct['count'] += 1
        obj.method_with_handler_async_result_user_types(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithConcreteHandlerUserTypeSubtype(self):
        dct = dict(count=0)
        def handler(obj):
            self.assertEqual(type(obj), RefedInterface1)
            self.assertEqual(obj.get_string(), 'echidnas')
            dct['count'] += 1
        arg = Factory.create_concrete_handler_user_type(handler)
        obj.method_with_concrete_handler_user_type_subtype(arg)
        self.assertEqual(dct['count'], 1)


    def testMethodWithAbstractHandlerUserTypeSubtype(self):
        dct = dict(count=0)
        def handler(obj):
            self.assertEqual(type(obj), RefedInterface1)
            self.assertEqual(obj.get_string(), 'echidnas')
            dct['count'] += 1
        arg = Factory.create_abstract_handler_user_type(handler)
        obj.method_with_abstract_handler_user_type_subtype(arg)
        self.assertEqual(dct['count'], 1)


    def testMethodWithConcreteHandlerUserTypeSubtypeExtension(self):
        dct = dict(count=0)
        def handler(obj):
            self.assertEqual(type(obj), RefedInterface1)
            self.assertEqual(obj.get_string(), 'echidnas')
            dct['count'] += 1
        arg = Factory.create_concrete_handler_user_type_extension(handler)
        obj.method_with_concrete_handler_user_type_subtype_extension(arg)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerVoid(self):
        dct = dict(count=0)
        def handler(val):
            self.assertIsNone(val)
            dct['count'] += 1
        obj.method_with_handler_void(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultVoid(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(err)
            self.assertIsNone(val)
            dct['count'] += 1
        obj.method_with_handler_async_result_void(False, handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerAsyncResultVoidFails(self):
        dct = dict(count=0)
        def handler(val, err):
            self.assertIsNone(val)
            self.assertEqual(err.getMessage(), 'foo!')
            dct['count'] += 1
        obj.method_with_handler_async_result_void(True, handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerThrowable(self):
        dct = dict(count=0)
        def handler(err):
            self.assertEqual(err.getMessage(), 'cheese!')
            dct['count'] += 1
        obj.method_with_handler_throwable(handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithHandlerGenericUserType(self):
        def run_test(value, assertion):
            dct = dict(count=0)
            def handler(obj):
                self.assertIsNotNone(obj)
                self.assertEqual(type(obj), GenericRefedInterface)
                assertion(obj.get_value())
                dct['count'] += 1
            obj.method_with_handler_generic_user_type(value, handler)
            self.assertEqual(dct['count'], 1)
        run_test('string_value', lambda x: self.assertEqual(x, 'string_value'))
        run_test({'key' : 'key_value'}, lambda x: self.assertEqual(x, {'key' : 'key_value'}))
        run_test(['foo', 'bar', 'juu'], lambda x: self.assertEqual(x, ['foo', 'bar', 'juu']))


    def testMethodWithHandlerAsyncResultGenericUserType(self):
        def run_test(value, assertion):
            dct = dict(count=0)
            def handler(obj, err):
                self.assertIsNone(err)
                self.assertIsNotNone(obj)
                self.assertEqual(type(obj), GenericRefedInterface)
                assertion(obj.get_value())
                dct['count'] += 1
            obj.method_with_handler_async_result_generic_user_type(value, handler)
            self.assertEqual(dct['count'], 1)
        run_test('string_value', lambda x: self.assertEqual(x, 'string_value'))
        run_test({'key' : 'key_value'}, lambda x: self.assertEqual(x, {'key' : 'key_value'}))
        run_test(['foo', 'bar', 'juu'], lambda x: self.assertEqual(x, ['foo', 'bar', 'juu']))


    def testMethodWithGenericParam(self):
        obj.method_with_generic_param('String', 'foo')
        obj.method_with_generic_param('JsonObject', {'foo' : 'hello','bar' : 123})
        obj.method_with_generic_param('JsonArray', ['foo', 'bar', 'wib'])


    def testMethodWithGenericHandler(self):
        dct = dict(count=0)
        def str_handler(val):
            self.assertEqual(type(val), unicode)
            self.assertEqual(val, 'foo')
            dct['count'] += 1
        obj.method_with_generic_handler('String', str_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def do_handler(val):
            self.assertEqual(val.getString(), 'bar')
            dct['count'] += 1
        obj.method_with_generic_handler('Ref', do_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_obj_handler(val):
            self.assertEqual(type(val), dict)
            self.assertEqual(val, {'foo' : 'hello', 'bar' : 123})
            dct['count'] += 1
        obj.method_with_generic_handler('JsonObject', json_obj_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_arr_handler(val):
            self.assertEqual(type(val), list)
            self.assertEqual(val, ['foo', 'bar', 'wib'])
            dct['count'] += 1
        obj.method_with_generic_handler('JsonArray', json_arr_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_obj_complex_handler(val):
            self.assertEqual(type(val), dict)
            self.assertEqual(val, {'outer' : {'foo' : 'hello'}, 
                                   'bar' : ['this', 'that']})
            dct['count'] += 1
        obj.method_with_generic_handler('JsonObjectComplex', json_obj_complex_handler)
        self.assertEqual(dct['count'], 1)


    def testMethodWithGenericHandlerAsyncResult(self):
        dct = dict(count=0)
        def str_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), unicode)
            self.assertEqual(val, 'foo')
            dct['count'] += 1
        obj.method_with_generic_handler_async_result('String', str_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def do_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val.getString(), 'bar')
            dct['count'] += 1
        obj.method_with_generic_handler_async_result('Ref', do_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_obj_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), dict)
            self.assertEqual(val, {'foo' : 'hello', 'bar' : 123})
            dct['count'] += 1
        obj.method_with_generic_handler_async_result('JsonObject', json_obj_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_arr_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), list)
            self.assertEqual(val, ['foo', 'bar', 'wib'])
            dct['count'] += 1
        obj.method_with_generic_handler_async_result('JsonArray', json_arr_handler)
        self.assertEqual(dct['count'], 1)

        dct = dict(count=0)
        def json_obj_complex_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(type(val), dict)
            self.assertEqual(val, {'outer' : {'foo' : 'hello'}, 
                                   'bar' : ['this', 'that']})
            dct['count'] += 1
        obj.method_with_generic_handler_async_result('JsonObjectComplex', json_obj_complex_handler)
        self.assertEqual(dct['count'], 1)


    def testJsonParams(self):
        obj.method_with_json_params({'cat' : 'lion', 'cheese' : 'cheddar'}, 
                                    ['house', 'spider'])


    def testNullJsonParams(self):
        self.assertRaises(TypeError, obj.method_with_null_json_params, None, None)


    def testJsonHandlerParams(self):
        dct = dict(count=0)
        def obj_handler(val):
            self.assertEqual(val, {'cheese' : 'stilton'})
            dct['count'] += 1
        def arr_handler(val):
            self.assertEqual(val, ['socks', 'shoes'])
            dct['count'] += 1
        obj.method_with_handler_json(obj_handler, arr_handler)
        self.assertEqual(dct['count'], 2)


    def testNullJsonHandlerParams(self):
        dct = dict(count=0)
        def obj_handler(val):
            self.assertIsNone(val)
            dct['count'] += 1
        def arr_handler(val):
            self.assertIsNone(val)
            dct['count'] += 1
        obj.method_with_handler_null_json(obj_handler, arr_handler)
        self.assertEqual(dct['count'], 2)


    def testComplexJsonHandlerParams(self):
        dct = dict(count=0)
        def obj_handler(val):
            self.assertEqual(val, {'outer' : {'socks' : 'tartan'},
                                   'list' : ['yellow', 'blue']})
            dct['count'] += 1
        def arr_handler(val):
            self.assertEqual(val, [[{'foo' : 'hello'}], [{'bar' : 'bye'}]])
            dct['count'] += 1
        obj.method_with_handler_complex_json(obj_handler, arr_handler)
        self.assertEqual(dct['count'], 2)


    def testJsonHandlerAsyncResultParams(self):
        dct = dict(count=0)
        def obj_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, {'cheese' : 'stilton'})
            dct['count'] += 1
        def arr_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, ['socks', 'shoes'])
            dct['count'] += 1
        obj.method_with_handler_async_result_json_object(obj_handler)
        obj.method_with_handler_async_result_json_array(arr_handler)
        self.assertEqual(dct['count'], 2)


    def testNullJsonHandlerAsyncResultParams(self):
        dct = dict(count=0)
        def obj_handler(val, err):
            self.assertIsNone(val)
            self.assertIsNone(err)
            dct['count'] += 1
        def arr_handler(val, err):
            self.assertIsNone(val)
            self.assertIsNone(err)
            dct['count'] += 1

        obj.method_with_handler_async_result_null_json_object(obj_handler)
        obj.method_with_handler_async_result_null_json_array(arr_handler)
        self.assertEqual(dct['count'], 2)


    def testComplexJsonHandlerAsyncResultParams(self):
        dct = dict(count=0)
        def obj_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, {'outer' : {'socks' : 'tartan'},
                                   'list' : ['yellow', 'blue']})
            dct['count'] += 1
        def arr_handler(val, err):
            self.assertIsNone(err)
            self.assertEqual(val, [{'foo' : 'hello'}, {'bar' : 'bye'}])
            dct['count'] += 1
        obj.method_with_handler_async_result_complex_json_object(obj_handler)
        obj.method_with_handler_async_result_complex_json_array(arr_handler)
        self.assertEqual(dct['count'], 2)


    def testBasicReturns(self):
        ret = obj.method_with_byte_return()
        self.assertEqual(type(ret), int)
        self.assertEqual(ret, 123)
        ret = obj.method_with_short_return()
        self.assertEqual(type(ret), int)
        self.assertEqual(ret, 12345)
        ret = obj.method_with_int_return()
        self.assertEqual(type(ret), int)
        self.assertEqual(ret, 12345464)
        ret = obj.method_with_long_return()
        self.assertEqual(type(ret), long)
        self.assertEqual(ret, 65675123)
        ret = obj.method_with_float_return()
        self.assertEqual(type(ret), float)
        self.assertEqual(ret, 1.23)
        ret = obj.method_with_double_return()
        self.assertEqual(type(ret), float)
        self.assertEqual(ret, 3.34535)
        ret = obj.method_with_boolean_return()
        self.assertEqual(type(ret), bool)
        self.assertEqual(ret, True)
        ret = obj.method_with_char_return()
        self.assertEqual(type(ret), unicode)
        self.assertEqual(ret, 'Y')
        ret = obj.method_with_string_return()
        self.assertEqual(type(ret), unicode)
        self.assertEqual(ret, 'orangutan')


    def testVertxGenReturn(self):
        ret = obj.method_with_vertx_gen_return()
        self.assertEqual(type(ret), RefedInterface1)
        self.assertEqual(ret.get_string(), 'chaffinch')


    def testVertxGenNullReturn(self):
        ret = obj.method_with_vertx_gen_null_return()
        self.assertIsNone(ret)


    def testAbstractVertxGenReturn(self):
        ret = obj.method_with_abstract_vertx_gen_return()
        self.assertIsInstance(ret, RefedInterface2)
        self.assertEqual(ret.get_string(), 'abstractchaffinch')


    #def testMapComplexJsonArrayReturn(self):
        #def handler(map):
            #m = map['foo']
            #self.assertEqual(m, [{'foo' : 'hello'}, {'bar' : 'bye'}])
        #obj.method_with_map_complex_json_array_return(handler)


    #def testOverloadedMethods(self):
        #@refed_obj.set_string('dog')
        #called = false
        #ret = obj.overloaded_method('cat', @refed_obj)
        #self.assertEqual(ret, 'meth1')
        #ret = obj.overloaded_method('cat', @refed_obj, 12345) { |animal| self.assertEqual(animal, 'giraffe') ; called = true }
        #self.assertEqual(ret, 'meth2')
        #self.assertEqual(called, true)
        #called = false
        ## for some reason animal is sometimes equals to giraffe and sometimes empty
        #ret = obj.overloaded_method('cat') { |animal| called = true }
        #self.assertEqual(ret, 'meth3')
        #self.assertEqual(called, true)
        #called = false
        #ret = obj.overloaded_method('cat', @refed_obj) { |animal| self.assertEqual(animal, 'giraffe') ; called = true }
        #self.assertEqual(ret, 'meth4')
        #self.assertEqual(called, true)
        #self.argument_error { obj.overloaded_method 'cat' }
        #self.argument_error { obj.overloaded_method('cat', @refed_obj, 12345) }
        #self.argument_error { obj.overloaded_method {} }


    #def testSuperInterfaces(self):
        #obj.super_method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
        #self.assertEqual(obj.is_a?(Testmodel::SuperInterface1), true)
        #obj.other_super_method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
        #self.assertEqual(obj.is_a?(Testmodel::SuperInterface2), true)


    #def testMethodWithGenericReturn(self):
        #ret = obj.method_with_generic_return('JsonObject')
        #self.assertEqual(ret.class, Hash)
        #self.assertEqual(ret, {'foo'=>'hello','bar'=>123})
        #ret = obj.method_with_generic_return('JsonArray')
        #self.assertEqual(ret.class, Array)
        #self.assertEqual(ret, %w(foo bar wib))


    #def testFluentMethod(self):
        #ret = obj.fluent_method('bar')
        #self.assertEqual(ret, obj)


    #def testStaticFactoryMethod(self):
        #ret = Testmodel::TestInterface.static_factory_method('bar')
        #self.assertEqual(ret.class, Testmodel::RefedInterface1)
        #self.assertEqual(ret.get_string, 'bar')


    #def testMethodWithCachedReturn(self):
        #ret = obj.method_with_cached_return('bar')
        #ret2 = obj.method_with_cached_return('bar')
        #self.equals ret, ret2
        #ret3 = obj.method_with_cached_return('bar')
        #self.equals ret, ret3
        #self.equals ret.get_string, 'bar'
        #self.equals ret2.get_string, 'bar'
        #self.equals ret3.get_string, 'bar'
        #ret.set_string 'foo'
        #self.equals ret2.get_string, 'foo'
        #self.equals ret3.get_string, 'foo'


    #def testJsonReturns(self):
        #ret = obj.method_with_json_object_return
        #self.assertEqual(ret, {'cheese'=>'stilton'})
        #ret = obj.method_with_json_array_return
        #self.assertEqual(ret, %w(socks shoes))


    #def testNullJsonReturns(self):
        #ret = obj.method_with_null_json_object_return
        #self.is_nil(ret)
        #ret = obj.method_with_null_json_array_return
        #self.is_nil(ret)


    #def testComplexJsonReturns(self):
        #ret = obj.method_with_complex_json_object_return
        #self.equals ret, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}
        #ret = obj.method_with_complex_json_array_return
        #self.equals ret, [{'foo' => 'hello'}, {'bar' => 'bye'}]


    #def testEnumReturn(self):
        #ret = obj.method_with_enum_return('JULIEN')
        #self.assertEqual(:JULIEN, ret)


    #def testMapReturn(self):
        #readLog = []
        #writeLog = []
        #map = obj.method_with_map_return{ |op|
          #if op =~ /put\([^,]+,[^\)]+\)/ || op =~ /remove\([^\)]+\)/ || op == 'clear()'
            #writeLog.push op
          #elsif op == 'size()' || op =~ /get\([^\)]+\)/ || op == 'entrySet()'
            #readLog.push op
          #else
            #raise "unsupported #{op}"
          #end
        #}
        #map['foo'] = 'bar'
        #self.equals writeLog, ['put(foo,bar)']
        #readLog.clear
        #writeLog.clear
        #self.equals map['foo'], 'bar'
        #self.is_not_nil readLog.index('get(foo)')
        #self.equals writeLog, []
        #map['wibble'] = 'quux'
        #readLog.clear
        #writeLog.clear
        #self.equals map.size, 2
        #self.equals map['wibble'], 'quux'
        #self.is_not_nil readLog.index('size()')
        #self.equals writeLog, []
        #readLog.clear
        #writeLog.clear
        #map.delete('wibble')
        #self.equals writeLog, ['remove(wibble)']
        #self.equals map.size, 1
        #map['blah'] = '123'
        #key_dct = dict(count=0)
        #readLog.clear
        #writeLog.clear
        #map.each { |k,v|
          #if key_count == 0
            #self.equals k, 'foo'
            #self.equals v, 'bar'
            #key_dct['count'] += 1
          #else
            #self.equals k, 'blah'
            #self.equals v, '123'
          #end
        #}
        #self.is_not_nil readLog.index('entrySet()')
        #self.equals writeLog, []
        #readLog.clear
        #writeLog.clear
        #map.clear
        #self.equals writeLog, ['clear()']


    #def testMapStringReturn(self):
        #map = obj.method_with_map_string_return {}
        #val = map['foo']
        #self.equals val.class, String
        #self.equals val, 'bar'
        #map['juu'] = 'daa'
        #self.equals map, {'foo'=>'bar','juu'=>'daa'}
        #self.argument_error { map['wibble'] = 123 }
        #self.equals map, {'foo'=>'bar','juu'=>'daa'}


    #def testMapJsonObjectReturn(self):
        #map = obj.method_with_map_json_object_return {}
        #json = map['foo']
        #self.equals json.class, Hash
        #self.equals json['wibble'], 'eek'
        #map['bar'] = {'juu'=>'daa'}
        #self.equals map, {'foo'=>{'wibble'=>'eek'},'bar'=>{'juu'=>'daa'}}
        #self.argument_error { map['juu'] = 123 }
        #self.equals map, {'foo'=>{'wibble'=>'eek'},'bar'=>{'juu'=>'daa'}}


    #def testMapComplexJsonObjectReturn(self):
        #map = obj.method_with_map_complex_json_object_return {}
        #m = map['foo']
        #self.equals m, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}


    #def testMapJsonArrayReturn(self):
        #map = obj.method_with_map_json_array_return {}
        #arr = map['foo']
        #self.equals arr.class, Array
        #self.equals arr, ['wibble']
        #map['bar'] = ['spidey']
        #self.equals map, {'foo'=>['wibble'],'bar'=>['spidey']}
        #self.argument_error { map['juu'] = 123 }
        #self.equals map, {'foo'=>['wibble'],'bar'=>['spidey']}


    #def testMapLongReturn(self):
        #map = obj.method_with_map_long_return {}
        #num = map['foo']
        #self.equals num.class, Fixnum
        #self.equals num, 123
        #map['bar'] = 321
        #self.equals map, {'foo'=>123,'bar'=>321}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>123,'bar'=>321}


    #def testMapIntegerReturn(self):
        #map = obj.method_with_map_integer_return {}
        #num = map['foo']
        #self.equals num.class, Fixnum
        #self.equals num, 123
        #map['bar'] = 321
        #self.equals map, {'foo'=>123,'bar'=>321}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>123,'bar'=>321}


    #def testMapShortReturn(self):
        #map = obj.method_with_map_short_return {}
        #num = map['foo']
        #self.equals num.class, Fixnum
        #self.equals num, 123
        #map['bar'] = 321
        #self.equals map, {'foo'=>123,'bar'=>321}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>123,'bar'=>321}


    #def testMapByteReturn(self):
        #map = obj.method_with_map_byte_return {}
        #num = map['foo']
        #self.equals num.class, Fixnum
        #self.equals num, 123
        #map['bar'] = 12
        #self.equals map, {'foo'=>123,'bar'=>12}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>123,'bar'=>12}


    #def testMapCharacterReturn(self):
        #map = obj.method_with_map_character_return {}
        #num = map['foo']
        #self.equals num.class, Fixnum
        #self.equals num, 88
        #map['bar'] = 89
        #self.equals map, {'foo'=>88,'bar'=>89}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>88,'bar'=>89}


    #def testMapBooleanReturn(self):
        #map = obj.method_with_map_boolean_return {}
        #num = map['foo']
        #self.equals num.class, TrueClass
        #self.equals num, true
        #map['bar'] = false
        #self.equals map, {'foo'=>true,'bar'=>false}
        #map['juu'] = 'something'
        #map['daa'] = nil
        #self.equals map, {'foo'=>true,'bar'=>false,'juu'=>true,'daa'=>false}


    #def testMapFloatReturn(self):
        #map = obj.method_with_map_float_return {}
        #num = map['foo']
        #self.equals num.class, Float
        #self.equals num, 0.123
        #map['bar'] = 0.321
        #self.equals map['foo'], 0.123
        #self.equals map['bar'], 0.321
        #self.equals map.keys.sort, %w(bar foo)
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map['foo'], 0.123
        #self.equals map['bar'], 0.321
        #self.equals map.keys.sort, %w(bar foo)


    #def testMapDoubleReturn(self):
        #map = obj.method_with_map_double_return {}
        #num = map['foo']
        #self.equals num.class, Float
        #self.equals num, 0.123
        #map['bar'] = 0.321
        #self.equals map, {'foo'=>0.123,'bar'=>0.321}
        #self.argument_error { map['juu'] = 'something' }
        #self.equals map, {'foo'=>0.123,'bar'=>0.321}


    #def testMapNullReturn(self):
        #map = obj.method_with_null_map_return
        #self.is_nil map


    #def testListStringReturn(self):
        #ret = obj.method_with_list_string_return
        #self.has_class ret, Array
        #self.equals ret, %w(foo bar wibble)


    #def testListLongReturn(self):
        #ret = obj.method_with_list_long_return
        #self.has_class ret, Array
        #self.equals ret, [123,456]


    #def testListJsonObjectReturn(self):
        #ret = obj.method_with_list_json_object_return
        #self.has_class ret, Array
        #self.equals ret, [{'foo'=>'bar'},{'blah'=>'eek'}]


    #def testListComplexJsonObjectReturn(self):
        #ret = obj.method_with_list_complex_json_object_return
        #self.has_class ret, Array
        #self.equals ret, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}]


    #def testListJsonArrayReturn(self):
        #ret = obj.method_with_list_json_array_return
        #self.has_class ret, Array
        #self.equals ret, [['foo'],['blah']]


    #def testListComplexJsonArrayReturn(self):
        #ret = obj.method_with_list_complex_json_array_return
        #self.has_class ret, Array
        #self.equals ret, [[{'foo' => 'hello'}],[{'bar' => 'bye'}]]


    #def testListVertxGenReturn(self):
        #ret = obj.method_with_list_vertx_gen_return
        #self.has_class ret, Array
        #self.has_class ret[0], Testmodel::RefedInterface1
        #self.equals ret[0].get_string, 'foo'
        #self.has_class ret[1], Testmodel::RefedInterface1
        #self.equals ret[1].get_string, 'bar'


    #def testSetStringReturn(self):
        #ret = obj.method_with_set_string_return
        #self.has_class ret, Set
        #self.equals ret, Set.new(%w(foo bar wibble))


    #def testSetLongReturn(self):
        #ret = obj.method_with_set_long_return
        #self.has_class ret, Set
        #self.equals ret, Set.new([123,456])


    #def testSetJsonObjectReturn(self):
        #ret = obj.method_with_set_json_object_return
        #self.has_class ret, Set
        #self.equals ret, Set.new([{'foo'=>'bar'},{'blah'=>'eek'}])


    #def testSetComplexJsonObjectReturn(self):
        #ret = obj.method_with_set_complex_json_object_return
        #self.has_class ret, Set
        #self.equals ret, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}].to_set


    #def testSetJsonArrayReturn(self):
        #ret = obj.method_with_set_json_array_return
        #self.has_class ret, Set
        #self.equals ret, Set.new([['foo'],['blah']])


    #def testSetComplexJsonArrayReturn(self):
        #ret = obj.method_with_set_complex_json_array_return
        #self.has_class ret, Set
        #self.equals ret, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]].to_set


    #def testSetVertxGenReturn(self):
        #ret = obj.method_with_set_vertx_gen_return
        #self.has_class ret, Set
        #ret.each { |elt| self.has_class(elt, Testmodel::RefedInterface1) }
        #self.assertEqual(ret.map { |o| o.get_string }.to_set, Set.new(%w(foo bar)))


    #def testThrowableReturn(self):
        #ret = obj.method_with_throwable_return 'bogies'
        #self.assertEqual('bogies', ret.message)


    #def testCustomModule(self):
        #my = Acme::MyInterface.create
        #test_interface = my.method
        #test_interface.method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
        #sub = my.sub
        #ret = sub.reverse "hello"
        #self.equals ret, "olleh"


    #def testMethodWithListParams(self):
        #obj.method_with_list_params(
            #%w(foo bar),
            #[2, 3],
            #[12, 13],
            #[1234, 1345],
            #[123, 456],
            #[{:foo=>'bar'}, {:eek=>'wibble'}],
            #[['foo'], ['blah']],
            #[Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('foo'), Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('bar')],
            #[{:foo=>'String 1',:bar=>1,:wibble=>1.1}, {:foo=>'String 2',:bar=>2,:wibble=>2.2}]
        #)
        #self.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


    #def testMethodWithSetParams(self):
        #obj.method_with_set_params(
            #Set.new(['foo', 'bar']),
            #Set.new([2, 3]),
            #Set.new([12, 13]),
            #Set.new([1234, 1345]),
            #Set.new([123, 456]),
            #Set.new([{:foo=>'bar'}, {:eek=>'wibble'}]),
            #Set.new([['foo'], ['blah']]),
            #Set.new([Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('foo'), Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('bar')]),
            #Set.new([{:foo=>'String 1',:bar=>1,:wibble=>1.1}, {:foo=>'String 2',:bar=>2,:wibble=>2.2}])
        #)
        #self.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


    #def testMethodWithMapParams(self):
        #obj.method_with_map_params(
            #{'foo'=>'bar','eek'=>'wibble'},
            #{'foo'=>2,'eek'=>3},
            #{'foo'=>12,'eek'=>13},
            #{'foo'=>1234,'eek'=>1345},
            #{'foo'=>123,'eek'=>456},
            #{'foo'=>{'foo'=>'bar'},'eek'=>{'eek'=>'wibble'}},
            #{'foo'=>['foo'],'eek'=>['blah']},
            #{'foo'=>Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('foo'),'eek'=>Testmodel::RefedInterface1.new(RefedInterface1Impl.new).set_string('bar')}
        #)
        #self.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


    #def testEnumParam(self):
        #ret = obj.method_with_enum_param('sausages', :TIM)
        #self.assertEqual(ret, 'sausagesTIM')


if __name__ == "__main__":
    meth = sys.argv[-1]
    print("Testing {}".format(meth))
    with util.handle_java_error():
        case = TestAPI(meth)
        case.debug()
        util.vertx_shutdown()

