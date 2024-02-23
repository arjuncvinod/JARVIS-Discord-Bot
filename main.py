import discord
import decouple
import openai
from discord.ext import commands
import time

jarvis = commands.Bot(command_prefix="/", intents=discord.Intents.all())

openai.api_key = decouple.config('OPENAI_API_KEY')

def generate_app_ideas(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def trimmsg(text):
    return text[:1800]

@jarvis.event
async def on_ready():
    activity = discord.Game(name="Grand Theft Auto VI")
    await jarvis.change_presence(activity=activity)
    print(f'Logged in as {jarvis.user.name}')

@jarvis.event
async def on_member_join(member):
    welcome_channel = jarvis.get_channel(894996143862329395)
    welcome_message = f"Welcome to the server {member.name} 🤗"
    message_to_member = f"Welcome to {member.guild.name}"
    await welcome_channel.send(welcome_message)
    await member.send(message_to_member)

@jarvis.event
async def on_message(message):
    if message.author.bot:
        return
    await message.add_reaction("❤️")
    async with message.channel.typing():
        try:
            response = generate_app_ideas(message.content)
        except openai.error.OpenAIError as e:
            if "rate limit" in str(e).lower():
                print(f"Rate limiting detected. Retrying in 60 seconds.")
                time.sleep(60)
                response = generate_app_ideas(message.content)
            else:
                print(f"OpenAI Error: {e}")
                response = "An error occurred."

        await message.reply(trimmsg(response))

@jarvis.command()
async def servername(ctx):
    server_name = ctx.guild.name
    await ctx.send(f"This server's name is: {server_name}")

jarvis.run(decouple.config('TOKEN'))
