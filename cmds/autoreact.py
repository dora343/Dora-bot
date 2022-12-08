import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('settings.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Autoreact(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, msg):
         

            keyword1 = '<:chick:786220756102545409>'
            keyword2 = 'rushia'
            keyword3 = 'dora'
            keyword4 = '<@!838746426259406918>'
            keyword5 = '<@838746426259406918>'
            keyword6 = '@everyone'
            keyword7 = '@here'
            keyword10 = '燿'
            keyword11 = '楓'

            if msg.content == keyword1 and msg.author != self.bot.user:
                pass

            if msg.content == keyword2 and msg.author != self.bot.user:
                await msg.channel.send(jdata['rushia_live2d'])

            if msg.content == keyword3 and msg.author != self.bot.user:
                await msg.channel.send(f'<@{jdata["Dora_id"]}>')

            if (keyword4 in msg.content or keyword5 in msg.content) and msg.author != self.bot.user and msg.author.id != 400941378395439104:
                await msg.reply(
                    '屌你老母tag乜撚嘢啊 仆你個街食屎狗==\n' + \
                    '咁鍾意tag人我成全你\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n')

            if (keyword4 in msg.content or keyword5 in msg.content) and msg.author != self.bot.user and msg.author.id == 400941378395439104:
                await msg.channel.send('<@400941378395439104> 💖💖💖')

            if keyword6 in msg.content and msg.author != self.bot.user and not msg.author.guild_permissions.administrator:
                await msg.reply(
                    '屌你老母tag乜撚嘢啊 仆你個街食屎狗==\n' + \
                    '咁鍾意tag人我成全你\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n')

            if keyword7 in msg.content and msg.author != self.bot.user and not msg.author.guild_permissions.administrator:
                await msg.reply(
                    '屌你老母tag乜撚嘢啊 仆你個街食屎狗==\n' + \
                    '咁鍾意tag人我成全你\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n' + \
                    f'<@{msg.author.id}><@{msg.author.id}><@{msg.author.id}>\n')

            if msg.content == keyword10 and msg.author != self.bot.user and msg.author.id == 400941378395439104:
                await msg.channel.send('<@445943313384865813>')

            if msg.content == keyword11 and msg.author != self.bot.user and msg.author.id == 400941378395439104:
                await msg.channel.send('<@242543304418394124>')

        # await self.bot.process_commands(msg)


def setup(bot):
    bot.add_cog(Autoreact(bot))
