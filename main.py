import discord
import decouple 
from discord.ext import commands

jarvis=commands.Bot(command_prefix="/",intents=discord.Intents.all())


@jarvis.event

async def on_member_join(member):
    welcome_channel=jarvis.get_channel(894996143862329395)
    welcome_message= f"Welcome to the server {member.name} 🤗"
    messge_to_member=f"Welcome to {member.guild.name}"
    await welcome_channel.send(welcome_message)
    await member.send(messge_to_member)


@jarvis.event
async def on_message(message):
    if message.author.bot:
        return
    # await message.reply("Roger that!")
    await message.add_reaction("❤️")


@jarvis.command()
async def servername(ctx):
    server_name = ctx.guild.name
    await ctx.send(f"This server's name is: {server_name}")


jarvis.run(decouple.config('TOKEN'))

