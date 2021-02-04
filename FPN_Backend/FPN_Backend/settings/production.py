from .base import *

DEBUG = False
ALLOWED_HOSTS = ['172.17.0.1,api.thefinpro.net,167.172.168.48'] 

try:
    from .local import *
except ImportError:
    pass
