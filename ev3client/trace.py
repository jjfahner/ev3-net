#
# Tracing
#

# Imports
import sys

#
# Trace class
#
class Trace():

    # Trace levels
    TRACE_LEVEL_ERROR   = 0
    TRACE_LEVEL_WARNING = 1
    TRACE_LEVEL_INFO    = 2
    TRACE_LEVEL_VERBOSE = 3

    # Trace names
    trace_level_str = ('[ERROR]', '[WARNING]', '[INFO]', '[VERBOSE]')

    # Set trace config
    level = TRACE_LEVEL_INFO
    dest  = sys.stderr

    #
    # Debug printing
    #
    @staticmethod
    def Write(msg_level, *args, **kwargs):
        if msg_level <= Trace.level:
            print(Trace.trace_level_str[msg_level], *args, **kwargs, file=Trace.dest)

    #
    # Trace helpers
    #
    Error     = lambda *args, **kwargs : Trace.Write(Trace.TRACE_LEVEL_ERROR, *args, **kwargs)
    Warning   = lambda *args, **kwargs : Trace.Write(Trace.TRACE_LEVEL_WARNING, *args, **kwargs)
    Info      = lambda *args, **kwargs : Trace.Write(Trace.TRACE_LEVEL_INFO, *args, **kwargs)
    Verbose   = lambda *args, **kwargs : Trace.Write(Trace.TRACE_LEVEL_VERBOSE, *args, **kwargs)
