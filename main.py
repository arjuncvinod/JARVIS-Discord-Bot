import discord
import decouple 
from discord.ext import commands
import openai

jarvis=commands.Bot(command_prefix="/",intents=discord.Intents.all())

def generate_app_ideas(prompt):
    openai.api_key = decouple.config('OPENAI_API_KEY')

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


def trimmsg(text):
    return text[:1800]
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
    await message.add_reaction("❤️")
    async with message.channel.typing():
    	await message.reply(trimmsg(generate_app_ideas(message.content)))
   		


@jarvis.command()
async def servername(ctx):
    server_name = ctx.guild.name
    await ctx.send(f"This server's name is: {server_name}")


jarvis.run(decouple.config('TOKEN'))