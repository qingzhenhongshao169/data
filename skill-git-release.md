---
name: git-release
description: 从 git 提交历史自动生成 changelog / release notes，支持 conventional commits 解析
---

# Git Release Skill

根据当前分支的 git 提交历史，自动生成结构化的 changelog 或 release notes。

## 触发条件
- 用户输入 `/git-release` 或提到"生成 changelog"、"release notes"、"发版说明"
- 用户说"总结一下这次要发版的内容"

## 工作流程

### 第1步：确定版本范围
1. 运行 `git tag --sort=-v:refname | head -5` 获取最近的 tag
2. 运行 `git log <last-tag>..HEAD --oneline` 获取当前版本的所有提交
3. 如果没有 tag，则使用 `git log --oneline --since="2 weeks ago"`

### 第2步：解析提交信息
按 conventional commits 规范分类：
- `feat:` → ✨ 新功能 (Features)
- `fix:` → 🐛 修复 (Bug Fixes)
- `perf:` → ⚡ 性能优化 (Performance)
- `refactor:` → ♻️ 重构 (Refactoring)
- `docs:` → 📝 文档 (Documentation)
- `style:` → 💄 样式 (Styles)
- `test:` → ✅ 测试 (Tests)
- `chore:` → 🔧 杂项 (Chores)
- `ci:` → 👷 CI/CD
- `build:` → 📦 构建 (Build)
- `breaking:` 或 `BREAKING CHANGE` → 💥 破坏性变更 (Breaking Changes)

### 第3步：生成 changelog
按以下模版输出：

```markdown
# 🚀 Release v<version> (<date>)

## 💥 破坏性变更
- ...

## ✨ 新功能
- ...

## 🐛 修复
- ...

## ⚡ 性能优化
- ...

## ♻️ 重构
- ...

## 📝 文档
- ...

## 🔧 杂项
- ...

---

**完整对比**: `<last-tag>...<new-tag>`
```

### 第4步：可选操作
- 询问用户是否需要自动打 tag
- 询问是否需要推送到远程
- 询问是否需要创建 GitHub Release

## 注意事项
- 不包含 merge commit（`--no-merges`）
- 如果 commit message 不规范，归入"其他"分类
- 自动从远程获取最新 tag
