import pathlib

# FIND AND RESTORE WAVS
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


# FIND AND RESTORE JPEGS
def restore_JPEG(file,found_jpegs):
	pass
	# new_JPEG = pathlib.Path(f"restored_jpeg_{found_jpegs+1}.jpeg")
	# start_img = 1
	# current = file.read(1)
	# current_before = b'0'
	# with new_JPEG.open('wb') as new_file:
	# 	new_file.write(b'\xFF\xD8')
	# 	while start_img > 0:
	# 		current_before = current
	# 		current = file.read(1)
	# 		new_file.write(current)
	# 		if current_before+current == b'\xFF\xD8':
	# 			start_img += 1
	# 		if current_before+current == b'\xFF\xD9':
	# 			start_img -= 1


absolutePath = input('Pfad zur .img-Datei eingeben: ')
# /Users/martinberdau/Desktop/HA/4.Semester/AngewandtesProgrammieren/ProgrammierProject2/data_deleted.img

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]
print(disk_size)


with disk.open('rb') as file:
	# initial 4 bytes that will be looked at to find header
	b3 = file.read(1)
	b2 = file.read(1)
	b1 = file.read(1)
	b0 = file.read(1)

	for x in range(disk_size - 4):
		if b1+b0 == b'\xFF\xD8':
			JPEG_type = file.read(2)
			if JPEG_type == b'\xFF\xE0':
				restore_JPEG(file,found_jpegs)
				found_jpegs += 1

		if b3+b2+b1+b0 == b'RIFF':
			print("RIFF gefunden")
			file_length = int.from_bytes(file.read(4),"little")
			riff_type = file.read(4)
			if riff_type == b'WAVE':
				print("WAVE-Datei")
				restore_wave(file,file_length,found_wavs)
				found_wavs += 1
			if riff_type == b'AVI ':
				print("AVI-Datei")
				restore_avi(file,file_length,found_avis)
				found_avis += 1

		b3 = b2
		b2 = b1
		b1 = b0
		b0 = file.read(1)

