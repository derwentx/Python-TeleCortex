"""
Run a given script and check STDOUT and STDERR for strings that indicate that it has failed.
Restart the script periodically.
Rerout stdin/stdout/stderr from watchdog process to child process

Usage:

    python watchdog.py <your script>

To get a list of poc scripts and what they do, check out poc/__init__.py
"""

import fcntl
import os
import pty
import subprocess
import errno
import sys
import signal
import time
import tty
import termios

from six import text_type, binary_type

ENCODING = 'latin-1'
BUFFSIZE = 2048

SIGNAL_DICT = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
     if v.startswith('SIG') and not v.startswith('SIG_'))

def watchdog_print(thing):
    print("[watchdog] %s" % text_type(thing))

def set_nonblocking(file_obj):
    flags = fcntl.fcntl(file_obj, fcntl.F_GETFL)
    # print("flags before on %s are %s" % (file_obj, flags))
    flags = flags | os.O_NONBLOCK
    # print("flags after on %s are %s" % (file_obj, flags))
    fcntl.fcntl(file_obj, fcntl.F_SETFL, flags)

def set_blocking(file_obj):
    flags = fcntl.fcntl(file_obj, fcntl.F_GETFL)
    # print("flags before on %s are %s" % (file_obj, flags))
    flags = flags & ~os.O_NONBLOCK
    # print("flags after on %s are %s" % (file_obj, flags))
    fcntl.fcntl(file_obj, fcntl.F_SETFL, flags)

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

def pgid_exists(pgid):
    if pgid < 0:
        return False
    if pgid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.killpg(pgid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

def actually_kill_proc(proc):
    try:
        exc = None
        if pid_exists(proc.pid):
            pgid = os.getpgid(proc.pid)
            if pgid_exists(pgid):
                watchdog_print("terminating")
                watchdog_print("my_pid: %s, my_pgid: %s, my_ppid: %s, proc_pid: %s proc_pgid: %s" % (
                    os.getpid(), os.getpgid(os.getpid()), os.getppid(),
                    proc.pid, os.getpgid(proc.pid)
                ))
                os.killpg(pgid, signal.SIGTERM)
                return
    except OSError as this_exc:
        exc = this_exc
    watchdog_print("tried to terminate process that is already dead: %s" % str(exc))

def check_out_for_exceptions(out, exceptions):
    for exc in exceptions:
        if exc.upper() in out.upper():
            watchdog_print("found %s in output" % exc)
            return True

def describe_retval(retval):
    if retval is None:
        return "timeout"
    elif retval < 0:
        return "%s%s" % (retval, " (%s)" % SIGNAL_DICT[-retval] if -retval in SIGNAL_DICT else '')
    elif retval > 0:
        return "%s%s" % (retval, " (%s)" % errno.errorcode[retval] if retval in errno.errorcode else '')
    return "success"

def text_2_bin(text):
    return binary_type(text, ENCODING)

def bin_2_text(text):
    return text_type(text, ENCODING)

def watchdog(args, exceptions, timeout=3600):
    """
    creates a subprocess using args, monitors output for exceptions (case insensitive), and restarts if found
    """
    watchdog_print("press ctrl-c to kill process, r<enter> to restart")

    restarts = 0
    last_restart = False

    while not last_restart:
        watchdog_print("creating process with args: %s" % args)

        pty_master, pty_slave = pty.openpty()
        aux_master, aux_slave = pty.openpty()

        # probably not necessary?
        # tty.setraw(pty_master)
        tty.setraw(pty_slave)
        # tty.setraw(aux_master)
        tty.setraw(aux_slave)

        stdin_orig_settings = termios.tcgetattr(sys.stdin)

        set_blocking(pty_slave)
        set_blocking(aux_slave)

        proc = subprocess.Popen(
            args=args,
            stdin=pty_slave,
            stdout=pty_slave,
            stderr=aux_slave,
            close_fds=True,
            preexec_fn=os.setsid,
        )


        time.sleep(0.1)

        start = time.clock()

        last_io_cycle = False

        try:
            while proc.returncode is None and (time.clock() - start < timeout) and not last_io_cycle:
                # watchdog_print("start of loop")
                try:
                    set_nonblocking(sys.stdin)
                    stdin_text = bin_2_text(os.read(sys.stdin.fileno(), BUFFSIZE))
                    set_blocking(sys.stdin)
                except (IOError, OSError):
                    stdin_text = None
                except Exception as exc:
                    watchdog_print("! READ STDIN FAILED: %s %s, " % (type(exc), exc))
                    raise exc
                finally:
                    set_blocking(sys.stdin)

                if stdin_text is not None and len(stdin_text) > 0:
                    stdin_binary = text_2_bin(stdin_text)
                    print("SEND STDIN %s" % (repr(stdin_binary)))
                    if text_2_bin('\x03') in stdin_binary: # ctrl -c
                        watchdog_print("raising KeyboardInterrupt")
                        raise KeyboardInterrupt("received '\\x03' from stdin")

                    elif text_2_bin('r') in stdin_binary:
                        watchdog_print("received r from stdin, restarting")
                        proc.terminate()
                    else:
                        os.write(pty_master, stdin_binary)

                try:
                    set_nonblocking(pty_master)
                    stdout_text = bin_2_text(os.read(pty_master, BUFFSIZE))
                    set_blocking(pty_master)
                except (IOError, OSError):
                    stdout_text = None
                except Exception as exc:
                    watchdog_print("! READ STDOUT FAILED: %s %s, " % (type(exc), exc))
                    raise exc
                if stdout_text is not None:
                    # watchdog_print("RECV STDOUT %s" % (repr(stdout_text)))
                    # print(text_2_bin(stdout_text))

                    if check_out_for_exceptions(stdout_text, exceptions):
                        time.sleep(0.1)
                        try:
                            set_nonblocking(pty_master)
                            stdout_text += bin_2_text(os.read(pty_master, BUFFSIZE))
                            set_blocking(pty_master)
                        except (IOError, OSError):
                            pass
                        last_io_cycle = True
                        actually_kill_proc(proc)

                    os.write(sys.stdout.fileno(), text_2_bin(stdout_text))

                try:
                    set_nonblocking(aux_master)
                    stderr_text = bin_2_text(os.read(aux_master, BUFFSIZE))
                    set_blocking(aux_master)
                except (IOError, OSError):
                    stderr_text = None
                except Exception as exc:
                    watchdog_print("! READ STDERR FAILED: %s %s, " % (type(exc), exc))
                    raise exc
                if stderr_text is not None:

                    if check_out_for_exceptions(stderr_text, exceptions):
                        time.sleep(0.1)
                        try:
                            set_nonblocking(aux_master)
                            stderr_text += bin_2_text(os.read(aux_master, BUFFSIZE))
                            set_blocking(aux_master)
                        except (IOError, OSError):
                            pass

                        last_io_cycle = True
                        actually_kill_proc(proc)

                    os.write(sys.stdout.fileno(), text_2_bin(stderr_text))

                # watchdog_print("end of loop")
                time.sleep(0.01)
                sys.stdout.flush()
                proc.poll()

        except KeyboardInterrupt:
            last_restart = True
        except Exception as exc:
            watchdog_print("there was an exception in the main loop: %s %s" % (
                type(exc), exc
            ))
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, stdin_orig_settings)
            watchdog_print("outside of io loop, proc.returncode is %s - %s" % (
                proc.returncode, describe_retval(proc.returncode)
            ))
            if proc.returncode is None:
                actually_kill_proc(proc)
            end = time.clock()
            if(end - start < 0.1 and restarts > 1):
                watchdog_print("subprocess terminated immediately after multiple restarts, waiting")
                time.sleep(1)

        if last_restart:
            break

        restarts += 1
        watchdog_print("restart number %d" % restarts )


def main():
    if len(sys.argv) < 2:
        print('usage: %s script_name [script_arguments]' % sys.argv[0])
    args = [sys.executable] + sys.argv[1:]
    watchdog(args, ['Exception', 'Traceback (most recent call last)'])


if __name__ == '__main__':
    main()
