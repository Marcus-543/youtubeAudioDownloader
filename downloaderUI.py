from tkinter import *
from pytube import YouTube, Playlist
import os
import re
import moviepy.editor as mp

class App:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Audio Downloader")

        self.path = "downloads"
        self.url = ""

        self.url_label = Label(master, text="Insira o link do vídeo ou da playlist:")
        self.url_label.pack()

        self.url_entry = Entry(master, width=50)
        self.url_entry.pack()

        self.download_button = Button(master, text="Baixar", command=self.downloads)
        self.download_button.pack()

    def recebeURL(self):
        self.url = self.url_entry.get()

    def baixaAudio(self):
        video = YouTube(self.url)
        audio_stream = video.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(output_path=self.path)
            self.converteParaMP3()
        else:
            print("Nenhuma faixa encontrada na url fornecida.")

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

root = Tk()
my_app = App(root)
root.mainloop()