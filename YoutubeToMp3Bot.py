import telebot
from telebot import types
from pytube import YouTube, Playlist
import os

API_Key = "6594313189:AAEiLNF212n6pDf7qOzaQ5eLHNemHhILLeM"

bot = telebot.TeleBot(API_Key)

def download_song(url):
    out_file = YouTube(url).streams.filter(only_audio=True).first().download()
    return out_file

def download_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    os.mkdir(playlist.title)
  
    for url in playlist:
        out_file = YouTube(url).streams.filter(only_audio=True).first().download(output_path=str(playlist.title))
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    return playlist.title

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Download 1 song'))
    markup.add(types.KeyboardButton('Download whole playlist'))
    bot.send_message(message.chat.id, "Do you want to download 1 song or whole playlist?", reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    if message.text == 'Download 1 song':
        bot.reply_to(message, "Please enter the URL of the song you want to download.")
        bot.register_next_step_handler(message, handle_song_choice)
    elif message.text == 'Download whole playlist':
        bot.reply_to(message, "Please enter the URL of the playlist you want to download.")
        bot.register_next_step_handler(message, handle_playlist_choice)
    else:
        bot.reply_to(message, "Sorry, I don't understand that choice.")

def handle_song_choice(message):
    url = message.text
    try:
        file_path = download_song(url)
        bot.send_audio(message.chat.id, audio=open(file_path, 'rb'))
        os.remove(file_path)  # Remove the downloaded file after sending
        bot.send_message(message.chat.id, "Song downloaded successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")
        os.remove(file_path)

def handle_playlist_choice(message):
    playlist_url = message.text
    try:
        folder_path = download_playlist(playlist_url)
        files = [f"{folder_path}/{file}" for file in os.listdir(folder_path)]
        for file in files:
            bot.send_audio(message.chat.id, audio=open(file, 'rb'))
            os.remove(file)  # Remove the downloaded file after sending
        os.rmdir(folder_path)  # Remove the empty folder after sending all files
        bot.send_message(message.chat.id, "Playlist downloaded successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")
        for file in files:
            bot.send_audio(message.chat.id, audio=open(file, 'rb'))
            os.remove(file)  # Remove the downloaded file after sending
        os.rmdir(folder_path)  # Remove the empty folder after sending all files

bot.infinity_polling()