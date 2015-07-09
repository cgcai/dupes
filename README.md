dupes
=====

Finds duplicate files based on SHA-1 hash of file contents.

##Options

`-r`: recurses on subdirectories
`-D`: removes duplicates by preserving the first file and deleting all others that share the same `sha1_id`.

## Output format

    <index>:<sha1_id>:<path>

`index`: human-readable, numeric index  
`sha1_id`: first 4-bytes of the SHA-1 hash  
`path`: path of the duplicate
