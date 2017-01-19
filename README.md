# RedDayRestrict

This bot will monitor submissions to your subreddit and will automatically remove any posts with links to specific websites if it is not an acceptable day to do so. For example, if you only wanted YouTube links to be allowed on Tuesdays and Thursdays, this could do that.

## Requirements

* Python 3.5+
* [praw](praw.readthedocs.io)
* Bot account with moderator status on your subreddit

## Usage

Create a new folder and copy `RedDayRestrict.py` into it. In that same folder, create a file named `message.md`. `message.md` will be sent to each user after their post is removed, so write something nice and courteous explaining why you're autoremoving their content. (Note: You can use markdown)

After you have done this, open `RedDayRestrict.py`. After the first comment block there are two lines of `#`'s that indicate what variables you will need to change. Edit the file accordingly and save it. When all this is done, simply start the script and let it run.
