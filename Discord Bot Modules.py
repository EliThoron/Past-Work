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
        
        
        
#Random number generator
@client.command(aliases=['Rand', 'Random', 'random', 'RAND', 'RANDOM', 'rand'], brief = 'I\'ll make a random number for you!', description = 'Put one number to get a random number between it and 1. Put 2 numbers to get a random number between the 2. Put a third one on top of the two to add decimal places based on thay number. Eg \"!random 0 10 4\" can give you 3.9471.')
async def randomnumber(ctx, *args):
    #checks if it contains only integers
    if contains_only_integers(args):
        #checks length
        if len(args) >= 2: 
            #sorts the data
            argslist = sorted([abs(int(args[0])), abs(int(args[1]))])
            if len(args) == 2:
                argslist.append(0)
            else:
                argslist.append(args[2])
            #sends random number
            await ctx.send(f'{random.randint(argslist[0], argslist[1]) + round(random.random(), abs(int(argslist[2])))}')
        elif len(args) == 1:
            await ctx.send(f'{random.randint(0, abs(int(args[0])))}')
        else:
            await ctx.send("Didn't provide range for random number.")
    else:
        await ctx.send("Remove all non-integer characters and try again.")

#checks if all the varibles are integers
def contains_only_integers(args):
    contains_nonintegers = True
    for values in args:
        while contains_nonintegers:
            try:
                inttest = int(values)
                break
            except (TypeError, ValueError):
                contains_nonintegers = False
    return contains_nonintegers

#Coinflip
@client.command(aliases=['Coin', 'coin', 'COIN', 'coinflip', 'COINFLIP', 'flip', 'Flip', 'FLIP'], description = 'I\'ll flip a coin and tell you what happens!')
async def CoinFlip(ctx):
    if random.randint(1, 2) == 1:
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")
