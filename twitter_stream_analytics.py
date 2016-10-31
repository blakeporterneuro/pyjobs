# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 01:30:14 2016

Adapted from Adil Moujahid: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
All credit goes to Adil, thank you for your post! 
Author: Blake Porter (www.blakeporterneuro.com)

Updates Adil's code so it works with python 3.xx
Adds the ability to automatically open links in your internet browser
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import webbrowser


tweets_data_path = 'twitter_jobs.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print(len(tweets_data))

tweets = pd.DataFrame()

#tweets['YOUR STRING HERE'] = list(map(lambda tweet: tweet.get('YOUR STRING HERE', None),tweets_data))
tweets['text'] = list(map(lambda tweet: tweet.get('text', None),tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet.get('lang', None),tweets_data))
tweets['country'] = list(map(lambda tweet: tweet.get('place',{}).get('country', None) if tweet.get('place') != None else None,tweets_data))


tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

def word_in_text(word,text):
    if text == None:
        return False
    word = word.lower()
    text = text.lower()    
    match = re.search(word,text)
    if match:
        return True
    else:
        return False
        
tweets['postdoc'] = tweets['text'].apply(lambda tweet: word_in_text('postdoc', tweet))
tweets['postdoctoral'] = tweets['text'].apply(lambda tweet: word_in_text('postdoctoral', tweet))

print('postdoc ', tweets['postdoc'].value_counts()[True])
print("postdoctoral: ", tweets['postdoctoral'].value_counts()[True])

titles = [ 'postdoc', 'postdoctoral']
tweets_by_titles = [tweets['postdoc'].value_counts()[True], tweets['postdoctoral'].value_counts()[True]]

x_pos = list(range(len(titles)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_titles, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: postdoc vs. postdoctoral (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(titles)
plt.grid()

tweets['job'] = tweets['text'].apply(lambda tweet: word_in_text('job', tweet))
tweets['position'] = tweets['text'].apply(lambda tweet: word_in_text('position', tweet))

tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('job', tweet) or word_in_text('position', tweet))

print("job: ", tweets['job'].value_counts()[True])
print("position: ", tweets['position'].value_counts()[True])
print("relevant", tweets['relevant'].value_counts()[True])

print(tweets[tweets['relevant'] == True]['postdoc'].value_counts()[True])
print(tweets[tweets['relevant'] == True]['postdoctoral'].value_counts()[True])

tweets_by_title_2 =   [tweets[tweets['relevant'] == True]['postdoc'].value_counts()[True], 
                      tweets[tweets['relevant'] == True]['postdoctoral'].value_counts()[True]]

x_pos = list(range(len(titles)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_title_2, width,alpha=1,color='g')
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: postdoc vs. postdoctoral (Relevant data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(titles)
plt.grid()

def extract_link(text):
    if text == None:
        return ''
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

tweets_relevant = tweets[tweets['relevant'] == True] #only relevant tweets
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != ''] #only tweets with a link
tweets_relevant_with_link = tweets_relevant_with_link.drop_duplicates(subset=['link']) #remove duplicates

#open all the links in your default browser
link_count = 0
for link_number in range(len(tweets_relevant_with_link)):   
    webbrowser.get().open(tweets_relevant_with_link.iat[link_number,8])
    link_count += 1
    if link_count == 9: #if 10 links have been opened (we start at 0)
        input('Press enter to continue opening links') #wait for user to press enter
        link_count = 0 #reset link_count to 0





