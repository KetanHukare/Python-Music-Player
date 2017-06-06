import os
import mutagen
import mutagen.mp3
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from tkinter import ttk
from tkinter.filedialog import askopenfilename

root = Tk()
root.title("Maza Player")
root.minsize(300, 300)
f = ttk.Frame(root, height = 300, width = 100)
f.grid(column = 0, row = 0)

list_of_songs = []
real_names = []

index = 0
play_pause_index = 0
v = StringVar()
songlabel = Label(f, textvariable = v, width = 20)



def select_song():
	file = askopenfilename(parent = root)
	if file.endswith(".mp3"):
		try:
			directory_path = os.path.realpath(file)
			audio = ID3(directory_path)
			real_names.append(audio['TIT2'].text[0])
			list_of_songs.append(file)
		except mutagen.id3.ID3NoHeaderError:
			real_names.append(file)
	player_init()
	updatelabel()


def directory_chooser():
	directory = askdirectory()
	try:
		os.chdir(directory)
	except FileNotFoundError:
		print ("Directory Not Found: Error Occurred")
		exit(0)	
	for files in os.listdir(directory):
		if files.endswith(".mp3"):
			try:
				directory_path = os.path.realpath(files)
				audio = ID3(directory_path)
				real_names.append(audio['TIT2'].text[0])
				list_of_songs.append(files)
			except mutagen.id3.ID3NoHeaderError:
				real_names.append(files)
	real_names.reverse()

	for items in real_names:
		listbox.insert(0, items)

	real_names.reverse()

	print (list_of_songs)
	print (real_names)
#	try:
	player_init()


def updatelabel():
	global index
	global songname
	v.set(real_names[index])
#	return songname

def player_init():
	global list_of_songs
	mp3 = mutagen.mp3.MP3(list_of_songs[0])
	pygame.mixer.init(frequency=mp3.info.sample_rate)
	# pygame.mixer.init()
	pygame.mixer.music.load(list_of_songs[0])


def play_pause_song(event):
	global play_button
	global play_pause_index
	if (play_pause_index == 0):
		pygame.mixer.music.play()
		play_button["text"] ="Pause"
	elif(play_pause_index % 2 == 0):
		pygame.mixer.music.unpause()
		play_button["text"] ="Pause"
	else:
		pygame.mixer.music.pause()
		play_button["text"] ="Play"

	updatelabel()
	play_pause_index += 1



def next_song(event):
	global index
	index = (index + 1) % len(list_of_songs)
	pygame.mixer.music.load(list_of_songs[index])
	pygame.mixer.music.play()
	updatelabel()
	global play_pause_index
	play_pause_index = 1

def prev_song(event):
	global index
	index = index - 1
	pygame.mixer.music.load(list_of_songs[index])
	pygame.mixer.music.play()
	updatelabel()
	global play_pause_index
	play_pause_index = 1

def stop_song(event):
	global play_button
	play_button["text"] = "Play"
	pygame.mixer.music.stop()
	v.set("")
	global play_pause_index
	play_pause_index = 0



label = ttk.Label(f,text= 'Playlist')
label.grid(column = 1, columnspan = 2, row = 0)

listbox = Listbox(f)

play_button = Button(f, text = "Play" , width=12)

next_button = Button(f, text = "Next", width=12)

prev_button = Button(f, text = "Previous", width=12)

stop_button = Button(f, text = "Stop", width=12)




menubar = Menu(f)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command = directory_chooser )
filemenu.add_command(label = "Play Song", command = select_song)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

listbox.grid(column = 0, row = 1, columnspan = 6, rowspan = 3)
prev_button.grid(column = 0, row = 6)
play_button.grid(column = 1, row = 6)
next_button.grid(column = 2, row = 6)
stop_button.grid(column = 3, row = 6)

songlabel.grid(column = 0, row = 7, columnspan = 4)

play_button.bind("<Button-1>", play_pause_song)
next_button.bind("<Button-1>", next_song)
prev_button.bind("<Button-1>", prev_song)
stop_button.bind("<Button-1>", stop_song)


root.mainloop()