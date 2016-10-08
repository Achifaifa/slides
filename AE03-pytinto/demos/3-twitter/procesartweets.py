import json, tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import apikeys, ventanas

auth=OAuthHandler(apikeys.apikey, apikeys.apisecret)
auth.set_access_token(apikeys.consumerkey, apikeys.consumersecret)
api=tweepy.API(auth)
# Set window
w=ventanas.update_window()
w.send(None)

class listener(StreamListener):

  def on_data(self, data):

    try:
      data=json.loads(data)

      text=data["text"]
      text="\n".join([i for i in text.split("\n") if i])
      user=data["user"]["name"]
      username=data["user"]["screen_name"]
      date=data["created_at"]

      with open("tweets.txt","a+") as t:
        t.write("[%s] %s (%s)\n%s\n"%(date,user,username,text.replace("\n"," ")))
      w.send((date,user,username,text))
      print "Actualizado"
    
    except BaseException as e:
      print "----------------------\n",e

    finally:
      return True

  def on_error(self, status):
    
    print(status)
    return True

twitter_stream = Stream(auth, listener())
twitter_stream.filter(track=['AE03 pythonmola'])
