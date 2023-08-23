import os
import discord
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # 起動時にメッセージを送信するチャンネルIDを設定
    startup_channel_id = 1126060676989849712  # ここにチャンネルIDを入力
    
    startup_channel = bot.get_channel(startup_channel_id)
    if startup_channel:
        await startup_channel.send('くもぱわ～BANBOTが起動しました。')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 自身のメッセージは無視

        # 通知するチャンネルのIDを指定
    # メッセージリンクの正規表現パターン
    link_pattern = r'https://discord\.com/channels/\d+/\d+/\d+'
    matches = re.findall(link_pattern, message.content)

    for link in matches:
        link_parts = link.split('/')
        if len(link_parts) == 7:  # 正しいリンク形式である場合
            guild_id = int(link_parts[4])
            channel_id = int(link_parts[5])
            message_id = int(link_parts[6])

            try:
                guild = bot.get_guild(guild_id)
                channel = guild.get_channel(channel_id)
                msg = await channel.fetch_message(message_id)

                # メッセージを通知するチャンネルに送信
                notify_channel = bot.get_channel(1126060676989849712)  # 通知先のチャンネルIDを指定
                await notify_channel.send(f"-> {msg.content}")
            except Exception as e:
                print(f"Error: {e}")

    await bot.process_commands(message)

token = os.environ["DISCORD_TOKEN"]
bot.run(token)
