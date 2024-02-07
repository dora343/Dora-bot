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
    
    

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("音樂已停止播放。")



def setup(bot):
    bot.add_cog(Voice(bot))
