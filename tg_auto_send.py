# -*- coding: utf-8 -*-
import os
import random
import time
import pytz
from datetime import datetime, timedelta
from pyrogram import Client

# -------------------------- 配置项（可直接修改） --------------------------
# 细粒度随机等待范围：0~300秒（0~5分钟）
MIN_WAIT_SECONDS = 0
MAX_WAIT_SECONDS = 300

# -------------------------- 工具函数 --------------------------
def get_env(key, required=True, default=None):
    """读取环境变量，带必填校验"""
    value = os.getenv(key)
    if required and not value:
        print(f"❌ 环境变量 {key} 未配置")
        exit(1)
    return value if value else default

# -------------------------- 核心逻辑 --------------------------
def fine_grained_random_wait():
    """细粒度随机等待（适配窗口剩余时间）"""
    # 配置时区（北京时间）
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz)
    
    # 读取目标窗口信息（从YAML传递）
    target_hour = int(get_env("TARGET_HOUR", required=False, default=now.hour))
    window_start = int(get_env("TARGET_WINDOW_START", required=False, default=0))
    window_end = int(get_env("TARGET_WINDOW_END", required=False, default=59))
    
    # 二次校验：确保当前时间在目标窗口内（兜底）
    if now.hour != target_hour or not (window_start <= now.minute <= window_end):
        print("⚠️  当前时间不在目标窗口内，立即发送消息")
        return
    
    # 计算窗口剩余秒数（避免等待超时）
    current_minute = now.minute
    remaining_window_seconds = max(0, (window_end - current_minute) * 60)
    
    # 最大等待时间 = 配置的最大值 和 窗口剩余时间 的较小值
    actual_max_wait = min(MAX_WAIT_SECONDS, remaining_window_seconds)
    
    # 窗口末尾直接发送
    if actual_max_wait <= 0:
        print("⏭ 已接近窗口末尾，立即发送消息")
        return
    
    # 用当日日期做种子，确保当天随机时间固定（避免重复触发时等待时间不同）
    date_seed = int(now.strftime("%Y%m%d"))
    random.seed(date_seed)
    
    # 生成随机等待秒数
    wait_seconds = random.randint(MIN_WAIT_SECONDS, actual_max_wait)
    send_time = now + timedelta(seconds=wait_seconds)
    
    # 打印随机信息
    print(f"\n🎲 细粒度随机配置：")
    print(f"   当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   目标窗口：{target_hour}点 {window_start}-{window_end}分")
    print(f"   窗口剩余：{remaining_window_seconds} 秒")
    print(f"   随机等待：{wait_seconds} 秒（{wait_seconds/60:.1f} 分钟）")
    print(f"   预计发送：{send_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 分段等待（每10秒打印一次进度，避免无响应）
    print(f"\n⏳ 等待发送中...（按Ctrl+C可终止）")
    remaining = wait_seconds
    while remaining > 0:
        step = min(10, remaining)
        print(f"   剩余 {remaining} 秒", end="\r")
        time.sleep(step)
        remaining -= step
    print("\n✅ 等待完成，开始发送消息！")

def send_tg_message():
    """发送Telegram消息"""
    try:
        # 初始化TG客户端
        app = Client(
            name="smart_random_session",
            api_id=get_env("TG_API_ID"),
            api_hash=get_env("TG_API_HASH"),
            session_string=get_env("TG_SESSION_STRING")
        )
        
        # 连接并发送消息
        app.start()
        if app.is_connected:
            target_user = get_env("TG_TARGET_USER")
            message = get_env("TG_MESSAGE", required=False, default="/checkin")
            
            # 发送消息
            app.send_message(target_user, message)
            
            # 打印成功日志
            now = datetime.now(pytz.timezone("Asia/Shanghai"))
            print(f"\n✅ [{now.strftime('%Y-%m-%d %H:%M:%S')}] 消息发送成功！")
            print(f"   接收对象：{target_user}")
            print(f"   消息内容：{message}")
            
            app.stop()
            return True
        else:
            print("❌ Telegram客户端连接失败")
            return False
    
    except Exception as e:
        print(f"\n❌ 消息发送失败：{str(e)}")
        return False

# -------------------------- 主函数 --------------------------
if __name__ == "__main__":
    print("="*50)
    print("🚀 启动 Telegram 智能随机签到脚本")
    print("="*50)
    
    # 第一步：细粒度随机等待
    fine_grained_random_wait()
    
    # 第二步：发送消息
    send_success = send_tg_message()
    
    # 第三步：退出状态（0=成功，1=失败）
    print("\n" + "="*50)
    if send_success:
        print("📤 脚本执行完成（成功）")
        exit(0)
    else:
        print("❌ 脚本执行完成（失败）")
        exit(1)
