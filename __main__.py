# import pipimport
# pipimport.install()
import tkinter
from tkinter import *
import sys
import os
import __listener__

# TODO
# - every second i call API
# - timer

heroesSize = 55
heroes = ['H0','H1','H2','H3','H4'] # TODO is usefull?

class window:

  def __init__(self, root):
    self.buttons = []
    # image = "img.png",
    # buttons for heroes and abilities
    self.buttons.append(tkinter.Button(top, bg = "red", text = "H0", command = lambda: self.click("H0")))
    self.buttons.append(tkinter.Button(top, text = "P0_H0", command = lambda: self.click("P0_H0")))
    self.buttons.append(tkinter.Button(top, text = "P1_H0", command = lambda: self.click("P1_H0")))
    self.buttons.append(tkinter.Button(top, bg = "red", text = "H1", command = lambda: self.click("H1")))
    self.buttons.append(tkinter.Button(top, text = "P0_H1", command = lambda: self.click("P0_H1")))
    self.buttons.append(tkinter.Button(top, text = "P1_H1", command = lambda: self.click("P1_H1")))
    self.buttons.append(tkinter.Button(top, bg = "red", text = "H2", command = lambda: self.click("H2")))
    self.buttons.append(tkinter.Button(top, text = "P0_H2", command = lambda: self.click("P0_H2")))
    self.buttons.append(tkinter.Button(top, text = "P1_H2", command = lambda: self.click("P1_H2")))
    self.buttons.append(tkinter.Button(top, bg = "red", text = "H3", command = lambda: self.click("H3")))
    self.buttons.append(tkinter.Button(top, text = "P0_H3", command = lambda: self.click("P0_H3")))
    self.buttons.append(tkinter.Button(top, text = "P1_H3", command = lambda: self.click("P1_H3")))
    self.buttons.append(tkinter.Button(top, bg = "red", text = "H4", command = lambda: self.click("H4")))
    self.buttons.append(tkinter.Button(top, text = "P0_H4", command = lambda: self.click("P0_H4")))
    self.buttons.append(tkinter.Button(top, text = "P1_H4", command = lambda: self.click("P1_H4")))

    for b in self.buttons:  
      b.pack()
      if b['text'][0:1] == 'H':
        b.place(bordermode=OUTSIDE, height=heroesSize, width=heroesSize, x=0, y=(int(b['text'][1:2])*heroesSize))
      elif b['text'][0:2] == 'P0':
        b.place(bordermode=OUTSIDE, height=heroesSize/2, width=heroesSize/2, x=heroesSize, y=(int(b['text'][4:5])*heroesSize))
      elif b['text'][0:2] == 'P1':
        b.place(bordermode=OUTSIDE, height=heroesSize/2, width=heroesSize/2, x=heroesSize, y=(int(b['text'][4:5])*heroesSize)+heroesSize/2)

  def click(self, button):
    print(button) #debug message
    # self.label.config(text = selection)

def func(event):
  # TODO... Connection test
  key = sv.get()
  text_file = open(os.path.join(os.path.dirname(__file__), 'key.config'), "w")
  text_file.write(key)
  text_file.close()
  entry.destroy()

def center(root):
  # Gets the requested values of the height and widht.
  windowWidth = root.winfo_reqwidth()
  windowHeight = root.winfo_reqheight()
  # Gets both half the screen width/height and window width/height
  positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
  positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
  # Positions the window in the center of the page.
  root.geometry("+{}+{}".format(positionRight, positionDown))

if __name__ == "__main__":
  # key management
  try:
    fileObject = open(os.path.join(os.path.dirname(__file__), 'key.config'), "r")
    key = fileObject.read()
  except:
    key = ''

  entry = Tk()
  
  entry.resizable(False, False)
  entry.attributes('-topmost', True)
  entry.title("")
  entry.iconbitmap(default=os.path.join(os.path.dirname(__file__), 'transparent.ico'))

  l = Label(entry, text = "API Key")
  l.pack(side = TOP, padx = 10, pady = 10)

  sv = StringVar()
  e = Entry(entry, bd = 5, textvariable = sv)
  e.bind('<Return>', func)
  e.pack(side = BOTTOM, padx = 10, pady = 10)
  e.delete(0,END)
  e.insert(0,key)
  # TODO select all

  # TODO onClose

  # TODO border
  
  entry.overrideredirect(True)
  center(entry)

  entry.mainloop()

  # start main

  top = tkinter.Tk()
  heroesSize = int(top.winfo_screenheight()/20)

  th = __listener__.listener()
  th.start()

  win = window(top)
  top.geometry(str(int(heroesSize*1.5))+"x"+str(heroesSize*5))
  top.overrideredirect(1) #Remove border
  top.resizable(False, False)
  top.attributes('-topmost', True)
  while True:
    # window update
    top.update_idletasks()
    top.update()
    # show/hide
    if __listener__.listener.isShowed:
      top.deiconify()
    else:
      top.withdraw()
    if not th.isAlive:
      break    

  top.destroy()
  top.quit()
  sys.exit()