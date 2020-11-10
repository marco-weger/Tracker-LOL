# import pipimport
# pipimport.install()

from logging import exception
from tkinter import *
import tkinter
from pynput import keyboard
import logging
import _thread
import sys

# TODO
# - ctrl+b show/unshow
# - combination to close app
# - every second i call API
# - screen proportion
# - timer

heroesSize = 55
heroes = ['H0','H1','H2','H3','H4']
# Setup logging
logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def helloCallBack(hero):
  print("hi there, i'm "+hero+"!")
  # tkMessageBox.showinfo( "Hello Python", "Hello World")

def createHeroes(top):
  buttons = []
  for h in heroes:
    buttons.append(tkinter.Button(top,  bg = "red", text = h, command = helloCallBack(h))) # image = "img.png",
    buttons.append(tkinter.Button(top, text = "P0_"+h, command = helloCallBack("P0_"+h)))
    buttons.append(tkinter.Button(top, text = "P1_"+h, command = helloCallBack("P1_"+h)))

  for b in buttons:  
    b.pack()
    if b['text'][0:1] == 'H':
      b.place(bordermode=OUTSIDE, height=heroesSize, width=heroesSize, x=0, y=(int(b['text'][1:2])*heroesSize))
    elif b['text'][0:2] == 'P0':
      b.place(bordermode=OUTSIDE, height=heroesSize/2, width=heroesSize/2, x=heroesSize, y=(int(b['text'][4:5])*heroesSize))
    elif b['text'][0:2] == 'P1':
      b.place(bordermode=OUTSIDE, height=heroesSize/2, width=heroesSize/2, x=heroesSize, y=(int(b['text'][4:5])*heroesSize)+heroesSize/2)

i = 0
def on_press(key):  # The function that's called when a key is pressed
  i = 0

def on_release(key):
  if hasattr(key, 'char'):
    if key.char == '\x0b':
      sys.exit(0)
    if key.char == '\x02':
      print("SHOW/UNSHOW")

def main(x,y):
  print(x)
  print(y)
  top = tkinter.Tk()
  createHeroes(top)
  top.geometry(str(int(heroesSize*1.5))+"x"+str(heroesSize*5))
  top.overrideredirect(1) #Remove border
  top.resizable(False, False)
  top.mainloop()

try:
  # CANT USE THIS TYPE OF THREAD ON MAC
  # th_main = _thread.start_new_thread( main, ("main",1) )
  # print(th_main)

  main(1,2)

  with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
    listener.join()  # Join the listener thread to the main thread to keep waiting for keys
except exception:
  print(exception)
