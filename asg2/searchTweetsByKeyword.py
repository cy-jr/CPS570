#searchTweetsByKeyword.py 
import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date

# Connect and authenticate to the twitter API
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# This class inherits from the Tweepy TweetListner class 
class TweetListener(StreamListener):
    ''' A listener handles tweets received from the stream and can print to stdout'''
 
    def __init__(self):
        super().__init__()
        self.neededTweets = 50 
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
                print("\nDone!")
                return False
            else:
                json.loads(data)
        return True

    
    def on_error(self, status):
        print(status)

# This method search tweets with the given keywords using the Stream API
def search_tweets_by_keyword_stream():
    # an object of the Tweet Listner object class
    twitterStream = Stream(auth, TweetListener(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    try: 
        twitterStream.filter(track=['Ohio','Weather']) # Streams tweets with the specified key words
    except KeyboardInterrupt:
        print("\n Program stopped!")

# This method search tweets with the given keywords using the Search API
def search_tweets_by_keywords_search():
    search_words = "Ohio" and "weather"
    current_date = date.today()  #"2020-10-25"
    date_since = current_date.strftime("%Y-%m-%d")
    try:
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(50)  
        for tweet in tweets:
            print(tweet.user.screen_name,":  ",tweet.text)        
            print(tweet.user.location, "\n")
    except KeyboardInterrupt:
        print("\nProgram Stopped!")

def main():
    print('Using the Search API:')
    search_tweets_by_keywords_search()

    print('Using the Stream API')
    search_tweets_by_keyword_stream()
    print('')     

    return

if __name__ == "__main__":
    main()
