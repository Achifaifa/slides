import smtplib, urllib
import passf
from email.mime.text import MIMEText

url="http://achi.se/temp/AE03"
web=urllib.urlopen(url).read()
with open ("web_vieja.txt") as archivo:
    web_vieja=archivo.read()

if web!=web_vieja: 
    webs=set(web.split('\n'))
    web_viejas=set(web_vieja.split('\n'))
    diferencia=webs.difference(web_viejas)
    
    txt="Hay avisos nuevos en %s!\nEstos son los nuevos avisos:\n\n"%url+"\n".join(diferencia).replace("<li> ","")
    mensaje=MIMEText(txt)
    mensaje['subject']="Avisos nuevos en %s"%url
    mensaje['from']="Aviso automatico"
    mensaje['to']="ae03demo@mail.com"

    s=smtplib.SMTP("smtp.mail.com", 587)
    s.ehlo()
    s.starttls()
    s.login("ae03demo@mail.com", passf.password)
    try:
      s.sendmail("ae03demo@mail.com", "ae03demo@mail.com", mensaje.as_string())
      with open("web_vieja.txt","w+") as archivo:
        archivo.write(web)
    except: pass
    finally:
        s.close()
