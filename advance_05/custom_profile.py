import cProfile
import functools
import io
import pstats
import time


def profile_dec(func):
    ps_global = pstats.Stats()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        retval = func(*args, **kwargs)
        profile.disable()
        stream = io.StringIO()
        psstats = pstats.Stats(profile, stream=stream).sort_stats('cumulative')
        ps_global.add(psstats)
        return retval

    def print_stat():
        ps_global.print_stats()

    wrapper.print_stat = print_stat
    return wrapper


def calculate_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} -> time work = {end_time - start_time}")
        return res
    return wrapper
