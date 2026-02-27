# tg_auto_send.py - GitHub Actions专用发送脚本
from pyrogram import Client
import os
from datetime import datetime

# 从GitHub Secrets读取配置
def get_secret(secret_name):
    value = os.getenv(secret_name)
    if not value:
        print(f"❌ 未配置{secret_name}")
        exit(1)
    return value

# 核心配置（从Secrets读取）
API_ID = get_secret("TG_API_ID")
API_HASH = get_secret("TG_API_HASH")
SESSION_STRING = get_secret("TG_SESSION_STRING")
TARGET_USER = get_secret("TG_TARGET_USER")
MESSAGE = get_secret("TG_MESSAGE", required=False) or "/checkin"

def send_checkin_message():
    """发送签到消息"""
    try:
        # 初始化客户端（用session string，无需本地文件/代理）
        app = Client(
            name="github_actions_session",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING  # 用你导出的session string
        )

        # 登录并发送消息（GitHub境外环境，无需代理）
        app.start()
        if app.is_connected:
            app.send_message(TARGET_USER, MESSAGE)
            print(f"✅ [{datetime.now()}] 签到消息发送成功！")
            print(f"   接收者：{TARGET_USER} | 内容：{MESSAGE}")
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
