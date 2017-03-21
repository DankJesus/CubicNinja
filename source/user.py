ranks = {'!': -1, ' ': 0, '+': 1, '%': 2, '@': 3, '&': 4, '#': 5, '~': 6, '_': 7}

def compareRank(rank1, rank2):
    print(rank1)
    print(rank2)
    return ranks[rank1] >= ranks[rank2]

def isWhitelisted(user, whitelisted_users):
    return user in whitelisted_users

def canUseCommand(command, message, user, username, Config):
    return isWhitelisted(username, Config['config']['whitelisted_users']) or compareRank(user[0], Config['commands'][command]['rank'])
