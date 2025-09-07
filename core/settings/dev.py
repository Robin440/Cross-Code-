
from core.settings.base import *
from utils.symbols import success, error, warning, loading, info

print(loading("Loading development settings..."))

DEBUG = True





print(success("Development settings loaded successfully."))
print(info("Remember to set DEBUG = False in production!"))