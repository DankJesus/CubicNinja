from plugins.imgur import Imgur
from plugins.logger import Logger

import threading

from bot import Bot
from config import Config

Settings = Config('config.yaml')
CubicNinja = Bot(Settings)
CubicNinja.connect('ws://sim.smogon.com:8000/showdown/websocket')
CubicNinja.login(Settings)
for i in Settings.autojoin_rooms:
    CubicNinja.send('|/join ' + i)

ChatLoop = threading.Thread(target = CubicNinja.chatLoop)
ChatLoop.start()
