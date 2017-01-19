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

RESTRICTED_LINK_DOMAINS = [ "youtube.com", "youtu.be" ]
# Put any domains you want restricted here.
# Should be surrounded by quotes and separated by commas, like so:
# RESTRICTED_LINK_DOMAINS = [ "youtube.com", "youtu.be" ]


DAYS_ALLOWED = [ 0, 1, 2, 3, 4, 5, 6 ]
# These are the days of the week that links to the restricted domains
# will be allowed. Delete the days you want the bot to remove posts.
# I.e. for only allowing posts on Tuesdays and Thursdays:
# DAYS_ALLOWED = [ 2, 4 ]
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
	exit("No "+MyDirPath+"message.md file found. Please create this file and write a message to send to offenders. You may use markdown if you wish.\n	Exiting.")

if not (MY_PERSONAL_REDDIT_ACCOUNT and REDDIT_BOT_USERNAME and REDDIT_BOT_PASSWORD and REDDIT_BOT_CLIENT_ID and REDDIT_BOT_SECRET and MY_SUBREDDIT and RESTRICTED_LINK_DOMAINS and REMOVAL_MESSAGE):
	exit("Error when defining variables. Please open "+__file__+" in a text editor and ensure all variables are defined.\n\n	Exiting.")

try:
	import praw
except:
	exit("Please install praw. The easiest way is to run 'pip3 install "+mod+"'. More information about praw can be found at http://praw.readthedocs.io\n\n	Exiting.")

try:
	reddit = praw.Reddit(client_id=REDDIT_BOT_CLIENT_ID,
						client_secret=REDDIT_BOT_SECRET,
						password=REDDIT_BOT_PASSWORD,
						user_agent="Removing posts from /r/"+MY_SUBREDDIT+" that go to a specific site on specific days, hosted by /u/"+MY_PERSONAL_REDDIT_ACCOUNT,
						username=REDDIT_BOT_USERNAME)
except Exception as e:
	exit("Reddit authentication failed. Check for correct credentials and internet connection\n\nMore details: "+str(e.args()))

from time import strftime as st
from time import gmtime
MySub = reddit.subreddit(MY_SUBREDDIT)
print("Successful launch. Monitoring...")
for submission in MySub.stream.submissions():
	print("Submission found.")
	postEpochTime = submission.created
	postWeekDay = eval(st("%w",gmtime(postEpochTime)))
	if postWeekDay not in DAYS_ALLOWED:
		print(":..Post not made on safe day. Checking link.")
		isOkay = True
		for domain in RESTRICTED_LINK_DOMAINS:
			if domain in submission.url:
				print("  :..Post contained restricted domain.")
				submission.mod.remove()
				submission.author.message("Submission removal",REMOVAL_MESSAGE)
				print("  :../u/"+submission.author.name+" notified of their wrongdoings.")
				isOkay = False
		if isOkay:
			print("  :..URL domain not found in restricted domains. Ignored.")
