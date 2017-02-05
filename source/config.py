# Settings
import yaml
class Config:
    def __init__(self, filename):
        with open(filename, 'r') as configFile:
            try:
                self.db = yaml.load(configFile)
            except yaml.YAMLError as e:
                print(e)
                print("RIP")
                raise

        self.showdown_login = self.db['config']['connection_info']['showdown']
        self.imgur_login = self.db['config']['connection_info']['imgur']
        self.twitter_login = self.db['config']['connection_info']['twitter']

        self.autojoin_rooms = self.db['config']['autojoin_rooms']

        self.whitelisted_users = self.db['config']['whitelisted_users']
        self.blacklisted_users = self.db['config']['blacklisted_users']

        self.commands = self.db['commands']
        print(self.commands)

    def update(self, filename):
        with open(filename, 'w') as configFile:
            try:
                import bot
                yaml.dump(bot.Bot.cfg, configFile, default_flow_style=False)
            except yaml.YAMLError as e:
                print(e)
