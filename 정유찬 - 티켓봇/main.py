import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import os

# 로그 폴더가 없는 경우 생성
if not os.path.exists("ticket_logs"):
    os.makedirs("ticket_logs")

# .env 파일에서 TOKEN과 CHANNEL_ID 로드
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 뷰에 timeout 없음
        self.add_item(CreateTicketButton())

class CreateTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📩 티켓 생성", style=discord.ButtonStyle.blurple, custom_id="create_ticket")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")
        
        # 사용자별 티켓 채널 확인
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.id}")
        if existing_channel:
            # 기존 채널에 "Close Ticket" 버튼 추가
            embed = discord.Embed(
                title="❗ 이미 티켓이 존재합니다",
                description=(
                    f"이미 생성된 티켓이 있습니다: {existing_channel.mention}\n"
                    "해당 티켓에서 문제를 해결하거나 아래 버튼을 눌러 티켓을 종료하세요."
                ),
                color=discord.Color.red()
            )
            view = CloseTicketView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            return

        # 새 티켓 채널 생성
        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.id}",
            category=category
        )
        
        # 권한 설정 (봇과 사용자 모두)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.me, read_messages=True, send_messages=True)  # 봇 권한 추가
        await channel.set_permissions(guild.default_role, read_messages=False)  # @everyone 권한 제거

        # 자동화된 초기 메시지 전송
        embed = discord.Embed(
            title="🎫 티켓 생성됨",
            description=(
                "티켓이 성공적으로 생성되었습니다. 문제가 있다면 여기에 메시지를 남겨주세요.\n\n"
                "아래의 **'Close Ticket' 버튼**을 눌러 티켓을 종료할 수 있습니다."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="티켓을 종료하면 대화 로그가 저장됩니다.")
        
        # Close Ticket 버튼 포함
        view = CloseTicketView()
        await channel.send(embed=embed, view=view)

        # 사용자에게 응답
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)



class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())

class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔒 티켓 종료 (Close Ticket)", style=discord.ButtonStyle.red, custom_id="close_ticket")

    async def callback(self, interaction: discord.Interaction):
        category = interaction.channel.category
        if category and category.name.lower() == "tickets":
            # 로그 기록
            log_content = ""
            async for msg in interaction.channel.history(limit=None, oldest_first=True):
                log_content += f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.author}: {msg.content}\n"

            log_filename = f"ticket_logs/ticket-{interaction.channel.name}.txt"

            # 로그 파일 저장
            with open(log_filename, "w", encoding="utf-8") as f:
                f.write(log_content)

            await interaction.response.send_message("티켓을 종료합니다. 대화 로그는 저장되었습니다.", ephemeral=True)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("티켓 채널이 아닙니다!", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(TicketView())  # 티켓 생성 뷰 등록

    # CHANNEL_ID로 지정된 채널에 티켓 생성 버튼 표시
    if CHANNEL_ID:
        try:
            channel = bot.get_channel(int(CHANNEL_ID))
            if channel:
                view = TicketView()
                await channel.send("티켓 생성을 위해 버튼을 눌러주세요!:", view=view)
                print(f"티켓 Setup 메시지 -> {CHANNEL_ID}")
            else:
                print(f"채널 ID {CHANNEL_ID}가 발견되지 않았습니다.")
        except Exception as e:
            print(f"티켓을 만드는데 에러가 발생했습니다...: {e}")
    else:
        print("CHANNEL_ID가 유효하지 않음.")

@bot.command()
async def setup_ticket(ctx):
    """수동 티켓 설정 명령어"""
    view = TicketView()
    await ctx.send("버튼을 클릭해 티켓을 생성하세요!", view=view)

if TOKEN:
    bot.run(TOKEN)
else:
    print("에러: 토큰 설정 안됨.")
