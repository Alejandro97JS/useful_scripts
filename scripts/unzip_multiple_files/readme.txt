Script to extract all zip files from a folder, and join all extracted files behind the same output folder.

It loops through all files of a given directory.
If the current file is a .zip file, the script extracts it and sends the output files to a common output folder.
All files inside inner folders will be flattened at the same level (output folder).

If there are conflicts among file names, the file will be saved with an integer at the end of the file name.
(With a maximum of 5 files with the same initial name)

Configuration:
It is enough to define:
- Absolute path to input directory (must already exist).
- Absolute path to output directory (if it does not exist, it will be created).
