Script to change file names of the given folders, according to a certain pattern.

It loops through all files.
If a filename matches the specified pattern, the code changes that name according to the configured action.

For example:

Input:
- file1.txt
- another_file2.txt
- FILE3.json
- my_file.txt
- MY_FILE_B.txt

Configuration:
- Search for regex "\d+" (at least one digit in the filename).
- Action: Delete digits and convert to lowercase.

Output:
- file.txt
- another_file.txt
- file.json
- my_file.txt
- MY_FILE_B.txt

Note the last file name is not converted to lowercase because it does not match the pattern (it has no digits).
