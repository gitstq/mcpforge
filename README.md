<div align="center">

# 🔧 MCPForge

**Lightweight MCP Tool Package Manager CLI Engine**

**轻量级 MCP 工具包管理 CLI 引擎**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/gitstq/mcpforge/releases)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 English

### Project Introduction

**MCPForge** is a lightweight, zero-dependency CLI tool designed to simplify the management of Model Context Protocol (MCP) servers and tools. It provides a unified interface for discovering, installing, running, and managing MCP packages from various sources including NPM, PyPI, and GitHub.

**Key Differentiators:**
- 🚀 **Zero Dependencies**: Pure Python implementation using only standard library
- 🎯 **Unified Interface**: Single CLI for all MCP package operations
- 🔍 **Smart Discovery**: Search and discover MCP servers across multiple registries
- 🛠️ **Project Scaffolding**: Generate new MCP server projects with templates
- ✅ **Configuration Validation**: Validate MCP server configurations

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📦 **Install** | Install MCP servers from NPM, PyPI, or GitHub |
| 🗑️ **Uninstall** | Remove installed packages cleanly |
| 📋 **List** | View all installed MCP servers and tools |
| 🔍 **Search** | Find MCP servers across multiple registries |
| ℹ️ **Info** | Get detailed information about packages |
| 🆕 **Init** | Create new MCP server projects from templates |
| ✅ **Validate** | Check MCP server configurations |
| ▶️ **Run** | Execute MCP servers with various transports |
| ⚙️ **Config** | Manage MCPForge settings |
| 🔄 **Update** | Update installed packages to latest versions |

### 🚀 Quick Start

#### Installation

```bash
# Install from source
pip install .

# Or install in development mode
pip install -e .
```

#### Basic Usage

```bash
# Install an MCP server from NPM
mcpforge install @modelcontextprotocol/server-filesystem

# Search for MCP servers
mcpforge search filesystem

# List installed packages
mcpforge list

# Create a new MCP server project
mcpforge init my-mcp-server --template python

# Validate an MCP server configuration
mcpforge validate ./my-server

# Run an MCP server
mcpforge run @modelcontextprotocol/server-filesystem
```

### 📖 Detailed Usage

#### Install Command

```bash
# Install from NPM
mcpforge install @modelcontextprotocol/server-filesystem

# Install from PyPI
mcpforge install pypi:mcp-server-example

# Install from GitHub
mcpforge install github:username/repo

# Install globally
mcpforge install @modelcontextprotocol/server-filesystem --global

# Save to project dependencies
mcpforge install @modelcontextprotocol/server-filesystem --save
```

#### Search Command

```bash
# Search across all sources
mcpforge search filesystem

# Limit results
mcpforge search filesystem --limit 10

# Search specific source
mcpforge search filesystem --source npm
```

#### Init Command

```bash
# Create Python MCP server
mcpforge init my-server --template python

# Create TypeScript MCP server
mcpforge init my-server --template typescript

# Specify output path
mcpforge init my-server --template python --path ./projects
```

### 💡 Design Philosophy

MCPForge was designed with the following principles:

1. **Simplicity**: Easy to install and use with intuitive commands
2. **Zero Dependencies**: No external dependencies for core functionality
3. **Extensibility**: Support for multiple package sources and templates
4. **Developer Experience**: Rich CLI with colors, progress indicators, and helpful messages

### 📦 Packaging & Deployment

```bash
# Build distribution packages
python setup.py sdist bdist_wheel

# Install locally
pip install dist/mcpforge-1.0.0-py3-none-any.whl
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 简体中文

### 项目介绍

**MCPForge** 是一个轻量级、零依赖的 CLI 工具，旨在简化 Model Context Protocol (MCP) 服务器和工具的管理。它为从各种来源（包括 NPM、PyPI 和 GitHub）发现、安装、运行和管理 MCP 包提供了统一的接口。

**核心差异化亮点：**
- 🚀 **零依赖**: 纯 Python 实现，仅使用标准库
- 🎯 **统一接口**: 单一 CLI 管理所有 MCP 包操作
- 🔍 **智能发现**: 跨多个注册表搜索和发现 MCP 服务器
- 🛠️ **项目脚手架**: 使用模板生成新的 MCP 服务器项目
- ✅ **配置验证**: 验证 MCP 服务器配置

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📦 **安装** | 从 NPM、PyPI 或 GitHub 安装 MCP 服务器 |
| 🗑️ **卸载** | 干净地移除已安装的包 |
| 📋 **列表** | 查看所有已安装的 MCP 服务器和工具 |
| 🔍 **搜索** | 跨多个注册表查找 MCP 服务器 |
| ℹ️ **信息** | 获取包的详细信息 |
| 🆕 **初始化** | 从模板创建新的 MCP 服务器项目 |
| ✅ **验证** | 检查 MCP 服务器配置 |
| ▶️ **运行** | 使用各种传输方式执行 MCP 服务器 |
| ⚙️ **配置** | 管理 MCPForge 设置 |
| 🔄 **更新** | 将已安装的包更新到最新版本 |

### 🚀 快速开始

#### 安装

```bash
# 从源码安装
pip install .

# 或以开发模式安装
pip install -e .
```

#### 基本用法

```bash
# 从 NPM 安装 MCP 服务器
mcpforge install @modelcontextprotocol/server-filesystem

# 搜索 MCP 服务器
mcpforge search filesystem

# 列出已安装的包
mcpforge list

# 创建新的 MCP 服务器项目
mcpforge init my-mcp-server --template python

# 验证 MCP 服务器配置
mcpforge validate ./my-server

# 运行 MCP 服务器
mcpforge run @modelcontextprotocol/server-filesystem
```

### 📖 详细使用指南

#### 安装命令

```bash
# 从 NPM 安装
mcpforge install @modelcontextprotocol/server-filesystem

# 从 PyPI 安装
mcpforge install pypi:mcp-server-example

# 从 GitHub 安装
mcpforge install github:username/repo

# 全局安装
mcpforge install @modelcontextprotocol/server-filesystem --global

# 保存到项目依赖
mcpforge install @modelcontextprotocol/server-filesystem --save
```

#### 搜索命令

```bash
# 跨所有源搜索
mcpforge search filesystem

# 限制结果数量
mcpforge search filesystem --limit 10

# 搜索特定源
mcpforge search filesystem --source npm
```

#### 初始化命令

```bash
# 创建 Python MCP 服务器
mcpforge init my-server --template python

# 创建 TypeScript MCP 服务器
mcpforge init my-server --template typescript

# 指定输出路径
mcpforge init my-server --template python --path ./projects
```

### 💡 设计理念

MCPForge 遵循以下设计原则：

1. **简洁性**: 易于安装和使用，命令直观
2. **零依赖**: 核心功能无外部依赖
3. **可扩展性**: 支持多种包源和模板
4. **开发者体验**: 丰富的 CLI，带颜色、进度指示器和有用的消息

### 📦 打包与部署

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 本地安装
pip install dist/mcpforge-1.0.0-py3-none-any.whl
```

### 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 繁體中文

### 專案介紹

**MCPForge** 是一個輕量級、零依賴的 CLI 工具，旨在簡化 Model Context Protocol (MCP) 伺服器和工具的管理。它為從各種來源（包括 NPM、PyPI 和 GitHub）發現、安裝、執行和管理 MCP 套件提供了統一的介面。

**核心差異化亮點：**
- 🚀 **零依賴**: 純 Python 實現，僅使用標準庫
- 🎯 **統一介面**: 單一 CLI 管理所有 MCP 套件操作
- 🔍 **智慧發現**: 跨多個註冊表搜尋和發現 MCP 伺服器
- 🛠️ **專案腳手架**: 使用模板生成新的 MCP 伺服器專案
- ✅ **配置驗證**: 驗證 MCP 伺服器配置

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📦 **安裝** | 從 NPM、PyPI 或 GitHub 安裝 MCP 伺服器 |
| 🗑️ **解除安裝** | 乾淨地移除已安裝的套件 |
| 📋 **列表** | 查看所有已安裝的 MCP 伺服器和工具 |
| 🔍 **搜尋** | 跨多個註冊表尋找 MCP 伺服器 |
| ℹ️ **資訊** | 取得套件的詳細資訊 |
| 🆕 **初始化** | 從模板建立新的 MCP 伺服器專案 |
| ✅ **驗證** | 檢查 MCP 伺服器配置 |
| ▶️ **執行** | 使用各種傳輸方式執行 MCP 伺服器 |
| ⚙️ **配置** | 管理 MCPForge 設定 |
| 🔄 **更新** | 將已安裝的套件更新到最新版本 |

### 🚀 快速開始

#### 安裝

```bash
# 從原始碼安裝
pip install .

# 或以開發模式安裝
pip install -e .
```

#### 基本用法

```bash
# 從 NPM 安裝 MCP 伺服器
mcpforge install @modelcontextprotocol/server-filesystem

# 搜尋 MCP 伺服器
mcpforge search filesystem

# 列出已安裝的套件
mcpforge list

# 建立新的 MCP 伺服器專案
mcpforge init my-mcp-server --template python

# 驗證 MCP 伺服器配置
mcpforge validate ./my-server

# 執行 MCP 伺服器
mcpforge run @modelcontextprotocol/server-filesystem
```

### 📖 詳細使用指南

#### 安裝命令

```bash
# 從 NPM 安裝
mcpforge install @modelcontextprotocol/server-filesystem

# 從 PyPI 安裝
mcpforge install pypi:mcp-server-example

# 從 GitHub 安裝
mcpforge install github:username/repo

# 全域安裝
mcpforge install @modelcontextprotocol/server-filesystem --global

# 儲存到專案依賴
mcpforge install @modelcontextprotocol/server-filesystem --save
```

#### 搜尋命令

```bash
# 跨所有來源搜尋
mcpforge search filesystem

# 限制結果數量
mcpforge search filesystem --limit 10

# 搜尋特定來源
mcpforge search filesystem --source npm
```

#### 初始化命令

```bash
# 建立 Python MCP 伺服器
mcpforge init my-server --template python

# 建立 TypeScript MCP 伺服器
mcpforge init my-server --template typescript

# 指定輸出路徑
mcpforge init my-server --template python --path ./projects
```

### 💡 設計理念

MCPForge 遵循以下設計原則：

1. **簡潔性**: 易於安裝和使用，命令直觀
2. **零依賴**: 核心功能無外部依賴
3. **可擴展性**: 支援多種套件來源和模板
4. **開發者體驗**: 豐富的 CLI，帶顏色、進度指示器和有用的訊息

### 📦 打包與部署

```bash
# 建置分發套件
python setup.py sdist bdist_wheel

# 本地安裝
pip install dist/mcpforge-1.0.0-py3-none-any.whl
```

### 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 倉庫
2. 建立特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by gitstq**

[⭐ Star us on GitHub](https://github.com/gitstq/mcpforge) | [🐛 Report Bug](https://github.com/gitstq/mcpforge/issues) | [💡 Request Feature](https://github.com/gitstq/mcpforge/issues)

</div>
