import os
import hashlib
import argparse

'''
    generate file md5 hash
'''


def get_file_hash(file_path) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_folder_hash_set(folder_path):
    file_set = {}

    for folder, subfolder, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(folder, filename)
            relative_path = os.path.relpath(file_path, folder_path)
            file_set[relative_path] = get_file_hash(file_path)

    return file_set


def compare_folder(folder1: str, folder2: str, result: str):
    file_set1 = get_folder_hash_set(folder1)
    file_set2 = get_folder_hash_set(folder2)

    unique_folder1 = set(file_set1.items()) - set(file_set2.items())
    unique_folder2 = set(file_set2.items()) - set(file_set1.items())

    with open(result, 'w') as output:
        output.write("%s: \n" % folder1)
        output.write("-" * 128)
        output.write("\n")

        for file_path, _ in unique_folder1:
            output.write(file_path + "\n")

        output.write("\n\n%s: \n" % folder2)
        output.write("-" * 128)
        output.write("\n")

        for file_path, _ in unique_folder2:
            output.write(file_path + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder1', type=str, default=None)
    parser.add_argument('--folder2', type=str, default=None)
    parser.add_argument('--output', type=str, default='result.txt')

    args = parser.parse_args()

    compare_folder(args.folder1, args.folder2, args.output)
