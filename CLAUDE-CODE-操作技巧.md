# Claude Code 高效操作技巧

个人使用 Claude Code 过程中总结的实用技巧，持续更新。

---

## 一、Slash Commands（斜杠命令）

| 命令 | 作用 | 常用场景 |
|------|------|----------|
| `/help` | 查看帮助 | 忘记命令时 |
| `/clear` | 清空上下文 | 话题切换，避免上下文污染 |
| `/compact` | 压缩上下文 | 对话很长时压缩历史，保留关键信息 |
| `/config` | 打开配置面板 | 修改主题、模型（推荐用 DeepSeek-v4-pro[1m]） |
| `/cost` | 查看 token 消耗 | 控制成本（DeepSeek 便宜但也要关注） |
| `/doctor` | 诊断环境问题 | Claude 行为异常时先跑这个 |
| `/init` | 生成 CLAUDE.md | 新项目第一步，让 Claude 理解项目结构 |
| `/review` | 审查当前分支代码 | 提交前自检 |
| `/security-review` | 安全审查 | 上线前必做 |
| `/simplify` | 代码优化建议 | 重构后让 Claude 帮你找冗余 |
| `/fewer-permission-prompts` | 减少权限弹窗 | 项目初始化后跑一次，把常用命令加白名单 |
| `/loop` | 定时循环任务 | 监控部署、轮询状态 |
| `/effort` | 调整思考深度 | 简单任务用 low，复杂任务用 max |
| `/update-config` | 修改 settings.json | 配置 hook、环境变量、权限 |
| `/keybindings-help` | 自定义快捷键 | 改提交键、添加快捷操作 |
| `/claude-api` | Claude API 代码助手 | 写 SDK 集成代码时 |
| `/login` / `/logout` | 账号登录登出 | 切换 API key |

---

## 二、终端交互（`!` 前缀）

在 Claude Code 中，用 `!` 前缀直接在对话中执行 shell 命令。

```bash
# 在 Claude Code 对话中直接输入
! git status
! npm test
! python main.py --debug
```

命令输出直接回显到对话中，不需要切到终端窗口，非常提升效率。

---

## 三、项目配置（CLAUDE.md）

项目根目录的 `CLAUDE.md` 是让 Claude 理解你项目的核心文件。每个对话启动时自动加载。

### 写法建议

```markdown
# 项目名

## 技术栈
- Python 3.12 + FastAPI + SQLAlchemy
- 前端 Vue 3 + Vite
- 数据库 PostgreSQL 16

## 项目结构
- `src/api/` - API 路由
- `src/models/` - 数据库模型
- `src/services/` - 业务逻辑
- `frontend/` - 前端代码

## 运行命令
- `make dev` - 启动开发环境
- `make test` - 运行测试
- `make lint` - 代码检查

## 注意事项
- 数据库 migration 用 Alembic，不要直接改表
- API 返回格式统一用 `{ code, data, message }`
- 不要用 print，统一用 loguru
```

### 关键原则
- **不要写显而易见的东西**：别写"src/ 是源代码目录"这种废话
- **写容易出错的地方**：约定、陷阱、非标准做法
- **精简**：CLAUDE.md 每次对话都加载，太长浪费 token

---

## 四、权限管理

### 三种级别
| 级别 | 文件位置 | 适用范围 |
|------|----------|----------|
| `user` | `~/.claude/settings.json` | 全局，所有项目 |
| `project` | `<项目>/.claude/settings.json` | 当前项目 |
| `local` | `<项目>/.claude/settings.local.json` | 本地（不提交 git） |

### 推荐的权限配置

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(python:*)",
      "Bash(ls:*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  }
}
```

### 技巧
- 常用只读命令用 `/fewer-permission-prompts` 一键加白名单
- 危险命令放 deny 列表防止误操作
- 项目级权限放 `.claude/settings.json`（可提交 git）
- 个人敏感配置放 `.claude/settings.local.json`（加入 .gitignore）

---

## 五、Hook 机制 - 自动化你的工作流

Hook 是 Claude Code 最强大的自动化功能，可以在特定事件触发自定义操作。

### 可用事件
| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 任何工具执行前 |
| `PostToolUse` | 任何工具执行后 |
| `Notification` | Claude 请求权限时 |
| `Stop` | Claude 响应结束时 |
| `SubagentStop` | 子 agent 完成时 |
| `PreCompact` | 上下文压缩前 |

### 实用 Hook 示例

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "afplay /System/Library/Sounds/Glass.aiff"
      }
    ]
  }
}
```

上面两个例子：
1. **每次 Claude 编辑文件后自动格式化** - 保持代码风格一致
2. **Claude 完成回复后播放提示音** - 不用盯着屏幕等

### 进阶用法

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit:*)",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/validate-commit-msg.py \"$CLAUDE_TOOL_INPUT\""
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "Bash(npm publish:*)",
        "hooks": [
          {
            "type": "text",
            "text": "⚠️ 你正在发布 npm 包！请确认版本号和 changelog 已更新。"
          }
        ]
      }
    ]
  }
}
```

---

## 六、快捷键

### 默认快捷键
| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Enter` | 提交消息 |
| `Ctrl+C` | 中断 Claude |
| `Ctrl+O` | 浏览文件附件 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清屏 |
| `↑/↓` | 历史消息导航 |
| `Tab` | 自动补全路径 |

### 自定义快捷键（`~/.claude/keybindings.json`）

```json
[
  {
    "keys": ["ctrl+s"],
    "command": "submit",
    "description": "Ctrl+S 提交消息（替代默认的 Ctrl+Enter）"
  },
  {
    "keys": ["ctrl+e"],
    "command": "openFile",
    "description": "快速打开文件"
  }
]
```

---

## 七、实用操作模式

### 1. 探索模式 - 理解陌生代码
```
"帮我理解这个项目的认证流程"
"这个 API 的调用链是怎样的？"
"找出所有涉及数据库迁移的代码"
```
技巧：让 Claude 用 Agent 工具并行搜索，比自己 grep 快得多。

### 2. 修复模式 - Bug 修完后自检
```bash
! git diff
/fewer-permission-prompts    # 减少后续弹窗
```
把 diff 丢给 Claude，描述现象，让它定位问题。

### 3. 重构模式 - 大改动分步做
```
第1步：先帮我提取这个 300 行函数的核心逻辑
第2步：按功能拆成 3 个小函数
第3步：写单元测试
/security-review               # 最后做安全检查
/simplify                      # 让 Claude 给优化建议
```

### 4. PR 模式 - 从代码到 PR 一站式
```
/review                        # 自我审查
/fewer-permission-prompts      # 减少后续操作弹窗
! git add <files> && git commit
"帮我把这些改动整理成 PR 描述"
! gh pr create --title "..." --body "..."
```

### 5. 监控模式 - 盯部署
```
/loop 5m "检查 vercel 部署状态，如果完成告诉我"
/loop 10m "检查 error 日志有没有新的异常"
```

---

## 八、上下文管理技巧

### 何时清空上下文
- 切换到完全不相关的任务
- 上下文超过 50 轮对话
- Claude 开始"忘记"前面的约定

### 何时压缩而非清空
- 还需要之前的知识，但对话太长了
- 用 `/compact` 保留关键信息

### 如何减少 token 消耗
1. **CLAUDE.md 尽量精简**：每次对话都加载
2. **用好 /clear 和 /compact**：别让垃圾对话占 token
3. **用 Agent 做大规模搜索**：Agent 结果只返回摘要，不占用你的主上下文
4. **善用 background 模式**：并行独立任务，不等结果

### 长任务的正确姿势
```
"做 A 时先用 Explore agent 搜索相关代码（background）"
"同时用 Plan agent 设计方案（background）"
"两个结果回来后我再决定怎么实现"
```

---

## 九、记忆系统

Claude Code 有持久化记忆功能，跨对话保留。

### 记忆类型
| 类型 | 用途 | 示例 |
|------|------|------|
| `user` | 你的角色、偏好、知识背景 | "我是后端开发，Python 10年经验，React 新手" |
| `feedback` | 你给过的工作方式反馈 | "不要 mock 数据库做测试" |
| `project` | 项目目标、进度、约束 | "认证模块改造是因为合规要求" |
| `reference` | 外部资源位置 | "Bug 跟踪用 Linear 项目 INGEST" |

### 用法
- `"记住我是 Python 后端开发"` - 保存用户信息
- `"以后不要写 docstring"` - 保存工作偏好
- `"这个项目的 Redis 用的是 cluster 模式"` - 保存项目上下文

**注意**：不要保存代码模式、文件路径、git 历史这类可以从代码库中直接推导的信息。

---

## 十、常见开发工作流

### 新项目上手
```bash
cd your-project
claude
/init                # 生成 CLAUDE.md，让 Claude 理解你的项目
/fewer-permission-prompts  # 减少权限弹窗
```

### 日常开发
```
"在 src/api/user.py 加一个获取用户列表的接口"
"帮我写一下对应的测试"
! curl localhost:8000/api/users  # 验证接口
```

### Code Review
```
/review              # 自我审查当前改动
# 或者
"review 一下这个 PR: https://github.com/xxx/pull/123"
```

### 发版前 checklist
```
/review              # 代码自查
/security-review     # 安全检查
! git diff main...HEAD --stat  # 看改动范围
/git-release         # 生成 changelog（如果装了相应 skill）
```

---

## 十一、常见坑与解决方案

| 问题 | 原因 | 解决 |
|------|------|------|
| Claude 编辑文件后格式乱了 | 没用 formatter hook | 加 PostToolUse hook 自动格式化 |
| 每次都要点确认很烦 | 权限弹窗太多 | `/fewer-permission-prompts` |
| Claude 开始"忘记"前面说的 | 上下文太长 | `/compact` 或 `/clear` |
| Claude 不懂我的项目 | 缺少 CLAUDE.md | `/init` 生成项目文档 |
| 子 agent 搜索不全 | 路径范围太窄 | 明确告诉 Agent 搜索范围要大 |
| Windows 下路径异常 | bash 模式使用 Linux 路径 | 用正斜杠 `/` 不要反斜杠 |
| 大文件读取超时 | 文件太大 | 用 `offset` 和 `limit` 分段读取 |

---

## 十二、自定义 Skill 写法

Skill 是一个带 frontmatter 的 markdown 文件，放在 `.claude/skills/` 目录下：

```markdown
---
name: my-skill
description: 一句话描述这个 skill 做什么
---

# My Skill 标题

## 触发条件
- 用户输入 `/my-skill` 或提到"xxx关键词"

## 工作流程

### 第1步：获取信息
1. 运行 xxx 获取数据
2. 分析结果

### 第2步：执行操作
- 核心逻辑描述
- 边界情况处理

## 输出格式
规定输出格式...

## 注意事项
- 特别提醒的点
```

### Skill 最佳实践
1. **命名用 kebab-case**：`git-release` 而不是 `GitRelease`
2. **触发条件要明确**：既支持 `/` 命令也支持自然语言
3. **工作流程要步骤化**：让 Claude 按流程执行，不要跳步
4. **输出格式要规定好**：避免每次输出不一致
5. **注意点单独列出**：边界情况、容易出错的地方
6. **放在项目的 `.claude/skills/` 下**：随项目 git 管理，团队共享

---

## 总结

| 场景 | 推荐操作 |
|------|----------|
| 新项目 | `/init` → `/fewer-permission-prompts` → 精修 CLAUDE.md |
| 写代码 | 直接对话 → `! 命令` 验证 → hook 自动格式化 |
| 修 Bug | 贴 diff → 描述现象 → 让 Claude 定位 → 验证修复 |
| 重构 | 分步执行 → `/security-review` → `/simplify` |
| PR | `/review` → 生成描述 → `gh pr create` |
| 发版 | `/git-release` → tag → push |
| 学习代码 | "帮我理解" → 让 Claude 画调用链 |

---

> 欢迎 PR 补充更多技巧！  
> 更新日期：2026-05-07
