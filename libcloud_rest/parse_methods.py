from libcloud.compute.base import NodeDriver
from libcloud.compute.providers import DRIVERS
from types import FunctionType

f_list = []
for k, v in NodeDriver.__dict__.iteritems():
    if type(v) == FunctionType and not k.startswith('_'):
        f_list.append(k)

PROVIDERS_TO_FUNCTIONS = {}
for k, v in DRIVERS.items():
    t = k, v[1]
    PROVIDERS_TO_FUNCTIONS[t] = f_list

for k, v in PROVIDERS_TO_FUNCTIONS.items():
    print k, v
