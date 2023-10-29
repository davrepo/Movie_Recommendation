import threading

class TimeoutException(Exception):   # Custom exception class
    pass

def break_after(seconds=2):
    def function(function):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def worker():
                try:
                    result[0] = function(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=worker)
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                print(f'Timeout Exception ({seconds}s) - {function}({args})')
            elif exception[0] is not None:
                raise exception[0]
            else:
                return result[0]

        return wrapper
    return function
