import json
from py4j.java_gateway import is_instance_of
from py4j.protocol import Py4JNetworkError

java_gateway = None
jvm = None
jvertx = None

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

def convert_char(ch):
    return chr(ch) if isinstance(ch, int) else ch

def json_to_python(obj):
    """Converts a Java JSON object to Python dict or list"""
    return json.loads(obj.encode()) if obj is not None else None

def list_obj_to_python(obj, type):
    """Converts a Java iterable of objects to a Python list"""
    if obj is None:
        return None
    result = []
    iterator = obj.iterator()
    while iterator.hasNext():
        val = iterator.next()
        result.append(type(json.loads(val.encode())) if val is not None else None)
    return result

def list_to_json(obj):
    """Converts a Python list to Java JsonArray"""
    return jvm.io.vertx.core.json.JsonArray(json.dumps(obj)) if obj is not None else None

def dict_to_json(obj):
    """Converts a Python dictionary to Java JsonObject"""
    return jvm.io.vertx.core.json.JsonObject(json.dumps(obj)) if obj is not None else None

def python_to_java(obj):
    """Converts an arbitrary Python object to Java"""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return dict_to_json(obj)
    elif isinstance(obj, list):
        return list_to_json(obj)
    return obj

def java_to_python(obj):
    """Converts an arbitrary Java object to Python"""
    if obj is None:
        return None
    elif is_instance_of(java_gateway, obj, jvm.io.vertx.core.json.JsonObject) or is_instance_of(java_gateway, obj, jvm.io.vertx.core.json.JsonArray):
        return json_to_python(obj)
    else:
        return obj
