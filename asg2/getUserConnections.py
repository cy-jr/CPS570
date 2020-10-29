# getUserConnections.py 

import const, json, sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.streaming import StreamListener 
from datetime import date
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_user_connections(screenName):
    try:
        try:
            sname = api.get_user(screenName)
            sn = [sname.id]
            users = api.lookup_users(user_ids=sn)    
        except TweepError:
            print('Could not find user')
        i = 1
        j = 1
        for user in users:
            print("User: ", user.screen_name)
            print("Friends: ", user.friends_count)
            try:
                for friend in tweepy.Cursor(api.friends, user.screen_name).items(20):
                    print (i," ", friend.screen_name)
                    i += 1
            except TweepError as error:
                print(str(error))
            try: 
                for friend in tweepy.Cursor(api.friends, user.screen_name).items(20):
                    print (j," ", friend.screen_name)
                    j += 1
            except TweepError as error:
                print(str(error))
            print("\n")
        
        for user in users:
            
            print("Followers: ", user.followers_count)

            for ff in tweepy.Cursor(api.followers, user.screen_name).items(20):
                print (" ", ff.screen_name)
        print("\n")
    except KeyboardInterrupt:
        print("\n Program stopped!")
        sys.exit()
        


def main():
    usernames = []
    if len(sys.argv) < 2:
        print("Error: Insufficient arguments \n Correct Usage: <interpreter> <programname>.py <file_containing_user_names>")
        sys.exit()
    filename = sys.argv[1]
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
        get_user_connections(name)

    print("Done!")
    return

if __name__ == "__main__":
    main()


