
from core.settings.base import *
from utils.symbols import success, error, warning, loading, info


print(loading("Loading production settings..."))

DEBUG = False




print(success("Production settings loaded successfully."))
print(info("Remember to set DEBUG = False in production!"))