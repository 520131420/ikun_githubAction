# Telegram 自动签到脚本
## 功能
- 每天在指定时段内随机时间发送签到消息
- 基于GitHub Actions运行，无需本地部署

## 使用方法
### 1. Fork本仓库
### 2. 配置GitHub Secrets
在仓库 → Settings → Secrets and variables → Actions 中添加以下Secrets：
| Secret名称 | 说明 | 示例 |
|------------|------|------|
| TG_API_ID | 你的TG API ID（从my.telegram.org获取） | 12345678 |
| TG_API_HASH | 你的TG API HASH | abc123def456ghi789 |
| TG_SESSION_STRING | 你的TG Session String（本地导出） | 1BVtsOJkXxxxx... |
| TG_TARGET_USER | 目标机器人/用户 | @iKuuuu_VPN_bot |
| TG_MESSAGE | 发送的消息 | /checkin |
| MIN_DELAY_MINUTES | 最小延迟分钟数（可选） | 0 |
| MAX_DELAY_MINUTES | 最大延迟分钟数（可选） | 30 |

### 3. 触发运行
- 手动触发：Actions → Telegram Auto Checkin → Run workflow
- 定时触发：默认每天北京时间9:00触发（可修改yml中的cron）

## 安全提示
- 切勿将Secrets信息硬编码到代码中
- 定期更换Session String
- 不要分享你的API ID/HASH和Session String
