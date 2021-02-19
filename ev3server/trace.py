#!/usr/bin/env python3

#
# Tracing
#

# Imports
import sys

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
def trace(msg_level, *args, **kwargs):
    global level
    global dest 
    
    if msg_level <= level:
        print(trace_level_str[level], *args, **kwargs, file=dest)

#
# Trace helpers
#
error     = lambda *args, **kwargs : trace(TRACE_LEVEL_ERROR, *args, **kwargs)
warning   = lambda *args, **kwargs : trace(TRACE_LEVEL_WARNING, *args, **kwargs)
info      = lambda *args, **kwargs : trace(TRACE_LEVEL_INFO, *args, **kwargs)
verbose   = lambda *args, **kwargs : trace(TRACE_LEVEL_VERBOSE, *args, **kwargs)
