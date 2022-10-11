import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="two")
    async def _two(self, ctx: SlashContext):
        embed = discord.Embed(title="embed two")
        await ctx.send(content="two", embeds=[embed])

def setup(bot):
    bot.add_cog(Slash(bot))