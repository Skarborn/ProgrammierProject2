''' This script restores deleted files from a disc
Further information can be found in the functions below.

Copyright (c) 2019

Authors: Martin Berdau, Johannes Ruesing, Tammo Sander

License (BSD):
It is allowed to use the code in any context, but the license has to
be maintained and the authors have to be mentioned in the source code.
'''

import pathlib
import time
from PySide2 import QtWidgets


def restore_wave(file, destination, file_length, found_WAVEs):
	""" Restores a found WAVE-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	file_length
		length in bytes after 'RIFF'-header.

	found_WAVEs
		amount of WAVEs that have been found.
		Used for numbering restored files.
	"""
	new_wav = pathlib.Path(destination+
		f"/restored_wav_{found_WAVEs+1}.wav")
	with new_wav.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'WAVE')
		new_file.write(file.read(file_length-4))


def restore_avi(file, destination, file_length, found_AVIs):
	""" Restores a found AVI-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	file_length
		length in bytes after 'RIFF'-header.

	found_AVIs
		amount of AVIs that have been found.
		Used for numbering restored files.
	 """
	new_avi = pathlib.Path(destination+
		f"/restored_avi_{found_AVIs+1}.avi")
	with new_avi.open('wb') as new_file:
		new_file.write(b'RIFF')
		new_file.write((file_length).to_bytes(4,'little'))
		new_file.write(b'AVI ')
		new_file.write(file.read(file_length-4))

def restore_JPEG(file, destination, found_JPEGs, b1, b0):
	""" Restores a found JPEG-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	found_JPEGs
		amount of JPEGs that have been found.
		Used for numbering restored files.

	b1, b0
		current byte sequence that has been read. For jpegs: xFF xE0
	 """
	new_JPEG = pathlib.Path(destination+
		f"/restored_jpeg_{found_JPEGs+1}.jpeg")
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

def restore_PNG(file, destination, found_PNGs):
	""" Restores a found PNG-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	found_PNGs
		amount of PNGs that have been found.
		Used for numbering restored files.
	 """
	new_PNG = pathlib.Path(destination+
		f"/restored_png_{found_PNGs+1}.png")
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

def restore_PDF(file, destination, found_PDFs):
	""" Restores a found PDF-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	found_PDFs
		amount of PDFs that have been found.
		Used for numbering restored files.
	 """
	new_PDF = pathlib.Path(destination+
		f"/restored_PDF_{found_PDFs+1}.pdf")
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

def restore_GIF(file, destination, found_GIFs, b_adda, b_addb):
	""" Restores a found GIF-file.

	If a file of this type has been found, it will be written to the
	current location.

	Parameters
	----------
	file
		the img-file with deleted files.

	destination
		archive in which file is writen.

	found_GIFs
		amount of GIFs that have been found.
		Used for numbering restored files.

	b_adda & b_addb
		to store two extra bytes, which define which version of GIF
		is used.


	 """
	new_GIF = pathlib.Path(destination+
		f"/restored_GIF_{found_GIFs+1}.gif")
	with new_GIF.open('wb') as new_file:
		new_file.write(b'GIF8'+b_adda+b_addb)
		b1 = b'0'
		b0 = file.read(1)
		while b1+b0 != b'\x00\x3B':
			new_file.write(b0)
			b1 = b0
			b0 = file.read(1)
		new_file.write(b'\x3B')

def results(found_WAVEs, found_AVIs, found_JPEGs, found_PNGs,
	found_PDFs, found_GIFs, time_used):
	""" Prints results on the console.

	This function prints out the amount of restored files and the
	time used to run the program.

	Parameters
	----------
	found_FILEs
		amount of files of type FILE that have been found.

	time_used
		time used running the program.


	 """
	print("--------------------")
	print("Bericht: ")
	print(f"Dauer: {round(time_used//60)} Minuten und {round(time_used%60)} Sekunden")
	print(f"Hergestellte WAVE: {found_WAVEs}")
	print(f"Hergestellte AVI: {found_AVIs}")
	print(f"Hergestellte JPEG: {found_JPEGs}")
	print(f"Hergestellte PNG: {found_PNGs}")
	print(f"Hergestellte PDF: {found_PDFs}")
	print(f"Hergestellte GIF: {found_GIFs}")

# START
def main():
	""" Restores deleted files from a IMG-file.

	The following files can be restored:
		- WAVE
		- AVI
		- JPEG
		- PNG
		- PDF
		- GIF

	A restore-function exists for each supported file-type.
	After one of those files has been found the corresponding
	function is called.

	After starting the program the user will be asked to point
	to the IMG-File. Afterwards the user has to determine the
	destination were the files will be written to and the program
	will start.

	After the program is done, a result message will be displayed.

	The main-function and some restore-function use a similar
	approach to find important byte sequences like the magic numbers
	that mark the start of a file.
	When reading the file past values will be stored.
	For better understanding this sequence is viewed as a signal with
	delayed elements and value bn where n is the delay.
	The most recent byte that has been read is therefore called b0
	and the byte before that b1 and so on.
	By combining those bytes a byte sequence like for example
	b'RIFF' can be formed and found on the disk.
	 """
	app = QtWidgets.QApplication()

	# path to IMG-file
	absolutePath = QtWidgets.QFileDialog.getOpenFileName(None,
		"Choose img-File","/","Images (*.img)")[0]

	# path to destination archive
	destination = QtWidgets.QFileDialog.getExistingDirectory(None,
	 "Choose Directory","/",QtWidgets.QFileDialog.DontUseNativeDialog)

	disk = pathlib.Path(absolutePath)
	disk_size = disk.stat()[6]

	print(f"Groesse des Speichers: {disk_size/1000/1000} MB.")

	# file counters
	found_WAVEs = 0
	found_AVIs = 0
	found_JPEGs = 0
	found_PNGs = 0
	found_PDFs =  0
	found_GIFs = 0

	time_start = time.time()

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
				restore_JPEG(file,destination,found_JPEGs,b1,b0)
				found_JPEGs += 1

			# PNGs
			if b3+b2+b1+b0 == b'\x89\x50\x4E\x47':
					b3 = file.read(1)
					b2 = file.read(1)
					b1 = file.read(1)
					b0 = file.read(1)
					if b3+b2+b1+b0 == b'\x0D\x0A\x1A\x0A':
						print("PNG gefunden")
						restore_PNG(file,destination,found_PNGs)
						found_PNGs += 1

			# GIF
			if b3+b2+b1+b0 == b'GIF8':
				b_adda = file.read(1)
				b_addb = file.read(1)
				if (b_adda+b_addb == b'9a')|(b_adda+b_addb == b'7a'):
					print("GIF gefunden")
					restore_GIF(file,destination,found_GIFs,b_adda,b_addb)
					found_GIFs += 1

			# PDF
			if b3+b2+b1+b0 == b'%PDF':
				b_add = file.read(1)
				if b_add == b'-':
					print("PDF gefunden")
					restore_PDF(file,destination,found_PDFs)
					found_PDFs += 1
			
			# RIFF
			if b3+b2+b1+b0 == b'RIFF':
				file_length = int.from_bytes(file.read(4),"little")
				riff_type = file.read(4)
				
				# WAVE
				if riff_type == b'WAVE':
					print("WAVE gefunden")
					restore_wave(file,destination,file_length,found_WAVEs)
					found_WAVEs += 1
				
				# AVI
				if riff_type == b'AVI ':
					print("AVI gefunden")
					restore_avi(file,destination,file_length,found_AVIs)
					found_AVIs += 1

			b3 = b2
			b2 = b1
			b1 = b0
			b0 = file.read(1)


	time_end = time.time()
	time_used = time_end-time_start
	results(found_WAVEs, found_AVIs, found_JPEGs, found_PNGs,
	found_PDFs, found_GIFs, time_used)

if __name__== "__main__":
  main()