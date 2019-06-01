import pathlib

def get_filelength(file):
    length = int.from_bytes(file.read(4),"little")
    return length
    

absolutePath = '/Users/martinberdau/Desktop/data_deleted.img'

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]


with disk.open('rb') as file:
    for x in range(disk_size):
        if file.read(1) == b'R':
            if file.read(1) == b'I':
                if file.read(1) == b'F':
                    if file.read(1) == b'F':
                        print("RIFF gefunden")
                        print(f"{get_filelength(file)} Bytes")
