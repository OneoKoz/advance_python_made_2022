import cProfile
import functools
import io
import pstats


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
