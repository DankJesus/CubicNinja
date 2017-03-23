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
        self.weather_api = str(self.db['config']['connection_info']['weather']['api_key'])

        self.autojoin_rooms = self.db['config']['autojoin_rooms']

        self.whitelisted_users = self.db['config']['whitelisted_users']
        self.blacklisted_users = self.db['config']['blacklisted_users']

        self.commands = self.db['commands']
        print(self.commands)

    @staticmethod
    def updateCommands(filename):
        with open('config.yaml', 'w') as configFile:
            try:
                import bot
                yaml.dump(bot.Bot.cfg, configFile, default_flow_style=False)
            except yaml.YAMLError as e:
                print(e)
