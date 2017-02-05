import sys, os
import user
import subprocess

# import plugins.imgur
import config

class Command:
    def __init__(self, command = '', message = '', room = '', username='~minnow', pm = False):
        import bot
        self.isEnabled = True
        self.isBad = False

        if bot.Bot.cfg['commands'][command]['enabled'] == False:
            self.isEnabled = False

        elif user.canUseCommand(command, message, username[0], username[1:], bot.Bot.cfg) == False:
            self.isBad = True

        self.command = command
        self.message = message
        self.room = room
        self.rank = username[0]
        self.username = username[1:]
        self.pm = pm

def say(command, message, room, username, pm):
    escapeCharacters = ['$', '!', '/', '.', '+']
    if message[0] in escapeCharacters:
        message = message.translate(''.join(escapeCharacters))
    return Command(command, message, room, username, pm)

def pm(command, message, room, username, pm):
    import bot
    com = message.find(',')
    if com == -1:
        return Command(command, 'Usage: ' + bot.cfg['commands']['pm']['example'], room, username, pm)
    return Command(command, message[com + 1:], room, username[0] + message[:com], True)

def join(command, message, room, username, pm):
    return Command(command, '/join ' + message, room, username, pm)

def leave(command, message, room, username, pm):
    return Command(command, '/leave ' + message, room, username, pm)

def man(command, message, room, username, pm):
    manpage = subprocess.check_output(['man', message])
    print(manpage)
    n = str(manpage)
    n = n.replace("\\n", "")
    n = n.replace("", "")

    desc = n.find(");")

    f = n.find('IS ')
    if f == -1:
        f = 0

    return Command(command, '``' + n[f+4:desc+2].strip() + '``', room, username, pm)

def toggle(command, message, room, username, pm):
    import bot
    x = Command(command, message, room, username, pm)
    if x.isBad == True:
        return

    bot.Bot.cfg['commands'][message]['enabled'] ^= True
    bot.Bot.update('config.yaml', False)
    return Command(command, 'Command ``' + message + '`` is now: ' + str(bot.Bot.cfg['commands'][message]['enabled']), room, username, pm)

def roll(command, message, room, username, pm):
    from random import randrange
    num = 0
    try:
        num = randrange(0, int(message) + 1)
    except Exception as e:
        return Command(command, "Invalid number.", room, username, pm)
        pass
        return False

    return Command(command, str(num), room, username, pm)

def permission(command, message, room, username, pm):
    import bot

    comma = message.find(',')
    if comma == -1:
        return Command(command, 'Usage: ' + bot.Bot.cfg['commands'][command]['example'], room, username, pm)

    x = Command(command, message[:comma], room, username, pm)
    if x.isBad == True:
        return
    print(message[:comma])
    bot.Bot.cfg['commands'][message[:comma]]['rank'] = message[comma + 2:].strip()
    bot.Bot.update('config.yaml', False)
    return Command(command, 'Command ' + message[:comma] + ' is now: ' + str(bot.Bot.cfg['commands'][message[:comma]]['rank']), room, username, pm)
