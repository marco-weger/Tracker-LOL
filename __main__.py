# import pipimport
# pipimport.install()
# pip3 install riotwatcher
# pip install pandas
# pip install Pillow
# pip install scipy
# pip install webcolors

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
import threading
import requests
import io
from io import BytesIO
import __color__

heroesSize = 10
VERSION = 0

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
  key_e.bind('<Return>', saveConfig)
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
  user_e.bind('<Return>', saveConfig)
  user_e.place(x=200, y=150, anchor="center")
  user_e.delete(0,END)
  user_e.insert(0,user)

  canvas.grid(row=0,column=0)

  entry.overrideredirect(True)
  center(entry)

  key_e.focus()
  key_e.select_range(0,'end')

  entry.mainloop()

def saveConfig(event):
  global key
  global user
  global entry

  key = key_sv.get()
  text_file = io.open(os.path.join(os.path.dirname(__file__), 'key.config'), "w")
  text_file.write(key)
  text_file.close()

  user = user_sv.get()
  text_file = io.open(os.path.join(os.path.dirname(__file__), 'user.config'), "w")
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

def th_scheduleCall():
  global update
  global th_call_isAlive
  while th_call_isAlive:
    if update == False:
      time.sleep(2)
      update = True

def th_gameLockup():
  global update
  global me
  global match_id
  global buttons
  global spell
  global last_match_id
  global btn_status

  game = watcher.get_current_game(me['id'])
  # print(game)

  try:
    game['participants']
    game['gameId']
  except Exception:
    match_id = -1
  else:
    match_id = game['gameId']
    if match_id != last_match_id:
      myteam = [x for x in game['participants'] if x['summonerName'] == me['name']][0]['teamId']
      challengers = [x for x in game['participants'] if x['teamId'] != myteam]
      
      j = 0
      for c in challengers: # x['championId'],x['spell1Id'],x['spell2Id']}
        buttons[j][0] = c['championId'] # watcher.get_champion_by_id() # not counted in api call rate

        tmp_spell = [x for x in spell if x['id'] == c['spell1Id']][0]['iconPath']
        tmp_spell = tmp_spell[1+tmp_spell.rindex('/'):]
        buttons[int(j)][5] = tmp_spell
        btn_status[int(j)*2][4] = [x for x in spell if x['id'] == c['spell1Id']][0]['cooldown']

        tmp_spell = [x for x in spell if x['id'] == c['spell2Id']][0]['iconPath']
        tmp_spell = tmp_spell[1+tmp_spell.rindex('/'):]
        buttons[int(j)][6] = tmp_spell
        btn_status[int(j)*2+1][4] = [x for x in spell if x['id'] == c['spell2Id']][0]['cooldown']

        j += 1
  update = False

def th_countdown(button):
  global btn_status

  btn_status[int(button)][2] = btn_status[int(button)][4]

  while btn_status[int(button)][2] > 0 and btn_status[int(button)][0]:
    time.sleep(1)
    btn_status[int(button)][2]-=1
  btn_status[int(button)][1] = threading.Thread(target=lambda: th_countdown(int(button)))
  btn_status[int(button)][0] = False

def click(button):
  global btn_status
  global match_id

  if not bool(btn_status[int(button)][0]) and match_id > -1:
    btn_status[int(button)][0] = True
    btn_status[int(button)][1].start()

if __name__ == "__main__":
  # key management
  try:
    fileObject = io.open(os.path.join(os.path.dirname(__file__), 'key.config'), "r")
    key = fileObject.read()
  except:
    key = 'API key'
  # user management
  try:
    fileObject = io.open(os.path.join(os.path.dirname(__file__), 'user.config'), "r")
    user = fileObject.read()
  except:
    user = 'Username'

  showConfigWindow()

  watcher = __lol__.RiotObserver(key,Regions.EUROPE_WEST)
  global me
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

    top = Tk()
    heroesSize = int(top.winfo_screenheight()/heroesSize)

    th_listener = __listener__.listener()
    th_listener.start()

    top.geometry(str(int(heroesSize*1.5))+"x"+str(heroesSize*5))
    top.overrideredirect(1) #Remove border
    top.resizable(False, False)
    top.attributes('-topmost', True)

    global update
    global th_call_isAlive
    global match_id
    global last_match_id
    global buttons
    global spell
    global btn_status

    spell = requests.get("http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json").json()

    buttons = []

    tmp_btn = []
    for i in range(10):
      tmp_btn.append(
        Canvas(
          top,
          width=int(heroesSize/2),
          height=int(heroesSize/2),
          border = 0,
          highlightthickness = 0,
          relief = "solid",
          bg = "black"
        )
      )
    
    tmp_btn[0].bind("<Button-1>", lambda event: click(0))
    tmp_btn[1].bind("<Button-1>", lambda event: click(1))
    tmp_btn[2].bind("<Button-1>", lambda event: click(2))
    tmp_btn[3].bind("<Button-1>", lambda event: click(3))
    tmp_btn[4].bind("<Button-1>", lambda event: click(4))
    tmp_btn[5].bind("<Button-1>", lambda event: click(5))
    tmp_btn[6].bind("<Button-1>", lambda event: click(6))
    tmp_btn[7].bind("<Button-1>", lambda event: click(7))
    tmp_btn[8].bind("<Button-1>", lambda event: click(8))
    tmp_btn[9].bind("<Button-1>", lambda event: click(9))

    # started/ended - thread - timer
    btn_status = [
      [False, threading.Thread(target=lambda: th_countdown(int(0))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(1))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(2))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(3))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(4))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(5))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(6))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(7))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(8))), 0, -1, 0, "white"],
      [False, threading.Thread(target=lambda: th_countdown(int(9))), 0, -1, 0, "white"],
    ]

    for i in (0,1,2,3,4):
      buttons.append(
        [
          'H'+str(i),
          Canvas(
            top,
            width = heroesSize,
            height = heroesSize,
            border = 0,
            highlightthickness = 0,
            relief = "solid",
            bg = "black"
          ),
          tmp_btn[i*2],
          tmp_btn[i*2+1],
          '','',''
        ]
      )

    i = 0
    while i < len(buttons):
      buttons[int(i)][1].place(x=0, y=int(i)*heroesSize)
      buttons[int(i)][2].place(x=heroesSize, y=int(i)*heroesSize)
      buttons[int(i)][3].place(x=heroesSize, y=int(i)*heroesSize+heroesSize/2)
      i += 1

    top.overrideredirect(True)

    # Schedule
    match_id = -1
    last_match_id = -1
    update = True
    th_call_isAlive = True

    th_call = threading.Thread(target=th_scheduleCall)
    th_call.start()
    th_lockup = threading.Thread(target=th_gameLockup)

    while True:
      if update and not th_lockup.is_alive():
        th_lockup = threading.Thread(target=th_gameLockup)
        th_lockup.start()

      if last_match_id != match_id:
        last_match_id = match_id
        if match_id > 0:
          i = 0
          while i < len(buttons):
            try:
              response = requests.get("http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/"+str(buttons[i][0])+".png")
              im = Image.open(BytesIO(response.content))
              im = im.resize((heroesSize, heroesSize), Image.ANTIALIAS)
              buttons[i][4] = PIL.ImageTk.PhotoImage(im)
              buttons[int(i)][1].create_image(0, 0, image = buttons[int(i)][4], anchor = NW)
            except Exception as e:
              print(str(e))

            try:
              response = requests.get("http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/data/spells/icons2d/" + str(buttons[int(i)][5]).lower())
              im = Image.open(BytesIO(response.content))
              im = im.resize((int(heroesSize/2), int(heroesSize/2)), Image.ANTIALIAS)

              btn_status[i*2][5] = str(__color__.hexToName("#"+str(__color__.colorInvert(__color__.getDominant(im))))) # color set

              buttons[int(i)][5] = PIL.ImageTk.PhotoImage(im)
              buttons[int(i)][2].create_image(0, 0, image = buttons[int(i)][5], anchor = NW)
            except Exception as e:
              print(str(e))

            try:
              response = requests.get("http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/data/spells/icons2d/" + str(buttons[int(i)][6]).lower())
              im = Image.open(BytesIO(response.content))
              im = im.resize((int(heroesSize/2), int(heroesSize/2)), Image.ANTIALIAS)

              btn_status[i*2+1][5] = str(__color__.hexToName("#"+str(__color__.colorInvert(__color__.getDominant(im))))) # color set
              
              buttons[int(i)][6] = PIL.ImageTk.PhotoImage(im)
              buttons[int(i)][3].create_image(0, 0, image = buttons[int(i)][6], anchor = NW)
            except Exception as e:
              print(str(e))

            i += 1
        else:
          print(match_id) 

      i = 0
      while i < len(buttons):
        try:
          # delete previous number
          if btn_status[i*2][3] > -1:
            buttons[int(i)][2].delete(btn_status[i*2][3])
            btn_status[i*2][3] = -1

          # delete previous number
          if btn_status[i*2+1][3] > -1:
            buttons[int(i)][3].delete(btn_status[i*2+1][3])
            btn_status[i*2+1][3] = -1

          if btn_status[i*2][2] > 0 and btn_status[i*2][0]:
            btn_status[i*2][3] = buttons[int(i)][2].create_text((int(heroesSize/4),int(heroesSize/4)),fill=btn_status[i*2][5],font="Arial 12 bold", text=btn_status[i*2][2])
          if btn_status[i*2+1][2] > 0 and btn_status[i*2+1][0]:
            btn_status[i*2+1][3] = buttons[int(i)][3].create_text((int(heroesSize/4),int(heroesSize/4)),fill=btn_status[i*2+1][5],font="Arial 12 bold", text=btn_status[i*2+1][2])
        except Exception as e:
          print(e)
        i += 1

      # window update
      top.update_idletasks()
      top.update()
      # show/hide
      if __listener__.listener.isShowed:
        top.deiconify()
      else:
        top.withdraw()
      if not th_listener.isAlive:
        break

  for b in btn_status:
    b[2] = 0
    b[0] = FALSE
    # if b[1].is_alive():
    #   b[1].join()

  th_lockup.join()
  th_call_isAlive = False
  th_call.join()
  top.destroy()
  top.quit()
  sys.exit()