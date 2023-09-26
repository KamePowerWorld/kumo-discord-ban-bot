import os
import discord
import datetime
import yaml
import traceback
from discord.ext import commands
from discord import Embed
from discord import Intents, Client, Interaction, Message
from discord.app_commands import CommandTree
from dotenv import load_dotenv
load_dotenv()
switch = False
class Feedback(discord.ui.Modal, title='BAN理由入力フォーム',):
    name = discord.ui.TextInput(
        label='BAN理由を指定してください。',
        placeholder='',
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'正常にBANできました。理由: {self.name.value}!', ephemeral=True)
        global target_id
        global target_thread_id
        global guild_id
        global ban_user
        global ban_bytext
        ban_text = self.name.value
        target_channel = client.get_channel(target_id)
        target_thread = target_channel.get_thread(target_thread_id)
        if target_thread is None:
            target = target_channel
        else:
            target = target_thread

        banned_by = None


        now = datetime.datetime.now()
        embed = Embed(
            type="rich",
            title="",
            description=f"{ban_user.mention} をBANしました",
            color=0xff0000,
            timestamp=now
        )
        embed.timestamp = now
        embed.add_field(name="ID", value=ban_user.id, inline=False)  
        if isinstance(ban_user, discord.Member) and ban_user.nick is not None :
            embed.add_field(name="ニックネーム", value=ban_user.nick, inline=False)
        elif isinstance(ban_user, discord.Member) and ban_user.name is not None :
            embed.add_field(name="ニックネーム", value=ban_user.name, inline=False)
        else:
            embed.add_field(name="ニックネーム", value="不明", inline=False)
        embed.add_field(name='BAN理由', value=ban_text, inline=False)

        embed.add_field(name='補足メッセージ', value=ban_bytext, inline=False)
        embed.set_thumbnail(url=ban_user.display_avatar.url)
        embed.set_author(name="BAN者情報", icon_url=ban_user.display_avatar.url)
        embed.set_footer(text=interaction.user, icon_url=banned_by)
        await target.send(embed=embed)


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

class MyClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self):
        global target_id
        global guild_id
        global target_thread_id
        global rollid
        print(f'Logged in as {client.user.name}')
        

        config = load_config()
        guild_id = config.get('guild_id', None)
        target_id = config.get('target_id', None)
        target_thread_id = config.get('target_thread_id', None)
        rollid =config.get("rollid", None)
        if guild_id:
            guild = client.get_guild(guild_id)
            
            if guild:
                await guild.chunk()


intents = Intents.default()
intents.bans = True  # BANイベントを有効化
intents.members = True
client = MyClient(intents=intents)

def load_config():
    with open('config.yml', 'r') as config_file:
        return yaml.load(config_file, Loader=yaml.SafeLoader)


@client.tree.context_menu(name="このメッセージを利用してBANする。")
async def greeting(interaction: Interaction, message: Message):  # original_messageをmessageに変更
    global rollid
    member = interaction.user.roles  # interaction.memberは通常、Memberオブジェクトを返すはずです。
    # rollidがmemberの中のどれかのロールのIDと一致するかをチェック
    has_role = any(role.id == rollid for role in member)
    if not has_role:
        await interaction.response.send_message('これを実行する権限がありません。', ephemeral=True)
        return
    else:
        await interaction.response.send_modal(Feedback())
        global ban_bynamedisplay_avatarurl
        global ban_user
        global ban_bytext
        global switch
        ban_user = message.author  # original_messageをmessageに変更
        ban_bynamedisplay_avatarurl = message.author.display_avatar.url  # original_messageをmessageに変更

        found_message = None

        for channel in interaction.guild.text_channels:
            try:
                # メッセージIDを使用してメッセージを取得
                msg = await channel.fetch_message(message.id)  # original_messageをmessageに変更
                if msg:  # メッセージが見つかった場合
                    found_message = msg
                    break
            except:
                # メッセージが見つからない場合は、次のチャンネルに進む
                continue

        if found_message:
            ban_bytext = found_message.content
        else:
            ban_bytext = "メッセージが見つかりませんでした。"
        # ギルド（サーバー）を取得
        
        guild = interaction.guild

        # ユーザーIDを使ってユーザーオブジェクトを取得
        user = await guild.fetch_member(message.author.id)

        # ユーザーをBAN
        switch = True
        await guild.ban(user, reason="")
        switch = False

@client.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    global target_id
    global target_thread_id
    global guild_id
    global switch
    if switch == True:
        return

    if guild.id != guild_id:
        return
    now = datetime.datetime.now()
    target_channel = client.get_channel(target_id)
    target_thread = target_channel.get_thread(target_thread_id)
    if target_thread is None:
        target = target_channel
    else:
        target = target_thread

    banned_by = None

    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        if entry.target == user:
            banned_by = entry.user
            break

    if target:
        if banned_by.name is not None:
            banned_by_name = banned_by.name  # banned_by.nameがNoneでない場合に名前を取得
        else:
            banned_by_name = "不明"  # がNoneの場合、"不明"として設定

        embed = discord.Embed(
            title=f"{banned_by_name}",
            color=discord.Color.red()  # 赤色
        )

        embed.timestamp = now
        embed = Embed(
            type="rich",
            title="",
            description=f"{user.mention} をBANしました",
            color=0xff0000,
            timestamp=now
        )

        embed.add_field(name="ID", value=user.id, inline=False)  
        if isinstance(user, discord.Member) and user.nick is not None :
            embed.add_field(name="サーバーニックネーム", value=user.nick, inline=False)
        elif isinstance(user, discord.Member) and user.name is not None :
            embed.add_field(name="サーバーニックネーム", value=user.name, inline=False)
        else:
            embed.add_field(name="サーバーニックネーム", value="不明", inline=False)
        ban_entry = await guild.fetch_ban(user)
        ban_reason = ban_entry.reason if ban_entry.reason else '不明'
        embed.add_field(name='BAN理由', value=ban_reason, inline=False)

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_author(name="Member Banned", icon_url=user.display_avatar.url)
        embed.set_footer(text=banned_by_name, icon_url=banned_by.display_avatar.url)
        await target.send(embed=embed)

token = os.environ["DISCORD_TOKEN"]
client.run(token)
