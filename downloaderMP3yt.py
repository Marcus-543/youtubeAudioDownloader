from pytube import YouTube, Playlist
import moviepy.editor as mp
import re
import os

class App:
	def __init__(self):
		self.path = "downloads"
		self.url = ""

	def recebeURL(self):
		self.url = input("digite o link do video ou da playlist que deseja baixar: ")

	def baixaAudio(self):
		video = YouTube(self.url)
		audio = video.streams.filter(only_audio=True).first().download(self.path)
		self.converteParaMP3()

	def baixaPlaylist(self):
		playlist = Playlist(self.url)
		count = 1
		for url in playlist:
			self.url = url
			self.baixaAudio()
			print("AUDIO"+str(count)+" DA PLAYLIST BAIXADO.")
			count += 1

	def converteParaMP3(self):
		for file in os.listdir(self.path):
			if re.search("mp4", file):
				mp4_path = os.path.join(self.path, file)
				mp3_path = os.path.join(self.path, os.path.splitext(file)[0]+".mp3")
				new_file = mp.AudioFileClip(mp4_path)
				new_file.write_audiofile(mp3_path)
				os.remove(mp4_path)

	def verificaDiretorioDownloads(self):
		if os.path.exists(self.path) == False:
			os.mkdir(self.path)

	def downloads(self):
		self.verificaDiretorioDownloads()
		self.recebeURL();
		print("baixando audio(s)...")
		if "playlist" in self.url:
			self.baixaPlaylist()
		else:
			self.baixaAudio()
		print("download(s) completo(s).")
		print("SUCESSO.")	

app = App()
app.downloads()