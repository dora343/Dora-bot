import typing as t
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os
import youtube_dl


class Voice(Cog_Extension):

    songname = ''

    @commands.command(name="connect", aliases=["join", "joinvoice"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        #"""Joins your voice channel"""
        author = ctx.message.author

        if channel == None:
            if author.voice == None:
                return await ctx.send('指令無效。\n你必須身處於語音頻道或於指令中指定語音頻道。')

            voice_channel = author.voice.channel

            if ctx.voice_client != None:
                if ctx.author.guild_permissions.administrator:
                    await ctx.voice_client.move_to(voice_channel)
                    await ctx.send(f'已連接至 {voice_channel.mention}.')
                else:
                    await ctx.send('你沒有足夠權限使用此指令。')
            else:
                await voice_channel.connect()
                await ctx.send(f'已連接至 {voice_channel.mention}.')

        else:

            voice_channel = channel
            if ctx.voice_client != None:
                if ctx.author.guild_permissions.administrator:
                    await ctx.voice_client.move_to(voice_channel)
                    await ctx.send(f'已連接至 {voice_channel.mention}.')
                else:
                    await ctx.send('你沒有足夠權限使用此指令。')
            else:
                await voice_channel.connect()
                await ctx.send(f'已連接至 {voice_channel.mention}.')

    @commands.command(name="disconnect", aliases=["fuckoff", "leave"])
    async def disconnect_command(self, ctx):

        if ctx.voice_client == None:
            await ctx.send('我並沒有身處於任何語音頻道。')
        else:
            if ctx.author.guild_permissions.administrator:
                channel = ctx.voice_client.channel.mention
                await ctx.voice_client.disconnect()
                await ctx.send(f'已從 {channel} 中斷連接.')
            else:
                await ctx.send('你沒有足夠權限使用此指令。')
    
    """
    @commands.command(name="play", aliases=["stream"])
    async def play_music_command(self, ctx, url: str):

        if ctx.voice_client == None:
            author = ctx.message.author
            voice_channel = author.voice.channel
            await voice_channel.connect()

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("請靜待音樂播放完畢或使用[.stop]停止播放音樂。")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                for i in range(len(file)):
                    if file[len(file)-1-i] == '-':
                        location = len(file)-1-i
                        break

                songname = file[0:location]
                os.rename(file, "song.mp3")

        ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
        await ctx.send('正在播放 `' + songname + '`。')

    @commands.command(name="resume")
    async def resume_command(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("音樂已恢復播放。")
        else:
            await ctx.send("音樂沒有被暫停。")

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("音樂已暫停播放。")
        else:
            await ctx.send("現時沒有播放任何音樂。")

    @commands.command(name="nowplaying", aliases=['np'])
    async def nowplaying_command(self, ctx):
        await ctx.send('`'+songname+'`')

        
    """

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("音樂已停止播放。")



def setup(bot):
    bot.add_cog(Voice(bot))
