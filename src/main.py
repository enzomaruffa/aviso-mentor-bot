import discord
import os
from dotenv import load_dotenv
# import requests as re

load_dotenv("../.env")

token = os.getenv('BOT_TOKEN')
forward_channel_id = os.getenv('FORWARD_CHANNEL_ID')
allowlist_guild_id = os.getenv('ALLOWLIST_GUILD_ID')

intents = discord.Intents.default()
# intents.members = True
client = discord.Client(intents=intents)

def build_embed(message, author_name, author_id, avatar_url, original_time):
  embed = discord.Embed(
    # title=message.content,
    description=message,
    color=discord.Color.blue()
  )

  embed.set_author(name=author_name, icon_url=avatar_url)
  embed.set_footer(text=f"{original_time.strftime('%d/%m/%Y, %H:%M:%S')} | Mensagem encaminhada pelo Avisa Mentor.")
  embed.add_field(name="\u200b", value=f"<@{author_id}>", inline=True)

  return embed

@client.event
async def on_ready():
  print('Bot started as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author.id == client.user.id:
    print("Message from bot. Returning...")
    return

  print(f'{message.author} said: {message.content}')

  # If the message is not in a dm, ignore
  if message.guild is not None:
    print("Message is not in a dm. Returning...")
    return

  guild = await client.fetch_guild(allowlist_guild_id) # find ID by right clicking on server icon and choosing "copy id" at the bottom
  member = await guild.fetch_member(message.author.id)

  if member is None: # find ID by right clicking on a user and choosing "copy id" at the bottom
      # The member is not in the server. Send a refusal message and return
      print("Member is not in the server. Sending refusal message and returning...")
      await message.channel.send(embed=discord.Embed(title="Eita!", description="Você não está na lista de membros autorizados para usar este bot. Entre na Academy :) *(ou reporte o erro pros mentores, hehe)*", color=0xcc1122))
      return

  # print("Building embed...")
  embed = build_embed(message.content, message.author.name, message.author.id, message.author.avatar.url, message.created_at)

  # print("Posting message...")
  channel = await client.fetch_channel(forward_channel_id)

  try:
    await channel.send(embed=embed)
    print("Message posted successfully")
    # Respond to the user that everything went well with a nice embed
    await message.channel.send(embed=discord.Embed(title="Tudo certo!", description=f"Mensagem enviada com sucesso!", color=0x00FF00))

  except Exception as e:
    print("Error posting message")
    print(e)
    # Respond to the user that something failed with a nice embed
    await message.channel.send(embed=discord.Embed(title="Eita!", description="Deu ruim! vise os mentores diretamente.", color=0xcc1122))

client.run(token)


