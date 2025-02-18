TOKEN = "DISCORDTOKEN"
ALLOWED_CHANNEL_ID = 1234561235678

import discord
from discord.ext import commands
import subprocess
import re

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return
    if client.user.mentioned_in(message):
        user_prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
    

        if not user_prompt:
            await message.channel.send("no prompt")
            return
        filtered_prompt = f"{user_prompt}. (Keep it short, simple)" # prefilters
        process = subprocess.Popen(["ollama", "run", "deepseek-r1:7b", filtered_prompt], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        decoded_output = output.decode("utf-8").strip()
        cleaned_message = re.sub(r"<think>.*?</think>", "", decoded_output, flags=re.DOTALL).strip() #stripping <think></think>
        await message.reply(cleaned_message[:2000])

client.run(TOKEN)
