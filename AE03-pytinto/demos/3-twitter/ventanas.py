#! /usr/bin/env python

import tkFont, Tkinter

# Windows is created when importing this module
root=Tkinter.Tk()
root.wm_title("AE03 tweets")
bigfont=tkFont.Font(root=root, font=None, name=None, family='Mono', size=50, weight='bold')
bigishfont=tkFont.Font(root=root, font=None, name=None, family='Mono', size=26, weight='bold')
smallfont=tkFont.Font(root=root, font=None, name=None, family='Mono', size=25)
Tkinter.mainloop(1) 

def update_window():

  handle=Tkinter.Label(text="", font=bigfont)
  handlename=Tkinter.Label(text="", font=bigishfont)
  date=Tkinter.Label(text="", font=bigishfont)
  tweet=Tkinter.Label(text="", font=smallfont, wraplength=800, justify="left")

  handle.pack(side="top", padx=10, fill="x")
  handlename.pack(side="top", padx=10, fill="x")
  date.pack(side="top", padx=10, fill="x")
  tweet.pack(side="top", padx=10, fill="x")
  root.update()

  while 1:
    try: 
      timestamp,user,username,text=yield
      timestamp=" ".join(timestamp.split()[1:4])
      handle.config(text="\n"+user)
      handlename.config(text="@"+username)
      date.config(text=timestamp+"\n")
      tweet.config(text=text)

      root.update()
    except: pass
