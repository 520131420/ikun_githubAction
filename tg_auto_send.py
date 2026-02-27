# tg_auto_send.py - 支持随机时间发送
from pyrogram import Client
import os
import random
import time
from datetime import datetime, timedelta

# 从GitHub Secrets读取配置（修复required参数）
def get_secret(secret_name, required=True):
    value = os.getenv(secret_name)
    if required and not value:
        print(f"❌ 未配置{secret_name}")
        exit(1)
    return value

# -------------------------- 随机时间配置（可自定义） --------------------------
# 配置1：随机延迟范围（单位：分钟）- 比如0-30分钟 → 9:00-9:30之间随机发送
MIN_DELAY_MINUTES = 0    # 最小延迟（分钟）
MAX_DELAY_MINUTES = 300  # 最大延迟（分钟）

# 配置2：可选 - 固定时段（如希望在9:00-10:00之间随机，可启用此配置）
# TARGET_HOUR_START = 9   # 起始小时
# TARGET_HOUR_END = 10     # 结束小时

def random_delay():
    """生成随机延迟并等待，输出预计发送时间"""
    # 方案1：基于延迟分钟数（推荐）
    # 生成0-300分钟之间的随机秒数
    delay_minutes = random.uniform(MIN_DELAY_MINUTES, MAX_DELAY_MINUTES)
    delay_seconds = int(delay_minutes * 60)
    
    # 方案2：基于固定时段（如需启用，注释方案1，取消注释方案2）
    # now = datetime.now()
    # start_time = now.replace(hour=TARGET_HOUR_START, minute=0, second=0, microsecond=0)
    # end_time = now.replace(hour=TARGET_HOUR_END, minute=0, second=0, microsecond=0)
    # random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
    # delay_seconds = random_seconds - int((now - start_time).total_seconds())
    # if delay_seconds < 0:
    #     delay_seconds = 0

    # 计算预计发送时间
    send_time = datetime.now() + timedelta(seconds=delay_seconds)
    print(f"\n🎲 随机延迟配置：")
    print(f"   延迟时长：{delay_seconds // 60}分{delay_seconds % 60}秒")
    print(f"   预计发送时间：{send_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 开始等待（显示倒计时，可选）
    print(f"\n⏳ 等待发送...（按Ctrl+C终止）")
    for i in range(delay_seconds, 0, -1):
        print(f"   剩余 {i // 60}分{i % 60}秒", end="\r")
        time.sleep(1)
    print("\n✅ 延迟结束，开始发送消息！")

# -------------------------- 核心配置 --------------------------
API_ID = get_secret("TG_API_ID")
API_HASH = get_secret("TG_API_HASH")
SESSION_STRING = get_secret("TG_SESSION_STRING")
TARGET_USER = get_secret("TG_TARGET_USER")
MESSAGE = get_secret("TG_MESSAGE", required=False) or "/checkin"

def send_checkin_message():
    """发送签到消息"""
    try:
        # 初始化客户端（GitHub境外环境，无需代理）
        app = Client(
            name="github_actions_session",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING
        )

        # 登录并发送消息
        app.start()
        if app.is_connected:
            app.send_message(TARGET_USER, MESSAGE)
            print(f"\n✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 消息发送成功！")
            print(f"   接收者：{TARGET_USER}")
            print(f"   内容：{MESSAGE}")
            app.stop()
            return True
        else:
            print("❌ 客户端未连接成功")
            return False

    except Exception as e:
        print(f"\n❌ 发送失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 启动Telegram随机时间发送脚本...")
    print(f"📅 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 第一步：执行随机延迟（核心！）
    random_delay()
    
    # 第二步：发送消息
    send_checkin_message()
    
    print("\n📤 脚本执行完成")
