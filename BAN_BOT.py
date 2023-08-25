import os
import discord
import datetime
import yaml
from discord.ext import commands
from discord import Embed

intents = discord.Intents.default()
intents.bans = True  # BANイベントを有効化
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

def load_config():
    with open('config.yml', 'r') as config_file:
        return yaml.load(config_file, Loader=yaml.SafeLoader)
    
@bot.event
async def on_ready():
    global target_id
    global guild_id
    global target_thread_id
    print(f'Logged in as {bot.user.name}')
    

    config = load_config()
    guild_id = config.get('guild_id', None)
    target_id = config.get('target_id', None)
    target_thread_id = config.get('target_thread_id', None)
    if guild_id:
        guild = bot.get_guild(guild_id)
        
        if guild:
            await guild.chunk()

@bot.event
async def on_member_ban(guild:discord.Guild, user:discord.User):
    global target_id
    global target_thread_id
    global guild_id
    if guild.id != guild_id :
        return
    now = datetime.datetime.now()
    target_channel = bot.get_channel(target_id)
    target_thread = target_channel.get_thread(target_thread_id)
    if target_thread is None:
        target = target_channel
    else :
        target = target_thread

    banned_by = None

    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        if entry.target == user:
            banned_by = entry.user
            break
    
    if target:
        if banned_by.name is not None :
            banned_by.name == "不明"
        embed = discord.Embed(                
            title=f"{banned_by.name}",
            color=discord.Color.red()  # 赤色
        )
        
        embed.timestamp=now
        embed = Embed(
            type="rich",
            title="",
            description=f"{user.mention} をBANしました",
            color=0xff0000,
            timestamp=now
        )

        embed.add_field(name="ID", value=user.name, inline=False)
        embed.add_field(name="ニックネーム", value=user.global_name, inline=False)
        if isinstance(user, discord.Member) and user.nick is not None:
            embed.add_field(name="サーバーニックネーム", value=user.nick, inline=False)
        ban_entry = await guild.fetch_ban(user)
        ban_reason = ban_entry.reason if ban_entry.reason else '不明'
        embed.add_field(name='BAN理由', value=ban_reason, inline=False)

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_author(name="Member Banned", icon_url=user.display_avatar.url)
        embed.set_footer(text=banned_by.name, icon_url=banned_by.display_avatar.url)
        await target.send(embed=embed)






token = os.environ["DISCORD_TOKEN"]
bot.run(token)
