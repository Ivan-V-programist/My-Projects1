from googlesearch import search 
from pytube import YouTube, Playlist
import os 

API_Key = "6594313189:AAEiLNF212n6pDf7qOzaQ5eLHNemHhILLeM"
#########################################################
                # Download functions #

def searchSong():
    link = input("Enter keyword or name: ")
    for j in search(link, tld="co.in", num=1, stop=1, pause=2): 
        return j
#download only 1 song
def downloadSong():
    url = input("Enter name of the song: ")
    out_file =YouTube(url).streams.filter(only_audio=True).first().download()

#download whole playlist
def downloadPlaylist():
    playlist = Playlist(
        input("Enter Playlist url: ")
    )
    os.mkdir(playlist.title)
  
# extract only audio 
    for url in playlist:
        out_file =YouTube(url).streams.filter(only_audio=True).first().download(output_path=str(playlist.title))
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 

                # Download functions #
#########################################################
            
  
  

downloadPlaylist()