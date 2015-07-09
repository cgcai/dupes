import argparse
import hashlib
from os import listdir, remove
from os.path import isfile, isdir, normpath


BLOCKSIZE = 131072


def hash_file(filename):
    hasher = hashlib.sha1()
    with open(filename, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def merge_dicts(left, right):
    new_dict = dict(left)
    for key in right:
        if key in left:
            new_dict[key] += right[key]
        else:
            new_dict[key] = right[key]
    return new_dict


def unique_files(directory, recurse=False):
    retval = {}
    items = [directory + '/' + i for i in listdir(directory)]
    files = [i for i in items if isfile(i)]

    for f in files:
        filehash = hash_file(f)
        if filehash not in retval:
            retval[filehash] = []
        retval[filehash].append(normpath(f))

    if recurse:
        subdirs = [i for i in items if isdir(i)]
        for sd in subdirs:
            result = unique_files(sd, recurse)
            retval = merge_dicts(retval, result)

    return retval


def duplicates(unique_files):
    return {key: unique_files[key] for key in unique_files
            if len(unique_files[key]) > 1}


def format_duplicates(dupes):
    n = 1
    buf = ''
    for key in dupes:
        for f in dupes[key]:
            buf += '{}:{}:{}\n'.format(n, key[:8], f)
        n += 1
    return buf


def deduplicate(dupes):
    for key in dupes:
        to_remove = dupes[key][1:]
        for f in to_remove:
            remove(f)


def main(args):
    files = unique_files(normpath(args.dir), recurse=args.r)
    dupes = duplicates(files)
    print(format_duplicates(dupes), end='')
    if args.D:
        deduplicate(dupes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Finds duplicate files')
    parser.add_argument('dir', type=str, help='The directory to operate on')
    parser.add_argument('-r', action='store_true', required=False,
                        help='Recurse on subdirectories')
    parser.add_argument('-D', action='store_true', required=False,
                        help='Delete duplicates (cannot be undone!)')
    args = parser.parse_args()
    main(args)
