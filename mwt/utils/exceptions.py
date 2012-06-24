import traceback
import sys


def get_stacktrace():
    exc_type, exc_value, exc_tb = sys.exc_info()
    return traceback.format_exception(exc_type, exc_value, exc_tb)


def get_stacktrace_string():
    return traceback.format_exc()
