# coding=utf-8
import time


def retry_call(label, func, attempts=3, wait_seconds=2, on_error=None, log_func=print):
    if attempts < 1:
        raise ValueError("attempts must be greater than 0")
    if wait_seconds < 0:
        raise ValueError("wait_seconds must not be negative")

    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception as exception:
            last_error = exception
            if log_func:
                log_func("{} failed on attempt {}/{}: {}".format(label, attempt, attempts, exception))
            if on_error:
                on_error(exception, attempt)
            if attempt < attempts:
                time.sleep(wait_seconds)
    raise last_error
