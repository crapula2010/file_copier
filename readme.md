This small project provides a quick way of filling a folder with a random selection of files from a source folder. For example say you have a 32 GB sd card which can be slotted into a music player and you wish to fill it with a random selection of mp3 files from your 1TB library. You can do this with the following command

$ mkdir target

$ ./file_copier.sh <source path of the root of your library> mp3 target 32000 20

This will copy a random selection of files from your library. Note files will be copied to numbered files e.g. 01.mp3, 02.mp3
The last parameter is used to limit how many files can be in each folder. To hopefully make them easier to handle by music players whoch sometimes don't like large folders. You will end up with the target folder containing a load of numbered folders. Each folder will contain a number of numbered mp3 files. For mp3s this is not a problem assuming the files are tagged correctly. For other file types this may or may not be an issue. For the purposes of this (in line with the way most storage works) 1MB is considered to be 1000000 bytes 

Works on linux or wsl
Needs python3

To install

$ python3 -m venv venv

$ pip install -r requirements.txt

$ mkdir cache

$ chmod +x file_copier.* 

To run

$ ./file_copier.sh <source_path> <file_type> <target_folder> <size_in_MB> <max_files_per_folder>

