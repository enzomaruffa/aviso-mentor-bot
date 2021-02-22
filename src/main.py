import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="sg!")

suggestions_channel_id = None

@bot.command()
async def ping(ctx, arg):
	message = arg
	author = ctx.author
	await forward_suggestion(message, author)

@bot.event
async def on_message(message):
	print(f"RECVD MESSAGE! {message}")
	if (message.guild is not None) or (message.author == bot.user):
		await bot.process_commands(message)
		return
	if suggestions_channel_id == None: 
		await message.channel.send("Ops! Temos um problema!")
		return
	author = message.author
	content = message.content
	await forward_suggestion(content, author)

@bot.command()
async def set_channel(ctx):
	print("COMANDO!!!!!")
	global suggestions_channel_id 
	suggestions_channel_id = ctx.channel.id
	await ctx.channel.send(f"Channel configured on {ctx.channel.id}!")

async def forward_suggestion(message, author):
	if suggestions_channel_id == None: return
	channel = bot.get_channel(suggestions_channel_id)
	await channel.send(f"{author} - {message}")

bot.run('ODEzMzg1MTM3OTg2MzM4ODQ2.YDOh8A.ppyzMuQ0rqxjUUsNSL5RNJ0RIjk')