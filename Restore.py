import pathlib

def restore_wave(file,file_length):
    new_wav = pathlib.Path("restored_wav.wav")
    with new_wav.open('wb') as new_file:
        new_file.write(b'RIFF')
        new_file.write((file_length).to_bytes(4, 'little'))
        new_file.write(b'WAVE')
        for data in range(file_length-16):
            new_file.write(file.read(1))
    

def restore_avi(file,file_length):
    pass

def restore_JPEG(file,file_length):
	new_JPEG = pathlib.Path("restored_jpeg.jpeg")
	with new_JPEG.open('wb') as new_file:
		for data in range(file_length):
			new_file.write(file.read(1))


absolutePath = '/Users/martinberdau/Desktop/data_deleted.img'

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]


with disk.open('rb') as file:
    for x in range(disk_size):
        if file.read(4) == b'RIFF':
            print("RIFF gefunden")
            file_length = int.from_bytes(file.read(4),"little")
            riff_type = file.read(4)
            if riff_type == b'WAVE':
                print("WAVE-Datei")
                restore_wave(file,file_length)
            if riff_type == b'AVI ':
                print("AVI-Datei")
                restore_avi(file,file_length)
        if file.read(2) == b'\xFF\xD8':
        	

