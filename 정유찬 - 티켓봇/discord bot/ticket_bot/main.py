import discord
from discord.ext import commands
from ticket_bot import TOKEN,setup_commands,TicketView,setup_handlers

class TicketBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 명령어 및 핸들러 설정
        setup_commands(self)
        setup_handlers(self)

        # 글로벌 명령어 동기화
        await self.tree.sync()
        print("Slash commands synced globally!")

bot = TicketBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: TOKEN not found in environment variables.")