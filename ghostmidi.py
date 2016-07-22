import tkinter as tk # Python 3
from PIL import ImageGrab
import time
import pygame.midi as midi
import atexit


midi.init()

for p in range(midi.get_count()):
	interf, name, i, o, opened = midi.get_device_info(p)
	name = name.decode('UTF-8')

	
	if i is 1:
		stype = "INPUT"
	else:
		stype = "OUTPUT"
	if opened is 0:
		sopened = "OPEN"
	else:
		sopened = "CLOSE"
	

	print(str(p)+' - '+name+' - '+stype+' - '+sopened)


player = midi.Output(6)


lastTime = time.time()

newNote = 0
lastNote = 0

root = tk.Tk()
# The image must be stored to Tk or it will be garbage collected.
root.image = tk.PhotoImage(file='crosshair.png')
label = tk.Label(root, image=root.image, bg='white')
root.wm_attributes("-topmost", True)
root.wm_attributes("-toolwindow", True)
root.wm_attributes("-transparentcolor", "white")
label.pack()

root.update()

xFix = 10
yFix = 31

@atexit.register
def goodbye():
    player.note_off(lastNote, 127,1)

while True:
	root.update()

	if time.time() > lastTime + 0.05:
		lastTime = time.time()
		image = ImageGrab.grab() #acepta un (x,x,w,h) en teoria
		color = image.getpixel(((root.winfo_x() + root.winfo_width()/2) + xFix, (root.winfo_y() + root.winfo_height()/2) + yFix))
		newNote =  int(color[0] / 255  * 30) + 40

		if newNote is not lastNote:
			player.note_off(lastNote, 127,1)
			player.note_on(newNote, 127,1)

		lastNote = newNote
