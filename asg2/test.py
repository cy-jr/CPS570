# test.py 

import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth)

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
    
def main():
    get_user_info('twitter')
    # get_user_connections('sammiesaliu')
    # searchTweetsByLocation()
    # searchTweetsByKeyword()
    return
 
    
    

def get_user_info(screenName): 
    # sn = [screenName]
    sname = api.get_user(screenName)
    print(sname)
    sys.exit()
    try:
        users = api.lookup_users(screen_names=sname.id)    
    except TweepError:
        print('Could not find user')
    sys.exit()
    for user in users:
            print("\n S creen name: ", user.screen_name)
            print('User ID: ', user.id)
            print('Location: ', user.location)
            print('User Description: ', user.description)
            print("The number of Followers: ", user.followers_count)
            print('The number of friends: ', user.friends_count)
            print('THe number of tweets: ', user.statuses_count)
            print('User URL: ', user.url)

def get_user_connections(screenname):
    sn = [screenname]
    users = api.lookup_users(screen_name=sn[0])
   
    for user in users:
        print("User: ", user.screen_name)
        print("Friends: ", user.friends_count)

        for friend in tweepy.Cursor(api.friends, user.screen_name).items(20):
            print (" ", friend.screen_name)
    print("\n")
    for user in users:
        
        print("Followers: ", user.followers_count)

        for ff in tweepy.Cursor(api.followers, user.screen_name).items(20):
            print (" ", ff.screen_name)
    print("\n")




    """
    search_words = "Ohio" and "weather"
    current_date = date.today()  #"2020-10-25"
    date_since = current_date.strftime("%Y-%m-%d")

    tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(3)
    for tweet in tweets:
        print(tweet.user.screen_name,":  ",tweet.text)        
        print(tweet.user.location, "\n")
    """
def searchTweetsByKeyword():
    twitterStream = Stream(auth, TweetListener(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    try: 
        twitterStream.filter(track=['Ohio','Weather'])
    except KeyboardInterrupt:
        print("stopped")
        

def searchTweetsByLocation():

    twitterStream = Stream(auth, TweetListener(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
   
    try: 
        twitterStream.filter(locations=[-84.311377,39.70185,-84.092938,39.920823])
        # print(tweets['text'],'\n')
    except KeyboardInterrupt:
        print("stopped")
    

 

    

if __name__ == "__main__":
    main()

