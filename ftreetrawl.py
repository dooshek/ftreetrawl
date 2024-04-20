import hashlib
import os

from rich.console import Console

console = Console()
HASH_EXTENSION = '.ftt-hash-sha1'

def calculate_sha1(file_path):
    """Calculate the SHA1 hash of a file."""
    with open(file_path, 'rb') as file:
        return hashlib.sha1(file.read()).hexdigest()

def hash_files(directory):
    """Process all files in a directory."""
    all_hashes = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(HASH_EXTENSION):
                continue
            file_path = os.path.join(root, file)
            hash_file_path = f"{file_path}{HASH_EXTENSION}"
            if not os.path.exists(hash_file_path):
                sha1 = calculate_sha1(file_path)
                with open(hash_file_path, 'w', encoding="utf-8") as hash_file:
                    hash_file.write(sha1)
            else:
                with open(hash_file_path, 'r', encoding="utf-8") as hash_file:
                    sha1 = hash_file.read()
            all_hashes.append(sha1)

    global_hash = hashlib.sha1(''.join(all_hashes).encode()).hexdigest()
    return global_hash

def hash_cleanup(directory):
    """Remove orphaned hash files in a directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(HASH_EXTENSION):
                original_file_path = os.path.join(root, file[:-len(HASH_EXTENSION)])
                if not os.path.exists(original_file_path):
                    os.remove(os.path.join(root, file))

hash_cleanup('tmp/')
print(hash_files('tmp/'))
