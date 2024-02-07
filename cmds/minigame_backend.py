
from core.classes import Cog_Extension
import json
import random
import os

class MinigameBackend(Cog_Extension):

    def __init__(self, bot):
        super().__init__(bot)


        self._file_path = os.path.dirname(__file__)

        self._OK_STATUS = 200
        self._GAMBLE_SUCCESS = 201
        self._GAMBLE_FAIL = 202
        # error status code:
        # 401: invalid JSON
        # 402: player profile not found
        # 403: invalid value
        # 404: players object not found
        # 405: player profile already exist
        # 406: bet is zero or negative
        # 407: insufficient token
        # 408: resurrect with non-zero token
        # 499: Unexpected error
        self._JSON_ERROR = 401
        self._PLAYER_NOT_FOUND_ERROR = 402
        self._VALUE_ERROR = 403
        self._PLAYERS_DICT_NOT_FOUND_ERROR = 404
        self._PLAYER_ALREADY_EXIST_ERROR = 405
        self._NON_POSITIVE_BET_ERROR = 406
        self._INSUFFICIENT_TOKEN_ERROR = 407
        self._RESURRECT_WITH_TOKEN_ERROR = 408
        self._UNEXPECTED_ERROR = 499
    
    def readData(self):
        data = dict()

        with open(self._file_path + '/minigame-data.json','r', encoding='utf-8') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.decoder.JSONDecodeError:
                return self._JSON_ERROR

        return data

    def writeData(self, data):
        with open(self._file_path + '/minigame-data.json','w', encoding='utf-8') as jsonfile:
                try:
                    json.dump(data, jsonfile, indent=2)
                except json.decoder.JSONDecodeError:
                    return self._JSON_ERROR
        
        return self._OK_STATUS

    def isValidPlayer(self, playerid):
        data = self.readData()
        if (data.get('players', -1) == -1): return self._PLAYERS_DICT_NOT_FOUND_ERROR
        if (data.get('players').get(str(playerid), -1) == -1): return self._PLAYER_NOT_FOUND_ERROR

        return self._OK_STATUS

    def createAccount(self, targetid, name):

        data = self.readData()
        if (data.get('players', -1) == -1):
            # create players dict
            data['players'] = dict()

        if (data.get('players').get(str(targetid), -1) != -1): return self._PLAYER_ALREADY_EXIST_ERROR
            
        template_player_profile = {
            'name': name, 
            'status': 'active',
            'currency': 100,
            'resurrection-count': 0,
            'highest-token': 100
        }

        data['players'][str(targetid)] = template_player_profile
        self.playercount = data['player-count']
        self.playercount = self.playercount + 1
        data['player-count'] = self.playercount

        self.writeData(data)
        return self._OK_STATUS

    def deleteAccount(self, targetid):

        status = self.isValidPlayer(targetid)
        if (status != self._OK_STATUS):
            return status


        data = self.readData()
        if (data['players'].pop(str(targetid), 499) == 499):
            return self._UNEXPECTED_ERROR
        self.playercount = data['player-count']
        self.playercount = self.playercount - 1
        data['player-count'] = self.playercount

        self.writeData(data)
        return self._OK_STATUS

    def getToken(self, targetid):

        if (self.isValidPlayer(str(targetid)) != self._OK_STATUS):
            return self._PLAYER_NOT_FOUND_ERROR, 0
        
        data = self.readData()
        return self._OK_STATUS, data.get('players').get(str(targetid)).get('currency')

    def addToken(self, amount, targetid):
        flag = True
        try:
            int(amount)
        except ValueError:
            flag = False
        currency = 0
        if (not(flag)): 
            return self._VALUE_ERROR


        data = self.readData()

        if (self.isValidPlayer(str(targetid)) != self._OK_STATUS):
            return self._PLAYER_NOT_FOUND_ERROR

        currency = data['players'][str(targetid)]['currency']
        currency = currency + int(amount)
        data['players'][str(targetid)]['currency'] = currency
        if (data.get('players').get(str(targetid)).get('highest-token', -1) == -1):
            # create highest-token
            data['players'][str(targetid)]['highest-token'] = 0

        highest = data['players'][str(targetid)]['highest-token']
        if (currency>highest):
            data['players'][str(targetid)]['highest-token'] = currency
        self.writeData(data)
        return self._OK_STATUS

    def gamble(self, amount, targetid):
        data = self.readData()
        currency = data.get('players', {}).get(str(targetid), {}).get('currency', -1)
        
        if (currency == -1):
            return self._PLAYER_NOT_FOUND_ERROR, 0

        amount = int(amount)
        if (amount <= 0):
            return self._NON_POSITIVE_BET_ERROR, 0

        if (amount > int(currency)):
            return self._INSUFFICIENT_TOKEN_ERROR, 0

        odds = 0.5 * 1000

        temp = random.randrange(1, 1000)
        
        if (temp > odds):
            amount = -1*int(amount) 
        

        status = self.addToken(str(-1*amount), targetid)
        if status == 1: 
            return self._VALUE_ERROR, 0

        if status == 2:
            return self._PLAYER_NOT_FOUND_ERROR, 0

        if (temp > odds): return self._OK_STATUS, self._GAMBLE_SUCCESS
        if (temp <= odds): return self._OK_STATUS, self._GAMBLE_FAIL

    def resurrect(self, targetid):
        if (self.isValidPlayer(str(targetid)) != self._OK_STATUS):
            return self._PLAYER_NOT_FOUND_ERROR, 0
            
        status = self.getToken(targetid)

        if (status[1] != 0):
            return self._RESURRECT_WITH_TOKEN_ERROR, 0

        data = self.readData()
        resurrect_token = data['resurrect-token']
        status = self.addToken(resurrect_token, targetid)
        
        if (status != self._OK_STATUS): return


        data = self.readData()

        # create entry if resurrection-count entry does not exist
        if data.get('players').get(str(targetid)).get('resurrection-count', -1) == -1:
            data['players'][str(targetid)]['resurrection-count'] = 0

        data['players'][str(targetid)]['resurrection-count'] = data['players'][str(targetid)]['resurrection-count'] + 1
        self.writeData(data)

        return self._OK_STATUS, resurrect_token

    def transferToken(self, srcid, dstid, amount):
        # data = await self.readData(ctx)
        pass

def setup(bot):
    pass