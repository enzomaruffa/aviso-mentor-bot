import discord
from discord.ext import commands
import pymongo 
import os

# Constants

token = os.environ.get('SUGGESTIONS_BOT_TOKEN')
mongo_url = os.environ.get('MONGO_URL')

# Bot 
suggestions_channel_id = None
bot = commands.Bot(command_prefix="sg!")

# MongoDB
client = pymongo.MongoClient(mongo_url)
db = client.Suggestions
suggestions = db["suggestions"]

def add_suggestion(message, author, author_id):
        print(f"add_suggestion! {message}, {author}")
        suggestion = { "Autor": author, "Mensagem": message, "ID do autor": author_id }
        x = suggestions.insert_one(suggestion)
        
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