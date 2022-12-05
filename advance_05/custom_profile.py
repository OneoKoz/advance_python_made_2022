import cProfile
import functools
import io
import pstats


def profile_dec(func):
    ps_global = pstats.Stats()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps_global.add(ps)
        return retval

    def print_stat():
        ps_global.print_stats()

    wrapper.print_stat = print_stat
    return wrapper
