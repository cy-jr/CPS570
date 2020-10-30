#getUserInfo.py 

import const, sys, os
import tweepy
from tweepy import TweepError

# Connect and authenticate to the twitter API
auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
auth.set_access_token(const.ACCESS_TOKEN, const.ACESS_TOKEN_SECRET)
api = tweepy.API(auth)

# This function obtains some information about a user given the users's screen name
def get_user_info(screenName):
    try:    
        try:
            sname = api.get_user(screenName)    # Uses the given screen name to get the user object 
        except TweepError:
            print('Could not find user screen name')    # User not found exception handler
            return False 
        sn = [sname.id] # obtains the user id from the user object
        try:
            users = api.lookup_users(user_ids=sn)   # performs another lookup based on the user id.         
        except TweepError as e:
            print(str(e))
            print('Could not find user id')
            return False
        
        
        # if user information is found, print the following fields. 
        for user in users:
                print("\n Screen name: ", user.screen_name)
                print('User ID: ', user.id)
                print('Location: ', user.location)
                print('User Description: ', user.description)
                print("The number of Followers: ", user.followers_count)
                print('The number of friends: ', user.friends_count)
                print('THe number of tweets: ', user.statuses_count)
                print('User URL: ', user.url, "\n")
    except KeyboardInterrupt:
        print("\n Program stopped!")

def main():
    # Program accepts a file containing list of user screen names
    usernames = []     # list for storing screen names
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
    
    # iterate through list to obtain and print user info
    for name in usernames:
        try:
            if (get_user_info(name) == False):
                break
        except KeyboardInterrupt:
            print("\nProgram Stopped!")

    print("Done!")
    return

if __name__ == "__main__":
    main()
