#! /usr/bin/env python

import json,subprocess,urllib2

jsonshit=json.loads(urllib2.urlopen("http://developer.echonest.com/api/v4/song/search?bucket=id:spotify&bucket=tracks&results=100&api_key=MZFEPELDSKFX4WAMA&artist=%s&title=%s"%(raw_input("group? ",),raw_input("title? ",))).read())
print jsonshit["response"]["songs"][0]["artist_name"],jsonshit["response"]["songs"][0]["title"]
processeddata=json.loads(urllib2.urlopen("https://api.spotify.com/v1/tracks/"+jsonshit["response"]["songs"][0]["tracks"][0]["foreign_id"].split(':')[2]).read())
subprocess.call(["vlc", processeddata["preview_url"]])