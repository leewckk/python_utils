"""
    do some file copy , and keep the file structure
    author: liwenchao
    Email: leewckk@gmail.com , leewckk@126.com
"""

import os
import shutil
import argparse


# check if file extension in extension list
def is_file_ext_in_list(filename: str, extlist: list):
    return any(filename.endswith(ext) for ext in extlist)


def copy_files(source_folder: str, destination_folder: str, exts: list):
    for foldername, subfolders, filenames in os.walk(source_folder):
        for filename in filenames:
            if len(exts) == 0 or is_file_ext_in_list(filename, exts):
                source_path = os.path.join(foldername, filename)

                # keep the file path relationship
                relative_path = os.path.relpath(source_path, source_folder)
                destination_path = os.path.join(destination_folder, relative_path)

                # make sure the destination folder exists
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                # copy file to destination
                shutil.copy2(source_path, destination_path)


file_extensions = ['.txt', '.c', 'h', '.hpp', '.hxx', '.cpp', '.cxx', 'mak']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=None)
    parser.add_argument('--dest', type=str, default=None)

    args = parser.parse_args()

    copy_files(args.source, args.dest, file_extensions)
