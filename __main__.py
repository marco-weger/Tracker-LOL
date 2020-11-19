# import pipimport
# pipimport.install()
# pip3 install riotwatcher
# pip install pandas
# pip install Pillow

import tkinter
from tkinter import *
import sys
import os
import __listener__
import __lol__
from __lol__ import Regions
import PIL
from PIL import ImageTk, Image
import time

# TODO
# - every 2 or 3 second i call API
# - timer

heroesSize = 55
heroes = ['H0','H1','H2','H3','H4']

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

def showConfigWindow():
  global key_sv
  global user_sv
  global entry

  entry = Tk()
  entry.resizable(False, False)
  entry.attributes('-topmost', True)

  #background
  try:
    img = PIL.ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "bg.png")))
    bg_width = img.width();
    bg_height = img.height();
    img_set = True
  except Exception:
    print("Can't open background image")
    bg_width = "400";
    bg_height = "180";
    img_set = False

  canvas = Canvas(
    entry,
    width = int(bg_width)-2,
    height = int(bg_height)-2,
    border = 0,
    relief = "solid",
  )

  if img_set:
    try:
      canvas.create_image(0, 0, anchor=NW, image=img)
    except Exception:
      print("Can't elaborate background image")

  key_sv = StringVar()
  key_e = Entry(
    canvas,
    bd = 1,
    relief = "groove",
    textvariable = key_sv,
    width = 44,
    justify = 'center'
  )
  key_e.config({"background": "#bbb"})
  key_e.bind('<Return>', func)
  key_e.place(x=200, y=75, anchor="center")
  key_e.delete(0,END)
  key_e.insert(0,key)

  user_sv = StringVar()
  user_e = Entry(
    canvas,
    bd = 1,
    relief = "groove",
    textvariable = user_sv,
    width = 44,
    justify = 'center'
  )
  user_e.config({"background": "#bbb"})
  user_e.bind('<Return>', func)
  user_e.place(x=200, y=150, anchor="center")
  user_e.delete(0,END)
  user_e.insert(0,user)  
  
  canvas.grid(row=0,column=0)
  
  entry.overrideredirect(True)
  center(entry)

  key_e.focus()
  key_e.select_range(0,'end')

  entry.mainloop()

def func(event):
  global key
  global user
  global entry

  key = key_sv.get()
  text_file = open(os.path.join(os.path.dirname(__file__), 'key.config'), "w")
  text_file.write(key)
  text_file.close()

  user = user_sv.get()
  text_file = open(os.path.join(os.path.dirname(__file__), 'user.config'), "w")
  text_file.write(user)
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
    key = 'API key'
  # user management
  try:
    fileObject = open(os.path.join(os.path.dirname(__file__), 'user.config'), "r")
    user = fileObject.read()
  except:
    user = 'Username'

  showConfigWindow()

  # TODO prevedere errore inserimento nome
  watcher = __lol__.RiotObserver(key,Regions.EUROPE_WEST)
  try:
    me = watcher.get_summoner_by_name(summoner_name=user) # This requeset is used as a 'login', is it fails i kill the process because username or key is broken
    if 'status' in me:
      if 'status_code' in me['status']:
        if int(me['status']['status_code']) >= 300:
          raise ValueError("Invalid username or API key")
  except Exception:
    raise ValueError(Exception)
  else:
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

    ##############################################
    # TODO FROM HERE MUST START WITH A TIMER
    time.sleep(1)
    game = watcher.get_current_game(me['id'])

    try:
      game['participants']
    except:
      print("Not in a game...")
    else:
      myteam = [x for x in game['participants'] if x['summonerName'] == TMP_NAME][0]['teamId']
      challengers = [x for x in game['participants'] if x['teamId'] != myteam]
      for c in challengers: # x['championId'],x['spell1Id'],x['spell2Id']}
        print(watcher.get_champion_by_id(c['championId']))

    # TODO maybe image from data dragon

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
    # END TIMER
    ##############################################

  top.destroy()
  top.quit()
  sys.exit()