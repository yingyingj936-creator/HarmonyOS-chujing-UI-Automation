# HarmonyOS-chujing-UI-Automation
出境服务卡片UI自动化

## 运行方式

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 按默认配置执行（`configs/default.toml`）

```bash
pytest -s -q
```

3. 覆盖设备或应用参数执行

```bash
pytest -s -q --device 172.16.130.67:5555 --bundle com.xxx --ability EntryAbility
```

4. 禁用自定义文件顺序（按 pytest 默认收集顺序执行）

```bash
pytest -s -q --disable-file-order
```
