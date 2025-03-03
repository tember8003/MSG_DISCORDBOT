import discord
from datetime import datetime
import os
import asyncio
from ticket_bot.utils import save_log

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 뷰에 timeout 없음
        self.add_item(CreateTicketButton())

class CreateTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📩 티켓 생성", style=discord.ButtonStyle.blurple, custom_id="create_ticket")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild

        # 카테고리 가져오기 또는 생성
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        # 사용자별 티켓 채널 확인
        existing_channel = discord.utils.get(
            category.text_channels,
            name=f"ticket-{interaction.user.id}"
        )
        if existing_channel:
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

        # "운영진" 역할 가져오기 -> 없으면 실패
        admin_role = discord.utils.get(guild.roles, name="운영진")
        if not admin_role:
            await interaction.response.send_message(
                "❗ '운영진' 역할을 찾을 수 없습니다. 관리자가 역할을 설정해야 합니다.", ephemeral=True
            )
            return

        # 권한 설정
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.me, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)  # 기본 역할 권한 제거
        await channel.set_permissions(admin_role, read_messages=True, send_messages=True)  # 운영진 권한 추가

        # 자동화된 초기 메시지 전송
        embed = discord.Embed(
            title="🎫 티켓 생성됨",
            description=(
                "티켓이 성공적으로 생성되었습니다. 문제가 있다면 여기에 메시지를 남겨주세요.\n\n"
                "운영진이 티켓을 확인할 수 있습니다."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="티켓을 종료하면 대화 로그가 저장됩니다.")
        
        # Close Ticket 버튼 포함
        view = CloseTicketView()
        await channel.send(embed=embed, view=view)

        # 사용자에게 응답 (개인화된 메시지)
        embed_response = discord.Embed(
            title="✅ 티켓이 생성되었습니다!",
            description=f"새로운 티켓이 성공적으로 생성되었습니다: {channel.mention}\n티켓 채널에서 대화를 할 수 있습니다!",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed_response, ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())

class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔒 티켓 종료 (Close Ticket)", style=discord.ButtonStyle.red, custom_id="close_ticket")

    async def callback(self, interaction: discord.Interaction):
        category = interaction.channel.category

        user_name = interaction.user.name  # 티켓을 생성한 유저 이름
        log_content = await save_log(interaction.channel,user_name) #나중을 위해 return 값 받아옴. 하지만 현재로선 쓸 곳 없음

        # Interaction 응답 - 사용자가 해당 채널에서 볼 수 있는 메시지
        await interaction.response.send_message(
            "티켓 채널이 성공적으로 종료되었습니다. 필요 시 다시 생성해주세요!", ephemeral=True
        )

        # 1.5초 지연
        await asyncio.sleep(1.5)

        # 채널 삭제
        await interaction.channel.delete()

        # 카테고리 삭제
        if category and not category.text_channels:
            await category.delete()

        ''' 개인 태그 후 알림 메시지 전송 (예: @정유찬 티켓이 성공적으로 종료되었습니다. 필요 시 다시 생성해주세요!)
        # CHANNEL_ID로 알림 메시지 전송
        guild = interaction.guild
        channel = guild.get_channel(int(os.getenv("CHANNEL_ID")))  # CHANNEL_ID 가져오기
        if channel:
            await channel.send(
                content=f"{interaction.user.mention}, 티켓이 성공적으로 종료되었습니다. 필요 시 다시 생성해주세요!"
            )
        else:
            print(f"지정된 CHANNEL_ID({os.getenv('CHANNEL_ID')})가 유효하지 않습니다.")
        '''