# HarmonyOS-chujing-UI-Automation

出境服务卡片 UI 自动化。

测试人员使用说明：

[测试人员部署与运行指南](docs/测试人员部署与运行指南.md)

## 快速运行

1. 创建本地环境并安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. 使用 USB 数据线连接设备，执行 `hdc list targets` 确认设备可见。

3. 执行全部用例

```powershell
python -m pytest -s -q tests `
  --alluredir=reports/allure-results `
  --clean-alluredir
```

4. 查看 Allure 报告

```powershell
allure serve reports/allure-results
```

## 配置说明

设备配置位于 `configs/default.toml`：

- `target_device`：`auto` 表示自动选择唯一的 USB 设备；多台设备时填写 USB 序列号。
- `bundle`、`ability`：被测元服务启动参数。
- `default_destination`：每条用例执行前后恢复的默认目的地。
- `cleanup_back_steps`：异常页面逐层返回的最大次数。

默认保持 `target_device = "auto"`。只有电脑同时连接多台 USB 设备时，
才需要填写 `hdc list targets` 显示的目标设备序列号。

## 生成目录

以下目录是运行产物，不应提交到 Git：

```text
reports/
tmp_hypium/
allure-report/
.pytest_cache/
__pycache__/
```
