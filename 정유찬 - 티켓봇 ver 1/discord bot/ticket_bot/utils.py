import os
from datetime import datetime

async def save_log(channel,user_name):
    # 로그 기록 저장
    log_content = ""
    async for msg in channel.history(limit=None, oldest_first=True):
        log_content += f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.author}: {msg.content}\n"

    # 로그 폴더가 없는 경우 생성 (나중에 필요 없음)
    if not os.path.exists("ticket_logs"):
        os.makedirs("ticket_logs")

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # 날짜 및 시간 포맷    
    log_filename = f"ticket_logs/{user_name}_{current_time}.txt"
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(log_content)
    
    return log_filename