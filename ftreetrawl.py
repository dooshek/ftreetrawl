"""Hash files in a directory, recursively and return the global hash for all files in a directory."""
import argparse
import json
import os
import pathlib

import xxhash

HASH_EXTENSION = '.ftt-hash-sha1'
CACHE_DIR = os.path.join(pathlib.Path.home(), '.cache', 'ftreetrawl')

def calculate_sha1(file_path: str, mtime: float) -> str:
    """Calculate the SHA1 hash of a file."""
    with open(file_path, 'rb') as file:
        file_hash = xxhash.xxh3_64_hexdigest(file.read())
        mtime_hash = xxhash.xxh3_64_hexdigest(str(mtime).encode())
        return xxhash.xxh3_64_hexdigest((file_hash + mtime_hash).encode())
    
def hash_files(directory: str) -> str:
    """Process all files in a directory."""
    all_hashes = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(HASH_EXTENSION):
                continue

            file_path = os.path.join(root, file)
            absolute_path = os.path.abspath(file_path)[1:]
            hash_file_path = os.path.join(CACHE_DIR, f"{absolute_path}{HASH_EXTENSION}")
            os.makedirs(os.path.dirname(hash_file_path), exist_ok=True)
            mtime = os.path.getmtime(file_path)

            if not os.path.exists(hash_file_path):
                sha1 = calculate_sha1(file_path, mtime)
                with open(hash_file_path, 'w', encoding="utf-8") as hash_file:
                    json.dump({'sha1': sha1, 'mtime': mtime}, hash_file)
            else:
                with open(hash_file_path, 'r', encoding="utf-8") as hash_file:
                    data = json.load(hash_file)
                if data['mtime'] != mtime:
                    sha1 = calculate_sha1(file_path, mtime)
                    with open(hash_file_path, 'w', encoding="utf-8") as hash_file:
                        json.dump({'sha1': sha1, 'mtime': mtime}, hash_file)
                else:
                    sha1 = data['sha1']
            all_hashes.append(sha1)

    global_hash = xxhash.xxh3_64_hexdigest(''.join(all_hashes).encode())
    return global_hash

def hash_cleanup(directory: str):
    """Remove orphaned hash files in a directory."""
    cwd_rel = os.getcwd()[1:]
    cache_dir = os.path.join(CACHE_DIR, cwd_rel, directory)
    
    for root, dirs, files in os.walk(cache_dir):
        for file in files:
            if not file.endswith(HASH_EXTENSION):
                continue
            original_base_dir_abs = root.replace(CACHE_DIR, '')
            original_file_path = os.path.join(original_base_dir_abs, file[:-len(HASH_EXTENSION)])
            if not os.path.exists(original_file_path):
                os.remove(os.path.join(root, file))

parser = argparse.ArgumentParser(description="Hash files in a directory, recursively and " +
                                 "return the global hash for all files in a directory.\n" +
                                 f"Create hash files with {HASH_EXTENSION} extension for " +
                                 "files that do not have one.\n\n" +
                                 "Also removes orphaned hash files if original files were removed."
                                )
parser.add_argument('directory', type=str, help='The directory to process')

args = parser.parse_args()

hash_cleanup(args.directory)
print(hash_files(args.directory))
