import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random

with open('settings.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class React(Cog_Extension):
    '''
    @commands.command()
    async def hi(self,ctx):
        await ctx.send('Hi.')

    @commands.command()
    async def bye(self,ctx):
        await ctx.send('Bye.')

    @commands.command()
    async def nazi(self, ctx):
        pic = discord.File(jdata['nazi_pic'])
        await ctx.send(file=pic)
    '''


    @commands.command()
    async def illuminati(self, ctx):
        pic = discord.File(jdata['illuminati_pic'])
        await ctx.send(file=pic)

    @commands.command()
    async def rickroll(self, ctx):
        await ctx.send(jdata['never_gonna_give_you_up'])

    @commands.command()
    async def everyone(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await ctx.send('@everyone')
        else:
            await ctx.send('You do not have the permission to do so.')

    @commands.command()
    async def pic(self, ctx):
        album = []
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/839925492031160370/183314818_135299598580994_8659868584108528311_n.png')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/840058048549486622/IMG_20210507_105003.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/839572233311485982/181173038_1665642183622629_152394064086579568_n.png')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/839449465097027594/20210505_183147.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/839093340472606760/IMG_20210504_185656.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/838841804970917908/IMG_20210501_015301.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/838841803985518642/IMG_20210501_015259.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/838371462740967454/20210502_190846.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/838206265192742934/E0UkplAUYAIpsRW.png')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/838133986211135508/illust_84777634_20210502_032110.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/837599148877283339/pettan.rushia-___CI9i7rsnAHu___-.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/837356479479676978/illust_84893043_20210429_235119.png')
        album.append(
            'https://tenor.com/view/uruha-rushia-hololive-rushia-%E6%BD%A4%E7%BE%BD%E3%82%8B%E3%81%97%E3%81%82-%E3%82%8B%E3%81%97%E3%81%82-gif-20955092')
        album.append(
            'https://pbs.twimg.com/media/E0j0XQrVIAMB9ij?format=jpg&name=large')
        album.append('https://pbs.twimg.com/media/E0IdKzNVcAAALyx.jpg')
        album.append('https://pbs.twimg.com/media/ExPyPkgXEAMAnai.jpg')
        album.append(
            'https://cdn.discordapp.com/attachments/805834778996899840/807066053209227284/84248553_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840171644155723787/89208936_p1.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840171773106192414/89208936_p4.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840171819943985154/89208936_p13.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840171987476545546/88724934_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172202074701844/89360230_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172334143897640/86074731_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172438112305152/86074731_p12.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172679712997386/88196730_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172836081238016/87229606_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840172933623709716/85195257_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840173035465211924/82483442_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840173208179310622/81438832_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840173517927874560/89553840_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/840170913412546600/840173644700450816/80001079_p0.png')
        album.append(
            'https://cdn.discordapp.com/attachments/790812908619431938/840466243140059156/FB_IMG_1620453148138.jpg')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/840738572947554355/E03TclmVoAkUWDa.png')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/840765204743847986/illust_89495550_20210509_092451.jpg')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/840933465456246794/89492977_p0.jpg')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/841053876602142740/E07zLDGVIAovzuG.jpg')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/841100032504889386/5b7c278dc68dc7581f56bddd23605af9.JPG')
        album.append('https://media.discordapp.net/attachments/790812908619431938/841297982356062228/006.jpg')
        album.append('https://na.cx/i/5ECiG8m.png')
        album.append('https://pbs.twimg.com/media/E03TclmVoAkUWDa.jpg')
        album.append('https://pbs.twimg.com/media/E1BjlBYVEAMXXWD.jpg')
        album.append('https://pbs.twimg.com/media/E0nx7IdVUAAFwXv.jpg')
        album.append('https://pbs.twimg.com/media/E0sdSp5VgAIHn0V.jpg')
        album.append('https://cdn.discordapp.com/attachments/790812908619431938/846420943693152276/image0.png')

        i = random.randrange(0, len(album)-1)
        await ctx.send(album[i])


def setup(bot):
    bot.add_cog(React(bot))
