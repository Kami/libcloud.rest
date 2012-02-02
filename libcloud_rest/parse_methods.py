import re
import inspect
from libcloud.compute.base import NodeDriver
from libcloud.compute.providers import DRIVERS
from types import FunctionType

IGNORE_FUNCTIONS = [
    'deploy_node',
    'create_node',
]

def ignored_function(func_str):
    return func_str.startswith('_') or func_str in IGNORE_FUNCTIONS

def get_argument(str, argspec):
    list = str.split(None, 2)
    arg_name = list[1].strip(':')
    arg_type = list[2]
    optional = False
    if argspec.defaults:
        for i, j in enumerate(argspec.defaults):
            if argspec.args[- (i + 1)] == arg_name:
                optional = True

    return {'name' : arg_name, 'type' : arg_type, 'optional' : optional}

def get_return(str):
    regex = '(.\{.*\})'
    val = re.search(regex, str)
    return val.group(0)

func_list = []
for x in inspect.getmembers(NodeDriver, inspect.ismethod):
    if not ignored_function(x[0]):
        func_detail = {}
        # function name
        func_detail['function_name'] = x[0]

        list_docs = inspect.getdoc(x[1]).splitlines()
        # for type and return
        list_of_argument = []
        list_of_return = []
        argspec = inspect.getargspec(x[1])
        for x in list_docs:
            if x.startswith('@type'):
                list_of_argument.append(get_argument(x, argspec))
            elif x.startswith('@return'):
                list_of_return.append(get_return(x))
        
        func_detail['argument_list'] = list_of_argument
        func_detail['return_list'] = list_of_return
        func_list.append(func_detail)


PROVIDERS_TO_FUNCTIONS = {}
for k, v in DRIVERS.items():
    t = k, v[1]
    PROVIDERS_TO_FUNCTIONS[t] = func_list

for k, v in PROVIDERS_TO_FUNCTIONS.items():
    print k, v, '\n'
