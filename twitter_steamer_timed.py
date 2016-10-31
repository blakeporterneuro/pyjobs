# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 01:30:14 2016

Adapted from Adil Moujahid: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
All credit goes to Adil, thank you for your post! 
Author: Blake Porter (www.blakeporterneuro.com)

Updates Adil's code so it works with python 3.xx
Adds the ability to stop the stream after a certain period of time has elapsed
"""

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time



consumer_key = '2AcBC8KToVmgBe7bHG83UFipG'
consumer_secret = 'WKvrSWA4vj3LiJyHiLGH6iqJaGGi01td5lusG6enyCej7Z4mLi'

access_token = '3258313183-ZHE8xNX5nG889JOYcGTL3uNWvBktN9vDKhAiRXl'
access_token_secret = 'aC55C6KFxfD6RtVaj8AhNBXHRWDfLo6J6yrDI2IT43dgM'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class MyStreamListener(StreamListener):
    def __init__(self, time_limit):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('twitter_jobs.json', 'a')
        super(MyStreamListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(data)
            self.saveFile.write('\n')
            return True
        else:
            self.saveFile.close()
            return False

myStream = Stream(auth, listener=MyStreamListener(time_limit=3600))
myStream.filter(track=['postdoc','postdoctoral'])
