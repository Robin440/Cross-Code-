class Symbols:
    """Class containing various symbols for use in the application."""
    
    USER = "👤"
    SETTINGS =  "⚙️"
    WARNING = "⚠️"
    ERROR = "❌"
    SUCCESS = "✅"
    INFO = "ℹ️"
    LOADING = "⏳"
    CHECKMARK = "✔️"
    CROSSMARK = "❌"
    STAR = "⭐"
    HEART = "❤️"
    FIRE = "🔥"
    CROSS_CODE = "👾"


class LogColors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    ORANGE = "\033[33m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[97m"


def format_message(message: str, level: str = "info") -> str:
    """
    Format a message with color, bold, and symbol.
    Levels: success, error, warning, loading, info
    """
    level = level.lower()

    if level == "success":
        return f"{LogColors.GREEN}{LogColors.BOLD}{Symbols.SUCCESS} : {message}{LogColors.RESET}\n"
    elif level == "error":
        return f"{LogColors.RED}{LogColors.BOLD}{Symbols.ERROR} : {message}{LogColors.RESET}\n"
    elif level == "warning":
        return f"{LogColors.YELLOW}{LogColors.BOLD}{Symbols.WARNING} : {message}{LogColors.RESET}\n"
    elif level == "loading":
        return f"{LogColors.BLUE}{LogColors.BOLD}{Symbols.LOADING} : {message}{LogColors.RESET}\n"
    elif level == "info":
        return f"{LogColors.WHITE}{LogColors.BOLD}{Symbols.INFO} : {message}{LogColors.RESET}\n"
    else:  # fallback
        return f"{LogColors.BOLD} : {message}{LogColors.RESET}\n"


def success(msg): return format_message(msg, "success")
def error(msg): return format_message(msg, "error")
def warning(msg): return format_message(msg, "warning")
def loading(msg): return format_message(msg, "loading")
def info(msg): return format_message(msg, "info")