import json

def json_error(result, code):
    return (json.dumps({'result': result}), code, 
                {'Content-Type': 'application/json'})

def json_success():
    return '{"result":"success"}', 200, {'Content-Type', 'application/json'}

def json_result(obj):
    return json.dumps(obj), 200, {'Content-Type': 'application/json'}
