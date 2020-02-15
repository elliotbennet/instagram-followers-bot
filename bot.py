from InstagramAPI import InstagramAPI
from time import sleep
import random
import config

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class InstagramBot:

    def __init__(self):
        if config.username == '' or config.password == '':
            print('Enter a username and password in ./config.py')
            return
        self.api = InstagramAPI(config.username, config.password)
        self.enabled = True
        self.following_users = []
        self.users_list = []

    def follow_users(self, unfollow=False):
        api = self.api
        api.login()
        api.getSelfUsersFollowing() # Get users which you are following
        result = api.LastJson
        for user in result['users']:
            self.following_users.append(user['pk'])
        for user in self.users_list:
            if not user['pk'] in self.following_users: # if new user is not in your following users                   
                print(bcolors.OKGREEN + '[+]' + bcolors.ENDC + ' Following ' + bcolors.OKBLUE + '@' + user['username'] + bcolors.ENDC)
                api.follow(user['pk'])
                if unfollow:
                    self.unfollow_random_user()
                sleep(300)
            else:
                print(bcolors.WARNING + '[*]' + bcolors.ENDC + ' Already following ' + bcolors.OKBLUE + '@' + user['username'] + bcolors.ENDC)

    def get_user_followers(self, target):
        api = self.api
        api.login()
        api.getUserFollowers(target)
        result = api.LastJson
        self.users_list = []

        if 'users' in result:
            for user in result['users']:
                self.users_list.append({'pk':user['pk'], 'username':user['username']})

        print(bcolors.WARNING + '[*]' + bcolors.ENDC + ' Found ' + bcolors.OKGREEN + str(len(self.users_list)) + bcolors.ENDC + ' users to follow')

    def unfollow_random_user(self):
        api = self.api
        api.login()
        api.getSelfUsersFollowing()
        result = api.LastJson

        if len(result['users']) <= len(config.unfollow_blacklist):
            return

        random_user = random.choice(result['users'])
        while random_user['username'] in config.unfollow_blacklist:
            random_user = random.choice(result['users'])

        print(bcolors.FAIL + '[-]' + bcolors.ENDC + ' Unfollowing ' + bcolors.OKBLUE + '@' + random_user['username'] + bcolors.ENDC)
        api.unfollow(random_user['pk'])


bot = InstagramBot()

while bot.enabled:
    bot.get_user_followers(target=config.target)
    bot.follow_users(unfollow=config.unfollow)
    sleep(300)

