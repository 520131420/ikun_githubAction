# Telegram 智能随机签到脚本
一款基于 GitHub Actions + Python 实现的 Telegram 自动签到工具，核心特性：**分层随机+低资源消耗+防批量执行**，每个 Fork 用户的执行时间完全独立，避免被风控。

## ✨ 核心优势
1. **双层随机策略**：
   - 粗粒度：每天随机锁定 1 个小时 + 1 个 10 分钟段（如 11:20-11:29）
   - 细粒度：在 10 分钟段内随机等待 0~5 分钟（精准到秒）
2. **极低资源消耗**：每天仅运行 ≈5 分钟，远低于 GitHub 免费额度（2000 分钟/月）
3. **防批量执行**：基于仓库唯一标识生成随机种子，Fork 后每个用户执行时间独立
4. **高稳定性**：发送失败不标记缓存，支持同窗口内重试；超时兜底，避免卡死
5. **灵活配置**：支持自定义执行时间范围、等待时长、发送消息内容

## 🚀 快速部署
### 步骤 1：Fork 本仓库
点击页面右上角 `Fork`，将仓库复制到你的 GitHub 账号下。

### 步骤 2：配置 GitHub Secrets
进入你 Fork 后的仓库 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`，添加以下配置：

| Secret 名称          | 必选 | 说明                                                                 | 示例值                  |
|----------------------|------|----------------------------------------------------------------------|-------------------------|
| `TG_API_ID`          | ✅    | Telegram 开发者 API ID（从 [my.telegram.org](https://my.telegram.org) 获取） | 1234567                 |
| `TG_API_HASH`        | ✅    | Telegram 开发者 API Hash                                             | abcdef1234567890abcdef  |
| `TG_SESSION_STRING`  | ✅    | Telegram 会话字符串（通过 pyrogram 生成）                            | （长字符串）            |
| `TG_TARGET_USER`     | ✅    | 签到目标（机器人 ID/用户名/聊天 ID）                                 | @iKuuuu_VPN_bot         |
| `TG_MESSAGE`         | ❌    | 签到指令（默认：`/checkin`）                                          | /sign                   |
| `BASE_HOUR_START`    | ❌    | 执行小时范围起始（默认：9）                                           | 8                       |
| `BASE_HOUR_END`      | ❌    | 执行小时范围结束（默认：14）                                          | 20                      |
| `RANDOM_SALT`        | ❌    | 随机盐值（增强随机性，可选）                                         | 123456                  |

### 步骤 3：启用 GitHub Actions
1. 进入仓库 → `Actions` → 点击 `I understand my workflows, go ahead and enable them`
2. 选择 `Telegram Auto Checkin (Smart Random)` → 启用工作流

### 步骤 4：测试运行（可选）
进入 `Actions` → `Telegram Auto Checkin (Smart Random)` → `Run workflow` → 点击 `Run workflow`，手动触发测试，查看日志确认是否正常执行。

## ⚙️ 自定义配置
### 1. 调整执行时间范围
#### 方式 1：通过 Secrets 配置（推荐）
- 修改 `BASE_HOUR_START`/`BASE_HOUR_END`，比如设置为 8~20 点：
  - `BASE_HOUR_START`: 8
  - `BASE_HOUR_END`: 20

#### 方式 2：直接修改 YAML 文件
编辑 `.github/workflows/tg_auto_checkin.yml`：
```yaml
env:
  BASE_HOUR_START: ${{ secrets.BASE_HOUR_START || 8 }}  # 起始小时
  BASE_HOUR_END: ${{ secrets.BASE_HOUR_END || 20 }}      # 结束小时
