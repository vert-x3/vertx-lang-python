import sys
import atexit

from py4j.java_gateway import JavaGateway, GatewayClient

from testmodel_python.testmodel.test_interface import TestInterface
from testmodel_python.testmodel.refed_interface1 import RefedInterface1
from testmodel_python.testmodel.factory import Factory
from acme_python.pkg.my_interface import MyInterface
from acme_python.sub.sub_interface import SubInterface

from vertx_python import util

util.vertx_init()

jvm = util.jvm

Assert = jvm.org.junit.Assert;
obj = TestInterface(jvm.io.vertx.codegen.testmodel.TestInterfaceImpl())
refed_obj = RefedInterface1(jvm.io.vertx.codegen.testmodel.RefedInterface1Impl())
refed_obj2 = RefedInterface1(jvm.io.vertx.codegen.testmodel.RefedInterface1Impl())

def testMethodWithBasicParams():
    print("MADE IT TO HERE")
    obj.method_with_basic_params(b'123', 12345, 1234567, 1265615234, 12.345, 12.34566, True, 88, 'foobar')


def testMethodWithBasicBoxedParams():
    obj.method_with_basic_boxed_params(b'123', 12345, 1234567, 1265615234, 12.345, 12.34566, True, 88)


def testMethodWithHandlerBasicTypes():
    dct = dict(count=0)
    def byte_handler(b):
        Assert.assertEquals(type(b), int)
        Assert.assertEquals(123, b, 0)
        dct['count'] += 1
    def short_handler(s):
        Assert.assertEquals(type(s), int)
        Assert.assertEquals(12345, s, 0)
        dct['count'] += 1
    def int_handler(i):
        Assert.assertEquals(type(i), int)
        Assert.assertEquals(1234567, i, 0)
        dct['count'] += 1
    def long_handler(l):
        Assert.assertEquals(type(l), long)
        Assert.assertEquals(1265615234, l, 0)
        dct['count'] += 1
    def float_handler(f):
        Assert.assertEquals(type(f), float)
        Assert.assertEquals(12.345, f, 0)
        dct['count'] += 1
    def double_handler(d):
        Assert.assertEquals(type(d), float)
        Assert.assertEquals(12.34566, d, 0)
        dct['count'] += 1
    def boolean_handler(b):
        Assert.assertEquals(type(b), bool)
        Assert.assertTrue(b)
        dct['count'] += 1
    def char_handler(c):
        Assert.assertEquals(type(c), str)
        Assert.assertEquals('X', c)
        dct['count'] += 1
    def string_handler(s):
        Assert.assertEquals(type(s), str)
        Assert.assertEquals('quux!', str)
        dct['count'] += 1

    obj.methodWithHandlerBasicTypes(byte_handler, short_handler, int_handler, long_handler,
                                    float_handler, double_handler, boolean_handler, char_handler,
                                    string_handler)
    Assert.assertEquals(dct['count'], 9, 0)
          
def testMethodWithHandlerAsyncResultBasicTypes():
    dct = dict(count=0)
    def byte_handler(b, err):
        Assert.assertEquals(type(b), int)
        Assert.assertEquals(123, b, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def short_handler(s, err):
        Assert.assertEquals(type(s), int)
        Assert.assertEquals(12345, s, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def int_handler(i, err):
        Assert.assertEquals(type(i), int)
        Assert.assertEquals(1234567, i, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def long_handler(l, err):
        Assert.assertEquals(type(l), long)
        Assert.assertEquals(1265615234l, l, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def float_handler(f, err):
        Assert.assertEquals(type(f), float)
        Assert.assertEquals(12.345, f, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def double_handler(d, err):
        Assert.assertEquals(type(d), float)
        Assert.assertEquals(12.34566, d, 0)
        Assert.assertNull(err)
        dct['count'] += 1
    def boolean_handler(b, err):
        Assert.assertEquals(type(b), bool)
        Assert.assertTrue(b)
        Assert.assertNull(err)
        dct['count'] += 1
    def char_handler(c, err):
        Assert.assertEquals(type(c), str)
        Assert.assertEquals('X', c)
        Assert.assertNull(err)
        dct['count'] += 1
    def string_handler(s, err):
        Assert.assertEquals(type(s), str)
        Assert.assertEquals('quux!', str)
        Assert.assertNull(err)
        dct['count'] += 1
    obj.method_with_handler_async_result_byte(False, byte_handler)
    obj.method_with_handler_async_result_short(False, byte_handler)
    obj.method_with_handler_async_result_integer(False, byte_handler)
    obj.method_with_handler_async_result_long(False, long_handler)
    obj.method_with_handler_async_result_float(False, float_handler)
    obj.method_with_handler_async_result_double(False, double_handler)
    obj.method_with_handler_async_result_boolean(False, boolean_handler)
    obj.method_with_handler_async_result_char(False, char_handler)
    obj.method_with_handler_async_result_string(False, string_handler)
    Assert.assertEquals(dct['count'], 9, 0)


def testMethodWithHandlerAsyncResultBasicTypesFails():
    dct = dict(count=0)
    def handler(x, err):
        Assert.assertNull(x);
        Assert.assertNotNull(err);
        Assert.assertEquals("foobar!", err.getMessage());
        dct['count'] += 1

    obj.method_with_handler_async_result_byte(True, handler)
    obj.method_with_handler_async_result_short(True, handler)
    obj.method_with_handler_async_result_integer(True, handler)
    obj.method_with_handler_async_result_long(True, handler)
    obj.method_with_handler_async_result_float(True, handler)
    obj.method_with_handler_async_result_double(True, handler)
    obj.method_with_handler_async_result_boolean(True, handler)
    obj.method_with_handler_async_result_char(True, handler)
    obj.method_with_handler_async_result_string(True, handler)
    Assert.assertEquals(dct['count'], 9, 0)

def testMethodWithUserTypes():
    refed_obj.set_string('aardvarks')
    obj.method_with_user_types(refed_obj)


def testObjectParam():
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


def testDataObjectParam():
    data_object = {"foo" : "Hello", "bar" : 123, "wibble" : 1.23}
    obj.method_with_data_object_param(data_object)


def testNullDataObjectParam():
    obj.method_with_null_data_object_param(None);


def testMethodWithHandlerDataObject():
    dct = dict(count=0)
    def handler(option):
        Assert.assertEquals("foo", option.foo)
        Assert.assertEquals(123, option.bar, 0)
        Assert.assertEquals(0.0, option.wibble, 0)
        dct['count'] += 1
    obj.method_with_handler_data_object(handler)
    Assert.assertEquals(dct['count'], 1, 0)


#def testMethodWithHandlerAsyncResultDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_data_object(false) { |err,val| Assert.is_nil(err); Assert.equals(val, {'foo' => 'foo', 'bar' => 123, 'wibble' => 0.0}); dct['count'] += 1 }
    #Assert.equals(count, 1)


#def testMethodWithHandlerAsyncResultDataObjectFails():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_data_object(true) { |err,val| Assert.is_nil(val); Assert.is_not_nil(err); Assert.equals(err.message, 'foobar!'); dct['count'] += 1 }
    #Assert.equals(count, 1)


#def testMethodWithHandlerListAndSet():
    #dct = dict(count=0)
    #obj.method_with_handler_list_and_set(
        #Proc.new { |val| Assert.equals(val, %w(foo bar wibble)); dct['count'] += 1 },
        #Proc.new { |val| Assert.equals(val, [5,12,100]); dct['count'] += 1 },
        #Proc.new { |val| Assert.equals(val, Set.new(%w(foo bar wibble))); dct['count'] += 1 }) do |val|
      #Assert.equals(val, Set.new([5,12,100])); dct['count'] += 1
    #end
    #Assert.equals(4, count)


#def testMethodWithHandlerAsyncResultListAndSet():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_string { |err,val| Assert.is_nil(err); Assert.equals(val, %w(foo bar wibble)); dct['count'] += 1 }
    #obj.method_with_handler_async_result_list_integer { |err,val| Assert.is_nil(err); Assert.equals(val, [5,12,100]); dct['count'] += 1 }
    #obj.method_with_handler_async_result_set_string { |err,val| Assert.is_nil(err); Assert.equals(val, Set.new(%w(foo bar wibble))); dct['count'] += 1 }
    #obj.method_with_handler_async_result_set_integer { |err,val| Assert.is_nil(err); Assert.equals(val, Set.new([5,12,100])); dct['count'] += 1 }
    #Assert.equals(4, count)


#def testMethodWithHandlerListVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_list_vertx_gen do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Testmodel::RefedInterface1)
      #Assert.equals(val[0].get_string, 'foo')
      #Assert.equals(val[1].class, Testmodel::RefedInterface1)
      #Assert.equals(val[1].get_string, 'bar')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListAbstractVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_list_abstract_vertx_gen do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].is_a?(Testmodel::RefedInterface2), true)
      #Assert.equals(val[0].get_string, 'abstractfoo')
      #Assert.equals(val[1].is_a?(Testmodel::RefedInterface2), true)
      #Assert.equals(val[1].get_string, 'abstractbar')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_vertx_gen do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Testmodel::RefedInterface1)
      #Assert.equals(val[0].get_string, 'foo')
      #Assert.equals(val[1].class, Testmodel::RefedInterface1)
      #Assert.equals(val[1].get_string, 'bar')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListAbstractVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_abstract_vertx_gen do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].is_a?(Testmodel::RefedInterface2), true)
      #Assert.equals(val[0].get_string, 'abstractfoo')
      #Assert.equals(val[1].is_a?(Testmodel::RefedInterface2), true)
      #Assert.equals(val[1].get_string, 'abstractbar')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_set_vertx_gen do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 2)
      #val.each { |elt| Assert.equals(elt.class, Testmodel::RefedInterface1) }
      #Assert.equals(val.map { |o| o.get_string }.to_set, Set.new(%w(foo bar)))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetAbstractVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_set_abstract_vertx_gen do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 2)
      #val.each { |elt| Assert.equals(elt.is_a?(Testmodel::RefedInterface2), true) }
      #Assert.equals(val.map { |o| o.get_string }.to_set, Set.new(%w(abstractfoo abstractbar)))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_vertx_gen do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 2)
      #val.each { |elt| Assert.equals(elt.class, Testmodel::RefedInterface1) }
      #Assert.equals(val.map { |o| o.get_string }.to_set, Set.new(%w(foo bar)))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetAbstractVertxGen():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_abstract_vertx_gen do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 2)
      #val.each { |elt| Assert.equals(elt.is_a?(Testmodel::RefedInterface2), true) }
      #Assert.equals(val.map { |o| o.get_string }.to_set, Set.new(%w(abstractfoo abstractbar)))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_list_json_object do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Hash)
      #Assert.equals(val[0], {'cheese' => 'stilton'})
      #Assert.equals(val[1].class, Hash)
      #Assert.equals(val[1], {'socks' => 'tartan'})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListNullJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_list_null_json_object do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListComplexJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_list_complex_json_object do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], {'outer' => {'socks' => 'tartan'}, 'list' => ['yellow', 'blue']})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Hash)
      #Assert.equals(val[0], {'cheese' => 'stilton'})
      #Assert.equals(val[1].class, Hash)
      #Assert.equals(val[1], {'socks' => 'tartan'})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListNullJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_null_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListComplexJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_complex_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_set_json_object do |val|
      #Assert.equals(val.class, Set)
      #val.each { |elt| Assert.equals(elt.is_a?(Hash), true) }
      #Assert.equals(val, Set.new([{'cheese' => 'stilton'},{'socks' => 'tartan'}]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetNullJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_set_null_json_object do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #val.each { |elt| Assert.is_nil(elt) }
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetComplexJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_set_complex_json_object do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #Assert.equals(val, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}].to_set)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #val.each { |elt| Assert.equals(elt.is_a?(Hash), true) }
      #Assert.equals(val, Set.new([{'cheese' => 'stilton'},{'socks' => 'tartan'}]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetNullJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_null_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #val.each { |elt| Assert.is_nil(elt) }
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetComplexJsonObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_complex_json_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #Assert.equals(val, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}].to_set)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_list_json_array do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Array)
      #Assert.equals(val[0], %w(green blue))
      #Assert.equals(val[1].class, Array)
      #Assert.equals(val[1], %w(yellow purple))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListNullJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_list_null_json_array do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 2)
      #Assert.equals(val[0].class, Array)
      #Assert.equals(val[0], %w(green blue))
      #Assert.equals(val[1].class, Array)
      #Assert.equals(val[1], %w(yellow purple))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListNullJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_null_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val.size, 1)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListComplexJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_complex_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]])
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_set_json_array do |val|
      #Assert.equals(val.class, Set)
      #val.each { |elt| Assert.equals(elt.is_a?(Array), true) }
      #Assert.equals(val, Set.new([%w(green blue), %w(yellow purple)]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetNullJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_set_null_json_array do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #val.each { |elt| Assert.is_nil(elt) }
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetComplexJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_set_complex_json_array do |val|
      #Assert.equals(val.class, Set)
      #Assert.equals(val, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]].to_set)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #val.each { |elt| Assert.equals(elt.is_a?(Array), true) }
      #Assert.equals(val, Set.new([%w(green blue), %w(yellow purple)]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetNullJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_null_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val.size, 1)
      #val.each { |elt| Assert.is_nil(elt) }
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListComplexJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_list_complex_json_array do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]])
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_list_data_object do |val|
      #Assert.equals(val.class, Array)
      #val.each { |elt| Assert.equals(elt.is_a?(Hash), true) }
      #Assert.equals(val[0], {'foo'=>'String 1','bar'=>1,'wibble'=>1.1})
      #Assert.equals(val[1], {'foo'=>'String 2','bar'=>2,'wibble'=>2.2})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerListNullDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_list_null_data_object do |val|
      #Assert.equals(val.class, Array)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerSetDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_set_data_object do |val|
      #Assert.equals(val, Set.new([{'foo'=>'String 1','bar'=>1,'wibble'=>1.1},{'foo'=>'String 2','bar'=>2,'wibble'=>2.2}]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerNullSetDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_set_null_data_object do |val|
      #Assert.equals(val, Set.new([nil]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetComplexJsonArray():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_complex_json_array do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Set)
      #Assert.equals(val, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]].to_set)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_data_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #val.each { |elt| Assert.equals(elt.is_a?(Hash), true) }
      #Assert.equals(val[0], {'foo'=>'String 1','bar'=>1,'wibble'=>1.1})
      #Assert.equals(val[1], {'foo'=>'String 2','bar'=>2,'wibble'=>2.2})
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultListNullDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_list_null_data_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Array)
      #Assert.equals(val[0], nil)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultSetDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_data_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val, Set.new([{'foo'=>'String 1','bar'=>1,'wibble'=>1.1},{'foo'=>'String 2','bar'=>2,'wibble'=>2.2}]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultNullSetDataObject():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_set_null_data_object do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val, Set.new([nil]))
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerUserTypes():
    #dct = dict(count=0)
    #obj.method_with_handler_user_types do |val|
      #Assert.equals(val.class, Testmodel::RefedInterface1)
      #Assert.equals(val.get_string, 'echidnas')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultUserTypes():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_user_types do |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val.class, Testmodel::RefedInterface1)
      #Assert.equals(val.get_string, 'cheetahs')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithConcreteHandlerUserTypeSubtype():
    #dct = dict(count=0)
    #arg = Testmodel::Factory.create_concrete_handler_user_type do |refedObj|
      #Assert.equals(refedObj.class, Testmodel::RefedInterface1)
      #Assert.equals(refedObj.get_string, 'echidnas')
      #dct['count'] += 1
    #end
    #obj.method_with_concrete_handler_user_type_subtype arg
    #Assert.equals(1, count)


#def testMethodWithAbstractHandlerUserTypeSubtype():
    #dct = dict(count=0)
    #arg = Testmodel::Factory.create_abstract_handler_user_type do |refedObj|
      #Assert.equals(refedObj.class, Testmodel::RefedInterface1)
      #Assert.equals(refedObj.get_string, 'echidnas')
      #dct['count'] += 1
    #end
    #obj.method_with_abstract_handler_user_type_subtype arg
    #Assert.equals(1, count)


#def testMethodWithConcreteHandlerUserTypeSubtypeExtension():
    #dct = dict(count=0)
    #arg = Testmodel::Factory.create_concrete_handler_user_type_extension do |refedObj|
      #Assert.equals(refedObj.class, Testmodel::RefedInterface1)
      #Assert.equals(refedObj.get_string, 'echidnas')
      #dct['count'] += 1
    #end
    #obj.method_with_concrete_handler_user_type_subtype_extension arg
    #Assert.equals(1, count)


#def testMethodWithHandlerVoid():
    #dct = dict(count=0)
    #obj.method_with_handler_void do |val|
      #Assert.is_nil(val)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultVoid():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_void(false) do |err|
      #Assert.is_nil(err)
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerAsyncResultVoidFails():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_void(true) do |err|
      #Assert.is_not_nil err
      #Assert.equals(err.message, 'foo!')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerThrowable():
    #dct = dict(count=0)
    #obj.method_with_handler_throwable do |err|
      #Assert.is_not_nil err
      #Assert.equals(err.message, 'cheese!')
      #dct['count'] += 1
    #end
    #Assert.equals(1, count)


#def testMethodWithHandlerGenericUserType():
    #def run_test(value, &assert)():
      #dct = dict(count=0)
      #obj.method_with_handler_generic_user_type(value) do |refedObj|
        #Assert.is_not_nil(refedObj)
        #Assert.equals(refedObj.class, Testmodel::GenericRefedInterface)
        #assert.call(refedObj.get_value)
        #dct['count'] += 1
      #end
      #Assert.equals(1, count)
    #end
    #run_test('string_value') { |value| Assert.equals(value, 'string_value') }
    #run_test({'key' => 'key_value'}) { |value| Assert.equals(value, {'key' => 'key_value'}) }
    #run_test(%w(foo bar juu)) { |value| Assert.equals(value, %w(foo bar juu)) }


#def testMethodWithHandlerAsyncResultGenericUserType():
    #def run_test(value, &assert)():
      #dct = dict(count=0)
      #obj.method_with_handler_async_result_generic_user_type(value) do |err,refedObj|
        #Assert.is_nil(err)
        #Assert.is_not_nil(refedObj)
        #Assert.equals(refedObj.class, Testmodel::GenericRefedInterface)
        #assert.call(refedObj.get_value)
        #dct['count'] += 1
      #end
      #Assert.equals(1, count)
    #end
    #run_test('string_value') { |value| Assert.equals(value, 'string_value') }
    #run_test({'key' => 'key_value'}) { |value| Assert.equals(value, {'key' => 'key_value'}) }
    #run_test(%w(foo bar juu)) { |value| Assert.equals(value, %w(foo bar juu)) }


#def testMethodWithGenericParam():
    #obj.method_with_generic_param 'String', 'foo'
    #obj.method_with_generic_param 'JsonObject', {'foo'=>'hello','bar'=>123}
    #obj.method_with_generic_param 'JsonArray', ['foo', 'bar', 'wib']


#def testMethodWithGenericHandler():
    #dct = dict(count=0)
    #obj.method_with_generic_handler('String') { |val| Assert.equals(val.class, String); Assert.equals(val, 'foo'); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler('Ref') { |val| Assert.equals(val.getString, 'bar'); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler('JsonObject') { |val| Assert.equals(val.class, Hash); Assert.equals(val, {'foo'=>'hello','bar'=>123}); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler('JsonArray') { |val| Assert.equals(val.class, Array); Assert.equals(val, ['foo','bar','wib']); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler('JsonObjectComplex') { |val| Assert.equals(val.class, Hash); Assert.equals(val, {'outer' => {'foo' => 'hello'}, 'bar'=> ['this', 'that']}); dct['count'] += 1 }
    #Assert.equals(1, count)


#def testMethodWithGenericHandlerAsyncResult():
    #dct = dict(count=0)
    #obj.method_with_generic_handler_async_result('String') { |err,val| Assert.is_nil(err); Assert.equals(val.class, String); Assert.equals(val, 'foo'); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler_async_result('Ref') { |err,val| Assert.is_nil(err); Assert.equals(val.getString, 'bar'); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler_async_result('JsonObject') { |err,val| Assert.is_nil(err); Assert.equals(val.class, Hash); Assert.equals(val, {'foo'=>'hello','bar'=>123}); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler_async_result('JsonObjectComplex') { |err,val| Assert.is_nil(err); Assert.equals(val.class, Hash); Assert.equals(val, {'outer' => {'foo' => 'hello'}, 'bar'=> ['this', 'that']}); dct['count'] += 1 }
    #Assert.equals(1, count)
    #dct = dict(count=0)
    #obj.method_with_generic_handler_async_result('JsonArray') { |err,val| Assert.is_nil(err); Assert.equals(val.class, Array); Assert.equals(val, ['foo','bar','wib']); dct['count'] += 1 }
    #Assert.equals(1, count)


#def testBasicReturns():
    #ret = obj.method_with_byte_return
    #Assert.equals(ret.class, Fixnum)
    #Assert.equals(ret, 123)
    #ret = obj.method_with_short_return
    #Assert.equals(ret.class, Fixnum)
    #Assert.equals(ret, 12345)
    #ret = obj.method_with_int_return
    #Assert.equals(ret.class, Fixnum)
    #Assert.equals(ret, 12345464)
    #ret = obj.method_with_long_return
    #Assert.equals(ret.class, Fixnum)
    #Assert.equals(ret, 65675123)
    #ret = obj.method_with_float_return
    #Assert.equals(ret.class, Float)
    #Assert.equals(ret, 1.23)
    #ret = obj.method_with_double_return
    #Assert.equals(ret.class, Float)
    #Assert.equals(ret, 3.34535)
    #ret = obj.method_with_boolean_return?
    #Assert.equals(ret.class, TrueClass)
    #Assert.equals(ret, true)
    #ret = obj.method_with_char_return
    #Assert.equals(ret.class, Fixnum)
    #Assert.equals(ret, 89)
    #ret = obj.method_with_string_return
    #Assert.equals(ret.class, String)
    #Assert.equals(ret, 'orangutan')


#def testVertxGenReturn():
    #ret = obj.method_with_vertx_gen_return
    #Assert.equals(ret.class, Testmodel::RefedInterface1)
    #Assert.equals(ret.get_string, 'chaffinch')


#def testVertxGenNullReturn():
    #ret = obj.method_with_vertx_gen_null_return
    #Assert.equals(nil, ret)


#def testAbstractVertxGenReturn():
    #ret = obj.method_with_abstract_vertx_gen_return
    #Assert.equals(ret.is_a?(Testmodel::RefedInterface2), true)
    #Assert.equals(ret.get_string, 'abstractchaffinch')


#def testMapComplexJsonArrayReturn():
    #map = obj.method_with_map_complex_json_array_return {}
    #m = map['foo']
    #Assert.equals m, [{'foo' => 'hello'}, {'bar' => 'bye'}]


#def testOverloadedMethods():
    #@refed_obj.set_string('dog')
    #called = false
    #ret = obj.overloaded_method('cat', @refed_obj)
    #Assert.equals(ret, 'meth1')
    #ret = obj.overloaded_method('cat', @refed_obj, 12345) { |animal| Assert.equals(animal, 'giraffe') ; called = true }
    #Assert.equals(ret, 'meth2')
    #Assert.equals(called, true)
    #called = false
    ## for some reason animal is sometimes equals to giraffe and sometimes empty
    #ret = obj.overloaded_method('cat') { |animal| called = true }
    #Assert.equals(ret, 'meth3')
    #Assert.equals(called, true)
    #called = false
    #ret = obj.overloaded_method('cat', @refed_obj) { |animal| Assert.equals(animal, 'giraffe') ; called = true }
    #Assert.equals(ret, 'meth4')
    #Assert.equals(called, true)
    #Assert.argument_error { obj.overloaded_method 'cat' }
    #Assert.argument_error { obj.overloaded_method('cat', @refed_obj, 12345) }
    #Assert.argument_error { obj.overloaded_method {} }


#def testSuperInterfaces():
    #obj.super_method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
    #Assert.equals(obj.is_a?(Testmodel::SuperInterface1), true)
    #obj.other_super_method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
    #Assert.equals(obj.is_a?(Testmodel::SuperInterface2), true)


#def testMethodWithGenericReturn():
    #ret = obj.method_with_generic_return('JsonObject')
    #Assert.equals(ret.class, Hash)
    #Assert.equals(ret, {'foo'=>'hello','bar'=>123})
    #ret = obj.method_with_generic_return('JsonArray')
    #Assert.equals(ret.class, Array)
    #Assert.equals(ret, %w(foo bar wib))


#def testFluentMethod():
    #ret = obj.fluent_method('bar')
    #Assert.equals(ret, obj)


#def testStaticFactoryMethod():
    #ret = Testmodel::TestInterface.static_factory_method('bar')
    #Assert.equals(ret.class, Testmodel::RefedInterface1)
    #Assert.equals(ret.get_string, 'bar')


#def testMethodWithCachedReturn():
    #ret = obj.method_with_cached_return('bar')
    #ret2 = obj.method_with_cached_return('bar')
    #Assert.equals ret, ret2
    #ret3 = obj.method_with_cached_return('bar')
    #Assert.equals ret, ret3
    #Assert.equals ret.get_string, 'bar'
    #Assert.equals ret2.get_string, 'bar'
    #Assert.equals ret3.get_string, 'bar'
    #ret.set_string 'foo'
    #Assert.equals ret2.get_string, 'foo'
    #Assert.equals ret3.get_string, 'foo'


#def testJsonReturns():
    #ret = obj.method_with_json_object_return
    #Assert.equals(ret, {'cheese'=>'stilton'})
    #ret = obj.method_with_json_array_return
    #Assert.equals(ret, %w(socks shoes))


#def testNullJsonReturns():
    #ret = obj.method_with_null_json_object_return
    #Assert.is_nil(ret)
    #ret = obj.method_with_null_json_array_return
    #Assert.is_nil(ret)


#def testComplexJsonReturns():
    #ret = obj.method_with_complex_json_object_return
    #Assert.equals ret, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}
    #ret = obj.method_with_complex_json_array_return
    #Assert.equals ret, [{'foo' => 'hello'}, {'bar' => 'bye'}]


#def testJsonParams():
    #obj.method_with_json_params({'cat' => 'lion', 'cheese' => 'cheddar'}, %w(house spider))


#def testNullJsonParams():
    #Assert.argument_error { obj.method_with_null_json_params(nil, nil) }


#def testJsonHandlerParams():
    #dct = dict(count=0)
    #obj.method_with_handler_json(
        #Proc.new { |val| Assert.equals(val, {'cheese'=>'stilton'}); dct['count'] += 1 }) do  |val|
      #Assert.equals(val, %w(socks shoes)); dct['count'] += 1
    #end
    #Assert.equals(2, count)


#def testNullJsonHandlerParams():
    #dct = dict(count=0)
    #obj.method_with_handler_null_json(
        #Proc.new { |val| Assert.is_nil(val); dct['count'] += 1 }) do |val|
      #Assert.is_nil(val); dct['count'] += 1
    #end
    #Assert.equals(2, count)


#def testComplexJsonHandlerParams():
    #dct = dict(count=0)
    #obj.method_with_handler_complex_json(
        #Proc.new { |val| Assert.equals(val, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}); dct['count'] += 1 }) do |val|
      #Assert.equals(val, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]])
      #dct['count'] += 1
    #end
    #Assert.equals(2, count)


#def testJsonHandlerAsyncResultParams():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_json_object { |err,val| Assert.is_nil(err); Assert.equals(val, {'cheese'=>'stilton'}); dct['count'] += 1 }
    #obj.method_with_handler_async_result_json_array { |err,val| Assert.is_nil(err); Assert.equals(val, ['socks','shoes']); dct['count'] += 1 }
    #Assert.equals(2, count)


#def testNullJsonHandlerAsyncResultParams():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_null_json_object { |err,val| Assert.is_nil(err); Assert.is_nil(val); dct['count'] += 1 }
    #obj.method_with_handler_async_result_null_json_array { |err,val| Assert.is_nil(err); Assert.is_nil(val); dct['count'] += 1 }
    #Assert.equals(2, count)


#def testEnumParam():
    #ret = obj.method_with_enum_param('sausages', :TIM)
    #Assert.equals(ret, 'sausagesTIM')


#def testEnumReturn():
    #ret = obj.method_with_enum_return('JULIEN')
    #Assert.equals(:JULIEN, ret)


#def testMapReturn():
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
    #Assert.equals writeLog, ['put(foo,bar)']
    #readLog.clear
    #writeLog.clear
    #Assert.equals map['foo'], 'bar'
    #Assert.is_not_nil readLog.index('get(foo)')
    #Assert.equals writeLog, []
    #map['wibble'] = 'quux'
    #readLog.clear
    #writeLog.clear
    #Assert.equals map.size, 2
    #Assert.equals map['wibble'], 'quux'
    #Assert.is_not_nil readLog.index('size()')
    #Assert.equals writeLog, []
    #readLog.clear
    #writeLog.clear
    #map.delete('wibble')
    #Assert.equals writeLog, ['remove(wibble)']
    #Assert.equals map.size, 1
    #map['blah'] = '123'
    #key_dct = dict(count=0)
    #readLog.clear
    #writeLog.clear
    #map.each { |k,v|
      #if key_count == 0
        #Assert.equals k, 'foo'
        #Assert.equals v, 'bar'
        #key_dct['count'] += 1
      #else
        #Assert.equals k, 'blah'
        #Assert.equals v, '123'
      #end
    #}
    #Assert.is_not_nil readLog.index('entrySet()')
    #Assert.equals writeLog, []
    #readLog.clear
    #writeLog.clear
    #map.clear
    #Assert.equals writeLog, ['clear()']


#def testMapStringReturn():
    #map = obj.method_with_map_string_return {}
    #val = map['foo']
    #Assert.equals val.class, String
    #Assert.equals val, 'bar'
    #map['juu'] = 'daa'
    #Assert.equals map, {'foo'=>'bar','juu'=>'daa'}
    #Assert.argument_error { map['wibble'] = 123 }
    #Assert.equals map, {'foo'=>'bar','juu'=>'daa'}


#def testMapJsonObjectReturn():
    #map = obj.method_with_map_json_object_return {}
    #json = map['foo']
    #Assert.equals json.class, Hash
    #Assert.equals json['wibble'], 'eek'
    #map['bar'] = {'juu'=>'daa'}
    #Assert.equals map, {'foo'=>{'wibble'=>'eek'},'bar'=>{'juu'=>'daa'}}
    #Assert.argument_error { map['juu'] = 123 }
    #Assert.equals map, {'foo'=>{'wibble'=>'eek'},'bar'=>{'juu'=>'daa'}}


#def testMapComplexJsonObjectReturn():
    #map = obj.method_with_map_complex_json_object_return {}
    #m = map['foo']
    #Assert.equals m, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}


#def testMapJsonArrayReturn():
    #map = obj.method_with_map_json_array_return {}
    #arr = map['foo']
    #Assert.equals arr.class, Array
    #Assert.equals arr, ['wibble']
    #map['bar'] = ['spidey']
    #Assert.equals map, {'foo'=>['wibble'],'bar'=>['spidey']}
    #Assert.argument_error { map['juu'] = 123 }
    #Assert.equals map, {'foo'=>['wibble'],'bar'=>['spidey']}


#def testMapLongReturn():
    #map = obj.method_with_map_long_return {}
    #num = map['foo']
    #Assert.equals num.class, Fixnum
    #Assert.equals num, 123
    #map['bar'] = 321
    #Assert.equals map, {'foo'=>123,'bar'=>321}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>123,'bar'=>321}


#def testMapIntegerReturn():
    #map = obj.method_with_map_integer_return {}
    #num = map['foo']
    #Assert.equals num.class, Fixnum
    #Assert.equals num, 123
    #map['bar'] = 321
    #Assert.equals map, {'foo'=>123,'bar'=>321}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>123,'bar'=>321}


#def testMapShortReturn():
    #map = obj.method_with_map_short_return {}
    #num = map['foo']
    #Assert.equals num.class, Fixnum
    #Assert.equals num, 123
    #map['bar'] = 321
    #Assert.equals map, {'foo'=>123,'bar'=>321}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>123,'bar'=>321}


#def testMapByteReturn():
    #map = obj.method_with_map_byte_return {}
    #num = map['foo']
    #Assert.equals num.class, Fixnum
    #Assert.equals num, 123
    #map['bar'] = 12
    #Assert.equals map, {'foo'=>123,'bar'=>12}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>123,'bar'=>12}


#def testMapCharacterReturn():
    #map = obj.method_with_map_character_return {}
    #num = map['foo']
    #Assert.equals num.class, Fixnum
    #Assert.equals num, 88
    #map['bar'] = 89
    #Assert.equals map, {'foo'=>88,'bar'=>89}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>88,'bar'=>89}


#def testMapBooleanReturn():
    #map = obj.method_with_map_boolean_return {}
    #num = map['foo']
    #Assert.equals num.class, TrueClass
    #Assert.equals num, true
    #map['bar'] = false
    #Assert.equals map, {'foo'=>true,'bar'=>false}
    #map['juu'] = 'something'
    #map['daa'] = nil
    #Assert.equals map, {'foo'=>true,'bar'=>false,'juu'=>true,'daa'=>false}


#def testMapFloatReturn():
    #map = obj.method_with_map_float_return {}
    #num = map['foo']
    #Assert.equals num.class, Float
    #Assert.equals num, 0.123
    #map['bar'] = 0.321
    #Assert.equals map['foo'], 0.123
    #Assert.equals map['bar'], 0.321
    #Assert.equals map.keys.sort, %w(bar foo)
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map['foo'], 0.123
    #Assert.equals map['bar'], 0.321
    #Assert.equals map.keys.sort, %w(bar foo)


#def testMapDoubleReturn():
    #map = obj.method_with_map_double_return {}
    #num = map['foo']
    #Assert.equals num.class, Float
    #Assert.equals num, 0.123
    #map['bar'] = 0.321
    #Assert.equals map, {'foo'=>0.123,'bar'=>0.321}
    #Assert.argument_error { map['juu'] = 'something' }
    #Assert.equals map, {'foo'=>0.123,'bar'=>0.321}


#def testMapNullReturn():
    #map = obj.method_with_null_map_return
    #Assert.is_nil map


#def testListStringReturn():
    #ret = obj.method_with_list_string_return
    #Assert.has_class ret, Array
    #Assert.equals ret, %w(foo bar wibble)


#def testListLongReturn():
    #ret = obj.method_with_list_long_return
    #Assert.has_class ret, Array
    #Assert.equals ret, [123,456]


#def testListJsonObjectReturn():
    #ret = obj.method_with_list_json_object_return
    #Assert.has_class ret, Array
    #Assert.equals ret, [{'foo'=>'bar'},{'blah'=>'eek'}]


#def testListComplexJsonObjectReturn():
    #ret = obj.method_with_list_complex_json_object_return
    #Assert.has_class ret, Array
    #Assert.equals ret, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}]


#def testListJsonArrayReturn():
    #ret = obj.method_with_list_json_array_return
    #Assert.has_class ret, Array
    #Assert.equals ret, [['foo'],['blah']]


#def testListComplexJsonArrayReturn():
    #ret = obj.method_with_list_complex_json_array_return
    #Assert.has_class ret, Array
    #Assert.equals ret, [[{'foo' => 'hello'}],[{'bar' => 'bye'}]]


#def testListVertxGenReturn():
    #ret = obj.method_with_list_vertx_gen_return
    #Assert.has_class ret, Array
    #Assert.has_class ret[0], Testmodel::RefedInterface1
    #Assert.equals ret[0].get_string, 'foo'
    #Assert.has_class ret[1], Testmodel::RefedInterface1
    #Assert.equals ret[1].get_string, 'bar'


#def testSetStringReturn():
    #ret = obj.method_with_set_string_return
    #Assert.has_class ret, Set
    #Assert.equals ret, Set.new(%w(foo bar wibble))


#def testSetLongReturn():
    #ret = obj.method_with_set_long_return
    #Assert.has_class ret, Set
    #Assert.equals ret, Set.new([123,456])


#def testSetJsonObjectReturn():
    #ret = obj.method_with_set_json_object_return
    #Assert.has_class ret, Set
    #Assert.equals ret, Set.new([{'foo'=>'bar'},{'blah'=>'eek'}])


#def testSetComplexJsonObjectReturn():
    #ret = obj.method_with_set_complex_json_object_return
    #Assert.has_class ret, Set
    #Assert.equals ret, [{'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']}].to_set


#def testSetJsonArrayReturn():
    #ret = obj.method_with_set_json_array_return
    #Assert.has_class ret, Set
    #Assert.equals ret, Set.new([['foo'],['blah']])


#def testSetComplexJsonArrayReturn():
    #ret = obj.method_with_set_complex_json_array_return
    #Assert.has_class ret, Set
    #Assert.equals ret, [[{'foo' => 'hello'}], [{'bar' => 'bye'}]].to_set


#def testSetVertxGenReturn():
    #ret = obj.method_with_set_vertx_gen_return
    #Assert.has_class ret, Set
    #ret.each { |elt| Assert.has_class(elt, Testmodel::RefedInterface1) }
    #Assert.equals(ret.map { |o| o.get_string }.to_set, Set.new(%w(foo bar)))


#def testComplexJsonHandlerAsyncResultParams():
    #dct = dict(count=0)
    #obj.method_with_handler_async_result_complex_json_object { |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val, {'outer' => {'socks' => 'tartan'}, 'list'=> ['yellow', 'blue']})
      #dct['count'] += 1
    #}
    #obj.method_with_handler_async_result_complex_json_array { |err,val|
      #Assert.is_nil(err)
      #Assert.equals(val, [{'foo' => 'hello'}, {'bar' => 'bye'}])
      #dct['count'] += 1
    #}
    #Assert.equals(2, count)


#def testThrowableReturn():
    #ret = obj.method_with_throwable_return 'bogies'
    #Assert.equals('bogies', ret.message)


#def testCustomModule():
    #my = Acme::MyInterface.create
    #test_interface = my.method
    #test_interface.method_with_basic_params(123, 12345, 1234567, 1265615234, 12.345, 12.34566, true, 88, 'foobar')
    #sub = my.sub
    #ret = sub.reverse "hello"
    #Assert.equals ret, "olleh"


#def testMethodWithListParams():
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
    #Assert.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


#def testMethodWithSetParams():
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
    #Assert.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


#def testMethodWithMapParams():
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
    #Assert.argument_error { obj.method_with_list_params(nil, nil, nil, nil, nil, nil, nil, nil) }


if __name__ == "__main__":
    meth = sys.argv[3]
    print("calling {}".format(meth))
    globals()[meth]()
