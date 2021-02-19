#!/usr/bin/env python3

import sys
import os
import io
import fnmatch
import re
import stat
import errno
from os.path import abspath

import socket

#
# Handle cache
#
handle_cache = {}


# Trace levels
TRACE_LEVEL_ERROR   = 0
TRACE_LEVEL_WARNING = 1
TRACE_LEVEL_INFO    = 2
TRACE_LEVEL_VERBOSE = 3

# Trace names
trace_level_str = ('[ERROR]', '[WARNING]', '[INFO]', '[VERBOSE]')

# Set trace config
trace_level = TRACE_LEVEL_INFO
trace_dest = sys.stderr

#
# Debug printing
#
def trace(level, *args, **kwargs):
    global trace_level
    global trace_dest 
    
    if level <= trace_level:
        print(trace_level_str[level], *args, **kwargs, file=trace_dest)

#
# Trace helpers
#
trace_error     = lambda *args, **kwargs : trace(TRACE_LEVEL_ERROR, *args, **kwargs)
trace_warning   = lambda *args, **kwargs : trace(TRACE_LEVEL_WARNING, *args, **kwargs)
trace_info      = lambda *args, **kwargs : trace(TRACE_LEVEL_INFO, *args, **kwargs)
trace_verbose   = lambda *args, **kwargs : trace(TRACE_LEVEL_VERBOSE, *args, **kwargs)

#
# Retrieve a handle
#
def GetHandle(name):    
    global handle_cache

    # Retrieve from cached handles
    handle = handle_cache.get(name)
    if handle != None:
        handle.seek(0)
        return handle

    # Inspect the device
    path = abspath('/sys/class/' + name)
    try:
        mode = stat.S_IMODE(os.stat(path)[stat.ST_MODE])
    except:
        trace_warning('Cannot stat', name)
        return None

    # Determine mode flags
    r_ok = mode & stat.S_IRGRP
    w_ok = mode & stat.S_IWGRP
    if r_ok and w_ok:
        mode_str = 'r+'
    elif w_ok:
        mode_str = 'w'
    elif r_ok:
        mode_str = 'r'
    else:
        trace_warning('Cannot access', name)
        return None

    # Open the device
    try:
        handle = io.FileIO(path, mode_str)
    except:
        trace_warning("Cannot open", name)
        return None

    # Cache the handle and return it
    handle_cache[path] = handle   
    return handle


#
# Send command to client
#
def SendCommand(sock, cmd):
    if cmd == None:
        cmd = str()

    data = (len(cmd) + 4).to_bytes(4, byteorder='little') + cmd.encode()
    try:
        sock.sendall(data)
        return True
    except Exception as ex:
        trace_warning('Send failed', ex)
        return False

#
# Perform a read command
#
def ReadCommand(name):
    
    # Obtain handle to device
    handle = GetHandle(name)
    if handle == None:
        return None

    # Try to execute command
    try:
        return handle.read().strip().decode()
    except Exception as ex:
        trace_warning('Read failed on', name, ex)
        return None


#
# Write a command to a device
#
def WriteCommand(name, cmd):
    
    # Obtain handle to device
    handle = GetHandle(name)
    if handle == None:
        return False

    # Convert string to bytes
    if isinstance(cmd, str):
        cmd = cmd.encode()
    
    # Try to execute command
    try:
        handle.write(cmd)
        handle.flush()
        return True
    except Exception as ex:
        trace_warning("Write failed on", name, ex)
        return False


#
# Execute a name command
#
def ExecName(sock, parts):

    class_name = parts[1]
    name_pattern = ':' + parts[2]

    path_root  = '/sys/class/'
    class_path = abspath(path_root + class_name)

    name = ''
    for subdir in os.listdir(class_path):
        
        device_path = class_path + '/' + subdir
        trace_verbose(device_path)
        
        with io.FileIO(device_path + '/address') as f:
            address = f.read().strip().decode()
        
        if name_pattern in address:
            name = class_name + '/' + subdir
            trace_verbose('return', name)
            break

    # Send name back to client
    return SendCommand(sock, name)
    

#
# Execute a Get command
#
def ExecGet(sock, parts):

    # Check parts count
    if len(parts) != 2:
        return False

    # Read the value from the device
    value = ReadCommand(parts[1])

    # Send it to the client
    return SendCommand(sock, value)


#
# Execute a Set command
#
def ExecSet(sock, parts):
    
    # Check parts count
    if len(parts) != 3:
        return False

    # Write the command to the device
    return WriteCommand(parts[1], parts[2])


#
# Execute a function
#
def Exec(sock, cmd):

    # Split command into parts
    parts = cmd.decode().split(':')
    if len(parts) < 1:
        return False

    # Show command
    trace_verbose('Executing command', parts)

    # First part is command
    if parts[0] == 'name':
        return ExecName(sock, parts)
    elif parts[0] == 'get':
        return ExecGet(sock, parts)
    elif parts[0] == 'set':
        return ExecSet(sock, parts)
    else:
        trace_warning('Invalid command type', parts[0])
        return False


#
# Handle a connection
#
def HandleConnection(sock, addr):
    
    # Start with empty data buffer
    data = bytes()
    recv = bytes()

    # Process packets until connection closed
    while True:

        # Receive request
        try:
            recv = sock.recv(1024)
        except:
            return

        # Empty receive, connection closed
        if not recv:
            trace_info('Connection closed')
            return True

        # Add received to data
        trace_verbose('Received', len(recv), 'bytes')
        data += recv

        # Process data
        while len(data) >= 4:

            # Parse request length 
            data_len = int.from_bytes(data[:4], byteorder='little')
            trace_verbose('Expect', data_len, 'bytes, have', len(data))
            if len(data) < data_len:
                break

            # Extract command from data
            cmd = data[4:data_len]
            data = data[data_len:]

            # Perform command
            if not Exec(sock, cmd):
                return False

#
# Main function
#
def Main():
    # Create listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        
        # TODO make configurable
        sock.bind(('0.0.0.0', 44444))
        sock.listen()
        
        # Accept and handle connections
        while True:
            
            # Wait for connection
            trace_info('Listening...')
            conn, addr = sock.accept()

            # Process connection
            trace_info('Connection from', addr)
            with conn:
                HandleConnection(conn, addr)
            trace_info('Disconnected')

#
# Run main function
#
Main()
