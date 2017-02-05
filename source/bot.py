import websocket, requests, json
from importlib import reload
import config
class Bot(config.Config):
    challstr = None
    ws = None
    update = None
    cfg = None
    availableCommands = []
    def __init__(self, cfg):
        self.ws = None
        Bot.cfg = cfg.db
        Bot.update = cfg.update

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
            print("Unable to fetch challstr, exiting!")
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
        print(Bot.availableCommands)


    @classmethod
    def sendMessage(cls, Command):
        if Command.pm == False: cls.ws.send('%s|%s' % (Command.room, Command.message))
        else: cls.ws.send('|/w %s, %s' % (Command.username, Command.message))
        print(cls.ws.recv())

    @staticmethod
    def getUsername(message, count):
        import re
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
        print(message[0])
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
        Bot.update('config.yaml', True)
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
        room = ''
        while True:
            rawMessage = cls.ws.recv()
            print(rawMessage)
            isPM = False
            username = cls.getUsername(rawMessage, 3)
            if rawMessage[:8].find('|pm|') != -1:
                isPM = True
                username = cls.getUsername(rawMessage, 2)
            room = cls.getRoom(rawMessage, room)
            message = cls.getMessage(rawMessage)

            n = message.find(' ')
            if n == -1:
                n = len(message)
            try:
                if message[1:n] in Bot.availableCommands and message[0] in Bot.cfg['config']['commmand_characters']:
                    import commands
                    if Bot.cfg['commands'][message[1:n]]['function'] == 'reload':
                        x = commands.Command(message[1:n], message[n+1:], room, username, isPM)
                        if x.isBad == True:
                            cls.sendMessage(commands.Command('reload', 'Invalid permissions.', room, username, isPM))
                            pass
                        else:
                            cls.reloadCommands(cls, room)
                            cls.sendMessage(commands.Command('reload', 'Commands and config reloaded successfully!', room, username, isPM))

                        continue
                    func = getattr(commands, Bot.cfg['commands'][message[1:n]]['function'])
                    x = func(message[1:n], message[n+1:], room, username, isPM)
                    print(x.isBad)
                    print(x.isEnabled)
                    if x.isBad == True:
                        cls.sendMessage(commands.Command('reload', 'Invalid permissions.', room, username, isPM))
                        pass
                    if x.isEnabled == False:
                        cls.sendMessage(commands.Command('reload', 'Command disabled.', room, username, isPM))
                        pass
                    else:
                        cls.sendMessage(x)

            except Exception as e:
                import commands
                cls.sendMessage(commands.Command('say', 'Wew, an error. Let\'s try to pass that. In case developers are curious: ' + str(e), room, username, isPM))
                pass
