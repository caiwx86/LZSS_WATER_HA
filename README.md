# 水费查询集成 (Water Bill Integration) - 兴泸水务

这是一个用于 Home Assistant 的水费查询集成，可以自动获取水费余额信息。

## 功能特点

- 自动获取水费余额
- 支持自定义更新间隔

## 安装方法

### 通过 HACS 安装（推荐）

1. 确保你已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中点击 "集成"
3. 点击右上角的三个点
4. 选择 "自定义仓库"
5. 在 "仓库" 字段中输入：`https://github.com/caiwx86/LZSS_WATER_HA`
6. 在 "类别" 下拉菜单中选择 "集成"
7. 点击 "添加"
8. 在 HACS 中搜索 "Water Bill"
9. 点击安装
10. 重启 Home Assistant

### 手动安装

1. 下载最新的 [release](https://github.com/caiwx86/LZSS_WATER_HA/releases)
2. 将 `water_bill` 文件夹复制到你的 `custom_components` 目录
3. 重启 Home Assistant

## 配置

在 `configuration.yaml` 中添加以下配置：

```yaml
water_bill:
  account_number: "你的户号"
  scan_interval: 3600  # 可选，默认每小时更新一次
```

## 支持的传感器

- `sensor.water_bill_balance` - 当前水费余额

## 故障排除

如果遇到问题，请检查：

1. 户号是否正确
2. 网络连接是否正常
3. 查看 Home Assistant 日志中是否有错误信息

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 许可证

MIT License