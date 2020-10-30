# getUserConnections.py 

import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date

# Connect and authenticate to the twitter API
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# this function obtains the friends and followers for a given screen name
def get_user_connections(screenName):
    try:
        try:
            sname = api.get_user(screenName)    # Uses the given screen name to get the user object 
        except TweepError:
            print('Could not find user screen name')
            return False
        sn = [sname.id]     # Gets user id from the user object 
        try:
            users = api.lookup_users(user_ids=sn)   # gets user object from the user id 
        except TweepError as e:
            print(str(e))
            print('Could not find user id')
            return False
            
        i = 1
        j = 1
        
        # obtain the users friends
        for user in users:
            print("User: ", user.screen_name)
            print("Friends: ", user.friends_count)
            try:
                for friend in tweepy.Cursor(api.friends, user.screen_name).items(20):
                    print (i," ", friend.screen_name)
                    i += 1
            except TweepError as error:
                print(str(error))           
            print("\n")
        
        # obtain the user's followers 
        for user in users:
            try:
                print("Followers: ", user.followers_count)
                for ff in tweepy.Cursor(api.followers, user.screen_name).items(20):
                    print (j," ", ff.screen_name)
                    j += 1
                print("\n")
            except TweepError as e:
                print(str(e))
    except KeyboardInterrupt:
        print("\n Program stopped!")
        sys.exit()
        


def main():

    # Program accepts a file containing list of user screen names
    usernames = []
    if len(sys.argv) < 2:
        print("Error: Insufficient arguments \n Correct Usage: <interpreter> <programname>.py <file_containing_user_names>")
        sys.exit()
    filename = sys.argv[1]
    # file handler
    try:
        with open(filename) as file:
            for line in file:
                line = line.strip()
                usernames.append(line)
    except IOError as error:
        print(error)
        print('Error 404(-ish): file non-existent')
        sys.exit(1)
    # print(usernames)
    
    for name in usernames:
        if(get_user_connections(name) == False): 
            break
    print("Done!")
    return

if __name__ == "__main__":
    main()


