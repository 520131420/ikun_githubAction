# tg_auto_send.py - 安全版（无任何硬编码敏感信息）
from pyrogram import Client
import os
import random
import time
from datetime import datetime, timedelta

# 从环境变量读取配置（仅通过GitHub Secrets传递）
def get_secret(secret_name, required=True):
    value = os.getenv(secret_name)
    if required and not value:
        print(f"❌ 环境变量 {secret_name} 未配置")
        exit(1)
    return value

# 随机延迟配置（可公开，无风险）
MIN_DELAY_MINUTES = int(get_secret("MIN_DELAY_MINUTES", required=False) or 0)
MAX_DELAY_MINUTES = int(get_secret("MAX_DELAY_MINUTES", required=False) or 30)

def random_delay():
    """随机延迟，避免固定时间发送"""
    delay_minutes = random.uniform(MIN_DELAY_MINUTES, MAX_DELAY_MINUTES)
    delay_seconds = int(delay_minutes * 60)
    send_time = datetime.now() + timedelta(seconds=delay_seconds)
    
    print(f"\n🎲 随机延迟配置：")
    print(f"   延迟时长：{delay_seconds // 60}分{delay_seconds % 60}秒")
    print(f"   预计发送时间：{send_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n⏳ 等待发送...")
    for i in range(delay_seconds, 0, -1):
        print(f"   剩余 {i // 60}分{i % 60}秒", end="\r")
        time.sleep(1)
    print("\n✅ 延迟结束，开始发送消息！")

def send_message():
    """发送消息（核心逻辑，无硬编码）"""
    try:
        # 核心配置全部从Secrets读取
        app = Client(
            name="github_actions_session",
            api_id=get_secret("TG_API_ID"),
            api_hash=get_secret("TG_API_HASH"),
            session_string=get_secret("TG_SESSION_STRING")
        )

        app.start()
        if app.is_connected:
            # 目标用户和消息也从Secrets读取
            target_user = get_secret("TG_TARGET_USER")
            message = get_secret("TG_MESSAGE", required=False) or "/checkin"
            
            app.send_message(target_user, message)
            print(f"\n✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 消息发送成功！")
            app.stop()
            return True
        else:
            print("❌ 客户端未连接成功")
            return False

    except Exception as e:
        print(f"\n❌ 发送失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 启动Telegram随机时间发送脚本（安全版）")
    print(f"📅 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    random_delay()
    send_message()
    print("\n📤 脚本执行完成")
