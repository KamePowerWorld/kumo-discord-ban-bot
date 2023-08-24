import os
import discord
from discord.ext import commands
import yaml
import asyncio

intents = discord.Intents.default()
intents.bans = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_config():
    with open('config.yml', 'r') as config_file:
        return yaml.load(config_file, Loader=yaml.SafeLoader)

user_reaction_counts = {}
user_timeout = {}

@bot.event
async def on_ready():
    #開発者の隠しメッセージ
    print(f'くもぱわ～ {bot.user.name}が起動しました。')

@bot.event
async def on_reaction_add(reaction, user):
    config = load_config()
    target_channel_id = config['action_BotConfig']['id']
    message = reaction.message
    user_id = user.id
    max_reaction_count = config['action_BotConfig']['count']
    timeout_seconds = config['action_BotConfig']['timeout']

    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        if reaction.count > 1:
            # 既存のリアクションに対しては常に許可
            return
        
        if user_reaction_counts.get(user_id, 0) >= max_reaction_count:
            await message.remove_reaction(reaction.emoji, user)

            if user_id not in user_timeout:
                user_timeout[user_id] = True
                await asyncio.sleep(timeout_seconds)
                user_timeout.pop(user_id, None)
                
            return
        
        # 新規リアクションのみをカウント
        if reaction.count == 1:
            if user_id not in user_reaction_counts:
                user_reaction_counts[user_id] = 0
            user_reaction_counts[user_id] += 1


        
token = os.environ["DISCORD_TOKEN"]
bot.run(token)
