import pathlib

# FIND WAVS
def restore_wave(file,file_length,found_wavs):
	new_wav = pathlib.Path(f"restored_wav_{found_wavs+1}.wav")
	with new_wav.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'WAVE')
		for data in range(file_length-4):
			new_file.write(file.read(1))

# FIND AVIS
def restore_avi(file,file_length,found_avis):
	new_avi = pathlib.Path(f"restored_avi_{found_avis+1}.avi")
	with new_avi.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'AVI ')
		for data in range(file_length-4):
			new_file.write(file.read(1))


def restore_JPEG(file,found_jpegs):
	new_JPEG = pathlib.Path(f"restored_jpeg_{found_jpegs+1}.jpeg")
	current = file.read(1)
	current_before = b'0'
	with new_JPEG.open('wb') as new_file:
		while current_before+current != b'\xFF\xD9':
			current_before = current
			current = file.read(1)
			new_file.write(current_before)
		new_file.write(b'\xD9')


absolutePath = input('Pfad zur .img-Datei eingeben: ')
# /Users/martinberdau/Desktop/HA/4.Semester/AngewandtesProgrammieren/ProgrammierProject2/data_deleted.img

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]


# counts for files
found_wavs = 0
found_avis = 0
found_jpegs = 0

with disk.open('rb') as file:
##    for x in range(disk_size):
##        if file.read(4) == b'RIFF':
##            print("RIFF gefunden")
##            file_length = int.from_bytes(file.read(4),"little")
##            riff_type = file.read(4)
##            if riff_type == b'WAVE':
##                print("WAVE-Datei")
##                restore_wave(file,file_length,found_wavs)
##                found_wavs += 1
##            if riff_type == b'AVI ':
##                print("AVI-Datei")
##                restore_avi(file,file_length,found_avis)
##                found_avis += 1
                
	for x in range(disk_size):
		if file.read(2) == b'\xFF\xD8':
				restore_JPEG(file,found_jpegs)
				found_jpegs += 1
