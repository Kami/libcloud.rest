import re
import inspect
from libcloud.compute.base import NodeDriver
from libcloud.compute.providers import DRIVERS

IGNORE_FUNCTIONS = [
    'deploy_node',
    'create_node',
]


# ignore functions that start with _ (private functions)
# and functions that we don't support currently
def ignored_function(func_str):
    return func_str.startswith('_') or func_str in IGNORE_FUNCTIONS


# make a dictionary of argument name, type, and whether it's optional
# from the docstring and the function information using inspect
def get_argument(docstring_line, argspec):
    # expected str is following:
    # @type location: L{NodeLocation}
    docstring_list = docstring_line.split(None, 2)
    arg_name = docstring_list[1].strip(':')
    arg_type = docstring_list[2]
    optional = False
    # ArgSpec(args=['self', 'location'], varargs=None, keywords=None, defaults=(None,))
    if argspec.defaults:
        for i, j in enumerate(argspec.defaults):
            if argspec.args[-(i + 1)] == arg_name:
                optional = True

    return {'name': arg_name, 'type': arg_type, 'optional': optional}


# get the return value from the docstring
def get_return(docstring_line):
    regex = '(.\{.*\})'
    val = re.search(regex, docstring_line)
    return val.group(0)

# get the function name, argument list, return value list
# for the functions of the NodeDriver class
func_list = []
# method_tuple looks like this:
# ('list_images', <unbound method NodeDriver.list_images>)
for method_tuple in inspect.getmembers(NodeDriver, inspect.ismethod):
    if not ignored_function(method_tuple[0]):
        func_detail = {}
        # get function name
        func_detail['function_name'] = method_tuple[0]

        list_docs = inspect.getdoc(method_tuple[1]).splitlines()
        # get argument list, return value list
        list_of_arguments = []
        list_of_return_values = []
        argspec = inspect.getargspec(method_tuple[1])
        for docstring_line in list_docs:
            if docstring_line.startswith('@type'):
                list_of_arguments.append(get_argument(docstring_line, argspec))
            elif docstring_line.startswith('@return'):
                list_of_return_values.append(get_return(docstring_line))

        func_detail['argument_list'] = list_of_arguments
        func_detail['return_list'] = list_of_return_values
        func_list.append(func_detail)


# get the list of drivers that libcloud supports,
# and list of functions that each driver has
PROVIDERS_TO_FUNCTIONS = {}
for driver_id, driver_tuple in DRIVERS.items():
    driver_name = driver_tuple[1]
    driver_id_and_name = driver_id, driver_name
    PROVIDERS_TO_FUNCTIONS[driver_id_and_name] = func_list

if __name__ == '__main__':
    for driver_id_and_name, func_list in PROVIDERS_TO_FUNCTIONS.items():
        driver_name = driver_id_and_name[1]
        print driver_name
        for func in func_list:
            print "Function name: %s, Argument list: %s, Return list: %s" % \
                    (func['function_name'], func['argument_list'], func['return_list'])
        print "=" * 80
