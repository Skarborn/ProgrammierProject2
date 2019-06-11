# Programming Task via Python to restore deleted objects from an img-file
This program is the result of the task to create a Python script which restores deleted files from a copy of a disk (img-file). By deleting files of any kind (without destroying them physically), not everything but only the file-names are deallocated. This is the reason why it is possible to retrieve the data just by finding it and refilling the missing parts, like the given program Restore.py does. 
The script is able to restore the formats:
* PDF
* JPEG
* PNG
* WAVE
* AVI
* GIF

## Getting Started
First of all, [Python3](https://www.python.org/downloads/) should be installed. Because the library PySide2 is imported, it is also necessary to install it with [pip](https://pip.pypa.io/en/stable/)
```
$ pip install PySide2
```
or (because of the varying pip versions):
```
$ pip3 install PySide2
```
It may occurr that the modules time and pathlib are not pre-installed as well, therefore they have to be installed in the way PySide2 was added.
Then the user has to download the zip-file of the
 [GitHub-homepage](https://github.com/Skarborn/ProgrammierProject2) and to run it from the path, where the file is located (see **Running the Program**). 

## Running the Program

To run the program, the user just has to type one of the following commands in the shell depending on which platform is used: If windows is runned on the computer, the shell-program cmd is probably applied, therefore the command is
```
$ python Restore.py
```
Otherwise terminal (macOS and linux) has to be used to run the Restore-file
```
$ python3 Restore.py
```
The user will afterwards be asked to state, where the img-file, which has to be restored, is positioned by clicking on the opened display. Afterwards another window of the same kind is opened for the user to decide where the restored data should be saved.

## Built With
* [Python3](https://www.python.org/downloads/) - Programed and runned with
* [Sublime Text](https://www.sublimetext.com/3) - Used TextEditor; possible Tool to show the source code

## Versioning
Version 1.0
This program is finished at the moment, updates might be uploaded sometimes.

## Authors
* **Martin Berdau** - *Programmer* -
[MartinBerdau](https://github.com/MartinBerdau)
* **Tammo Sander** - *Programmer* - 
[TammoSan](https://github.com/TammoSan)
* **Johannes Rüsing** - *Programmer* -
[Skarborn](https://github.com/Skarborn)

## License
**BSD-License**:
It is allowed to use the code in any context, but the license has to be maintained and the authors have to be mentioned in the source code.

