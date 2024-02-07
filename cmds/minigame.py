
from discord.ext import commands
from cmds.minigame_backend import MinigameBackend
import typing as t
import re
class Minigame(MinigameBackend):
    # file_path = os.path.dirname(__file__)

    def __init__(self, bot):
        MinigameBackend.__init__(self, bot)

    async def handleError(self, ctx, status):
        if (status == self._PLAYER_NOT_FOUND_ERROR):
            await ctx.message.reply('You are not registered.')
            return status

        if (status == self._VALUE_ERROR):
            await ctx.message.reply('Invalid amount')
            return

        if (status == self._PLAYERS_DICT_NOT_FOUND_ERROR):
            await ctx.message.reply('missing player dict')
            return status

        if (status == self._PLAYER_ALREADY_EXIST_ERROR):
            await ctx.message.reply('You are already registered')
            return status
        
        if (status == self._NON_POSITIVE_BET_ERROR):
            await ctx.message.reply('You cannot place zero/negative bet.')
            return status

        if (status == self._INSUFFICIENT_TOKEN_ERROR):
            await ctx.message.reply('You do not have enough tokens.')
            return status

        if (status == self._INSUFFICIENT_TOKEN_ERROR):
            await ctx.message.reply('You can only resurrect with 0 token.')
            return status

        if (status == self._UNEXPECTED_ERROR):
            await ctx.message.reply('something broke unexpectedly')    
            return status

        return status    



    


    @commands.command(name='createAccount',aliases=['register'])
    async def createAccountCommand(self, ctx):
        
        status = self.createAccount(ctx.author.id, ctx.author.name)
        await self.handleError(ctx, status)
        if (status != self._OK_STATUS): return
        
        await ctx.message.reply('player profile created.')

    @commands.command(name='deleteAccount',aliases=['quitgame'])
    async def deleteAccountCommand(self, ctx):
        
        status = self.deleteAccount(ctx.author.id)
        await self.handleError(ctx, status)
        if (status != self._OK_STATUS): return

        await ctx.message.reply('Your account is deleted.')
            
    @commands.command(name='getToken',aliases=['token'])
    async def getTokenCommand(self, ctx, targetid:t.Optional[str]):

        if (not targetid):
            targetid = ctx.author.id

        status = self.getToken(targetid)
        await self.handleError(ctx, status[0])
        if (status[0] != self._OK_STATUS): return
  
        await ctx.message.reply(F'You have {status[1]} tokens.')
        if (int(status[1]) == 0):
            await ctx.send('Use .revive to start again.')

    @commands.command(name='addToken',aliases=['addtoken'])
    async def addTokenCommand(self, ctx, amount, targetid:t.Optional[str]):
        if (ctx.author.id != 400941378395439104):
            await ctx.message.reply('You do not have permission to do so.')
            return 0
        
        if (not targetid):
            targetid = ctx.author.id

        status = self.addToken(amount, targetid)
        await self.handleError(ctx, status)
        if (status != self._OK_STATUS): return

        await ctx.message.reply(F'Added {amount} tokens.')
        
    @commands.command(name='gamble',aliases=['g'])
    async def gambleCommand(self, ctx, amount:t.Optional[str]):
        if not amount:
            await ctx.message.reply('Please specify your bet.')
            return 0
        
        status = self.gamble(amount, ctx.author.id)
        await self.handleError(ctx, status[0])
        if (status[0] != self._OK_STATUS): return

        data = self.readData()
        currency = data.get('players', {}).get(str(ctx.author.id), {}).get('currency', -1)

        if (status[1] == self._GAMBLE_SUCCESS):
            await ctx.message.reply(F'Success! **{amount} tokens** have been added to your account.\nYou have {currency} tokens.')
            return 0

        if (status[1] == self._GAMBLE_FAIL):
            await ctx.message.reply(F'Unlucky! **{amount} tokens** have been taken from your account.\nYou have {currency} tokens.')
            if (int(currency) == 0):
                await ctx.send('Use .revive to start again.')
            
            return 0

    @commands.command(name='resurrect',aliases=['revive','復活'])
    async def resurrectCommand(self, ctx):
        status = self.resurrect(ctx.author.id)
        await self.handleError(ctx, status[0])
        if (status[0] != self._OK_STATUS): return
        resurrect_token = status[1]
        await ctx.message.reply(F'You have resurrected. Added {resurrect_token} tokens to your account.')

    # @commands.command(name='getLoginBonus',aliases=['revive','復活'])
    # async def getLoginBonus(self, ctx):

    
class BotMinigame(Minigame):

    def __init__(self, bot):
        MinigameBackend.__init__(self, bot)
        Minigame.__init__(self, bot)



    @commands.Cog.listener()
    async def on_message(self, msg):


        # reject normie
        if msg.author.bot != True:
            return

        # reject this bot
        if msg.author.id == self.bot.user.id:
            # await msg.channel.send('yay')
            return    

        ctx = await self.bot.get_context(msg)

        patternCreateAccount    = "^[.](createAccount|register)$"
        patternDeleteAccount    = "^[.](deleteAccount|quitgame)$"
        patternGetToken         = "^[.](getToken|token)$"
        patternGetTokenOpt      = "^[.](getToken|token)[ ][0-9]{1,}$"
        patternAddToken         = "^[.](addToken|addtoken)[ ](-[1-9][0-9]{0,}|[1-9][0-9]{0,})$"
        patternAddTokenOpt      = "^[.](addToken|addtoken)[ ](-[1-9][0-9]{0,}|[1-9][0-9]{0,})[ ][0-9]{1,}$"
        patternGamble           = "^[.](gamble|g)$"
        patternGambleOpt        = "^[.](gamble|g)[ ][0-9]{1,}$"
        patternResurrect        = "^[.](resurrect|revive|復活)$"

        if (re.match(patternCreateAccount,msg.content)):
            await self.createAccountCommand(ctx)
            return

        if (re.match(patternDeleteAccount,msg.content)):
            await self.deleteAccountCommand(ctx)
            return    

        if (re.match(patternGetToken,msg.content)):
            await self.getTokenCommand(ctx,None)
            return

        if (re.match(patternGetTokenOpt,msg.content)):
            arg1 = re.findall("[0-9]{1,}",msg.content)[0] 
            await self.getTokenCommand(ctx,arg1)
            return

                

        if (re.match(patternAddToken,msg.content)):
            arg1 = re.findall("(-[1-9][0-9]{0,}|[1-9][0-9]{0,})",msg.content)[0]
            await self.addTokenCommand(ctx,arg1,None)
            return

        if (re.match(patternAddTokenOpt,msg.content)):
            arg1 = re.findall("(-[1-9][0-9]{0,}|[1-9][0-9]{0,})",msg.content)[0]
            arg2 = re.findall("[0-9]{1,}",msg.content)[0]
            await self.addTokenCommand(ctx,arg1,arg2)
            return

        if (re.match(patternGamble,msg.content)):
            await self.gambleCommand(ctx,None)
            return  

        if (re.match(patternGambleOpt,msg.content)):
            arg1 = re.findall("[0-9]{1,}",msg.content)[0]
            await self.gambleCommand(ctx,arg1)
            return            

        if (re.match(patternResurrect,msg.content)):
            await self.resurrectCommand(ctx)
            return
 



def setup(bot):
    # bot.add_cog(Minigame(bot))
    bot.add_cog(BotMinigame(bot))
