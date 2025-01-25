import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from flask import Flask, request, jsonify
import logging
import asyncio
import threading

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
API_KEY = os.getenv('API_KEY')
logging.basicConfig(level=logging.INFO)
# Discord 봇의 인텐트 설정
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello, Discordbot Test!"
ALLOWED_IPS = ['192.168.0.2','127.0.0.1']
@app.route('/send', methods=['POST'])
def send_message():
    try:
        client_ip = request.remote_addr
        if client_ip not in ALLOWED_IPS:
            logging.warning(f'Unauthorized IP: {client_ip}')
            return jsonify({'error': 'Forbidden'}), 403
        received_api_key=request.headers.get('X-API-Key')
        if received_api_key!=API_KEY:
            logging.WARNING('API키가 실패하였습니다!')
            return jsonify({'error': '인증실패'}), 401
        data=request.get_json()
        mesasage=['first_blood_problem','first_blood_person','first_blood_school']
        for m in mesasage:
            if not data or m not in data :
                return jsonify({'error': '메시지가 존재하지 않습니다.'}), 400
        first_blood_problem=data['first_blood_problem']
        first_blood_person=data['first_blood_person']
        first_blood_school=data['first_blood_school']
        message=f"problem:{first_blood_problem}-{first_blood_school}:{first_blood_person}님"
        
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                    title='First Blood',
                    description=first_blood_problem,
                    color=int('3498db', 16)
                    )
            embed.add_field(
                name=first_blood_person,
                value=first_blood_school,
                inline=False
            )
            asyncio.run_coroutine_threadsafe(channel.send(message, embed=embed), bot.loop)
            logging.info(f'Message sent to channel ID {CHANNEL_ID}')
            return jsonify({'status':'메시지가 전송됨'}), 200
        else:
            logging.error(f'Channel ID:{CHANNEL_ID}를 찾을 수 없음')
            return jsonify({'error':'채널을 찾을 수 없음'}),404
        #return jsonify({'first_blood':f"problem:{first_blood_problem}-{first_blood_school}:{first_blood_person}님"})
    except Exception as e:
        logging.exception('Error while processing /send request.')
        return jsonify({'error: str(e)'}), 500

def run_flask():
    app.run(host='0.0.0.0', port=8080,debug=False, use_reloader=False)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
bot.run(TOKEN)