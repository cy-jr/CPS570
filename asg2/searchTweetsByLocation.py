# searchTweetsByLocation.py 

import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date

# Connect and authenticate to the twitter API
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# This program streams the latest tweets in the dayton, OH region. The user location displayed in the output is based on the 
# This class inherits from the Tweepy TweetListner class 
class TweetListener(StreamListener):
    ''' A listener handles tweets received from the stream and can print to stdout'''
 
    def __init__(self):
        super().__init__()
        self.neededTweets = 50 
        self.count = 0

    # This method typically passes the data to the on_status method, here I added a few lines to print the data to stdout. 
    def on_data(self,data):
        try:
            tweet_json = json.loads(data) # collects the tweets/data as json
            print(tweet_json['user']['screen_name'],": ",tweet_json['text'])
            print("Location: ",tweet_json['user']['location'], "\n")
        except TypeError:
            print("Something's wrong here... must be the JSON!")
        else: 
            self.count += 1 
            if (self.count == self.neededTweets):
                print("\n Done!")
                return False
            else:
                json.loads(data)
        return True

    
    def on_error(self, status):
        print(status)

def search_tweets_by_location():
    print("Most recent tweets in the Dayton OH region using the Streaming API:")
    print("Note: the location displayed is based on the user profile. \n")
    twitterStream = Stream(auth, TweetListener(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
   
    try: 
        twitterStream.filter(locations=[-84.311377,39.70185,-84.092938,39.920823])   # Stream tweets within the Dayton OH region specified by the bounded box.     
    except KeyboardInterrupt:
        print("stopped")
         

def main():
    search_tweets_by_location()        
    return

if __name__ == "__main__":
    main()

