import constants
import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord import File



lastJoin = constants.MIKU_ID
lastLeave = constants.MIKU_ID
lastAFK = constants.MIKU_ID



#Says Hello and Goodbye to users when they join and leave
@client.event
async def on_voice_state_update(member, before, after):
    role = discord.utils.find(lambda r: r.name == 'Miku Fan', member.guild.roles)
    global lastJoin
    global lastLeave
    global lastAFK
    channel_message = {constants.VC_PRIVATE : {
        "id" : constants.TEXT_PRIVATE, 
        "join_message" : f'Great to see you, {member.name} <:mikuwave:802983954369871902>'}, 
    constants.VC_MOVIE : {
        "id" : constants.TEXT_MOVIE, 
        "join_message" : f'Have fun watching the movie, {member.name} <:mikuwave:802983954369871902>'}, 
    "else" : {
        "id" : constants.TEXT_DEFAULT, 
        "join_message" : f'Great to see you, {member.name} <:mikuwave:802983954369871902>'}}
    #Greets people who join
    if before.channel is None and after.channel is not None and (member.id != constants.MIKU_ID) and (member.id != lastJoin):
        if not after.channel.id in channel_message.keys():
            #gets text channel id
            channeldictid = channel_message["else"]["id"]
            #gets correct join message
            channeldictmessage = channel_message["else"]["join_message"]
        else:
            #gets text channel id
            channeldictid = channel_message[after.channel.id]["id"]
            #gets correct join message
            channeldictmessage = channel_message[after.channel.id]["join_message"]
        #gets channel object
        channel = client.get_channel(channeldictid)
        #sends correct join message
        await channel.send(channeldictmessage)
                
    #Says bye to people who leave
    if before.channel is not None and after.channel is None and (member.id != constants.MIKU_ID) and (member.id != lastLeave):
        if not before.channel.id in channel_message.keys():
            #gets appropriate channel id
            channeldictid = channel_message["else"]["id"]
        else:
            #gets appropriate channel id
            channeldictid = channel_message[before.channel.id]["id"]
        #gets channel object from channel id
        channel = client.get_channel(channeldictid)
        #sends goodbye message
        await channel.send(f'It was nice seeing you, {member.name} <:mikuwave:802983954369871902>')

    #not my code, one of the other devs on this bot created the majority of the afk code, I only did a little optimization
    elif before.channel is not None and after.afk and (member.id != constants.MIKU_ID) and (member.guild.id == gaggle):
        #drags me back if I go afk
        if (member.id == constants.SAPH_ID):
            await member.move_to(before.channel)
        #laughs at people for being afk
        else:
            channel = client.get_channel(constants.TEXT_DEFAULT)
            if (member.id != lastAFK):
                if role in member.roles:
                    await channel.send(f'Sweet dreams, {member.name} <:mikuwave:802983954369871902>')
                    lastAFK = member.id
                else:
                    await channel.send(f'{member.name} fell asleep in vc <:pepePoint:749035016251506778>')
                    lastAFK = member.id

    #gives user vc role
    if before.channel is None and after.channel.id is not None and member.id != constants.MIKU_ID:
        #Gets the 'IN VC' role as a object
        vcrole = discord.utils.get(member.guild.roles, name="IN VC")
        #adds the role
        await member.add_roles(vcrole)
    elif before.channel.id in listofchannels and after.channel is None and member.id != constants.MIKU_ID:
        #Gets the 'IN VC' role as a object
        vcrole = discord.utils.get(member.guild.roles, name="IN VC")
        #adds the role
        await member.remove_roles(vcrole)
        
        
        
