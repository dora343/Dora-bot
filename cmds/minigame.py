import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import os
import typing as t

class Minigame(Cog_Extension):
    counter = 0
    num = 194052
    playercount = 0
    # @commands.command()
    # async def illuminati(self, ctx):
    #     pic = discord.File(jdata['illuminati_pic'])
    #     await ctx.send(file=pic)

    file_path = os.path.dirname(__file__)

    OK_STATUS = 200
    GAMBLE_SUCCESS = 201
    GAMBLE_FAIL = 202
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
    __JSON_ERROR = 401
    __PLAYER_NOT_FOUND_ERROR = 402
    __VALUE_ERROR = 403
    __PLAYERS_DICT_NOT_FOUND_ERROR = 404
    __PLAYER_ALREADY_EXIST_ERROR = 405
    __NON_POSITIVE_BET_ERROR = 406
    __INSUFFICIENT_TOKEN_ERROR = 407
    __RESURRECT_WITH_TOKEN_ERROR = 408
    __UNEXPECTED_ERROR = 499

    async def handleError(self, ctx, status):
        if (status == self.__PLAYER_NOT_FOUND_ERROR):
            await ctx.message.reply('You are not registered.')
            return status

        if (status == self.__VALUE_ERROR):
            await ctx.message.reply('Invalid amount')
            return

        if (status == self.__PLAYERS_DICT_NOT_FOUND_ERROR):
            await ctx.message.reply('missing player dict')
            return status

        if (status == self.__PLAYER_ALREADY_EXIST_ERROR):
            await ctx.message.reply('You are already registered')
            return status
        
        if (status == self.__NON_POSITIVE_BET_ERROR):
            await ctx.message.reply('You cannot place zero/negative bet.')
            return status

        if (status == self.__INSUFFICIENT_TOKEN_ERROR):
            await ctx.message.reply('You do not have enough tokens.')
            return status

        if (status == self.__INSUFFICIENT_TOKEN_ERROR):
            await ctx.message.reply('You can only resurrect with 0 token.')
            return status

        if (status == self.__UNEXPECTED_ERROR):
            await ctx.message.reply('something broke unexpectedly')    
            return status

        return status    



    def readData(self):
        data = dict()

        with open(self.file_path + '/minigame-data.json','r', encoding='utf-8') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.decoder.JSONDecodeError:
                return self.__JSON_ERROR

        return data

    def writeData(self, data):
        with open(self.file_path + '/minigame-data.json','w', encoding='utf-8') as jsonfile:
                try:
                    json.dump(data, jsonfile, indent=2)
                except json.decoder.JSONDecodeError:
                    return self.__JSON_ERROR
        
        return self.OK_STATUS

    def isValidPlayer(self, playerid):
        data = self.readData()
        if (data.get('players', -1) == -1): return self.__PLAYERS_DICT_NOT_FOUND_ERROR
        if (data.get('players').get(str(playerid), -1) == -1): return self.__PLAYER_NOT_FOUND_ERROR

        return self.OK_STATUS

    def createAccount(self, targetid, name):

        data = self.readData()
        if (data.get('players', -1) == -1):
            # create players dict
            data['players'] = dict()

        if (data.get('players').get(str(targetid), -1) != -1): return self.__PLAYER_ALREADY_EXIST_ERROR
            
        template_player_profile = {
            'name': name, 
            'status': 'active',
            'currency': 100,
            'resurrection-count': 0 
        }

        data['players'][str(targetid)] = template_player_profile
        self.playercount = data['player-count']
        self.playercount = self.playercount + 1
        data['player-count'] = self.playercount

        self.writeData(data)
        return self.OK_STATUS

    def deleteAccount(self, targetid):

        status = self.isValidPlayer(targetid)
        if (status != self.OK_STATUS):
            return status


        data = self.readData()
        if (data['players'].pop(str(targetid), 499) == 499):
            return self.__UNEXPECTED_ERROR
        self.playercount = data['player-count']
        self.playercount = self.playercount - 1
        data['player-count'] = self.playercount

        self.writeData(data)
        return self.OK_STATUS

    def getToken(self, targetid):

        if (self.isValidPlayer(str(targetid)) != self.OK_STATUS):
            return self.__PLAYER_NOT_FOUND_ERROR, 0
        
        data = self.readData()
        return self.OK_STATUS, data.get('players').get(str(targetid)).get('currency')

    def addToken(self, amount, targetid):
        flag = True
        try:
            int(amount)
        except ValueError:
            flag = False
        currency = 0
        if (not(flag)): 
            return self.__VALUE_ERROR


        data = self.readData()

        if (self.isValidPlayer(str(targetid)) != self.OK_STATUS):
            return self.__PLAYER_NOT_FOUND_ERROR

        currency = data['players'][str(targetid)]['currency']
        currency = currency + int(amount)
        data['players'][str(targetid)]['currency'] = currency
        if (data.get('players').get(str(targetid), -1) == -1):
            # create highest-token
            data['players'][str(targetid)]['highest-token'] = dict()
        self.writeData(data)
        return self.OK_STATUS

    def gamble(self, amount, targetid):
        data = self.readData()
        currency = data.get('players', {}).get(str(targetid), {}).get('currency', -1)
        
        if (currency == -1):
            return self.__PLAYER_NOT_FOUND_ERROR, 0

        amount = int(amount)
        if (amount <= 0):
            return self.__NON_POSITIVE_BET_ERROR, 0

        if (amount > int(currency)):
            return self.__INSUFFICIENT_TOKEN_ERROR, 0

        odds = 0.5 * 1000

        temp = random.randrange(1, 1000)
        
        if (temp > odds):
            amount = -1*int(amount) 
        

        status = self.addToken(str(-1*amount), targetid)
        if status == 1: 
            return self.__VALUE_ERROR, 0

        if status == 2:
            return self.__PLAYER_NOT_FOUND_ERROR, 0

        if (temp > odds): return self.OK_STATUS, self.GAMBLE_SUCCESS
        if (temp <= odds): return self.OK_STATUS, self.GAMBLE_FAIL

    def resurrect(self, targetid):
        if (self.isValidPlayer(str(targetid)) != self.OK_STATUS):
            return self.__PLAYER_NOT_FOUND_ERROR
            
        status = self.getToken(targetid)

        if (status[1] != 0):
            return self.__RESURRECT_WITH_TOKEN_ERROR, 0

        data = self.readData()
        resurrect_token = data['resurrect-token']
        status = self.addToken(resurrect_token, targetid)
        
        if (status != self.OK_STATUS): return


        data = self.readData()

        # create entry if resurrection-count entry does not exist
        if data.get('players').get(str(targetid)).get('resurrection-count', -1) == -1:
            data['players'][str(targetid)]['resurrection-count'] = 0

        data['players'][str(targetid)]['resurrection-count'] = data['players'][str(targetid)]['resurrection-count'] + 1
        self.writeData(data)

        return self.OK_STATUS, resurrect_token

    def transferToken(self, srcid, dstid, amount):
        # data = await self.readData(ctx)
        pass


    @commands.command(name='createAccount',aliases=['register'])
    async def createAccountCommand(self, ctx):
        
        status = self.createAccount(ctx.author.id, ctx.author.name)
        await self.handleError(ctx, status)
        if (status != self.OK_STATUS): return
        
        await ctx.message.reply('player profile created.')

    @commands.command(name='deleteAccount',aliases=['quitgame'])
    async def deleteAccountCommand(self, ctx):
        
        status = self.deleteAccount(ctx.author.id)
        await self.handleError(ctx, status)
        if (status != self.OK_STATUS): return

        await ctx.message.reply('Your account is deleted.')
            
    @commands.command(name='getToken',aliases=['token'])
    async def getTokenCommand(self, ctx, targetid:t.Optional[str]):

        if (not targetid):
            targetid = ctx.author.id

        status = self.getToken(targetid)
        await self.handleError(ctx, status[0])
        if (status[0] != self.OK_STATUS): return
  
        await ctx.message.reply(F'You have {status[1]} tokens.')
        if (int(status[1]) == 0):
            await ctx.send('Use .revive to start again.')

    @commands.command(name='addCurrency',aliases=['addtoken'])
    async def addTokenCommand(self, ctx, amount, targetid:t.Optional[str]):
        if (ctx.author.id != 400941378395439104):
            await ctx.message.reply('You do not have permission to do so.')
            return 0
        
        if (not targetid):
            targetid = ctx.author.id

        status = self.addToken(amount, targetid)
        await self.handleError(ctx, status)
        if (status != self.OK_STATUS): return

        await ctx.message.reply(F'Added {amount} tokens.')
        
    @commands.command(name='gamble',aliases=['g'])
    async def gambleCommand(self, ctx, amount:t.Optional[str]):
        if not amount:
            await ctx.message.reply('Please specify your bet.')
            return 0
        
        status = self.gamble(amount, ctx.author.id)
        await self.handleError(ctx, status[0])
        if (status[0] != self.OK_STATUS): return

        data = self.readData()
        currency = data.get('players', {}).get(str(ctx.author.id), {}).get('currency', -1)

        if (status[1] == self.GAMBLE_SUCCESS):
            await ctx.message.reply(F'Success! **{amount} tokens** have been added to your account.\nYou have {currency} tokens.')
            return 0

        if (status[1] == self.GAMBLE_FAIL):
            await ctx.message.reply(F'Unlucky! **{amount} tokens** have been taken from your account.\nYou have {currency} tokens.')
            if (int(currency) == 0):
                await ctx.send('Use .revive to start again.')
            
            return 0

    @commands.command(name='resurrect',aliases=['revive','復活'])
    async def resurrectCommand(self, ctx):
        status = self.resurrect(ctx.author.id)
        await self.handleError(ctx, status[0])
        if (status[0] != self.OK_STATUS): return
        resurrect_token = status[1]
        await ctx.message.reply(F'You have resurrected. Added {resurrect_token} tokens to your account.')

    # @commands.command(name='getLoginBonus',aliases=['revive','復活'])
    # async def getLoginBonus(self, ctx):

    





def setup(bot):
    bot.add_cog(Minigame(bot))
