import tkinter as tk # Python 3
from PIL import ImageGrab
import time
import pygame.midi as midi
import atexit
import msvcrt
import sys

midi.init()

	


lastTime = time.time()

xFix = 10
yFix = 31

ghostMonoNotes = []



master = tk.Tk()
master.title("MASTER")
master.wm_attributes("-topmost", True)
master.wm_attributes("-toolwindow", True)


player = midi.Output

RUNNING = True

def playNote(note,ON=True):
	global player
	if ON:
		player.note_on(note, 127,1)
	else:
		player.note_off(note, 127,1)

def removeItself(widget):
	global ghostMonoNotes
	ghostMonoNotes.remove(widget)

class GhostMonoNote:
	def __init__(self, index):
		self.index = index

		self.newNote = 0
		self.lastNote = 0

		self.root = tk.Toplevel(master)
		# The image must be stored to Tk or it will be garbage collected.
		self.root.image = tk.PhotoImage(file='images/crosshair.png')
		self.label = tk.Label(self.root, image=self.root.image, bg='white')
		self.root.wm_attributes("-topmost", True)
		self.root.wm_attributes("-toolwindow", True)
		self.root.wm_attributes("-transparentcolor", "white")
		self.label.pack()

		self.root.update()
		self.root.title("MonoNote "+str(self.index))


		self.root.protocol("WM_DELETE_WINDOW", self.destroy)

	def checkPixel(self, image):
		self.color = image.getpixel(((self.root.winfo_x() + self.root.winfo_width()/2) + xFix, (self.root.winfo_y() + self.root.winfo_height()/2) + yFix))
		self.newNote =  int(self.color[0] / 255  * 30) + 40

		if self.newNote is not self.lastNote:
			playNote(self.lastNote,False)
			playNote(self.newNote)

		self.lastNote = self.newNote

	def destroy(self):
		removeItself(self)
		playNote(self.lastNote,False)
		self.root.destroy()

def addGhostMonoNote():
	global ghostMonoNotes
	ghostMonoNotes.append(GhostMonoNote(len(ghostMonoNotes)))

def setPort(widgy,var):
	global player

	p = var.get()
	p = int(p[0])
	player = midi.Output(p)

	b = tk.Button(master, text="New Grabber", command=addGhostMonoNote)
	b.pack()

	widgy.destroy()


variable = tk.StringVar()
variable.set("Set Output Port") # default value
options = []
for p in range(midi.get_count()):
	interf, name, i, o, opened = midi.get_device_info(p)
	name = name.decode('UTF-8')
	
	if i is 0 and opened is 0:
		options.append(str(p)+' - '+name)
w = tk.OptionMenu(master, variable, *options, command=lambda x: setPort(w,variable))
w.pack()

def allNoteOff():
	for n in range(128):
		playNote(n,False)

def goodbye():
	global RUNNING
	RUNNING = False
	for g in ghostMonoNotes:
		g.destroy()	

master.protocol("WM_DELETE_WINDOW", goodbye)


while RUNNING:
	master.update()
	if time.time() > lastTime + 0.05:
		lastTime = time.time()
		image = ImageGrab.grab() #acepta un (x,x,w,h) en teoria

		for g in ghostMonoNotes:
			g.checkPixel(image)
else:
	allNoteOff()
	master.destroy()
	midi.quit()	
	sys.exit()