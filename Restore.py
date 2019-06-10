import pathlib

# FIND AND RESTORE WAVS
def restore_wave(file,file_length,found_wavs):
	new_wav = pathlib.Path(f"restored_wav_{found_wavs+1}.wav")
	with new_wav.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'WAVE')
		new_file.write(file.read(file_length-4))

# FIND AVIS
def restore_avi(file,file_length,found_avis):
	new_avi = pathlib.Path(f"restored_avi_{found_avis+1}.avi")
	with new_avi.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'AVI ')
		new_file.write(file.read(file_length-4))

# FIND FLACS
def restore_flac(file,file_length,found_flacs):
	pass
	# new_flac = pathlib.Path(f"restored_flac_{found_flacs+1}.flac")
	# with new_flac.open('wb') as new_file:
	# 	new_file.write((file_length).to_bytes(4,'big'))
	# 	new_file.write(b'fLaC')
	# 	for data in range(file_length-4):
	# 		new_file.write(file.read(1))


# FIND AND RESTORE JPEGS
def restore_JPEG(file,found_jpegs,b1,b0):
	new_JPEG = pathlib.Path(f"restored_jpeg_{found_jpegs+1}.jpeg")
	with new_JPEG.open('wb') as new_file:
		new_file.write(b'\xFF\xD8'+b1+b0)

		while b1 + b0 != b'\xFF\xDA':
			block_length = file.read(2)
			new_file.write(block_length)
			new_file.write(file.read(int.from_bytes(block_length, \
				'big')-2))

			b1 = file.read(1)
			b0 = file.read(1)
			new_file.write(b1+b0)

		while b1 + b0 != b'\xFF\xD9':
			b1 = b0
			b0 = file.read(1)
			new_file.write(b0)

def restore_PNG(file, found_PNGs):
	new_PNG = pathlib.Path(f"restored_png_{found_PNGs+1}.png")
	with new_PNG.open('wb') as new_file:
		new_file.write(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
		block_length = file.read(4)
		chunk_name = file.read(4)
		while chunk_name != b'IEND':
			new_file.write(block_length)
			new_file.write(chunk_name)
			new_file.write(file.read(int.from_bytes(block_length, \
				'big')))
			new_file.write(file.read(4))
			block_length = file.read(4)
			chunk_name = file.read(4)

		new_file.write(block_length)
		new_file.write(chunk_name)
		new_file.write(file.read(int.from_bytes(block_length, \
			'big')))
		new_file.write(file.read(4))

def restore_PDF(file, found_PDFs):
	new_PDF = pathlib.Path(f"restored_PDF_{found_PDFs+1}.pdf")
	with new_PDF.open('wb') as new_file:
		new_file.write(b'%PDF-')
		b6 = b'0'
		b5 = b'0'
		b4 = b'0'
		b3 = b'0'
		b2 = b'0'
		b1 = b'0'
		b0 = file.read(1)
		while b4+b3+b2+b1+b0 != b'%%EOF':
			new_file.write(b0)
			b6 = b5
			b5 = b4
			b4 = b3
			b3 = b2
			b2 = b1
			b1 = b0
			b0 = file.read(1)
		new_file.write(b'F')
		if b6 == b'\x30':
			b0 = file.read(1)
			while b4+b3+b2+b1+b0 != b'%%EOF':
				new_file.write(b0)
				b4 = b3
				b3 = b2
				b2 = b1
				b1 = b0
				b0 = file.read(1)
			new_file.write(b'F')




absolutePath = input('Pfad zur .img-Datei eingeben: ')
# /Users/martinberdau/Desktop/HA/4.Semester/AngewandtesProgrammieren/ProgrammierProject2/data_deleted.img

disk = pathlib.Path(absolutePath)
disk_size = disk.stat()[6]

print(f"Groesse des Speichers: {disk_size/1000/1000} MB.")

found_jpegs = 0
found_wavs = 0
found_avis = 0
found_flacs = 0
found_PNGs = 0
found_PDFs = 0

with disk.open('rb') as file:
	# initial 4 bytes that will be looked at to find header
	b3 = file.read(1)
	b2 = file.read(1)
	b1 = file.read(1)
	b0 = file.read(1)

	for x in range(disk_size - 4):

		# JPEGs
		if b3+b2+b1+b0 == b'\xFF\xD8\xFF\xE0':
			print("JPEG gefunden")
			restore_JPEG(file,found_jpegs,b1,b0)
			found_jpegs += 1

		# PNGs
		if b3+b2+b1+b0 == b'\x89\x50\x4E\x47':
				b3 = file.read(1)
				b2 = file.read(1)
				b1 = file.read(1)
				b0 = file.read(1)
				if b3+b2+b1+b0 == b'\x0D\x0A\x1A\x0A':
					print("PNG gefunden")
					restore_PNG(file,found_PNGs)
					found_PNGs += 1

		# MP3
		

		# PDF
		if b3+b2+b1+b0 == b'%PDF':
			b_add = file.read(1)
			if b_add == b'-':
				print("PDF gefunden")
				restore_PDF(file,found_PDFs)
				found_PDFs += 1


		# FLACs
		if b3+b2+b1+b0 == b'\x66\x4C\x61\x43':
			print("FLAC gefunden")
			file_length = int.from_bytes(file.read(4),"big")
			restore_flac(file,file_length,found_flacs)
			found_flacs += 1
		
		# RIFFs
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