"""Hash files in a directory, recursively and return the global hash for all files in a directory."""
import argparse
import concurrent.futures
import json
import multiprocessing
import os
import pathlib

import psutil
import xxhash

CPUS = multiprocessing.cpu_count()
HASH_EXTENSION = '.ftt-hash-sha1'
CACHE_DIR = os.path.join(pathlib.Path.home(), '.cache', 'ftreetrawl')

parser = argparse.ArgumentParser(description="Hash files in a directory, recursively and " +
                                 "return the global hash for all files in a directory.\n" +
                                 f"Create hash files with {HASH_EXTENSION} extension for " +
                                 "files that do not have one.\n\n" +
                                 "Also removes orphaned hash files if original files were removed."
                                )
parser.add_argument('directory', type=str, help='The directory to process')
parser.add_argument('--no-cache', action='store_true', help=f'Disable caching to {CACHE_DIR}')
parser.add_argument('--threads', type=int, help=f'Number of threads for hashing (default: {CPUS})', default=CPUS)

args = parser.parse_args()

total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)
CHUNK_RAM_PCT = 0.05  # 5% of total memory
if total_memory <= 2:
    CHUNK_RAM_PCT = 0.1  # 10% of total memory
CHUNK_SIZE = int(total_memory * CHUNK_RAM_PCT * 1024 * 1024 * 1024 / args.threads)
    
def calculate_sha1(file_path: str, mtime: float) -> str:
    """Calculate the SHA1 hash of a file."""
    file_hash = xxhash.xxh3_64()

    with open(file_path, 'rb') as file:
        while chunk := file.read(CHUNK_SIZE):
            file_hash.update(chunk)

    mtime_hash = xxhash.xxh3_64_hexdigest(str(mtime).encode())
    return xxhash.xxh3_64_hexdigest((file_hash.hexdigest() + mtime_hash).encode())

def process_file(file_path: str, no_cache: bool) -> str:
    """Process a file and return its hash."""
    mtime = os.path.getmtime(file_path)
    absolute_path = os.path.abspath(file_path)[1:]
    hash_file_path = os.path.join(CACHE_DIR, f"{absolute_path}{HASH_EXTENSION}")
    os.makedirs(os.path.dirname(hash_file_path), exist_ok=True)

    if not os.path.exists(hash_file_path) or no_cache:
        sha1 = calculate_sha1(file_path, mtime)
        if not no_cache:
            with open(hash_file_path, 'w', encoding="utf-8") as hash_file:
                json.dump({'sha1': sha1, 'mtime': mtime}, hash_file)
    else:
        with open(hash_file_path, 'r', encoding="utf-8") as hash_file:
            data = json.load(hash_file)
        if data['mtime'] != mtime:
            sha1 = calculate_sha1(file_path, mtime)
            if not no_cache:
                with open(hash_file_path, 'w', encoding="utf-8") as hash_file:
                    json.dump({'sha1': sha1, 'mtime': mtime}, hash_file)
        else:
            sha1 = data['sha1']
    return sha1

def hash_files(directory: str, no_cache: bool, num_threads: int) -> str:
    """Process all files in a directory."""
    all_hashes = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_file = {executor.submit(process_file, os.path.join(root, file), no_cache): file for root, dirs, files in os.walk(directory) for file in files if not file.endswith(HASH_EXTENSION)}
        for future in concurrent.futures.as_completed(future_to_file):
            all_hashes.append(future.result())

    global_hash = xxhash.xxh3_64_hexdigest(''.join(sorted(all_hashes)).encode())    
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

hash_cleanup(args.directory)
print(hash_files(args.directory, args.no_cache, args.threads))