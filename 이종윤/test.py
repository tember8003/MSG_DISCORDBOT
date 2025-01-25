import discord
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
API_KEY = os.getenv('API_KEY')
class MyClient(discord.Client):
    async def on_ready(self): #비동기 통신 처리
        print(f'Logged in as {self.user}')
        try:
            channel = await self.fetch_channel(int(CHANNEL_ID))
            await channel.send('Hello World')
            print(f'Message sent to channel ID {CHANNEL_ID}')
        except discord.NotFound:
            print(f'채널 ID {CHANNEL_ID}을(를) 찾을 수 없음.')
        except discord.Forbidden:
            print('봇에게 해당 채널에 메시지를 보낼 권한이 없음.')
        except discord.HTTPException as e:
            print(f'메시지 전송 중 오류 발생: {e}')

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)



