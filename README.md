# ftreetrawl

`ftreetrawl` is a Python command-line tool that recursively processes all files in a specified directory, generating SHA1 hash files for each file that does not already have a corresponding hash file. The tool uses the `.ftt-hash-sha1` extension for hash files.

In addition to generating hash files, `ftreetrawl` also calculates a global hash by concatenating all individual file hashes and computing the SHA1 hash of the result.

The tool also includes a cleanup feature that removes orphaned hash files. If a file has been removed from the directory but its corresponding hash file still exists, `ftreetrawl` will remove the orphaned hash file.

## Usage

Run `ftreetrawl` with the directory to process as a command-line argument:

```bash
python ftreetrawl.py <directory>
```

or using the binary executable:

```bash
ftreetrawl <directory>
```

The tool will process all files in the specified directory, generate hash files as needed, calculate the global hash, and perform cleanup of orphaned hash files. The global hash is printed to the console.

## Install
You can run ftreetrawl by cloning the repository and running the script directly with Python 3.x or you can use binary executables provided in the releases section. 

## License
ftreetrawl is available under the MIT License. See LICENSE for more details.

## Last Words
FtreeTrawl is based on dtreetrawl by [Derek Chafin](

This Markdown text can be placed in a README.md file in the root of your project repository. It provides a brief description of the tool, its usage, requirements, and license information.