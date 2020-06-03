#!/usr/bin/env python


def str2bool(v):
    import argparse
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_args():
    import argparse

    p = argparse.ArgumentParser(description="Copy files")
    p.add_argument(
        'path', type=str, help='source file path')
    p.add_argument(
        'type', type=str, help='file type to copy')
    p.add_argument(
        'target', type=str, help='path to copy files to')
    p.add_argument(
        'max_size', type=int, help='size in MB to copy')
    p.add_argument(
        'max_files_per_folder', type=int,
        help='max files for per folder for target 0=unlimited')
    p.add_argument(
        '--clear-cache', type=str2bool,
        nargs='?', const=True, default=False,
        help='clear the cache')

    return p.parse_args()


def get_files(file_path, file_type):

    # TODO fix shitty portability
    cf = file_path.replace('/', '_') + '_' + file_type
    cache_file = f'cache/{cf}.pickle'
    files = read_cache(cache_file)

    if files:
        return files

    from pathlib import Path
    file_list = []
    count = 0
    for path in Path(file_path).rglob(f'*.{file_type}'):
        count += 1
        file_list.append((path, path.stat().st_size))
        if count % 100 == 0:
            print(f'Found {count} files')

    # Save cache
    # cache based on source folder
    with open(cache_file, 'wb') as f:
        import pickle
        pickle.dump(file_list, f)
    return file_list


def get_copy_files(files, max_size):
    import random
    print("Randomising...")
    random.shuffle(files)
    print("Randomised.")
    current_size = 0
    file_list = []
    for file in files:
        # Use base 10 for MB
        if current_size + file[1] > max_size*1000*1000:
            break
        file_list.append(file[0])
        current_size += file[1]
    return file_list


def copy_files(files, target_folder, max_files_per_folder):
    import shutil
    import pathlib
    fno = 0
    fc = 0
    for file in files:
        if max_files_per_folder == 0:
            tf = target_folder
        else:
            tf = target_folder + f'/{fno:08d}'
            if fc == 0:
                pathlib.Path(tf).mkdir(parents=True, exist_ok=True)
            tf = tf + f'/{fc:02d}.mp3'
        print(f"copying {file} to {tf}")
        try:
            shutil.copy(str(file), tf)
            fc += 1
            if fc >= max_files_per_folder:
                fno += 1
                fc = 0
        except Exception:
            print(f"ERROR: Failed to copy {file}")


def read_cache(cache_file):
    import pickle

    try:
        with open(cache_file, 'rb') as f:
            cache = pickle.load(f)
    except FileNotFoundError:
        print("Not found")
        cache = None
    return cache


args = parse_args()
if args.clear_cache:
    import pathlib
    # TODO improve shitty portability
    cache_file = args.path.replace('/', '_') + '_' + args.type
    f = pathlib.Path(f'cache/{cache_file}.pickle')
    if f.is_file():
        f.unlink()

file_list = get_files(args.path, args.type)
files = get_copy_files(file_list, args.max_size)

copy_files(files, args.target, args.max_files_per_folder)
