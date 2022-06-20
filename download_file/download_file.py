#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    This is the helper for download_files.py so please use it instead.
'''

import sys, time, os, argparse

import urllib2, cookielib

def verbose(msg, log_filepath = None, endline = '\n'):
    message = '{}{}'.format(msg, endline)
    if log_filepath:
        with open(log_filepath, 'a') as fso:
            fso.write(message)
    sys.stdout.write(message)
    sys.stdout.flush()
    time.sleep(0.01)

save_file = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Try download some files')

    parser.add_argument(
        '--url',
        help='Url to download',
        type=str
    )
    parser.add_argument(
        '--save_file',
        help='Save file = 1, or not = 0',
        default=0,
        type=int
    ) 
    args = parser.parse_args()

    cur_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(cur_path, 'temps')
    if args.save_file:
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

    log_filepath = os.path.join(cur_path, 'stdout_{}.log'.format(time.time()))
    stop_filepath = os.path.join(cur_path, 'stop.txt')
    
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    
    content_len = 0
    total_bytes = 0
    while True:
        if os.path.isfile(stop_filepath):
            sys.exit(0)
        
        tt = time.time()
        glue = "&" if "?" in args.url else "?"
        url =  "{}{}timestamp={}".format(args.url, glue, tt)

        req = urllib2.Request(url, headers=hdr)
        page = urllib2.urlopen(req)

        try:
            page = urllib2.urlopen(req)
            content = page.read()
            content_len = len(content)
            total_bytes = total_bytes + content_len
            verbose('Downloaded {} bytes from {}. Totally: {} MB'.format(content_len, url, round(total_bytes/1048576)), log_filepath)
            
            if args.save_file:
                file_to_save = os.path.join(save_path, 'image{}.png'.format(tt))
                verbose('Save download file to {}'.format(file_to_save), log_filepath)
                with open(file_to_save, 'wb') as fso:
                    fso.write(content)
        except:
            verbose('Error download file with url {}, skipping'.format(url), log_filepath)

    sys.exit(0)