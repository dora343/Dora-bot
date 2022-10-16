from multiprocessing import pool
from this import d
import turtle
from types import prepare_class
import discord
import scipy 
from discord.ext import commands
from discord.ext.commands import has_permissions
from sympy import true
from core.classes import Cog_Extension
import typing as t
import json
import math
import random
import secrets
import re
import os


class MyView(discord.ui.View): 
    hitpoint=5
    attack=5
    defence=5

    hp_cap=1200
    atk_cap=1200
    def_cap=1200

    actual_hp_value = 1
    actual_atk_value = 1
    actual_def_value = 1

    exp = 0

    msg = ""

    turn=1
    max_turn=75

    hp_lvl=0
    atk_lvl=0
    def_lvl=0
    exp_lvl=0

    lvl_up_cost = 3
    lvl_cap = 9

    hp_trial=0
    atk_trial=0
    def_trial=0

    base_lvl_stat = [1, 2, 4, 7, 12, 20, 32, 48, 70, 100]

    hp_fail=(hp_lvl - min(hp_lvl,atk_lvl,def_lvl))*0.1
    atk_fail=(hp_lvl - min(atk_lvl,atk_lvl,def_lvl))*0.1
    def_fail=(hp_lvl - min(def_lvl,atk_lvl,def_lvl))*0.1

    log_rate_coef = 0
    log_rate = 1 - (max(hp_lvl,atk_lvl,def_lvl) - min(hp_lvl,atk_lvl,def_lvl))*log_rate_coef 

    fixed_event_turn = [12, 24, 36, 48, 60, 72]

    #status effect here
    booster_20  = 0
    booster_40  = 0
    booster_60  = 0
    booster_80  = 0
    booster_100 = 0

    hp_lock = 0
    atk_lock = 0
    def_lock = 0
    
    fail_rate_0 = 0
    fail_rate_half = 0
    fail_rate_double = 0

    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    def build_msg(self):
        msg = "回合：" + str(self.turn) + "/"+str(self.max_turn) + "\n\n"
        if self.fail_rate_half > 0:
            msg = msg + "特殊狀態：練習上手◯ ("+str(self.fail_rate_half)+"/3) (訓練失敗率減半)\n\n"
        msg = msg + "HP = " + str(self.hitpoint) + "/" +str(self.hp_cap) + " ( +"+str(self.actual_hp_value) +" ) \n"
        msg = msg + "ATK = " + str(self.attack)  + "/" +str(self.atk_cap) + " ( +"+str(self.actual_atk_value) +" ) \n"
        msg = msg + "DEF = " + str(self.defence) + "/" +str(self.def_cap) + " ( +"+str(self.actual_def_value) +" ) "
        return msg

    def fixed_event_check(self):

        #12
        if self.turn == 12:
            self.hp_lvl+=1
            self.atk_lvl+=1
            self.def_lvl+=1
            
            self.hitpoint+=5
            self.attack+=5
            self.defence+=5

            self = self.update_value()
            
            msg = ""
            msg = msg + "=========觸發固有事件！=========\n\n"

            msg = msg + "--> 所有屬性訓練等級提升 ！\n\n"

            msg = msg + "生命力 LV" +str(self.hp_lvl)   +" --> 生命力 LV" +str(self.hp_lvl+1)  + "\n"
            msg = msg + "攻擊力 LV" +str(self.atk_lvl)  +" --> 攻擊力 LV" +str(self.atk_lvl+1) + "\n"
            msg = msg + "防禦力 LV" +str(self.def_lvl)  +" --> 防禦力 LV" +str(self.def_lvl+1) + "\n\n"

            msg = msg + "--> 所有屬性+5 ！\n\n"

            msg = msg + "生命力 " + str(self.hitpoint-5) + " --> 生命力 " + str(self.hitpoint) +" \n"
            msg = msg + "攻擊力 " + str(self.attack-5)   + " --> 攻擊力 " + str(self.attack)   +" \n"
            msg = msg + "防禦力 " + str(self.defence-5)  + " --> 防禦力 " + str(self.defence)  +" \n\n"

            msg = msg + "==============================\n\n"

            msg = msg + self.build_msg()

            self.msg = msg
            return self

        #24
        if self.turn == 24:
            self.hitpoint+=10
            self.attack+=10
            self.defence+=10

            self.booster_20 = 3

            self = self.update_value()
            msg = ""
            msg = msg + "=========觸發固有事件！=========\n\n"

            msg = msg + "--> 所有屬性+10 ！\n\n"

            msg = msg + "生命力 " + str(self.hitpoint-10) + " --> 生命力 " + str(self.hitpoint) +" \n"
            msg = msg + "攻擊力 " + str(self.attack-10)   + " --> 攻擊力 " + str(self.attack)   +" \n"
            msg = msg + "防禦力 " + str(self.defence-10)  + " --> 防禦力 " + str(self.defence)  +" \n\n"

            msg = msg + "--> 獲得特殊狀態：練習上手 LV1\n\n"

            msg = msg + "描述：你從身體中感受到一股不可思議的魔力！\n"
            msg = msg + "效果：三回合內，訓練效果增加20%\n\n"

            msg = msg + "==============================\n\n"

            msg = msg + self.build_msg()

            self.msg = msg


            return self

        #36
        if self.turn == 36:

            self.hitpoint+=10
            self.attack+=10
            self.defence+=10

            self.fail_rate_half = 3


            self = self.update_value()
            msg = ""
            msg = msg + "=========觸發固有事件！=========\n\n"

            msg = msg + "--> 所有屬性+10 ！\n\n"

            msg = msg + "生命力 " + str(self.hitpoint-10) + " --> 生命力 " + str(self.hitpoint) +" \n"
            msg = msg + "攻擊力 " + str(self.attack-10)   + " --> 攻擊力 " + str(self.attack)   +" \n"
            msg = msg + "防禦力 " + str(self.defence-10)  + " --> 防禦力 " + str(self.defence)  +" \n\n"

            msg = msg + "--> 獲得特殊狀態：練習上手◯\n\n"

            msg = msg + "描述：你從身體中感受到一股不可思議的魔力！\n"
            msg = msg + "效果：三回合內，訓練失敗率減半0%\n\n"

            msg = msg + "==============================\n\n"

            msg = msg + self.build_msg()

            self.msg = msg


            return self
        #48

        #60

        #72

  
    def calculate_value(self,type):
        self = self.update_value()

        if type==0:
            self.hitpoint += self.actual_hp_value
            if self.hp_trial%self.lvl_up_cost == 0 and self.hp_lvl < self.lvl_cap:
                self.hp_lvl+=1

        if type==1:
            self.attack += self.actual_atk_value
            if self.atk_trial%self.lvl_up_cost == 0 and self.atk_lvl < self.lvl_cap:
                self.atk_lvl+=1

        if type==2:
            self.defence += self.actual_def_value
            if self.def_trial%self.lvl_up_cost == 0 and self.def_lvl < self.lvl_cap:
                self.def_lvl+=1

        self = self.update_value()

        return self

    def update_value(self):
        self.log_rate = 1 - (max(self.hp_lvl,self.atk_lvl,self.def_lvl) - min(self.hp_lvl,self.atk_lvl,self.def_lvl))*self.log_rate_coef 
        self.actual_hp_value = max(1,round(self.base_lvl_stat[self.hp_lvl]*self.log_rate))
        self.actual_atk_value = max(1,round(self.base_lvl_stat[self.atk_lvl]*self.log_rate))
        self.actual_def_value = max(1,round(self.base_lvl_stat[self.def_lvl]*self.log_rate))
        
        if self.hitpoint == self.hp_cap:
            self.actual_hp_value = 0
        if self.attack == self.atk_cap:
            self.actual_atk_value = 0
        if self.defence == self.def_cap:
            self.actual_def_value = 0
        
        if (self.hp_cap - self.hitpoint) < self.actual_hp_value:
            self.actual_hp_value = self.hp_cap - self.hitpoint

        if (self.atk_cap - self.attack) < self.actual_atk_value:
            self.actual_atk_value = self.atk_cap - self.attack

        if (self.def_cap - self.defence) < self.actual_def_value:
            self.actual_def_value = self.def_cap - self.defence

        return self

    @discord.ui.button(label="HP LV1", style=discord.ButtonStyle.success) 
    async def hp_button_callback(self, button, interaction):
        
        self.hp_trial+=1 
         
        self = self.calculate_value(0)

        self.turn+=1

        if self.turn==self.max_turn:
            for child in self.children:
                child.disabled = True

        if self.turn in self.fixed_event_turn:
            self = self.fixed_event_check()
        else:
            self.msg = self.build_msg()

        if self.fail_rate_half > 0 :
            self.fail_rate_half -=1
        
        #button.label="HP LV"+str(self.hp_lvl+1)
        
        self.children[0].label = "HP LV" +str(self.hp_lvl+1)
        self.children[1].label = "ATK LV"+str(self.atk_lvl+1)
        self.children[2].label = "DEF LV"+str(self.def_lvl+1)

        await interaction.response.edit_message(content=self.msg,view=self) 

    @discord.ui.button(label="ATK LV1", style=discord.ButtonStyle.danger) 
    async def atk_button_callback(self, button, interaction): 
        
        self.atk_trial+=1 
         
        self = self.calculate_value(1)

        self.turn+=1

        if self.turn==self.max_turn:
            for child in self.children:
                child.disabled = True

        if self.turn in self.fixed_event_turn:
            self = self.fixed_event_check()
        else:
            self.msg = self.build_msg()

        if self.fail_rate_half > 0 :
            self.fail_rate_half -=1
        
        #button.label="HP LV"+str(self.hp_lvl+1)
        
        self.children[0].label = "HP LV" +str(self.hp_lvl+1)
        self.children[1].label = "ATK LV"+str(self.atk_lvl+1)
        self.children[2].label = "DEF LV"+str(self.def_lvl+1)

        await interaction.response.edit_message(content=self.msg,view=self) 

    @discord.ui.button(label="DEF LV1", style=discord.ButtonStyle.primary) 
    async def def_button_callback(self, button, interaction): 
        
        self.def_trial+=1 
         
        self = self.calculate_value(2)

        self.turn+=1

        if self.turn==self.max_turn:
            for child in self.children:
                child.disabled = True

        if self.turn in self.fixed_event_turn:
            self = self.fixed_event_check()
        else:
            self.msg = self.build_msg()

        if self.fail_rate_half > 0 :
            self.fail_rate_half -=1
        
        #button.label="HP LV"+str(self.hp_lvl+1)
        
        self.children[0].label = "HP LV" +str(self.hp_lvl+1)
        self.children[1].label = "ATK LV"+str(self.atk_lvl+1)
        self.children[2].label = "DEF LV"+str(self.def_lvl+1)

        await interaction.response.edit_message(content=self.msg,view=self) 


class Main(Cog_Extension):

    @commands.command()
    async def test(self, ctx):
        msg="回合：1/75\n\n"
        msg=msg+ "HP = 5/1200 ( +1 )\n"
        msg=msg+ "ATK = 5/1200 ( +1 )\n"
        msg=msg+ "DEF = 5/1200 ( +1 )"

        await ctx.send(msg,view=MyView(timeout=10))


    @commands.command()
    async def ping(self, ctx):
        temp=F'**網絡延遲: {round(self.bot.latency*1000)} ms**'
        await ctx.message.reply('**Pong!**\n'+temp)

    @commands.command()
    async def roll(self, ctx, msg: t.Optional[str]):    

        if msg:
            temp = msg.split("-")
            # await ctx.send(str(temp))
            if len(temp) > 2:
                await ctx.send('無效的範圍')
            else:
                # await ctx.send('Valid range.')

                for i in range(len(temp)):
                    for j in range(len(temp[i])):
                        if not temp[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                            return await ctx.send('無效的範圍')

                if len(temp) == 1:
                    temp = list(map(int, temp))
                    if temp[0] in [0, 1]:
                        await ctx.send('無效的範圍')
                    else:
                        await ctx.send(F'**{ctx.author.name}** rolls **{random.randrange(1,temp[0])}** (1-{temp[0]})')
                else:
                    temp = list(map(int, temp))
                    await ctx.send(F'**{ctx.author.name}** rolls **{random.randrange(temp[0],temp[1])}** ({temp[0]}-{temp[1]})')

        else:
            await ctx.message.reply(F'**{ctx.author.name}** rolls **{random.randrange(1,100)}** (1-100)')

    @commands.command()
    async def extra(self, ctx, dmg, hp):
        remain = math.ceil(90-90*int(hp)/int(dmg)+20)
        if remain > 90:
            remain = 90
        await ctx.message.reply(f'**補償秒數：{remain}秒**')





    @commands.command()
    async def wash(self, ctx):
        if ctx.author.guild_permissions.administrator:
            msg = '.'
            for i in range(1998):
                msg = msg + '\n'
            msg = msg + '.'
            await ctx.send(msg)
        else:
            await ctx.send('你沒有足夠權限使用此指令')

    @commands.command(name="shift")
    async def _go(self, ctx):
        # await ctx.send("fku")
        def checktime(number): # 檢查是不是合法的時間
            return (number >= 0 and number <= 130) and \
                ((number // 100 == 0 and number % 100 <= 59 and number % 100 >= 0) or \
                (number // 100 == 1 and number % 100 <= 30 and number % 100 >= 0))

        def transform_time(original_time): # 轉換秒數
            result = ""
            if original_time < 60:
                if original_time < 10:
                    result += "00" + str(original_time)
                else:
                    result += "0" + str(original_time)
            else:
                if 60 <= original_time < 70:
                    result += str(original_time // 60) + "0" + str(original_time % 60)
                else:
                    result += str(original_time // 60) + str(original_time % 60)
            return result

        message = ctx.message
        message1 = message.content.lower() # 轉為小寫
        message2 = "" 
        for c in message1:
            if c in ("，", "、", "。"):
                message2 += c
            elif 65281 <= ord(c) <= 65374:
                message2 += chr(ord(c) - 65248)
            elif ord(c) == 12288: # 空格字元
                message2 += chr(32)
            else:
                message2 += c
        # message2 將 message1 轉為半形
        if re.match(r"\s*\.shift\s*[\s\S]+", message2):
            tr = re.match(r"\s*\.shift\s*(\d+)\s*\n([\s\S]+)", message2)
            if tr:
                time = int(tr.group(1))
                if 1 <= time <= 90:
                    lines = tr.group(2).split("\n")
                    resultline = ""
                    for line in lines:
                        filter = line.replace(":", "").replace("\t", "") # 過濾特殊字元
                        match = re.match(r'(\D*)(\d{2,3})((\s*[~-]\s*)(\d{2,3}))?(.*)?', filter) # 擷取時間
                        if match:
                            content1 = match.group(1) # 時間前面的文字
                            timerange = match.group(3) # 056~057 這種有範圍的時間
                            time1 = int(match.group(2)) # 有範圍的時間 其中的第一個時間
                            time2 = 0
                            if timerange is not None and match.group(5) is not None:
                                time2 = int(match.group(5)) # 有範圍的時間 其中的第二個時間
                            rangecontent = match.group(4) # 第一個時間和第二個時間中間的字串
                            content2 = match.group(6) # 時間後面的文字
                            if checktime(time1) and ((timerange is None and match.group(5) is None) or (timerange is not None and match.group(5) is not None and checktime(time2))):
                                totaltime1 = time1 % 100 + (time1 // 100) * 60 # time1的秒數
                                newtime1 = totaltime1 - (90 - time)
                                result = ""
                                if newtime1 < 0: # 如果時間到了 後續的就不要轉換
                                    continue # 迴圈跳到下一個
                                if match.group(5) is None:
                                    result = content1 + transform_time(newtime1) + content2
                                else:
                                    totaltime2 = time2 % 100 + time2 // 100 * 60 # time2的秒數
                                    newtime2 = totaltime2 - (90 - time)
                                    result = content1 + transform_time(newtime1) + rangecontent + transform_time(newtime2) + content2
                                resultline += result
                            else:
                                resultline += line
                        else:
                            resultline += line
                        resultline += "\n"
                    resultline = "```rust\n" + resultline + "\n\n```"
                    await ctx.reply(resultline)
                else:
                    await ctx.reply("您輸入的補償秒數錯誤，秒數必須要在 1～90 之間！")
            else:
                await ctx.reply("您輸入的秒數格式錯誤！正確的格式為\n.shift 補償秒數\n文字軸\n\n(補償秒數後面請直接換行，不要有其他字元)")
        
    """shift
    @commands.command()
    async def shift(self, ctx, second, *, msg):

        # 計算剩餘秒數
        n = int(second)
        if n >= 100:
            n -= 40
        n = 90 - n

        nodigit = []
        # 把整段文字分行拆開
        m = re.split('\n', msg)
        content = []
        for i in range(len(m)):

            # 移除冒號
            m[i] = m[i].replace(':', '', 1)

            # 偵測字串內的數字
            flag1 = False
            flag2 = False
            ind = [0]

            for j in range(len(m[i])):
                if not flag1:
                    if m[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        flag1 = True
                        ind.append(j)
                else:
                    if (not flag2) and (not m[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                        flag2 = True
                        ind.append(j)

            ind.append(len(m[i]))

            # 分拆字串中第一組數字
            content.append([])
            for k in range(len(ind)-1):
                content[i].append(m[i][ind[k]:ind[k+1]])

            # 偵測無數字的字串
            if len(content[i]) == 1:
                nodigit.append(i)

        # 排除無數字的字串
        copy = []
        for i in range(len(content)):
            if i in nodigit:
                continue
            else:
                copy.append(content[i])

        # 提取所有指定數字
        time = []
        for i in range(len(copy)):
            time.append(int(copy[i][1]))

        # 補償秒數計算
        num = []
        for x in time:
            if x >= 100:
                x-=40
                x -= n
                if x < 100 and x > 60:
                    x += 40
            else:
                x -= n
                if x >= 60:
                    x += 40
            num.append(x)

        # 把數字及字串重組成一組文字
        result = '```glsl\n'
        for i in range(len(copy)):
            if i in nodigit:
                y = content[i][0] + '\n'
                result = result + y

            y = copy[i][0] + str(num[i]) + copy[i][2] + '\n'
            result = result + y
        result = result + '```'
        await ctx.message.reply(result)
    """
    
    @commands.command(name='pu',aliases=['p','u','o'])
    async def draw_pool(self, ctx):
        
        three_star = 0.03
        two_star = 0.18
        one_star = 1-two_star-three_star
        
        pool_up = 0.007

        if ctx.message.content == '.p':
        
            three_star = 0.06
            two_star = 0.18
            one_star = 1-two_star-three_star
            
            pool_up = 0.014

        if ctx.message.content == '.o':
            
            three_star = 0.03
            two_star = 0.18
            one_star = 1-two_star-three_star
            
            pool_up = 0.004
                
        one_star_amount = 0
        two_star_amount = 0
        three_star_amount = 0

        check = False
        result = []
        stone = 0
        amount = 0
        #msg = ''
        
        for i in range(200):
            temp = random.randrange(1, 1000)
            if i % 10 == 0 and i != 0:
                result.append(2)
                if temp <= three_star*1000:
                    result[i] = 3
                if temp <= pool_up*1000:
                    result[i] = 4
                    amount = i + 1
                    break
            else:
                result.append(1)
                if temp <= two_star*1000:
                    result[i] = 2
                if temp <= three_star*1000:
                    result[i] = 3
                if temp <= pool_up*1000:
                    result[i] = 4
                    amount = i + 1
                    break
                if i == 199:
                    check = True
                    amount = i + 1
        
        for i in range(amount):
                if result[i] == 1:
                    stone += 1
                    one_star_amount += 1
                if result[i] == 2:
                    stone += 10
                    two_star_amount += 1
                if result[i] == 3:
                    stone += 50
                    three_star_amount += 1
                if result[i] == 4:
                    stone += 50
                    three_star_amount += 1

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(amount)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(amount) + f'**抽才抽到** PICKUP ({round(100*pool_up,2)}%)**\n\n'
           

        msg = msg + '<:card_rainbow:840146360874696705>' + \
                str(three_star_amount) + '個，其中有' + str(1) + \
                '個' + '<:card_up:840146439778205741>\n'

        msg = msg + '<:card_gold:840146246295617578>' + \
            str(two_star_amount) + '個\n'

        msg = msg + '<:card_silver:840146174459772948>' + \
            str(one_star_amount) + '個\n\n'

        msg = msg + '總計抽到了**' + str(stone) + '**個女神石'
    
        if ctx.message.content=='.p':
                msg = '*[PICKUP 1.4%]*\n' + msg

        if ctx.message.content=='.o':
                msg = '*[PICKUP 0.4%]*\n' + msg

        '''
        if ctx.message.content=='.u':
                msg = '*[PICKUP 0.7%]*\n' + msg
        '''
        
        await ctx.message.reply(msg)


    @commands.command(name='umahorsepool',aliases=['k'])
    async def umamusume_draw_horse_pool(self,ctx,amounts: t.Optional[str]):
        if not amounts:
            amount = 1
        else:
            amount = int(amounts)
            if amount > 21313 and ctx.author.id != 400941378395439104:
                amount *= 6
                amount *= 5000
                return await ctx.message.reply('屌你老母咪叫我抽咁撚多隻<:chick:786220756102545409><:chick:786220756102545409><:chick:786220756102545409>\n你肯課' + str(amount) + '粒<:umajewel:986644206158229554>我就抽')
        
        
        SSR = 0.03
        SR = 0.18
        R = 1-SR-SSR
        pool_up = 0.0075
        
        pool_up_cutoff = int(pool_up*10000) #75
        SSR_cutoff = int(SSR*10000) #300
        SR_cutoff = int(SSR_cutoff + SR*10000) #2100
                
        R_amount = 0
        SR_amount = 0
        SSR_amount = 0

        maximum_draw = amount*200

        current_acquired = 0

        check = False

        for counter in range(1,maximum_draw+1):

            #Draw simulation
            result = random.randrange(1,10001) 
            if result in range(1,pool_up_cutoff+1):
                SSR_amount += 1
                current_acquired += 1
            if result in range(pool_up_cutoff+1,SSR_cutoff+1):
                SSR_amount += 1
            if result in range(SSR_cutoff+1,SR_cutoff+1):
                SR_amount +=1
            if result in range(SR_cutoff+1,10001):
                if counter % 10 == 0:
                    SR_amount += 1
                else: R_amount += 1

            #200PT
            if counter % 200 == 0:
                current_acquired += 1  
                SSR_amount +=1

            #Check finish
            if current_acquired == amount:
                break

        if counter == maximum_draw:
            check = True

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(counter)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(counter) + f'**抽才抽到 **{amount}** 隻** PICKUP 馬娘 ({round(100*pool_up,2)}%)**\n\n'

        msg = msg + '花費了**'+str(counter*150)+'**個 <:umajewel:986644206158229554>\n\n'
        

        msg = msg + '<:threestar:986646189179039755> ' + \
                str(SSR_amount) + '隻，其中有' + str(1) + \
                '隻' + ' <:umapickup:986648647678713996>\n'

        msg = msg + '<:twostar:986646154034962513> ' + \
            str(SR_amount) + '隻\n'

        msg = msg + '<:onestar:986646095432130580> ' + \
            str(R_amount) + '隻\n\n'

        msg = msg + '總計抽到了**' + str(SSR_amount*20 + SR_amount*3 + R_amount) + '**個 <:stone:986645073930358835>'
    
        #msg = '*[PICKUP 0.75%]*\n' + msg

        
        await ctx.message.reply(msg)

    @commands.command(name='umasupportpool-sr',aliases=['sr'])
    async def umamusume_draw_support_pool_sr_mode(self,ctx,amounts: t.Optional[str]):
        if not amounts:
            amount = 5
        else:
            amount = int(amounts)
            if amount > 21313 and ctx.author.id != 400941378395439104:
                amount *= 6
                amount *= 5000
                return await ctx.message.reply('屌你老母咪叫我抽咁撚多張<:chick:786220756102545409><:chick:786220756102545409><:chick:786220756102545409>\n你肯課 ' + str(amount) + '粒<:umajewel:986644206158229554>我就抽')
    
        
        SSR = 0.03
        SR = 0.18
        R = 1-SR-SSR

        pool_up = 0.0225

        SSR_cutoff = int(SSR*10000) #300
        pool_up_cutoff = int(SSR_cutoff + pool_up*10000) #525
        SR_cutoff = int(SSR_cutoff + SR*10000) #2100

        R_amount = 0
        SR_amount = 0
        SSR_amount = 0
        current_acquired = 0
        counter = 0

        while (current_acquired != amount):

            counter += 1

            #Draw simulation
            result = random.randrange(1,10001) 
            if result in range(1,SSR_cutoff+1):
                SSR_amount += 1
            if result in range(SSR_cutoff+1,pool_up_cutoff+1):
                SR_amount += 1
                current_acquired += 1
            if result in range(pool_up_cutoff+1,SR_cutoff+1):
                SR_amount +=1
            if result in range(SR_cutoff+1,10001):
                if counter % 10 == 0:
                    SR_amount += 1
                else: R_amount += 1
            
            
        
        
        msg = '**'+ctx.author.name + '** 花了**' + \
            str(counter) + f'**抽才抽到 **{amount}** 張** PICKUP 支援卡 ({round(100*pool_up,2)}%)**\n\n'

        msg = '**[SR模式]**\n' + msg
        msg = msg + '花費了**'+str(counter*150)+'**個 <:umajewel:986644206158229554>\n\n'
        

        

        msg = msg + '<:threestar:986646189179039755> ' + \
            str(SSR_amount) + '張\n'

        msg = msg + '<:twostar:986646154034962513> ' + \
                str(SR_amount) + '張，其中有' + str(amount) + \
                '張' + ' <:umasrpickup:993754852662464532>\n'

        msg = msg + '<:onestar:986646095432130580> ' + \
            str(R_amount) + '張\n\n'
        
        await ctx.message.reply(msg)

    @commands.command(name='umasupportpool-double',aliases=['2ssr'])
    async def umamusume_draw_support_pool_double(self,ctx):
        
        amounts = 5

        if not amounts:
            amount = 5
        else:
            amount = int(amounts)
            if amount > 21313 and ctx.author.id != 400941378395439104:
                amount *= 6
                amount *= 5000
                return await ctx.message.reply('屌你老母咪叫我抽咁撚多張<:chick:786220756102545409><:chick:786220756102545409><:chick:786220756102545409>\n你肯課' + str(amount) + '粒<:umajewel:986644206158229554>我就抽')
        
        SSR = 0.03
        SR = 0.18
        R = 1-SR-SSR
                
        pool_up_A = 0.0075
        pool_up_B = 0.0075
        
    
        pool_up_A_cutoff = int(pool_up_A*10000) #75
        pool_up_B_cutoff = int(pool_up_A_cutoff + pool_up_B*10000) #150
        SSR_cutoff = int(SSR*10000) #300
        SR_cutoff = int(SSR_cutoff + SR*10000) #2100

        R_amount = 0
        SR_amount = 0
        SSR_amount = 0

        maximum_draw = 2000

        A_acquired = 0
        B_acquired = 0

        exchange = 0

        check = False

        for counter in range(1,maximum_draw+1):

            #Draw simulation
            result = random.randrange(1,10001) 
            if result in range(1,pool_up_A_cutoff+1):
                SSR_amount += 1
                A_acquired += 1
            if result in range(pool_up_A_cutoff+1,pool_up_B_cutoff+1):
                SSR_amount += 1
                B_acquired += 1
            if result in range(pool_up_B_cutoff+1,SSR_cutoff+1):
                SSR_amount += 1
            if result in range(SSR_cutoff+1,SR_cutoff+1):
                SR_amount +=1
            if result in range(SR_cutoff+1,10001):
                if counter % 10 == 0:
                    SR_amount += 1
                else: R_amount += 1

            #200PT
            if counter % 200 == 0:
                exchange += 1  
                SSR_amount +=1

            #Check finish

            remaining_cards = max(5-A_acquired,0) + max(5-B_acquired,0)
            if remaining_cards == exchange:
                break

        if counter == maximum_draw:
            check = True

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(counter)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(counter) + f'**抽才把 **2 種 PICKUP 支援卡 ({round(100*pool_up_A,2)}%)** 抽到滿凸\n\n'

        msg = msg + '花費了**'+str(counter*150)+'**個 <:umajewel:986644206158229554>\n\n'
        

        msg = msg + '<:threestar:986646189179039755> ' + \
                str(SSR_amount) + '張，其中有' + str(A_acquired) + \
                '張' + ' <:umapickup:986648647678713996> + '+ str(B_acquired) + '張 <:umapickup:986648647678713996>\n'

        msg = msg + '<:twostar:986646154034962513> ' + \
            str(SR_amount) + '張\n'

        msg = msg + '<:onestar:986646095432130580> ' + \
            str(R_amount) + '張\n\n'
    
        msg = '**[SSR模式 - Double_UP!]**\n' + msg

        
        await ctx.message.reply(msg)

    @commands.command(name='umasupportpool',aliases=['ssr'])
    async def umamusume_draw_support_pool(self,ctx,amounts: t.Optional[str]):
        
        if not amounts:
            amount = 5
        else:
            amount = int(amounts)
            if amount > 21313 and ctx.author.id != 400941378395439104:
                amount *= 6
                amount *= 5000
                return await ctx.message.reply('屌你老母咪叫我抽咁撚多張<:chick:786220756102545409><:chick:786220756102545409><:chick:786220756102545409>\n你肯課' + str(amount) + '粒<:umajewel:986644206158229554>我就抽')
        
        SSR = 0.03
        SR = 0.18
        R = 1-SR-SSR
                
        pool_up = 0.0075
    
        pool_up_cutoff = int(pool_up*10000) #75
        SSR_cutoff = int(SSR*10000) #300
        SR_cutoff = int(SSR_cutoff + SR*10000) #2100

        R_amount = 0
        SR_amount = 0
        SSR_amount = 0

        maximum_draw = amount*200

        current_acquired = 0

        check = False

        for counter in range(1,maximum_draw+1):

            #Draw simulation
            result = random.randrange(1,10001) 
            if result in range(1,pool_up_cutoff+1):
                SSR_amount += 1
                current_acquired += 1
            if result in range(pool_up_cutoff+1,SSR_cutoff+1):
                SSR_amount += 1
            if result in range(SSR_cutoff+1,SR_cutoff+1):
                SR_amount +=1
            if result in range(SR_cutoff+1,10001):
                if counter % 10 == 0:
                    SR_amount += 1
                else: R_amount += 1

            #200PT
            if counter % 200 == 0:
                current_acquired += 1  
                SSR_amount +=1

            #Check finish
            if current_acquired == amount:
                break

        if counter == maximum_draw:
            check = True

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(counter)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(counter) + f'**抽才抽到 **{amount}** 張** PICKUP 支援卡 ({round(100*pool_up,2)}%)**\n\n'

        msg = msg + '花費了**'+str(counter*150)+'**個 <:umajewel:986644206158229554>\n\n'
        

        msg = msg + '<:threestar:986646189179039755> ' + \
                str(SSR_amount) + '張，其中有' + str(amount) + \
                '張' + ' <:umapickup:986648647678713996>\n'

        msg = msg + '<:twostar:986646154034962513> ' + \
            str(SR_amount) + '張\n'

        msg = msg + '<:onestar:986646095432130580> ' + \
            str(R_amount) + '張\n\n'
    
        msg = '**[SSR模式]**\n' + msg

        
        await ctx.message.reply(msg)

    '''
    @commands.command(name='umadoubleup',aliases=['K'])
    async def umamusume_draw_horse_double_up_pool(self,ctx):
        three_star = 0.03
        two_star = 0.18
        one_star = 1-two_star-three_star
        
        pool_up1 = 0.015
        pool_up2 = 0.0075
                
        one_star_amount = 0
        two_star_amount = 0
        three_star_amount = 0
        pickup1_amount = 0
        #pickup2_amount

        check = False
        drawed_one = False
        result = []
        stone = 0
        amount = 0
        #msg = ''
        
        for i in range(200):
            temp = random.randrange(1, 10000)
            if i % 10 == 0 and i != 0:
                result.append(2)
                if temp <= three_star*10000:
                    result[i] = 3
                if temp <= pool_up1*10000:
                    result[i] = 4
                    if drawed_one:
                        amount = i + 1
                        break
                    if not drawed_one:
                        drawed_one = true
                if temp <= pool_up2*10000:
                    result[i] = 5
                    if drawed_one:
                        amount = i + 1
                        break
                    if not drawed_one:
                        drawed_one = true
            else:
                result.append(1)
                if temp <= two_star*10000:
                    result[i] = 2
                if temp <= three_star*10000:
                    result[i] = 3
                if temp <= pool_up1*10000:
                    result[i] = 4
                    if drawed_one:
                        amount = i + 1
                        break
                    if not drawed_one:
                        drawed_one = true
                if temp <= pool_up2*10000:
                    result[i] = 5
                    if drawed_one:
                        amount = i + 1
                        break
                    if not drawed_one:
                        drawed_one = true
                if i == 199:
                    check = True
                    amount = i + 1
        
        for i in range(amount):
                if result[i] == 1:
                    stone += 1
                    one_star_amount += 1
                if result[i] == 2:
                    stone += 3
                    two_star_amount += 1
                if result[i] == 3:
                    stone += 20
                    three_star_amount += 1
                if result[i] == 4:
                    stone += 20
                    three_star_amount += 1

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(amount)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(amount) + f'**抽才抽到** PICKUP 馬娘 ({round(100*pool_up,2)}%)**\n\n'

        msg = msg + '花費了**'+str(amount*150)+'**個 <:umajewel:986644206158229554>\n\n'
        

        msg = msg + '<:threestar:986646189179039755> ' + \
                str(three_star_amount) + '個，其中有' + str(1) + \
                '個' + ' <:umapickup:986648647678713996>\n'

        msg = msg + '<:twostar:986646154034962513> ' + \
            str(two_star_amount) + '個\n'

        msg = msg + '<:onestar:986646095432130580> ' + \
            str(one_star_amount) + '個\n\n'

        msg = msg + '總計抽到了**' + str(stone) + '**個 <:stone:986645073930358835>'
    
        msg = '*[PICKUP 0.75%]*\n' + msg

        
        await ctx.message.reply(msg)
    '''
    @commands.command(name="draw", aliases=["d", "D"])
    async def draw_card(self, ctx, number: t.Optional[str]):
        digit_emoji = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
        three_star = 0.03
        two_star = 0.18
        one_star = 1-two_star-three_star

        pool_up = 0.007

        if not number:
            ray = []
            result = []
            msg = ''
            stone = 0
            for i in range(9):
                ray.append(secrets.randbelow(1000)+1)
                result.append(1)
                if ray[i] <= 1000-one_star*1000:
                    result[i] = 2
                if ray[i] <= 1000-one_star*1000-two_star*1000:
                    result[i] = 3
                if ray[i] <= pool_up*1000:
                    result[i] = 4

            ray.append(secrets.randbelow(1000)+1)
            result.append(2)
            if ray[9] <= 1000-one_star*1000-two_star*1000:
                result[9] = 3
            if ray[9] <= pool_up*1000:
                result[9] = 4

            doramsg = ''

            for i in range(10):
                if result[i] == 1:
                    stone += 1
                    msg = msg + '<:card_silver:840146174459772948>'
                if result[i] == 2:
                    stone += 10
                    msg = msg + '<:card_gold:840146246295617578>'
                if result[i] == 3:
                    stone += 50
                    msg = msg + '<:card_rainbow:840146360874696705>'
                if result[i] == 4:
                    stone += 50
                    msg = msg + '<:card_up:840146439778205741>'


                if i == 4:
                    msg = msg + '\n\n'

            stone = str(stone)
            stone_msg = '<:plus:841710694679838730>'
            for i in range(len(stone)):
                stone_msg = stone_msg + digit_emoji[int(stone[i])]
            stone_msg = stone_msg + '<:stone:841707955543212123>\n\n'

            msg = stone_msg + msg  
            await ctx.send(msg)

        else:
            for i in range(len(number)):
                if not number[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return await ctx.send('無效的輸入數值')
            number = int(number)
            if number <= 0:
                return await ctx.send('無效的輸入數值')
            if number > 100000 and ctx.author.id != 400941378395439104:
                return await ctx.send('為什麼要欺負我<:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777>')
            tens = math.floor(number/10)
            # await ctx.send(tens)
            number -= tens

            ray = []
            result = []

            one_star_amount = 0
            two_star_amount = 0
            three_star_amount = 0
            pu_amount = math.floor((tens+number)/200)
            # await ctx.send(pu_amount)

            stone = 0
            for i in range(number):
                ray.append(secrets.randbelow(1000)+1)
                result.append(1)
                if ray[i] <= 1000-one_star*1000:
                    result[i] = 2
                if ray[i] <= 1000-one_star*1000-two_star*1000:
                    result[i] = 3
                if ray[i] <= pool_up*1000:
                    result[i] = 4

            for i in range(tens):
                ray.append(secrets.randbelow(1000)+1)
                result.append(2)
                if ray[i+number] <= 1000-one_star*1000-two_star*1000:
                    result[i+number] = 3
                if ray[i+number] <= pool_up*1000:
                    result[i+number] = 4

            for i in range(tens+number):
                if result[i] == 1:
                    stone += 1
                    one_star_amount += 1
                if result[i] == 2:
                    stone += 10
                    two_star_amount += 1
                if result[i] == 3:
                    stone += 50
                    three_star_amount += 1
                if result[i] == 4:
                    stone += 50
                    pu_amount += 1

            three_star_amount += pu_amount
            # await ctx.send(str(ray))

            msg = '**'+ctx.author.name + '** 抽了**' + \
                str(number+tens) + '**抽\n\n'
            msg = msg + '<:card_rainbow:840146360874696705>' + \
                str(three_star_amount) + '個，其中有' + str(pu_amount) + \
                '個' + '<:card_up:840146439778205741>\n'
            msg = msg + '<:card_gold:840146246295617578>' + \
                str(two_star_amount) + '個\n'
            msg = msg + '<:card_silver:840146174459772948>' + \
                str(one_star_amount) + '個\n\n'

            msg = msg + '總計抽到了**' + str(stone) + '**個女神石\n'

            await ctx.message.reply(msg)

    @commands.command(name="drawspecial", aliases=["ds", "DS"])
    async def draw_special_card(self, ctx, number: t.Optional[str]):
        prize_emoji = ['<:1_:845872250167361566>','<:2_:845872264493793281>','<:3_:845872276901855282>','<:4_:845872290075639849>','<:5_:845872311210475521>','<:6_:845872328999174164>']
        first_prize=5
        second_prize=10
        third_prize=50
        fourth_prize=100
        fifth_prize=235
        sixth_prize=600

        if not number:
            ray = []
            result = []
            msg = ''
            

            for i in range(9):
                ray.append(secrets.randbelow(1000)+1)
                result.append(6)
                if ray[i] <= 1000-sixth_prize:
                    result[i] = 5
                if ray[i] <= 1000-sixth_prize-fifth_prize:
                    result[i] = 4
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i] = 3
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i] = 2
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i] = 1

            ray.append(secrets.randbelow(1000)+1)
            result.append(5)
            if ray[9] <= 1000-sixth_prize-fifth_prize:
                result[9] = 4
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                result[9] = 3
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                result[9] = 2
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                result[9] = 1


            for i in range(10):
                if result[i] == 1:
                    msg = msg + prize_emoji[0]
                if result[i] == 2:
                    msg = msg + prize_emoji[1]
                if result[i] == 3:
                    msg = msg + prize_emoji[2]
                if result[i] == 4:
                    msg = msg + prize_emoji[3]
                if result[i] == 5:
                    msg = msg + prize_emoji[4]
                if result[i] == 6:
                    msg = msg + prize_emoji[5]


                if i == 4:
                    msg = msg + '\n\n'

            await ctx.send(msg)
        
        else:
            for i in range(len(number)):
                if not number[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return await ctx.send('無效的輸入數值')
            number = int(number)
            if number <= 0:
                return await ctx.send('無效的輸入數值')
            if number > 100000 and ctx.author.id != 400941378395439104:
                return await ctx.send('為什麼要欺負我<:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777>')
            tens = math.floor(number/10)
            # await ctx.send(tens)
            number -= tens

            ray = []
            result = []

            first_amount=0
            second_amount=0
            third_amount=0
            fourth_amount=0
            fifth_amount=0
            sixth_amount=0

            shard_amount=0
            heart_amount=0
            stone_amount=0

            tess=''
            for i in range(number):
                ray.append(secrets.randbelow(1000)+1)
                tess+=str(ray[i]) + ' '

                result.append(6)
                if ray[i] <= 1000-sixth_prize:
                    result[i] = 5
                if ray[i] <= 1000-sixth_prize-fifth_prize:
                    result[i] = 4
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i] = 3
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i] = 2
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i] = 1

            for i in range(tens):
                ray.append(secrets.randbelow(1000)+1)
                tess+=str(ray[i]) + ' '
                result.append(5)
                if ray[i+number] <= 1000-sixth_prize-fifth_prize:
                    result[i+number] = 4
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i+number] = 3
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i+number] = 2
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i+number] = 1

            for i in range(tens+number):
                if result[i] == 1:
                    first_amount += 1
                    shard_amount+=40
                    stone_amount+=5
                    heart_amount+=5

                if result[i] == 2:
                    second_amount += 1
                    shard_amount+=20
                    stone_amount+=5
                    heart_amount+=3

                if result[i] == 3:
                    third_amount += 1
                    shard_amount+=5
                    stone_amount+=1
                    heart_amount+=3

                if result[i] == 4:
                    fourth_amount += 1
                    shard_amount+=1
                    stone_amount+=1
                    heart_amount+=2

                if result[i] == 5:
                    fifth_amount += 1
                    stone_amount+=1
                    heart_amount+=1

                if result[i] == 6:
                    sixth_amount += 1
                    stone_amount+=1


            msg = '**'+ctx.author.name + '** 抽了**' + \
                str(number+tens) + f'**抽\n總計抽到了\n**{str(shard_amount)}**個記憶碎片\n**{str(heart_amount)}**個公主之心碎片\n**{str(stone_amount)}**個女神石\n'
            msg = msg + prize_emoji[0] + \
                str(first_amount) + '個\n'
            msg = msg + prize_emoji[1] + \
                str(second_amount) + '個\n'
            msg = msg + prize_emoji[2] + \
                str(third_amount) + '個\n'
            msg = msg + prize_emoji[3] + \
                str(fourth_amount) + '個\n'
            msg = msg + prize_emoji[4] + \
                str(fifth_amount) + '個\n'
            msg = msg + prize_emoji[5] + \
                str(sixth_amount) + '個'

            await ctx.message.reply(msg)
            #await ctx.send(tess)


def setup(bot):
    bot.add_cog(Main(bot))
