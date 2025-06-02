# 水费查询集成 (Water Bill Integration) - 兴泸水务

这是一个用于 Home Assistant 的水费查询集成，可以自动获取水费余额、消费和未缴费信息。

## 功能特点

- 自动获取水费余额
- 显示上月水费消费
- 显示未缴费笔数
- 显示未缴费金额
- 支持自定义更新间隔
- 自动获取表单验证值

## 安装方法

### 通过 HACS 安装（推荐）

1. 确保你已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中点击 "集成"
3. 点击右上角的三个点
4. 选择 "自定义仓库"
5. 在 "仓库" 字段中输入：`https://github.com/caiwx86/lzss_water_ha`
6. 在 "类别" 下拉菜单中选择 "集成"
7. 点击 "添加"
8. 在 HACS 中搜索 "兴泸水务"
9. 点击安装
10. 重启 Home Assistant

### 手动安装

1. 下载最新的 [release](https://github.com/caiwx86/lzss_water_ha/releases)
2. 将 `lzss_water` 文件夹复制到你的 `custom_components` 目录
3. 重启 Home Assistant

## 配置

在 `configuration.yaml` 中添加以下配置：

```yaml
lzss_water:
  account_number: "你的户号"
  scan_interval: 28800  # 可选，默认8小时更新一次
```

## 支持的传感器

集成提供以下传感器：

1. `sensor.lzss_water_balance` - 当前水费余额
   - 显示当前余额
   - 单位：元
   - 图标：水滴
   - 属性：账户号码、当前月份、最后更新时间

2. `sensor.lzss_water_consumption` - 上月水费消费
   - 显示上月消费金额
   - 单位：元
   - 图标：带百分比的水滴
   - 属性：账户号码、上月月份、最后更新时间

3. `sensor.lzss_water_unpaid_count` - 未缴费笔数
   - 显示未缴费的笔数
   - 单位：笔
   - 图标：警告圆圈
   - 属性：账户号码、当前月份、最后更新时间

4. `sensor.lzss_water_unpaid_amount` - 未缴费金额
   - 显示未缴费的总金额
   - 单位：元
   - 图标：空心警告圆圈
   - 属性：账户号码、当前月份、最后更新时间

## 故障排除

如果遇到问题，请检查：

1. 户号是否正确
2. 网络连接是否正常
3. 查看 Home Assistant 日志中是否有错误信息

常见错误：
- 无法获取表单验证值：可能是网站结构发生变化
- 未找到数据列表：可能是查询参数有误
- 连接超时：检查网络连接

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 许可证

MIT License