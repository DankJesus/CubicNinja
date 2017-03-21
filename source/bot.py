import websocket, requests, json
import re # for regex
from importlib import reload

import config
class Bot(config.Config):
    challstr, ws, update, cfg = None, None, None, None
    availableCommands = []
    def __init__(self, cfg):
        self.ws = None
        Bot.cfg = cfg.db
        Bot.update = cfg.updateCommands

    @classmethod
    def connect(cls, addr):
        try:
            cls.ws = websocket.create_connection(addr)
        except Exception as e:
            print("Error connecting to Showdown: {}.".format(e))
        cls.ws.recv(); cls.ws.recv() # just get challstr now
        tempString = cls.ws.recv().split('|')
        if tempString[1].lower() == 'challstr':
            cls.challstr = '|'.join(tempString[2:])
        else:
            print('Unable to fetch challstr, exiting!')
            cls.exitBot()

    @classmethod
    def login(cls, Config):
        url = "http://play.pokemonshowdown.com/action.php"

        values = {'act': 'login',
                  'name': Config.showdown_login['username'],
                  'pass': Config.showdown_login['password'],
                  'challstr': cls.challstr}
        r = requests.post(url, data=values)
        response = json.loads(r.text[1:])
        assertion = response["assertion"]

        cls.ws.send("|/trn " + Config.showdown_login['nickname'] + ",0," + assertion)

        for n in Bot.cfg['commands']:
            Bot.availableCommands.append(n)
        # print(Bot.availableCommands)


    @classmethod
    def send(cls, message):
        cls.ws.send(message)

    @classmethod
    def sendMessage(cls, Command):
        if Command.pm == False: cls.ws.send('%s|%s' % (Command.room, Command.message))
        else: cls.ws.send('|/w %s, %s' % (Command.username, Command.message))

    @staticmethod
    def getUsername(message, count):
        tempCounter = 0
        firstBreak, lastBreak = 0, 0
        for i in range(0, len(message)):
            if message[i] == "|":
                tempCounter += 1
                if tempCounter == count:
                    firstBreak = i
                elif tempCounter == count + 1:
                    lastBreak = i
                    break
        message = message[firstBreak + 1:lastBreak].lower()
        re.sub(r'\W+', '', message)
        return message

    @staticmethod
    def getRoom(message, old):
        if message[0] == '>':
            n = message.index('\n')
            return message[1:n]
        return old.lower()

    @staticmethod
    def reloadCommands(cls, room):
        import commands
        reload(commands)
        import commands

        import config
        Bot.availablecommands = []
        Bot.cfg = Config.cfg.update('config.yaml')
        for n in Bot.cfg['commands']:
            Bot.availableCommands.append(n)

    @staticmethod
    def getMessage(message):
        firstBreak = 0
        tempCounter = 0
        for i in range(0, len(message)):
            if message[i] == "|":
                tempCounter += 1
                if tempCounter == 4:
                    firstBreak = i
                    break
        message = message[firstBreak + 1:]
        return message

    @classmethod
    def chatLoop(cls):
        import commands
        room = ''
        while True:
            rawMessage = cls.ws.recv()
            username = cls.getUsername(rawMessage, 3)
            room = cls.getRoom(rawMessage, room)
            message = cls.getMessage(rawMessage)
            isPM = False

            if rawMessage[:8].find('|pm|') != -1:
                isPM = True
                username = cls.getUsername(rawMessage, 2)

            n = message.find(' ')
            if n == -1: n = len(message)

            if message[1:n] in Bot.availableCommands and message[0] in Bot.cfg['config']['commmand_characters']:
                try:
                    x = commands.Command(message[1:n], message[n+1:], room, username, isPM)
                    func = getattr(commands, Bot.cfg['commands'][message[1:n]]['function'])
                    if Bot.cfg['commands'][message[1:n]]['function'] == 'reload': # reload only
                        if x.canUse:
                            cls.reloadCommands(cls, room)
                            cls.sendMessage(commands.Command('reload', 'Commands and config reloaded successfully!', room, username, isPM))
                            continue
                        else:
                            cls.sendMessage(commands.Command('reload', 'Invalid permissions.', room, username, True))
                    x = func(message[1:n], message[n+1:], room, username, isPM)
                    if x == None:
                        pass
                    elif not x.canUse:
                        cls.sendMessage(commands.Command(message[1:n], 'Invalid permissions.', room, username, True))
                    elif x.isEnabled == False:
                        cls.sendMessage(commands.Command(message[1:n], 'Command disabled.', room, username, True))
                    else:
                        print(x.command)
                        print(x.message)
                        cls.sendMessage(x)
                except Exception as e:
                    cls.sendMessage(commands.Command('say', 'Wew, an error. In case developers (minnow) are curious: ' + str(e), room, username, isPM))
                    pass
