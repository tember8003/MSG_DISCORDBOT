import discord, pytz, datetime
from discord.ext import commands,tasks
from itertools import cycle
from discord.utils import get

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all()) #명령어

DISCORD_CHANNEL_ID = 1330808882993561703
DISCORD_BOT_TOKEN = ''
#토큰,서버아이디

user_role = ""
bot_status = cycle(["멍때리기", "밥먹기", "게임", "열심히 코딩","열심을 다해 쉬기"])
ROLE_EMOJI_DIC={"\U00000031\U000020E3":"***명지대학교***","\U00000032\U000020E3":"***00대학교***","\U00000033\U000020E3":"***00대학교***"}

@tasks.loop(seconds=300)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@bot.event
async def on_ready():
    print("Bot is connecting to Discord")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    change_status.start()
    if channel is None:
        channel.send('NO CHANNEL')
        return
    await channel.send('CONNECTED')

@bot.event
async def on_message(message):
    if message.content == "/우승자":
        embed = discord.Embed(title="코딩 대회 우승자", timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x00ff00)
        embed.add_field(name="유저네임",value=":trophy: 제 1회 우승자",inline=False)
        embed.add_field(name="유저네임",value=":trophy: 제 2회 우승자",inline=False)
        embed.add_field(name="유저네임",value=":trophy: 제 3회 우승자",inline=False)
        embed.set_thumbnail(url="https://tecoble.techcourse.co.kr/static/348a6c1ea3a4fa8b6990e3e3bf4e8490/20435/sample2.png")
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        await message.channel.send (embed=embed)

    if message.content.startswith ("/공지"):
        i = (message.author.guild_permissions.send_messages)
        if i is True:
            notice = message.content[4:]
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            embed = discord.Embed(title="***[역할 선택]***",description="학교에 맞는 이모지를 선택 해주시기 바랍니다\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(notice),color=0x00ff00)
            embed.set_footer(text="TITLE | 담당관리자:".format(message.author))
            await channel.send("@everyone", embed=embed)
        if i is False:
            await message.channel.send("{}, 당신은 관리자가 아닙니다.".format(message.author))

    if message.content == "/역할공지":
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        embed = discord.Embed(title="***역할지급***",description="아래 이모티콘을 클릭하여 역할을 받으세요! \n\n"+"\n".join([f"{emoji} : {role}"for emoji, role in ROLE_EMOJI_DIC.items()]),color=discord.Color.blue())
        ctx = await message.channel.send(embed=embed)
        for emoji in ROLE_EMOJI_DIC.keys():
            try:
                await ctx.add_reaction(emoji)
            except discord.HTTPException as e:
                print("ERROR")

@bot.event
async def on_raw_reaction_add(payload):
    pass

bot.run(DISCORD_BOT_TOKEN)