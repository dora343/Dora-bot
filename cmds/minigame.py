import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import os

class Minigame(Cog_Extension):
    counter = 0
    num = 194052
    playercount = 0
    # @commands.command()
    # async def illuminati(self, ctx):
    #     pic = discord.File(jdata['illuminati_pic'])
    #     await ctx.send(file=pic)

    file_path = os.path.dirname(__file__)
    
    def isValidPlayer(self, data, playerid):
        # 0: valid
        # 1: missing players dict
        # 2: missing player profile

        if (data.get('players', -1) == -1): return 1
        if (data.get('players').get(playerid, -1) == -1): return 2

        return 0

    async def readData(self, ctx):
        data = dict()

        with open(self.file_path + '/minigame-data.json','r', encoding='utf-8') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.decoder.JSONDecodeError:
                await ctx.send('invalid JSON detected')

        return data

    async def writeData(self, ctx, data):
        with open(self.file_path + '/minigame-data.json','w', encoding='utf-8') as jsonfile:
                try:
                    json.dump(data, jsonfile, indent=2)
                except json.decoder.JSONDecodeError:
                    await ctx.send('invalid JSON detected')
        
        return 0

    @commands.command(name='createAccount',aliases=['register'])
    async def createAccount(self, ctx):
        
        data = await self.readData(ctx)

        # check if this user exists
        x = data.get('players', -3)

        if (x == -3):
            await ctx.send('missing players dict, creating...')
            data['players'] = {}
            x = data.get('players')
            
        x = x.get(str(ctx.author.id), -2)

        if (x != -2):
            await ctx.send('You have already registered.')
            return 0

        if (x == -2):
            # create new profile for this player
            await ctx.send('creating player profile...')
            template_player_profile = {
                'name': ctx.author.name, 
                'status': 'active', 
                'currency': 100
            }

            data['players'][str(ctx.author.id)] = template_player_profile

            self.playercount = data['player-count']
            self.playercount = self.playercount + 1
            data['player-count'] = self.playercount

            await self.writeData(ctx, data)

            await ctx.send('player profile created.')
            await ctx.send(F'Current player count: {self.playercount}')

    @commands.command(name='deleteAccount',aliases=['quitgame'])
    async def deleteAccount(self, ctx):
        data = await self.readData(ctx)

        # check if this user exists
        x = data.get('players', -3)

        if (x == -3):
            await ctx.send('missing players dict')
            return 0
            
        x = x.get(str(ctx.author.id), -2)

        if (x == -2):
            await ctx.send('You are not registered.')
            return 0

        if (x != -2):
            if (data['players'].pop(str(ctx.author.id), -1) == -1):
                await ctx.send('error in removing player profile')
                return 0

            self.playercount = data['player-count']
            self.playercount = self.playercount - 1
            data['player-count'] = self.playercount

            await self.writeData(ctx, data)

            await ctx.send('player profile deleted.')
            await ctx.send(F'Current player count: {self.playercount}')
            
    @commands.command(name='getCurrency',aliases=['token'])
    async def getCurrency(self, ctx):
        data = await self.readData(ctx)

        currency = data.get('players', {}).get(str(ctx.author.id), {}).get('currency', -1)
        
        if (currency == -1):
            await ctx.message.reply('You are not registered.')
            return 0

        await ctx.message.reply(F'You have {currency} token(s).')

    @commands.command(name='addCurrency',aliases=['addtoken'])
    async def addCurrency(self, ctx, amount):
        if (ctx.author.id != 400941378395439104):
            await ctx.message.reply('You do not have permission to do so.')
            return 0
        
        flag = True
        try:
            int(amount)
        except ValueError:
            flag = False
        currency = 0
        if (flag): 
            await ctx.message.reply('Invalid amount.')
            return 0 

        data = await self.readData(ctx)

        if (self.isValidPlayer(data,str(ctx.author.id) != 0)):
            await ctx.message.reply('invalid player')
            return 0

        currency = data['players'][str(ctx.author.id)]['currency']
        old_currency = currency
        currency = currency + amount
        data['players'][str(ctx.author.id)]['currency'] = currency

        await self.writeData(ctx, data)
        await ctx.message.reply(F'You have {currency} ({old_currency} + {amount}) token(s).')
        
        








def setup(bot):
    bot.add_cog(Minigame(bot))
