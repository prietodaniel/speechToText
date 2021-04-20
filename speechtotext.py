######

import speech_recognition as sr
import os
import sys

from pydub import AudioSegment
from pydub.silence import split_on_silence
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                             QComboBox, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import threading
import time

whole_text = ""
idioma = "es-ES"

def get_large_audio_transcription(entorno, path, lang):
	entorno.label.setText("Comenzando conversión, preparando audio...")
	r = sr.Recognizer()

	# open the audio file using pydub
	sound = AudioSegment.from_wav(path)
	# split audio sound where silence is 700 miliseconds or more and get chunks
	chunks = split_on_silence(
		sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500,)

	folder_name = "audio-chunks"
	# create a directory to store the audio chunks
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	whole_text = ""
	# process each chunk
	for i, audio_chunk in enumerate(chunks, start=1):
		# ACA ACTUALIZO EL LABLE
		entorno.label.setText(
			"Conversion en progreso: {}%".format(int(i*100/len(chunks))))

		# export audio chunk and save it in
		# the `folder_name` directory.
		chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
		audio_chunk.export(chunk_filename, format="wav")
		# recognize the chunk
		with sr.AudioFile(chunk_filename) as source:
			audio_listened = r.record(source)
			# try converting it to text
			try:
				text = r.recognize_google(audio_listened, language = "en-US")
			except sr.UnknownValueError as e:
				print("Error:", str(e))
			else:
				text = f"{text.capitalize()}. "
				whole_text += text
	# return the text for all chunks detected
	# return whole_text
	f = open("{}txt".format(path[:-3]), 'a')
	f.write(whole_text)
	entorno.label.setText("Conversion Finalizada.\n Puede elegir otro archivo")
	f.close()


class App(QWidget):
	mensaje = "Seleccione el archivo a convertir (debe estar en formato WAV)."

	def __init__(self):
		super().__init__()
		self.title = 'SpeechToText'
		self.left = 700
		self.top = 300
		self.width = 400
		self.height = 200
		self.label = QLabel(self.mensaje, self)
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label.setAlignment(Qt.AlignCenter)
		self.setFixedSize(350, 240)
		self.initUI()

	def initUI(self):
		hbox = QHBoxLayout()
		vbox = QVBoxLayout()
		
		combo = QComboBox(self)
		
		combo.addItem('Español')
		combo.addItem('Ingles')
		
		combo.activated[str].connect(self.onActivated)
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		button = QPushButton('Seleccionar Archivo', self)
		button.setToolTip('This is an example button')
		button.move(100,70)
		button.clicked.connect(self.on_click)
		vbox.addWidget(self.label)
		vbox.addWidget(combo)
		vbox.addWidget(button)
		self.setLayout(vbox)
		self.setGeometry(300, 300, 350, 150)
		self.show()
		
	def on_click(self):
		print('Seleccionando Archivo')
		self.openFileNameDialog()
		
	def onActivated(self, text):
		if text == "Ingles":
			idioma = "ingles"
		else:
			idioma = "español"

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(
			self, "Escoger audio", "F:", "All Files (*.wav)", options=options)
		print(fileName[0:-3])
		if fileName:
			print(fileName)
			# x = threading.Thread(target=actualizarLabel, args=(self,1,))
			# x.start()
			x = threading.Thread(
				target=get_large_audio_transcription, args=(self, fileName, idioma))
			x.start()
		# full_text = get_large_audio_transcription(path)
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
