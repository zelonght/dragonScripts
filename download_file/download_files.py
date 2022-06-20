#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Syntax: python download_files.py --instances 10 --howlong 30 --save_file 1 --url "https://s1.vnecdn.net/vnexpress/restruct/i/v562/v2_2019/pc/graphics/logo.svg"
    A simple script to test file content serving/downloading from a server.
    Please caustious as this is kind of stress/load test and may slow down a server during testing.
'''

import sys, time, os, argparse
import subprocess as sp

def verbose(msg, endline = '\n'):
    sys.stdout.write('{}{}'.format(msg, endline))
    sys.stdout.flush()
    time.sleep(0.01)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Try download some files')

    parser.add_argument(
        '--url',
        help='Url to download',
        type=str
    )
    parser.add_argument(
        '--instances',
        help='Number of instances to run a time',
        default=10,
        type=int
    )
    parser.add_argument(
        '--howlong',
        help='How long to run (s). Note: create stop.txt to force stop',
        default=60,
        type=int
    )
    parser.add_argument(
        '--save_file',
        help='Save file = 1, or not = 0',
        default=0,
        type=int
    )

    args = parser.parse_args()

    cur_path = os.path.dirname(os.path.realpath(__file__))
    stop_filepath = os.path.join(cur_path, 'stop.txt')

    instances = int(args.instances)
    howlong = int(args.howlong)
    p = [None] * instances # Create array with fixed size
    for idx in range(0, instances):
        verbose('Running instance #{}/{}...'.format(idx+1, instances))
        p[idx] = sp.Popen(
            ['python', 'download_file.py','--url', args.url, '--save_file', str(args.save_file)],
            stdout = open(os.devnull, "w")
        )
        time.sleep(0.1)

    time.sleep(args.howlong)
    with open(stop_filepath, 'w') as fso:
        fso.write('Stop!')    
    
    sys.exit(0)
