#!/usr/bin/env python
from __future__ import division
import params
import os, sys, re, platform
import argparse
import subprocess, psutil, time
from datetime import datetime


def kill_proc_tree_by_name(process_name):
    """
        Kill all processes that contain process name
    """
    for proc in psutil.process_iter():
        try:  # There are some system process that we can't access
            if proc.name().lower().find(process_name) != -1:
                kill_proc_tree(proc.pid)
        except:
            pass

def kill_proc_tree(pid, including_parent=True):
    """
        Cross plat-form kill process by pid
        Ref: http://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows
    """
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        psutil.wait_procs(children, timeout=30)
        if including_parent:
            parent.kill()
            parent.wait(30)
    except psutil.NoSuchProcess:
        verbose('Process not found: please double check.')
        pass
    except psutil.TimeoutExpired:
        verbose('TimeoutExpired: please double check.')
        pass


def is_existing_proc_by_name(process_name):
    """
        Kill all processes that contain process name
    """
    for proc in psutil.process_iter():
        try:  # There are some system process that we can't access
            if proc.name().lower().find(process_name) != -1:
                return True
        except:
            pass
            
    return False

def check_any_apps_running():
    found_app = False
    for app in params.APPS_TO_CHECK: # if any([is_existing_proc_by_name(app) for app in params.APPS_TO_CHECK]):
        if is_existing_proc_by_name(app):
            verbose("Found {} is running!!!...\n\n".format(app))
            found_app = True
            break 
    if found_app:
        if params.ffmeg_p is None:
            verbose('Now running ffmpeg.exe as a subprocess...')
            current_tt_readable = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filepath = os.path.join(params.CUR_PATH, 'data', 'logs', 'log-{}.txt'.format(current_tt_readable))
            mv_filepath = os.path.join(params.CUR_PATH, 'data', 'mv-{}.mkv'.format(current_tt_readable))
            mmpeg_command = params.FFMEG_CMD.format(mv_filepath)
            
            verbose("... force end orphan ffmpeg.exe first.\n\n")
            kill_proc_tree_by_name("ffmpeg.exe")
            
            verbose("... creating new mv at {} and new log at {} using command  `{}`.\n\n".format(mv_filepath, log_filepath, mmpeg_command))
            params.record_started = time.time()
            with open(log_filepath, "w") as out:
                params.ffmeg_p = subprocess.Popen(
                    mmpeg_command,
                    stdout=out,
                    stderr=out,
                    creationflags=subprocessSkipCrash()
                )
        else:
            verbose('The ffmpeg.exe was running already.')
            if time.time() - params.record_started > params.record_max_hours:
                verbose("... force ending the session due to over {} seconds.\n\n".format(params.record_max_hours))
                if params.END_SESSION_MODE == 1:
                    verbose('... force closing session and lock the machine for more safe.')
                    os.system(os.path.join(params.CUR_PATH, 'lock-token.bat'))
                else:
                    for app in params.APPS_TO_CHECK:
                        verbose('... force closing {}.'.format(app))
                        kill_proc_tree_by_name(app)
                    verbose('... force closing ffmpeg.exe.')
                    kill_proc_tree(params.ffmeg_p.pid)
                    kill_proc_tree_by_name("ffmpeg.exe") # to be more safe
                    params.ffmeg_p = None
                    verbose('... done and wait for next cycle.\n\n')
            else:
                verbose("... nothing to do before {} seconds.\n\n".format(params.record_max_hours))
    else:
        if params.ffmeg_p is None:
            verbose('No apps found, ffmpeg.exe is not running, we can take some break!\n\n')
        else:    
            verbose('No apps found, ffmpeg.exe is running, time to stop...\n')
            kill_proc_tree(params.ffmeg_p.pid)
            kill_proc_tree_by_name("ffmpeg.exe") # to be more safe
            params.ffmeg_p = None
            verbose('... stopped ffmpeg.exe successfully!\n\n')


def subprocessSkipCrash():
    # Prevent report to be freezing even there is crashes during running subprocess
    # Ref: http://stackoverflow.com/questions/5069224/handling-subprocess-crash-in-windows
    if platform.system() == "Windows":
        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        SEM_FAILCRITICALERRORS = 0x0001 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX | SEM_FAILCRITICALERRORS)
        return 0x8000000 #win32con.CREATE_NO_WINDOW?
    else:
        return 0

def verbose(msg, endline = '\n'):
    """
        Output message to stdout with a verbosity level.
        This function also tries to flush events so that the message will be actually displayed in busy systems.
        Args:
            @msg [string] message to show
            @level [integer] verbosity level of this message
        Return:
            None
    """
    sys.stdout.write('{}: {}{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg, endline))
    sys.stdout.flush()
    time.sleep(0.01)


if __name__ == '__main__':

    # Creating lock file
    lock_filepath = os.path.join(params.CUR_PATH, 'lock.txt')
    with open(lock_filepath, 'w+') as fso:
        fso.close()
    while os.path.isfile(lock_filepath):
        check_any_apps_running()
        time.sleep(params.SLEEPING)

    sys.exit(0)

