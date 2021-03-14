import discord
import os
import requests
import json
import random
import re
import datetime
import calendar
from replit import db
from keep_alive import keep_alive
#from discord.utils import get
#from discord.ext import commands

bc = 807207433503768606

client = discord.Client()

SM_Info="""_ _ 
__**Staff Members**__
<@193651616669237248>\n<@297432174448082974>\n<@571359999348047873>\n<@393172256135577612>\n<@235742158429093889>\n
__**Teams Infomation**__
<@&711849567808782359>:  <:Diamond:664150683590852618> 3.3k  Ⓜ️ <@317328097915568129>  🧢 <@373547458518581248>
<@&721822855771324549>:  <:Diamond:664150683590852618> 3.1k  Ⓜ️ <@305010894537097217>  🧢 <@191320412334850059>
<@&811288021461893210>:  <:Platinum:664150630717194258> 2.8k  Ⓜ️ <@456462984676638720>  🧢 <@206799386070614016>
<@&788379443554418689>:  <:Platinum:664150630717194258> 2.7k  Ⓜ️ <@469924234697900032>  🧢 <@300326844492677121>
<@&798849466530660382>:  <:Platinum:664150630717194258> 2.5k  Ⓜ️ <@370860911516188673>  🧢 <@320463639695851523>\n\n"""
Socials_info ="""__**Socials**__
<:discord:820672512044171284> Discord : https://discord.gg/5Pu52GPSaj
<:twitter:820672510222794752> Twitter : https://twitter.com/PantheonEsport
<:twitch:820672509561012235> Twitch : https://www.twitch.tv/pantheonesport
<:youtube:820674331524726835> Youtube : https://www.youtube.com/channel/UCd7EYOnmsfV3WqlxaT93TYQ"""
Server_Info=SM_Info+Socials_info

Rules_1="""```diff
To be sure this Community stays amazing, make sure you've read the Rules and Guidelines stated below.

GROUND RULES
+ Be nice, Be respectful
  - Be civil. It's fine to have opinions, but don't enforce them upon others. Refrain from sensitive topics like gender, sexual preference religion and politics. Banter is fully allowed but don't exaggerate it.
  - No hate speech against anything. Period.
  - If a Staff Member asks you to stop doing something, it's time to stop. Failure in doing so might get you in trouble.

+ Spamming isn't allowed
  - This includes, but is not limited to: excessive use of capitalization, emojis, repeated lines of similar text/images/other content. Links and self-promotion can be done in media, but excessive spamming of said things is still not allowed.

+ Keep all discussion in the correct channels
  - Discussion about things not meant to be discussed in the channel will be eventually removed, or the people doing it will be warned. Repeated violations will have consequences.
  - The default server language is English. Please refrain from using any other language in public chats.
  - Impersonation of any member, especially the staff, is not allowed. No NSFW names or pictures.
  - The Staff reserves the right to change your nickname as and when they deem appropriate.

+ Doxing isn't allowed
  - Sharing other people's personal information in text chat won't be tolerated, unless said people are consensual in such thing.```"""

Rules_2="""```diff
+ VOICE CHAT RULES
  - Try to keep background noise as low as possible as it can sabotage your team's performance.
  - Signs of toxicity or hatred towards anything are to be strictly avoided.
  - No intentional 'ear rape' or any other loud noises. This could get you muted from VCs.
  - Joining a random VC just to troll the players will be treated as a serious offense.
  - We have music bots and music VCs for those who want to listen to songs. Playing songs through your mic in other channels will result in being muted.

- If you believe someone is breaking any of the above rules, send any of the Staff members a DM, preferably with proof. Action will be taken accordingly.```"""

Join_Us="""Want to join Pantheon Esports as a team?
**Fill this form:** https://forms.gle/z7dmKRmKc4B9397f8"""

requirements = {
    "MS":
    """-Must play most Main supports to a good level
-Must be very vocal and able to ult track
-Heroes: Lucio, Baptiste, Mercy, Brigitte""",
    "FS":
    """-Must play most Flex supports to a good level
-Must be very vocal and able to ult track
-Heroes: Ana, Zenyatta, Moira, Baptiste """,
    "MT":
    """-Must play most Main Tanks to a good level 
-Must be vocal and able to target/shot call
-Heroes: Winston, Reinhardt, Wrecking Ball, Orisa""",
    "OT":
    """-Must play most Off Tanks to a good level 
-Must be vocal and able to target/shot call
-Heroes: Dva, Zarya, Sigma, Roadhog""",
    "HDPS":
    """-Must play most hitscan dps to a good level
-Must be vocal enough
-Heroes: McCree, Repear, Widowmaker, Ashe, Tracer, Sombra, Soldier:76""",
    "FDPS":
    """-Must play most projectile dps to a good level
-Must be vocal enough
-Heroes: Echo, Genji, Hanzo, Sombra, Mei, Pharah, Doomfist, Junkrat""",
    "SDPS":
    """-Must play most dps to a good level
-Must be vocal enough""",
    "ST":
    """-Must play most Tanks to a good level 
-Must be vocal and able to target/shot call""",
    "SS":
    """-Must play most supports to a good level
-Must be very vocal and able to ult track"""
}

def getRoleMention(team):
  team = team.lower()
  switch = {
      'saturn': '<@&711849567808782359>',
      'mars': '<@&798849466530660382>',
      'persephone': '<@&721822855771324549>',
      'argos': '<@&788379443554418689>',
      'hypnos':'<@&811288021461893210>'
    }
  return switch.get(team, 'none')

def getRole(role):
    switch = {
        'MT': "Main Tank",
        'OT': "Off Tank",
        'ST': "Sub Tank",
        'HDPS': "Hitscan DPS",
        'FDPS': "Flex DPS",
        'SDPS': "Sub DPS",
        'MS': "Main Support",
        'FS': "Flex Support",
        'SS': "Sub Support"
    }
    return switch.get(role, "None")

def getTeam(team):
    team = team.lower()
    switch = {
        'saturn': 'Saturn',
        'mars': 'Mars',
        'persephone': 'Persephone',
        'argos': 'Argos',
        'hypnos':'Hypnos'
    }
    return switch.get(team, "None")


#lOOKING FOR STAFF/CUSTOM


def create_LFS_embed(role, requirements, userid):
    ch = role[0:1].lower()
    if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u':
        vow = 'an'
    else:
        vow = 'a'

    embed = discord.Embed(title="Pantheon Esports is looking for " + vow +
                          " " + role,
                          colour=discord.Colour.red())
    embed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/434369835254677517/662255647739346955/firstdraft.png'
    )
    embed.add_field(name='Requirements: ', value=requirements, inline=False)
    embed.add_field(name='Contact: ', value=userid, inline=False)
    return embed


#LOOKING FOR PLAYER


def create_LFP_embed(team, role, sr, userid, extra=None):
    embed = discord.Embed(title=getTeam(team) +
                          " is looking for players for the following role",
                          colour=discord.Colour.blurple())
    #print(userid)
    #embed.set_author(name=userid)
    embed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/434369835254677517/662255647739346955/firstdraft.png'
    )
    embed.add_field(name='Role: ', value=getRole(role), inline=True)
    embed.add_field(name='SR: ', value=sr, inline=True)
    embed.add_field(name='Requirements: ',
                    value=requirements[role],
                    inline=False)
    if (extra != None):
        embed.add_field(name='Other Requirements: ', value=extra, inline=False)
    embed.add_field(name='Contact: ', value=userid, inline=False)
    return embed


#LOOKING FOR MANAGER


def create_LFM_embed(team, sr, userid, extra=None):
    embed = discord.Embed(
        title="Pantheon Esports is looking for Manager for team " +
        getTeam(team),
        colour=discord.Colour.gold())
    embed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/434369835254677517/662255647739346955/firstdraft.png'
    )
    embed.add_field(name='Requirements: ',
                    value="""
                        -Manager needed for """ + sr + """SR team\n-Able to find scrims, ringers, and players whenever required\n-Able to book vod review with coach when needed\n-Attendance at scrims is not mandatory
                        """,
                    inline=False)
    if (extra != None):
        embed.add_field(name='Other Requirements: ', value=extra, inline=False)
    embed.add_field(name='Contact: ', value=userid, inline=False)
    return embed


#LOOKING FOR COACH


def create_LFC_embed(team,sr, userid, extra=None):
    embed = discord.Embed(
        title="Pantheon Esports is looking for coach for team " +
        getTeam(team),
        colour=discord.Colour.green())
    embed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/434369835254677517/662255647739346955/firstdraft.png'
    )
    #sr=sr.rstrip(" ")
    embed.add_field(name='Requirements: ',
                    value="""-Coach needed for """ + sr.strip() + """SR team\n-Able to attend at least a couple of scrims a week
-Dedicated and motivated to improve
-Experience preferred
-Regular VOD reviews""")
    if (extra != None):
        embed.add_field(name='Other Requirements: ', value=extra, inline=False)
    embed.add_field(name='Contact: ', value=userid, inline=False)
    return embed


@client.event
async def on_ready():
    print("This is working as {0.user}".format(client))


@client.event
async def on_message(msg):
    if msg.author == client:
        return
    valid_channels = ["bot-channel-for-staff-and-managers","bot-commands","schedule","rules","apply-as-a-team","server-info"]
    #COMMANDS
    if str(msg.channel) in valid_channels:
        if msg.content.startswith('$LFC'):
            print(msg.content)
            userid = msg.author.mention
            message = msg.content.split("$LFC ", 1)[1]
            team = message.split(" ")[0]
            sr = message.split(" ")[1]
            temp = team + " " + sr + " "
            try:
                extra = message.split(temp, 1)[1]
            except:
                extra = None
            embed = create_LFC_embed(team,sr, userid, extra)
            bot_channel = client.get_channel(bc)
            await bot_channel.send(embed=embed)

        if msg.content.startswith('$LFM'):
            userid = msg.author.mention
            message = msg.content.split("$LFM ", 1)[1]
            team = message.split(" ")[0]
            sr = message.split(" ")[1]
            temp = team + " " + sr + " "
            try:
                extra = message.split(temp, 1)[1]
            except:
                extra = None
            embed = create_LFM_embed(team, sr, userid, extra)
            bot_channel = client.get_channel(bc)
            await bot_channel.send(embed=embed)

        if msg.content.startswith('$LFP'):
            userid = msg.author.mention
            message = msg.content.split("$LFP ", 1)[1]
            team = message.split(" ")[0]
            role = message.split(" ")[1]
            sr = message.split(" ")[2]
            temp = team + " " + role + " " + sr + " "
            try:
                extra = message.split(temp, 1)[1]
            except:
                extra = None
            embed = create_LFP_embed(team, role, sr, userid, extra)
            bot_channel = client.get_channel(bc)
            await bot_channel.send(embed=embed)

        if msg.content.startswith('$LFS'):
            userid = msg.author.mention
            message = msg.content.split("$LFS ", 1)[1]
            result = re.findall(r'\[(.*?)\]', message, flags=re.M | re.S)
            role = result[0]
            requirements = result[1]
            embed = create_LFS_embed(role, requirements, userid)
            bot_channel = client.get_channel(bc)
            await bot_channel.send(embed=embed)

        #HELPER

        if msg.content.startswith('$Help LFP'):
            message = """
            Command Format:     `$LFP {TeamName} {Role} {SR RANGE} {Extra Requirements}`

                        Roles: 
                                Tanks: MT, OT, ST
                                DPS: HDPS, FDPS, SDPS
                                Support: MS, FS, SS

                        Please mention hero requirements for Sub Roles in 'Extra Requirements'
                        Mention if previous team experience is required in 'Extra Requirements'

                        \nExample:       
    **$LFP sol SDPS 2500-3000 
    -Should be able to play Genji, Hanzo, Mei
    -Previous team experience required**"""
            await msg.channel.send(message)

        if msg.content.startswith('$Help LFM'):
            message = """Command Format:        `$LFM {TeamName} {SR} {Extra Requirements}`
            
            Mention if managerial experience is required

                        \nExample:       
    **$LFM argos 2500+ 
    -No previous experience required**"""
            await msg.channel.send(message)
            
        if msg.content.startswith('$Help LFC'):
            message = """Command Format:        `$LFC {TeamName} {SR} {Extra Requirements}`

                        \nExample:       
    **$LFC saturn 3.3K
    -Must be atleast 4000SR**"""
            await msg.channel.send(message)

        if msg.content.startswith('$Help LFS'):
            message = """Command Format:        `$LFS [Role] [Requirements]`

                        \nExample:       
    **$LFS [Social Media Manager] [-Experience is preferred, but not mandatory
    -Knowledge of the role]**"""
            await msg.channel.send(message)
        
        if msg.content.startswith('$Help Schedule'):
          message= """Command Format:        `$Schedule {TeamName}`
          \nExample:       
            **$Schedule hypnos**"""
          await msg.channel.send(message)

        
        
        if msg.content.startswith('$Rules'):
          await msg.channel.send(Rules_1)
          await msg.channel.send(Rules_2)
        
        
        
        
        if msg.content.startswith('$Join'):
          await msg.channel.send(Join_Us)
        
        #For Schedule
        
        if msg.content.startswith('$Schedule '):
          team=msg.content.split("$Schedule ", 1)[1]
          #test=discord.Role.id(820633395977125948)
          react_pls=getRoleMention(team)+" Please react to the schedule. React with ❓ if you're unsure"
          await msg.channel.send(react_pls)
          #my_date = datetime.date.today()
          for day in range(1, 8):  
            tday = datetime.datetime.today() + datetime.timedelta(days=day)
            val=calendar.day_name[tday.weekday()]+" "+ tday.strftime("%d-%B")
            me= await msg.channel.send(str(val))
            await me.add_reaction("<:yesvote:820626301915496529>")
            await me.add_reaction("<:novote:820626301769220157>")
            await me.add_reaction("❓")

        #Server Info

        if msg.content.startswith('$Info'):
          await msg.channel.send(Server_Info)


keep_alive()
client.run(os.getenv('TOKEN'))
