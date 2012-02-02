import re
import inspect
from libcloud.compute.base import NodeDriver
from libcloud.compute.providers import DRIVERS

IGNORE_FUNCTIONS = [
    'deploy_node',
    'create_node',
]

# ignore the functions which start with _ (private functions)
# or some functions that we don't support currently
def ignored_function(func_str):
    return func_str.startswith('_') or func_str in IGNORE_FUNCTIONS

# make a dictionary of argument name, type, and whether it's optional
# from the docstring and the fucntion information using inspect
def get_argument(str, argspec):
    # expected str is following:
    #     @type location: L{NodeLocation}
    list = str.split(None, 2)
    arg_name = list[1].strip(':')
    arg_type = list[2]
    optional = False
    # ArgSpec(args=['self', 'location'], varargs=None, keywords=None, defaults=(None,)) 
    if argspec.defaults:
        for i, j in enumerate(argspec.defaults):
            if argspec.args[- (i + 1)] == arg_name:
                optional = True

    return {'name' : arg_name, 'type' : arg_type, 'optional' : optional}

# get the return value from the docstring
def get_return(str):
    regex = '(.\{.*\})'
    val = re.search(regex, str)
    return val.group(0)

# get the function name, argument list, return value list
# for the functions of the NodeDriver class
func_list = []
for x in inspect.getmembers(NodeDriver, inspect.ismethod):
    if not ignored_function(x[0]):
        func_detail = {}
        # get a function name
        func_detail['function_name'] = x[0]

        list_docs = inspect.getdoc(x[1]).splitlines()
        # get an argument list, return value list
        list_of_arguments = []
        list_of_return_values = []
        argspec = inspect.getargspec(x[1])
        for x in list_docs:
            if x.startswith('@type'):
                list_of_arguments.append(get_argument(x, argspec))
            elif x.startswith('@return'):
                list_of_return_values.append(get_return(x))
        
        func_detail['argument_list'] = list_of_arguments
        func_detail['return_list'] = list_of_return_values
        func_list.append(func_detail)


# get the list of drivers that libcloud supports,
# and list of functions that each driver has
PROVIDERS_TO_FUNCTIONS = {}
for k, v in DRIVERS.items():
    t = k, v[1]
    PROVIDERS_TO_FUNCTIONS[t] = func_list

for k, v in PROVIDERS_TO_FUNCTIONS.items():
    print k, v, '\n'
