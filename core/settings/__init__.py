# ANSI escape sequences
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
from utils.symbols import Symbols
import os

try:

    if os.getenv('ENVIRONMENT') == 'production':
        from .prod import *
        print(f"{GREEN}{BOLD}{Symbols.LOADING} : Loading production settings{RESET}\n")
    else:
        from .dev import *
        print(f"{YELLOW}{BOLD}{Symbols.LOADING} : Loading development settings{RESET}\n")
except Exception as e:
    print(f"{RED}{BOLD}{Symbols.ERROR} : Error loading settings: {e}{RESET}\n")
    raise str(e)

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/topics/settings/