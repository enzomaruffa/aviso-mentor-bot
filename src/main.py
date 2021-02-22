import discord
from discord.ext import commands
import pymongo 
import os

token = os.environ.get('SUGGESTION_BOT_TOKEN')
suggestions_channel_id = None
bot = commands.Bot(command_prefix="sg!")
client = pymongo.MongoClient("mongodb+srv://pastre:asdqwe123@cluster0.aarfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Suggestions
suggestions = db["suggestions"]

def add_suggestion(message, author):
	print(f"add_suggestion! {message}, {author}")
	suggestion = { "Autor": author, "Mensagem": message }
	x = suggestions.insert_one(suggestion)


# @bot.command()
# async def ping(ctx, arg):
# 	message = arg
# 	author = ctx.author
# 	await forward_suggestion(message, author)

@bot.event
async def on_message(message):
	if (message.guild is not None) or (message.author == bot.user):
		await bot.process_commands(message)
		return
	if suggestions_channel_id == None: 
		await message.channel.send("Ops! Temos um problema!")
		return
	author = message.author.name
	author_id = message.author.id
	content = message.content
	await forward_suggestion(content, author, author_id)

@bot.command()
async def set_channel(ctx):
	global suggestions_channel_id 
	suggestions_channel_id = ctx.channel.id
	await ctx.channel.send(f"Channel configured on {ctx.channel.id}!")

async def forward_suggestion(message, author, author_id):
	print(f"forward_suggestion! {message}, {author}")
	if suggestions_channel_id == None: return
	channel = bot.get_channel(suggestions_channel_id)
	add_suggestion(message, author, author_id)
	await channel.send(f"*{message}*")

bot.run(token)

