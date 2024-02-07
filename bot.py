import discord
from discord.ext import commands
import typing as t
import json
import random
import platform
import asyncio
import os
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


with open('settings.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())
bot.remove_command('help')

# 測試機器人是否在線上


@bot.event
async def on_ready():
    print("機器人已上線。")
    await bot.change_presence(activity=discord.Game(name="指令請用[.]"))

@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    print("機器人已下線。")
    await ctx.send("898")
    await bot.close()
    exit()

# 啟用指定模組


@bot.command(name='load', aliases=['l'])
async def module_load(ctx, module):
    if (ctx.author.id != jdata["Dora_id"]): 
        await ctx.send('你沒有足夠權限使用此指令')
        return

    if module == 'all' or module == 'a':
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                x = filename[:-3]
                bot.load_extension(f'cmds.{x}')
        print("已載入所有模組。")
        await ctx.send('已載入所有模組。')
    bot.load_extension(f'cmds.{module}')
    await ctx.send(F'已載入 **{module}** 模組。')

# 禁用指定模組


@bot.command(name='unload')
async def module_unload(ctx, module):
    if (ctx.author.id != jdata["Dora_id"]): 
        await ctx.send('你沒有足夠權限使用此指令')
        return

    if module == 'all' or module == 'a':
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                x = filename[:-3]
                bot.unload_extension(f'cmds.{x}')
        await ctx.send('已卸載所有模組。')
    bot.unload_extension(f'cmds.{module}')
    await ctx.send(F'已卸載 **{module}** 模組。')

# 重新載入指定模組


@bot.command(name='reload', aliases=['r'])
async def module_reload(ctx, module):
    if (ctx.author.id != jdata["Dora_id"]): 
        await ctx.send('你沒有足夠權限使用此指令')
        return
    
    if module == 'all' or module == 'a':
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                x = filename[:-3]
                bot.reload_extension(f'cmds.{x}')
        print("已重新載入所有模組。")
        await ctx.send('已重新載入所有模組。')
    else:
        bot.reload_extension(f'cmds.{module}')
        await ctx.send(F'已重新載入 **{module}** 模組。')

# 匯入所有可用的模組
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        x = filename[:-3]
        bot.load_extension(f'cmds.{x}')


@bot.command()
async def listallmodules(ctx):
    if (ctx.author.id != jdata["Dora_id"]): 
        await ctx.send('你沒有足夠權限使用此指令')
        return

    x = ''
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            x += filename[:-3] + ' '
    await ctx.send(x)


@bot.command()
async def help(ctx, input: t.Optional[str]):
    
    await ctx.send('wip')
    return

    
    page = []
    num_of_pages = 2
    for i in range(num_of_pages):
        temp = discord.Embed(
            title=f"機器人指令列表 Page {i+1}", 
            description="使用 [.help] 會顯示此嵌入信息 ",
            color=0x1ef0ac)
        temp.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/838746426259406918/c669241357389acadf6e83a4140d0d1a.png?size=4096")
        page.append(temp)
        page[i].set_footer(text=f"P.{i+1}")
    # await ctx.send(str(page))

    page[0].add_field(name=".help <頁碼>", value="顯示此嵌入信息\n可指定頁碼", inline=True)
    page[0].add_field(name=".ping", value="計算機器人網絡延遲", inline=True)
    page[0].add_field(
        name=".roll <a-b>", value="在 [a-b] 中隨機抽出整數\na,b 必須為正整數\n預設為[1-100]", inline=True)
    #page[0].add_field(name=".hi", value="回傳 Hi.", inline=False)
    #page[0].add_field(name=".bye", value="回傳 Bye.", inline=False)
    page[0].add_field(name=".illuminati", value="回傳光明會標誌", inline=True)
    page[0].add_field(name=".rickroll", value="?", inline=True)

    page[1].add_field(name=".connect .join .joinvoice <語音頻道>",
                      value="加入指定語音頻道\n預設為使用者所在之語音頻道\n語音頻道可使用名稱或ID", inline=False)
    page[1].add_field(name=".disconnect .leave .fuckoff",
                      value="退出語音頻道", inline=False)
    page[1].add_field(name=".play .stream <URL>",
                      value="播放指定音樂\n只能同時播放一首音樂\nYoutube URL限定 ", inline=False)
    page[1].add_field(name=".pause", value="暫停播放音樂", inline=False)
    page[1].add_field(name=".resume", value="繼續播放音樂", inline=False)
    page[1].add_field(name=".stop", value="停止播放音樂", inline=False)

    page[0].add_field(name=".extra <尾刀傷害> <王剩餘血量>",
                      value="公主連結戰隊戰\n計算補償秒數用", inline=True)
    page[0].add_field(name=".shift <剩餘秒數> <軸>",
                      value="公主連結戰隊戰\n補償刀用改軸器", inline=True)
    page[0].add_field(name=".draw .d <抽數>", value="公主連結\n抽卡模擬器", inline=True)
    page[0].add_field(name=".pic", value="油", inline=True)
    page[0].add_field(name=".u .p .o", value="公主連結\n抽PICKUP \n[.u] PICKUP 0.7%\n[.p] PICKUP 1.4%\n[.o] PICKUP 0.4%", inline=True)
    page[0].add_field(name=".ds <抽數>", value="公主連結\n復刻池獎勵轉蛋", inline=True)


    if input:
        if input in ['1', '2']:
            # await ctx.send('Valid input detected.')
            await ctx.send(embed=page[int(input)-1])
        else:
            await ctx.send('無效的頁碼。')
    else:
        await ctx.send(embed=page[0])

    # await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
