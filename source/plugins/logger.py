from datetime import datetime

class Logger:
    __log = None

    @staticmethod
    def init():
        Logger.log = open('log.txt', mode='a+')

    @staticmethod
    def exit():
        Logger.log.close()

    @staticmethod
    def logMessage(message, room, user):
        Logger.log = open('log.txt', mode='a+')
        currentTime = str(datetime.now())
        parsedString = "(%s)[%s]: %s (%s)\n" % (room, currentTime, message, user)
        Logger.log.write(parsedString)
        Logger.log.close()

        print(parsedString, end="")
