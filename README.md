# ftreetrawl

`ftreetrawl` is a Python command-line tool that recursively processes all files in a specified directory. For each file, it generates a SHA1 hash of the file's contents and its modification time, and stores this hash in a cache file. The tool uses the `.ftt-hash-sha1` extension for cache files.

In addition to generating cache files, `ftreetrawl` also calculates a global hash by concatenating all individual file hashes and computing the SHA1 hash of the result.

The tool also includes a cleanup feature that removes orphaned cache files. If a file has been removed from the directory but its corresponding cache file still exists, `ftreetrawl` will remove the orphaned cache file.

## Usage

Run `ftreetrawl` with the directory to process as a command-line argument:

```bash
python ftreetrawl.py <directory>
```

You can also disable caching with the `--no-cache` option:

```bash
python ftreetrawl.py --no-casche <directory> 
```

## Install
You can run ftreetrawl by cloning the repository and running the script directly with Python 3.x or you can use binary executables provided in the releases section.

## Final Remarks
The concept of ftreetrawl is inspired by dtreetrawlby. However, ftreetrawl is designed to be simpler and more efficient, making it ideal for frequently generating SHA hashes for an entire directory.

## License
ftreetrawl is available under the MIT License. See LICENSE for more details.

