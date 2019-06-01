import pathlib

def restore_wave(file,file_length):
    format_chunkname = file.read(4)
    format_chunklen = file.read(4)    
    dataformat = file.read(2)
    nchan = file.read(2)
    samplerate = file.read(4)
    bytespersecond = file.read(4)
    alignment = file.read(2)
    bitspersample = file.read(2)
    

def restore_avi(file,file_length):
    pass

absolutePath = '/Users/martinberdau/Desktop/data_deleted.img'

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]


with disk.open('rb') as file:
    for x in range(disk_size):
        if file.read(4) == b'RIFF':
            print("RIFF gefunden")
            file_length = int.from_bytes(file.read(4),"little")
            riff_type = file.read(4)
            if riff_type==b'WAVE':
                print("WAVE-Datei")
                restore_wave(file,file_length)
            if riff_type==b'AVI ':
                print("AVI-Datei")
                restore_avi(file,file_length)
