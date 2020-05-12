from tkinter import *
import socket
import tqdm
import os
import time

from socket import *

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


#type in location of image, lazy AF
root = Tk()
e = Entry(root, width=50)
e.pack()
#activates when the button is clicky clicked
def myClick():
#some code reused from assignment4
	filename = e.get()
	if filename.lower().endswith(('.png', '.jpg', '.tiff', '.bmp', '.gif', '.jpeg')) is True:
		serverName = '98.148.149.235'
		serverPort = 12000
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((serverName,serverPort))
		filesize = os.path.getsize(filename)
		sentence = 'post'
		clientSocket.send(sentence.encode())
		time.sleep(1)
		clientSocket.send(f"{filename}{SEPARATOR}{filesize}".encode())
		progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		with open(filename, "rb") as f:
			for _ in progress:
				bytes_read = f.read(BUFFER_SIZE)
				if not bytes_read:
					print("\nFile Successfully Delivered")
					break
				time.sleep(.5)
				clientSocket.sendall(bytes_read)
				progress.update(len(bytes_read))
		result = clientSocket.recv(1024)
		resultLabel=Label(root, text=result)
		resultLabel.pack()
	else:
		resultLabel=Label(root, text="Please enter a valid filetype (.png, .jpg, .tiff, .bmp, .gif, .jpeg)")
		resultLabel.pack()
#instructions for user
myLabel1 = Label(root, text="JJB-A Car Identifying Client GUI")
myLabel2 = Label(root, text="enter relative directory of image you want to search up")
myLabel3 = Label(root, text="ie: './folder/car.jpg'")
myLabel1.pack()
myLabel2.pack()
myLabel3.pack()
#issabutton
myButton = Button(root, text="Click Me!", command=myClick)
myButton.pack()

root.mainloop()
