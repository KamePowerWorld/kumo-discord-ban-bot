import os
import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.bans = True  # BANイベントを有効化
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
async def on_member_ban(guild, user):
    # 特定のチャンネルIDを設定
    target_channel_id = 1126060676989849712
    banned_by = None

    # 現在の日付と時間を取得
    now = datetime.datetime.now()

    # 特定のチャンネルにメッセージを送信
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        await target_channel.send(f'{now}')
    
    # BAN理由を取得
    ban_entry = await guild.fetch_ban(user)
    ban_reason = ban_entry.reason if ban_entry.reason else "理由は提供されていません。"
    
    # 特定のチャンネルにメッセージを送信
    target_channel = bot.get_channel(target_channel_id)
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        banned_by = entry.user
        break
    
    if target_channel:
        await target_channel.send(f'{user.name} がBANされました。BANした人: {banned_by.name if banned_by else "不明"}')
    
    # BANされたユーザーのIDを取得
    banned_user_id = user.id
    
    # 特定のチャンネルにメッセージを送信
    if target_channel:
        await target_channel.send(f'ユーザーID {banned_user_id} ')
    # BAN理由を取得
    ban_entry = await guild.fetch_ban(user)
    ban_reason = ban_entry.reason if ban_entry.reason else "理由は提供されていません。"
    
    # 特定のチャンネルにメッセージを送信
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        await target_channel.send(f'理由: {ban_reason}')


token = os.environ["DISCORD_TOKEN"]
bot.run(token)
