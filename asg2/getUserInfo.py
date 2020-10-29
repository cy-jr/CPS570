#getUserInfo.py 

import const, sys, os
import tweepy
from tweepy import TweepError
 

auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_user_info(screenName): 
    
    
    try:
        sname = api.get_user(screenName)
        sn = [sname.id]
        users = api.lookup_users(user_ids=sn)    
    except TweepError:
        print('Could not find user')
         
    
    for user in users:
            print("\n Screen name: ", user.screen_name)
            print('User ID: ', user.id)
            print('Location: ', user.location)
            print('User Description: ', user.description)
            print("The number of Followers: ", user.followers_count)
            print('The number of friends: ', user.friends_count)
            print('THe number of tweets: ', user.statuses_count)
            print('User URL: ', user.url, "\n")

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
        get_user_info(name)

    print("Done!")
    return

if __name__ == "__main__":
    main()
