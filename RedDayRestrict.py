#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  RedDayRestrict.py
#  
#  Copyright 2017 Keaton Brown <linux.keaton@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

########################################################################
# Fill in from here to the next long bar of #'s
# If two quotes ("") are provided, enter the relevent information 
# between them.

MY_PERSONAL_REDDIT_ACCOUNT=""
# Do not include "/u/"
# This is only used for Reddit's user_agent
# to tell the admins who's running this bot

REDDIT_BOT_USERNAME=""
# Do not include "/u/"
REDDIT_BOT_PASSWORD=""
REDDIT_BOT_CLIENT_ID=""
REDDIT_BOT_SECRET=""

MY_SUBREDDIT=""
# Do not include "/r/"

RESTRICTED_LINK_DOMAINS = [  ]
# Put any domains you want restricted here.
# Should be surrounded by quotes and separated by commas, like so:
# RESTRICTED_LINK_DOMAINS = [ "youtube.com", "youtu.be" ]
# Do not add anything if you want to restrict your subreddit to 
# self-posts only on the unrestricted days


RESTRICTED_DAYS = [ 0, 1, 2, 3, 4, 5, 6 ]
# These are the days of the week that links to the restricted domains
# will be blocked. Delete the days you want the bot to allow posts.
# I.e. for allowing all posts only on Tuesdays and Thursdays:
# RESTRICTED_DAYS = [ 0, 1, 3, 5, 6 ]
# Or, for only restricting posts on Sundays:
# RESTRICTED_DAYS = [ 0 ]
# Numbers should be separated by commas
# 0 = Sunday      4 = Thursday
# 1 = Monday      5 = Friday
# 2 = Tuesday     6 = Saturday
# 3 = Wednesday

# All done with variables!
########################################################################

MyDirPath = __file__.strip("RedDayRestrict.py")

try:
    REMOVAL_MESSAGE = open(MyDirPath+"message.md").read()
except:
    exit("No "+MyDirPath+"message.md file found. Please create this file and write a message to send to offenders. You may use markdown if you wish.\n    Exiting.")

if not (MY_PERSONAL_REDDIT_ACCOUNT and REDDIT_BOT_USERNAME and REDDIT_BOT_PASSWORD and REDDIT_BOT_CLIENT_ID and REDDIT_BOT_SECRET and MY_SUBREDDIT and RESTRICTED_LINK_DOMAINS and REMOVAL_MESSAGE):
    exit("Error when defining variables. Please open "+__file__+" in a text editor and ensure all variables are defined.\n\n    Exiting.")

try:
    import praw
except:
    exit("Please install praw. The easiest way is to run 'pip3 install "+mod+"'. More information about praw can be found at http://praw.readthedocs.io\n\n    Exiting.")

try:
    reddit = praw.Reddit(client_id=REDDIT_BOT_CLIENT_ID,
                        client_secret=REDDIT_BOT_SECRET,
                        password=REDDIT_BOT_PASSWORD,
                        user_agent="Removing posts from /r/"+MY_SUBREDDIT+" that go to a specific site on specific days, hosted by /u/"+MY_PERSONAL_REDDIT_ACCOUNT,
                        username=REDDIT_BOT_USERNAME)
except Exception as e:
    exit("Reddit authentication failed. Check for correct credentials and internet connection\n\nMore details: "+str(e.args()))

from time import strftime as st
from time import gmtime,sleep
MySub = reddit.subreddit(MY_SUBREDDIT)
print("Successful launch. Monitoring...")
while True:
    try:
        for submission in MySub.stream.submissions():
            print("Submission found.")
            postEpochTime = submission.created
            postWeekDay = eval(st("%w",gmtime(postEpochTime)))
            if postWeekDay in RESTRICTED_DAYS:
                print(":..Post not made on safe day. Checking link.")
                isOkay = True
                if RESTRICTED_LINK_DOMAINS:
                    for domain in RESTRICTED_LINK_DOMAINS:
                        if domain.lower() in submission.url.lower():
                            print("  :..Post contained restricted domain.")
                            submission.mod.remove()
                            submission.author.message("Submission removal",REMOVAL_MESSAGE)
                            print("  :../u/"+submission.author.name+" notified of their wrongdoings.")
                            isOkay = False
                else:
                    if not "reddit.com/r/"+MY_SUBREDDIT.lower() in submission.url.lower():
                        print("  :..Post contained restricted domain.")
                        submission.mod.remove()
                        submission.author.message("Submission removal",REMOVAL_MESSAGE)
                        print("  :../u/"+submission.author.name+" notified of their wrongdoings.")
                        isOkay = False
                if isOkay:
                    print("  :..URL domain not found in restricted domains. Ignored.")
    except Exception as e:
        print("There was an error:\n\n    "+str(e.args)+"\n\nTrying again in 30 seconds.")
        sleep(30)
