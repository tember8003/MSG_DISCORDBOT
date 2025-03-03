import discord
from discord.ext import commands 
from ticket_bot.config import CHANNEL_ID

def setup_handlers(bot: commands.Bot):
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

        # CHANNEL_ID로 지정된 채널에 메시지 전송
        if CHANNEL_ID:
            try:
                channel = bot.get_channel(int(CHANNEL_ID))  # 채널 ID 가져오기
                if channel:
                    await channel.send("봇이 실행되었습니다! `/티켓` 명령어를 사용하여 티켓을 생성하세요.")
                    print(f"안내 메시지 전송 완료 -> 채널 ID: {CHANNEL_ID}")
                else:
                    print(f"유효하지 않은 채널 ID: {CHANNEL_ID}")
            except Exception as e:
                print(f"채널에 메시지를 전송하는 중 에러 발생: {e}")
        else:
            print("CHANNEL_ID가 설정되지 않았습니다.")
    
    @bot.event
    async def on_message(message: discord.Message):
        # 명령어가 아닌 메시지를 무시
        if message.author.bot:
            return
        await bot.process_commands(message)