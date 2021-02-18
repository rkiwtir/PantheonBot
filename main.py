import discord
import os
import requests
import json
import random
import re
from replit import db
from keep_alive import keep_alive
bc = 807207433503768606
client = discord.Client()

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
-Must be vocal and abble to target/shot call
-Heroes: Winston, Reinhardt, Wrecking Ball, Orisa""",
    "OT":
    """-Must play most Off Tanks to a good level 
-Must be vocal and abble to target/shot call
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
-Must be vocal and abble to target/shot call""",
    "SS":
    """-Must play most supports to a good level
-Must be very vocal and able to ult track"""
}


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
        'sol': 'Sol Invictus',
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
    valid_channels = ["bot-channel-for-staff-and-managers"]
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

                        Example:       
    **$LFP sol SDPS 2500-3000 
    -Should be able to play Genji, Hanzo, Mei
    -Previous team experience required**"""
            await msg.channel.send(message)

        if msg.content.startswith('$Help LFM'):
            message = """Command Format:        `$LFM {TeamName} {SR} {Extra Requirements}`
            
            Mention if managerial experience is required

                        Example:       
    **$LFM argos 2500+ 
    -No previous experience required**"""
            await msg.channel.send(message)
            
        if msg.content.startswith('$Help LFC'):
            message = """Command Format:        `$LFC {TeamName} {SR} {Extra Requirements}`

                        Example:       
    **$LFC saturn 3.3K
    -Must be atleast 4000SR**"""
            await msg.channel.send(message)

        if msg.content.startswith('$Help LFS'):
            message = """Command Format:        `$LFS [Role] [Requirements]`

                        Example:       
    **$LFS [Social Media Manager] [-Experience is preferred, but not mandatory
    -Knowledge of the role]**"""
            await msg.channel.send(message)


keep_alive()
client.run(os.getenv('TOKEN'))
