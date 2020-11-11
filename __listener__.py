import threading
from pynput import keyboard
from logging import exception

class listener(threading.Thread):
  
  isShowed = True

  def __init__(self):
    threading.Thread.__init__(self)
    self.isAlive = True

  def run(self):
    with keyboard.Listener(on_release=lambda event: on_release(event, self)) as listener:  # Create an instance of Listener
      listener.join()  # Join the listener thread to the main thread to keep waiting for keys

  def get_id(self):   
    # returns id of the respective thread 
    if hasattr(self, '_thread_id'): 
      return self._thread_id 
    for id, thread in threading._active.items(): 
      if thread is self: 
        return id

def on_release(key, self):
  if hasattr(key, 'char'):
    if key.char == '\x0b':
      self.isAlive = False
      return False
    if key.char == '\x02':
      listener.isShowed = not listener.isShowed