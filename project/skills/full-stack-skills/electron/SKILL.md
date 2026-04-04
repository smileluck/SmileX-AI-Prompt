---
name: electron
description: Electron 跨平台桌面应用开发技能 - 构建 Windows、macOS、Linux 桌面应用
version: 1.0.0
author: teachingai
tags:
  - electron
  - desktop
  - cross-platform
  - javascript
  - nodejs
  - ipc
---

# Electron 跨平台桌面应用开发

## When to Use This Skill

Use this skill whenever the user wants to:

- Build cross-platform desktop applications with Electron
- Understand Electron architecture (main process, renderer process, preload)
- Implement IPC (Inter-Process Communication) between processes
- Create and manage BrowserWindow instances
- Implement menus, tray icons, and native features
- Package and distribute Electron applications
- Use Electron Forge for project scaffolding and building
- Debug and test Electron applications
- Implement security best practices
- Use Electron APIs (app, BrowserWindow, ipcMain, ipcRenderer, etc.)

## How to Use This Skill

This skill is organized to match the Electron official documentation structure.

### Identify the Topic

| User Request | Example File |
|-------------|--------------|
| Getting started/快速开始 | `examples/getting-started/installation.md` or `examples/getting-started/quick-start.md` |
| Main process/主进程 | `examples/processes/main-process.md` |
| Renderer process/渲染进程 | `examples/processes/renderer-process.md` |
| IPC communication/IPC 通信 | `examples/processes/ipc-communication.md` |
| BrowserWindow/窗口 | `examples/api/browser-window.md` |
| Menu/菜单 | `examples/api/menu.md` |
| Packaging/打包 | `examples/advanced/packaging.md` |
| Security/安全 | `examples/advanced/security.md` |

### Directory Structure

```
examples/
├── getting-started/           # 快速开始
│   ├── installation.md        # 安装 Electron 和基本设置
│   └── quick-start.md         # 快速入门教程
├── processes/                 # 进程
│   ├── main-process.md        # 主进程概念和使用
│   ├── renderer-process.md    # 渲染进程概念
│   ├── preload-scripts.md     # 预加载脚本使用
│   └── ipc-communication.md   # IPC 通信模式
├── api/                       # API 示例
│   ├── browser-window.md      # BrowserWindow 使用
│   ├── menu.md                # 菜单和上下文菜单
│   ├── tray.md                # 系统托盘
│   ├── dialog.md              # 文件对话框
│   ├── ipc-main.md            # ipcMain 使用
│   └── ipc-renderer.md        # ipcRenderer 使用
├── advanced/                  # 高级
│   ├── packaging.md           # 应用打包
│   ├── security.md            # 安全最佳实践
│   ├── auto-updater.md        # 自动更新
│   └── native-modules.md      # 原生模块
└── tools/                     # 工具
    ├── electron-forge.md      # Electron Forge 使用
    └── electron-fiddle.md     # Electron Fiddle 使用
```

### API Reference (api/)

```
api/
├── app.md              # app 模块 API
├── browser-window.md   # BrowserWindow API
├── ipc-main.md         # ipcMain API
├── ipc-renderer.md     # ipcRenderer API
├── menu.md             # Menu API
└── tray.md             # Tray API
```

### Templates (templates/)

```
templates/
├── main-process.md     # 主进程模板
├── preload-script.md   # 预加载脚本模板
├── renderer-process.md # 渲染进程模板
└── package-json.md     # package.json 模板
```

## Quick Start Example

```javascript
// main.js
const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

function createWindow() {
  const win = new BrowserWindow({
    width: 800, 
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,  // Security: always disable
      contextIsolation: true   // Security: always enable
    }
  })
  win.loadFile('index.html')
}

app.whenReady().then(createWindow)

// IPC handler example
ipcMain.handle('get-data', async () => {
  return { message: 'Hello from main process' }
})
```

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  getData: () => ipcRenderer.invoke('get-data')
})
```

## Best Practices

1. **Security**: Never enable `nodeIntegration` in renderer process, use preload scripts
2. **Process separation**: Keep main and renderer processes separate
3. **IPC communication**: Use IPC for safe communication between processes
4. **Resource management**: Properly clean up resources (windows, listeners)
5. **Error handling**: Implement proper error handling and crash reporting
6. **Performance**: Optimize for performance, use webContents for debugging
7. **Packaging**: Use Electron Forge or electron-builder for packaging
8. **Auto updates**: Implement auto-updater for production apps
9. **Native modules**: Handle native module compatibility
10. **Cross-platform**: Test on all target platforms

## Important Notes

- All examples follow Electron latest API
- Examples use both CommonJS (require) and ES modules (import)
- Each example file includes key concepts, code examples, and key points
- Always check the example file for best practices and common patterns
- Electron supports Windows, macOS, and Linux

## Resources

- **Official Website**: https://www.electronjs.org/zh/
- **Documentation**: https://www.electronjs.org/zh/docs/latest/
- **API Reference**: https://www.electronjs.org/zh/docs/latest/api/app
- **Electron Forge**: https://www.electronforge.io
- **Electron Fiddle**: https://www.electronjs.org/zh/fiddle
- **GitHub Repository**: https://github.com/electron/electron

## Keywords

Electron, desktop app, main process, renderer process, preload, IPC, BrowserWindow, Menu, Tray, Dialog, packaging, electron-builder, electron-forge, electron-fiddle, cross-platform, 桌面应用, 主进程, 渲染进程, IPC 通信, 窗口, 菜单, 托盘, 打包
