import pathlib
import time
from PySide2 import QtWidgets

class MainWidget(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)

		self.fortschritt = QtWidgets.QLabel("Fortschritt: ")
		self.wavs = QtWidgets.QLabel("Gefundene wave: ")
		self.avi = QtWidgets.QLabel("Gefundene avi: ")
		self.jpeg = QtWidgets.QLabel("Gefundene jpeg: ")
		self.png = QtWidgets.QLabel("Gefundene png: ")

		self.button = QtWidgets.QPushButton("Start")
		self.button.clicked.connect(self.launch_programm)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.fortschritt)
		self.layout.addWidget(self.wavs)
		self.layout.addWidget(self.avi)
		self.layout.addWidget(self.jpeg)
		self.layout.addWidget(self.png)
		self.layout.addWidget(self.button)


		self.setLayout(self.layout)


	def restore_wave(self,file,file_length,found_WAVEs):
		""" Restores a found WAVE-file.

		If a file of this type has been found, it will be written to the current
		location.

		Parameters
		----------
		file
			the img-file with deleted files

		file_length
			amount of bytes after 'RIFF'-header

		found_WAVEs
			amount of WAVEs that have been found.
			Used for numbering restored files.
		"""
		new_wav = pathlib.Path(self.destination+
			f"/restored_wav_{found_WAVEs+1}.wav")
		with new_wav.open('wb') as new_file:
			new_file.write(b'RIFF')
			new_file.write((file_length).to_bytes(4,'little'))
			new_file.write(b'WAVE')
			new_file.write(file.read(file_length-4))


	def restore_avi(self,file,file_length,found_AVIs):
		""" Restores a found AVI-file.

		If a file of this type has been found, it will be written to the current
		location.

		Parameters
		----------
		file
			the img-file with deleted files

		file_length
			amount of bytes after 'RIFF'-header

		found_AVIs
			amount of AVIs that have been found.
			Used for numbering restored files.
		 """
		new_avi = pathlib.Path(self.destination+
			f"/restored_avi_{found_AVIs+1}.avi")
		with new_avi.open('wb') as new_file:
			new_file.write(b'RIFF')
			new_file.write((file_length).to_bytes(4,'little'))
			new_file.write(b'AVI ')
			new_file.write(file.read(file_length-4))


	def restore_flac(self,file,file_length,found_FLACs):
		pass
		# new_flac = pathlib.Path(f"restored_flac_{found_FLACs+1}.flac")
		# with new_flac.open('wb') as new_file:
		#   new_file.write((file_length).to_bytes(4,'big'))
		#   new_file.write(b'fLaC')
		#   for data in range(file_length-4):
		#       new_file.write(file.read(1))



	def restore_JPEG(self,file,found_JPEGs,b1,b0):
		""" Restores a found JPEG-file.

		If a file of this type has been found, it will be written to the current
		location.

		Parameters
		----------
		file
			the img-file with deleted files

		found_JPEGs
			amount of JPEGs that have been found.
			Used for numbering restored files.

		b1, b0
			current byte sequence that has been read. For jpegs: xFF xE0
		 """
		new_JPEG = pathlib.Path(self.destination+
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

	def restore_PNG(self,file, found_PNGs):
		""" Restores a found PNG-file.

		If a file of this type has been found, it will be written to the current
		location.

		Parameters
		----------
		file
			the img-file with deleted files

		found_PNGs
			amount of PNGs that have been found.
			Used for numbering restored files.
		 """
		new_PNG = pathlib.Path(self.destination+
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

	def restore_PDF(self,file, found_PDFs):
		""" Restores a found PDF-file.

		If a file of this type has been found, it will be written to 
		the current location.

		Parameters
		----------
		file
			the img-file with deleted files

		found_PDFs
			amount of PDFs that have been found.
			Used for numbering restored files.

		b6, b5, b4, b3, b2, b1, b0
			current byte sequence that's being analysed
		 """
		new_PDF = pathlib.Path(self.destination+
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

	def restore_GIF(self, file, found_GIFs, b_adda, b_addb):
		new_GIF = pathlib.Path(self.destination+
			f"/restored_GIF_{found_GIFs+1}.gif")
		with new_GIF.open('wb') as new_file:
			new_file.write(b'GIF8'+b_adda+b_addb)
			b1 = b'0'
			b0 = file.read(1)
			while b3+b2+b1+b0 != b'\x00\x3B':
				new_file.write(b0)
				b1 = b0
				b0 = file.read(1)
			new_file.write(b'\x3B')


	# START
	def launch_programm(self):
		self.button.setEnabled(False)

		absolutePath = QtWidgets.QFileDialog.getOpenFileName(self, 
			"Choose img-File", "/" , "Images (*.img)")[0]


		self.destination = QtWidgets.QFileDialog.getExistingDirectory(self,
		 "Choose Directory","/",QtWidgets.QFileDialog.DontUseNativeDialog)


		disk = pathlib.Path(absolutePath)
		disk_size = disk.stat()[6]

		print(f"Groesse des Speichers: {disk_size/1000/1000} MB.")

		found_JPEGs = 0
		found_WAVEs = 0
		found_AVIs = 0
		found_FLACs = 0
		found_PNGs = 0
		found_PDFs = 0
		found_GIFs = 0

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
					self.restore_JPEG(file,found_JPEGs,b1,b0)
					found_JPEGs += 1

				# PNGs
				if b3+b2+b1+b0 == b'\x89\x50\x4E\x47':
						b3 = file.read(1)
						b2 = file.read(1)
						b1 = file.read(1)
						b0 = file.read(1)
						if b3+b2+b1+b0 == b'\x0D\x0A\x1A\x0A':
							print("PNG gefunden")
							self.restore_PNG(file,found_PNGs)
							found_PNGs += 1

				# GIF
				if b3+b2+b2+b0 == b'GIF8':
					b_adda = file.read(1)
					b_addb = file.read(1)
					if b_adda+b_addb == b'7a' || b_adda+b_addb == b'9a':
						print("GIF gefunden")
						self.restore_GIF(file,found_GIFs,b_adda,b_addb)
						found_GIFs += 1
				

				# PDF
				if b3+b2+b1+b0 == b'%PDF':
					b_add = file.read(1)
					if b_add == b'-':
						print("PDF gefunden")
						self.restore_PDF(file,found_PDFs)
						found_PDFs += 1


				# FLACs
				if b3+b2+b1+b0 == b'\x66\x4C\x61\x43':
					print("FLAC gefunden")
					file_length = int.from_bytes(file.read(4),"big")
					self.restore_flac(file,file_length,found_FLACs)
					found_FLACs += 1
				
				# RIFFs
				if b3+b2+b1+b0 == b'RIFF':
					print("RIFF gefunden")
					file_length = int.from_bytes(file.read(4),"little")
					riff_type = file.read(4)
					if riff_type == b'WAVE':
						print("WAVE-Datei")
						self.restore_wave(file,file_length,found_WAVEs)
						found_WAVEs += 1
					if riff_type == b'AVI ':
						print("AVI-Datei")
						self.restore_avi(file,file_length,found_AVIs)
						found_AVIs += 1

				b3 = b2
				b2 = b1
				b1 = b0
				b0 = file.read(1)

		self.button.setEnabled(True)

app = QtWidgets.QApplication()

mainWindow = QtWidgets.QMainWindow()
mainWindow.setCentralWidget(MainWidget())
mainWindow.setWindowTitle("Unser Programm")
mainWindow.show()

app.exec_()