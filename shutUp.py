#shutUp.py

#Import dependencies
import os
from random import randint
import math
import discord
from discord.ext import commands
from dotenv import load_dotenv

#Get the .env that has the bot token in it
load_dotenv()
TOKEN = os.getenv('SHUTUP_TOKEN')

#Create a new class for the bot's commands with a prefix
bot = commands.Bot(command_prefix="~")

#The event when Discord finishes sending data to the bot
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

#~randomquote command
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def randomquote(ctx):
    print("Running command randomquote")
    #Open the quotes.txt file with read access
    with open("quotes.txt", "r") as quoteList:
        #This variable holds a list of the quotes by line
        quoteArray = quoteList.readlines()
        #The length of the list
        listLength = len(quoteArray)
        #Generate a random number based on the length of the quote list (also in the context of a list index which is 0 - (length - 1))
        quoteNum = randint(0, listLength - 1)
        #Print the selected quote to the console
        print("Sent the quote -", quoteArray[quoteNum])
    #Send the quote in the chat
    await ctx.channel.send(quoteArray[quoteNum])

#~addquote command
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def addquote(ctx, *args): #*args since the quote will most likely be longer than one word
    print("Running command addquote")
    #Start an empty array for the entire quote
    quoteArray = []
    #Argument counter to limit the length of an added quote
    argCount = 0
    #For each argument add one to the argument counter
    for arg in args:
        argCount = argCount + 1
    #If there are more than 100 arguments don't add the quote
    if argCount > 100:
        await ctx.channel.send("This quote is too long, try again.")
    #If the quote is shorter than 100 words
    else:
        #Open the quotes.txt file with append access
        with open("quotes.txt", "a") as quoteAppend:
            #For each word in the quote
            for arg in args:
                #If the word is the last one add a newline after it
                if arg == args[len(args) - 1]:
                    quoteAppend.write(arg + "\n")
                #Otherwise add the word and a space afterward
                else:
                    quoteAppend.write(arg + " ")
        #Send in the chat that the quote was saved
        await ctx.channel.send("~!Added a quote!~")

#~quotelist command
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def quotelist(ctx, page):

    print("Running command quotelist")
    #Open the quotes.txt file with read access
    with open("quotes.txt", "r") as quoteList:
        pages = []
        #This variable holds a list of the quotes by line
        quoteArray = quoteList.readlines()

        arrayLength = len(quoteArray)

        # pagecount = math.ceil(arrayLength / 10)
        #
        # iter = 1
        #
        # while iter < pagecount:
        #     pages.push(iter)
        #     iter = iter + 1
        #This is where the full list will be held in a message
        fullMessage = ""
        #For each quote
        quotecnt = 0
        for quote in quoteArray:
            #If it's the first quote add backticks to start the message
            if quote == quoteArray[0]:
                fullMessage = fullMessage + "```" + str(quotecnt) + ") " + quote
                quotecnt = quotecnt + 1
            #If it's the last quote add backticks at the end
            elif quote == quoteArray[len(quoteArray) - 1]:
                fullMessage = fullMessage + "\n" + str(quotecnt) + ") " + quote + "```"
            #Add the quote and a newline
            else:
                fullMessage = fullMessage + "\n" + str(quotecnt) + ") " + quote
                quotecnt = quotecnt + 1
        #Send the final formatted list of quotes
        await ctx.channel.send(fullMessage)

#~quote command
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def quote(ctx, num):
    print("Running command quote")
    #Open the quotes.txt file with read access
    with open("quotes.txt", "r") as quoteList:
        #This variable holds a list of the quotes by line
        quoteArray = quoteList.readlines()
        #Show what was sent in the console
        print("Sent -", quoteArray[int(num)])
        #Send the quote in the channel
        await ctx.channel.send(quoteArray[int(num)])

#~removequote command
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def removequote(ctx, num):
    print("Running command removequote")
    #Open quotes.txt with read access so I can make an array of all of the quotes
    with open("quotes.txt", "r") as quoteList:
        quoteArray = quoteList.readlines()
    #Variable that represents the quote to be deleted
    delete = quoteArray[int(num)]
    #Open quotes.txt with write access
    with open("quotes.txt", "w") as quoteList:
        #Write every quote to the file except for the one to be deleted
        for line in quoteArray:
            if line != delete:
                quoteList.write(line)

#Who keyword check
@bot.event
async def on_message(message):
    print("Checking for keywords")
    #List of words to check for
    whoList = ["who", "what", "when", "where", "why", "how"]
    #If the bot is the one that sent the message don't do anything
    if message.author == bot.user:
        return
    #Variable for the content of the message
    messageContent = message.content.lower()
    #If the message isn't empty but is also less than 15 characters
    if len(messageContent) > 0 and len(messageContent) < 15:
        #Loop through each word in the list whoList and if one of the words is in the message tell the sender to shut up
        for word in whoList:
            if word in messageContent:
                await bot.get_channel(message.channel.id).send("God please shut up <@!" + str(message.author.id) + ">")
                break #Break so that it doesn't do it multiple times for one message
    else:
        print("None of the words were in the list.")
    #This lets the bot process commands and also listen for the keywords and is NECESSARY or commands wont work
    await bot.process_commands(message)

@quote.error
async def mineError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = "Too fast! Try again in {:.2f}s".format(error.retry_after)
        await ctx.channel.send(message)
    else:
        raise error

@quotelist.error
async def mineError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = "Too fast! Try again in {:.2f}s".format(error.retry_after)
        await ctx.channel.send(message)
    else:
        raise error

@randomquote.error
async def mineError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = "Too fast! Try again in {:.2f}s".format(error.retry_after)
        await ctx.channel.send(message)
    else:
        raise error

@addquote.error
async def mineError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = "Too fast! Try again in {:.2f}s".format(error.retry_after)
        await ctx.channel.send(message)
    else:
        raise error

@removequote.error
async def mineError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = "Too fast! Try again in {:.2f}s".format(error.retry_after)
        await ctx.channel.send(message)
    else:
        raise error

# @bot.event
# async def on_message(message):
#     print("Checking for michael")
#
#     print(message.author.name)
#
#     if message.author.name == "Communist Cookie":
#         with open("insults.txt", "r") as roastList:
#             list = roastList.readlines()
#             roastNum = randint(0, len(list) - 1)
#             await bot.get_channel(message.channel.id).send("<@!194192754396364801> " + list[9])
#     #This lets the bot process commands and also listen for the keywords and is NECESSARY or commands wont work
#     await bot.process_commands(message)


#Run the bot with the secret token
bot.run(TOKEN)
