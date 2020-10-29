# searchTweetsByLocation.py 

import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class TweetListener(StreamListener):
    ''' A listener handles tweets received from the stream and can print to stdout'''
 
    def __init__(self):
        super().__init__()
        self.neededTweets = 5 
        self.count = 0
    
    def on_data(self,data):
        try:
            tweet_json = json.loads(data)
            print(tweet_json['user']['screen_name'],": ",tweet_json['text'])
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

    twitterStream = Stream(auth, TweetListener(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
   
    try: 
        twitterStream.filter(locations=[-84.311377,39.70185,-84.092938,39.920823])        
    except KeyboardInterrupt:
        print("stopped")
         

def main():
    search_tweets_by_location()        
    return

if __name__ == "__main__":
    main()

