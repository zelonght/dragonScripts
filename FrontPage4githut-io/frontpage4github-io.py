"""MS FrontPage came with paths having prefix with `_` (e.g.: _derived, _overlay, _themes) and they are not compatible or support by github.io (e.g.: 404 return code when accessing in browser). This script will search and rename such those folders and modify the linkings (e.g.: href, src) in htm files to solve that problem.

Author: LongTruong (zelonght)
Copyright: https://github.com/zelonght/dragonScripts
"""

import os, sys
import argparse
from shutil import copyfile, copytree, rmtree

def copyAndRename(base_path, oldFolder, newFolder):
    # Step 1: Copy as renaming folder with `_` in prefix.
    print("Renaming  images asset from {} to {}...".format(oldFolder, newFolder))
    os.rename(os.path.join(base_path, oldFolder), os.path.join(base_path, newFolder))

    # Step 2: modify the htm page with the path changes in step 1.
    for html_file in os.listdir(base_path):
        if os.path.splitext(html_file)[1] == '.htm':
            html_filepath = os.path.join(base_path, html_file)
            print("Modifying image src for {}...".format(html_filepath))
            with open(html_filepath, mode = 'r+', encoding = 'utf-8') as f:
                file_content = f.read()
                file_content_new = file_content.replace('"'+oldFolder, '"'+newFolder)
                f.seek(0)
                f.truncate()
                f.write(file_content_new)
                f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse parameters for the script')
    parser.add_argument('--path', help='path to the MSFrontPage site',default = os.path.abspath(__file__))
    parser.add_argument('--mode', help='mode report to converse: 0 - From MSFrontPage to github-io, 1 - From github-io back to MSFrontPage', default = 0)
    argz, remaining_argv = parser.parse_known_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)   
    args = parser.parse_args()
    print(args)

    if os.path.exists(args.path) is False:
        raise RuntimeError('Invalid value for path or path does not exist.')
    args.mode = int(args.mode)
    if not args.mode in [0, 1]:    
        raise RuntimeError('Invalid value for parameter mode')

    folders = ['_derived', '_overlay', '_themes'] 
    if args.mode == 0:
        for folder in folders:
            copyAndRename(args.path, folder, 'ms'+folder)
    else:# args.mode == 1
        for folder in folders:
            copyAndRename(args.path, 'ms'+folder, folder)

