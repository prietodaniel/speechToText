import speech_recognition as sr 
import os 
import sys

from pydub import AudioSegment
from pydub.silence import split_on_silence
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


def get_large_audio_transcription(path):
    
	"""
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
	r = sr.Recognizer()

	# open the audio file using pydub
	sound = AudioSegment.from_wav(path)  
	# split audio sound where silence is 700 miliseconds or more and get chunks
	chunks = split_on_silence(sound,min_silence_len = 500,silence_thresh = sound.dBFS-14,keep_silence=500,)

	folder_name = "audio-chunks"
	# create a directory to store the audio chunks
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	whole_text = ""
    # process each chunk 
	for i, audio_chunk in enumerate(chunks, start=1):
		##ACA ACTUALIZO EL LABLE
		
		print("{}/{}".format(i,len(chunks)))
		
		# export audio chunk and save it in
		# the `folder_name` directory.
		chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
		audio_chunk.export(chunk_filename, format="wav")
		# recognize the chunk
		with sr.AudioFile(chunk_filename) as source:
			audio_listened = r.record(source)
			# try converting it to text
			try:
				text = r.recognize_google(audio_listened, language="es-ES")
			except sr.UnknownValueError as e:
				print("Error:", str(e))
			else:
				text = f"{text.capitalize()}. "
				whole_text += text
	# return the text for all chunks detected
	return whole_text

def prueba(fileName):
	return fileName

	
class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 file dialogs - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.openFileNameDialog()
		self.show()
    
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		full_text = "asd"
		if fileName:
			print(fileName)
			prueba(fileName)
			#full_text = get_large_audio_transcription(path)
			f = open("{}txt".format(fileName[:-3]),'a')
			f.write(full_text)
			f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
	
	
