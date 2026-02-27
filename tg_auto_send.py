# tg_auto_send.py - 修复版
from pyrogram import Client
import os
from datetime import datetime

def get_secret(secret_name, required=True):
    value = os.getenv(secret_name)
    if required and not value:
        print(f"❌ 未配置{secret_name}")
        exit(1)
    return value

# 核心配置（从Secrets读取）
API_ID = get_secret("TG_API_ID")
API_HASH = get_secret("TG_API_HASH")
SESSION_STRING = get_secret("TG_SESSION_STRING")
TARGET_USER = get_secret("TG_TARGET_USER")
MESSAGE = get_secret("TG_MESSAGE", required=False) or "/checkin"  # 现在可以用required=False了

def send_checkin_message():
    try:
        app = Client(
            name="github_actions_session",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING
        )
        app.start()
        if app.is_connected:
            app.send_message(TARGET_USER, MESSAGE)
            print(f"✅ [{datetime.now()}] 签到消息发送成功！")
            app.stop()
            return True
        else:
            print("❌ 客户端未连接")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 启动GitHub Actions Telegram签到脚本...")
    send_checkin_message()
    print("📤 脚本执行完成")
