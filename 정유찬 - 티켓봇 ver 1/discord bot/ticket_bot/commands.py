import discord
from ticket_bot.viewUI import TicketView

def setup_commands(bot):
    @bot.tree.command(name="티켓", description="티켓 생성 버튼을 표시합니다.")
    async def ticket(interaction: discord.Interaction):
        view = TicketView()
        await interaction.response.send_message("티켓 생성을 위해 아래 버튼을 눌러주세요!", view=view, ephemeral=True)

    @bot.tree.command(name="티켓_도움말", description="티켓 사용법을 안내드립니다.")
    async def help_bot(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎟️ 티켓 사용 방법",
            description=(
                "**티켓 사용 가이드**\n\n"
                "1. `/티켓` 명령어를 입력해 티켓 생성 버튼을 표시합니다! \n"
                "2. `📩 티켓 생성` 버튼을 눌러 티켓 채널을 만듭니다.\n"
                "3. 생성된 티켓 채널 안에서 운영진과 대화를 할 수 있습니다!\n"
                "-💬 질문, 요청 등 운영진과 소통해야 할 대화가 있으시다면 티켓 봇을 통해 대화해주세요!!\n"
                "4. `🔒 티켓 종료` 버튼을 눌러 티켓을 종료할 수 있습니다.\n\n"
                "티켓 종료 시, 대화 내용이 저장되고 채널이 삭제됩니다."
            ),
            color=discord.Color.blurple()
        )
        embed.set_footer(text="다른 추가 질문이 있다면 운영진에게 문의해주세요!")
        await interaction.response.send_message(embed=embed, ephemeral=True)