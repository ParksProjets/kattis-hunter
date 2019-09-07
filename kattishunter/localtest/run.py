"""

Run a batch of tests and return CPU time.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, os.path as path
import sys
import signal
from typing import Text, List
import logging

logger = logging.getLogger(__name__)


def setfd(fd: int, filename: Text, flag: int):
    "Pipe the given file to the pipe defined by fd."

    if isinstance(filename, str):
        tmpfd = os.open(filename, flag)
        os.dup2(tmpfd, fd)
        os.close(tmpfd)
    else:
        os.dup2(filename, fd)



def runexe(argv: List[Text], stdin: Text, stdout: Text):
    "Run the test executable."

    pid = os.fork()
    if pid == 0:
        try:
            setfd(0, stdin, os.O_RDONLY)
            setfd(1, stdout, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            os.execvp(argv[0], argv)
        except Exception as exc:
            os.kill(os.getpid(), signal.SIGTERM)

    return pid



def runtest(infile: Text, exe: Text):
    "Run the given test."

    # Create pipes for comunnicating between server and client.
    folder = path.dirname(exe)
    s2p_r, s2p_w = os.pipe()
    p2s_r, p2s_w = os.pipe()

    # Run server and client.
    logger.debug("Running test for input '%s'.", path.basename(infile))
    exe = path.abspath(exe)
    pidserver = runexe([exe, "s", "l", infile], p2s_r, s2p_w)
    pidclient = runexe([exe], s2p_r, p2s_w)

    # Wait for the client and kill the server.
    (_, status, rusage) = os.wait4(pidclient, 0)
    os.kill(pidserver, signal.SIGTERM)

    # Return client status and CPU time.
    rtime = rusage.ru_utime + rusage.ru_stime
    logger.debug("Test done in %.2f s with status %d.", rtime, status >> 8)
    return (status >> 8, rtime)
