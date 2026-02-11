# 乐课网直播自动点名答题工具
基于 Selenium 实现的乐课网 (leke.cn) 直播课堂自动点名应答工具。
1.核心功能
    1.1.精准定位乐课网 ant-modal 核心点名答题弹窗，兼容单纯点名按钮场景
    1.2.识别加减法题目（支持中文 / 英文加减号：+/＋、-/－），自动计算答案
    1.3.自动匹配答案选项并点击，支持自动提交答题结果
    1.4.带时间戳的实时日志输出，清晰展示每一步操作流程
    1.5.支持 Ctrl+C 终止监控，脚本结束后按 R 键一键重启
    1.6.自动安装依赖（Chrome、Python、Selenium），降低使用门槛
    1.7.快速开始（自动安装，推荐）
2.前置条件
    2.1.Windows 7/10/11 64 位系统
    2.2.网络通畅（需下载 Chrome、Python、核心脚本）
    2.3.文件夹路径无中文 / 空格 / 特殊字符
3.操作步骤
    1.下载并解压项目压缩包到本地
    2.双击运行 app.bat，脚本将自动完成以下操作：
    3.自动提权为管理员（确保安装权限）
    4.关闭现有 Chrome，检测 / 自动安装 Chrome 64 位
    5.检测 / 自动安装 Python 3.12.1（自动添加到系统 PATH）
    6.通过清华源安装 Selenium 4.17.2 依赖
    7.自动下载 app.py 核心脚本
    8.启动 Chrome 调试模式并打开乐课网
    9.手动登录乐课网账号，进入目标直播课堂
    10.脚本将持续监控答题弹窗，检测到后自动完成答题
    11.终止脚本：按下 Ctrl + C
    12.重启脚本：脚本结束后按 R 键，自动重启 Chrome 调试窗口并重新运行脚本
4.手动安装
    若自动安装失败，可手动执行以下步骤：
    步骤 1：安装 Chrome 浏览器
        下载离线安装包并安装：https://dl.google.com/chrome/install/standalonesetup64.exe默认路径：C:\Program Files\Google\Chrome\Application\chrome.exe
    步骤 2：安装 Python
        下载 Python 3.12+（推荐 3.12.1）：
        https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
        安装时务必勾选「Add Python to PATH」
        验证安装：打开 CMD 执行 python --version，能显示版本即成功
    步骤 3：安装依赖库
        CMD 中执行（清华源加速）：
        pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
        pip install selenium==4.17.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
    步骤 4：下载核心脚本
        手动下载 app.py 到本地（与启动脚本同目录）：https://leke.verber.eu.org/app.py
    步骤 5：启动 Chrome 调试模式
        CMD 中执行（替换你的目录为实际路径）：
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="你的目录\chrome_debug" "https://www.leke.cn"
    步骤 6：运行答题脚本
        python app.py
