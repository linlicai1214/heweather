# 和风天气插件 For HomeAssistant

本插件利用和风天气API，可将和风天气数据接入[HomeAssistant](https://www.home-assistant.io),。且该插件支持HA后台界面集成，无需配置yaml即可轻松完成配置。

## 安装

#### 通过`Samba`或`SFTP`手动安装
> 下载并复制`custom_components/heweather`文件夹到HA根目录下的`custom_components`文件夹

## 配置

### 添加集成:
> [⚙️ 配置](https://my.home-assistant.io/redirect/config) > 设备与服务 > [🧩 集成](https://my.home-assistant.io/redirect/integrations) > [➕ 添加集成](https://my.home-assistant.io/redirect/config_flow_start?domain=heweather) > 🔍 搜索 `Heweather`

或者点击: [![添加集成](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=heweather)

- **API KEY**：你的密钥
- **城市**：城市代码, 填写要查询的城市LocationID或者经纬度,也可是使用城市名称(中英文)进行模糊匹配 eg（北京，beijing）
- **名称**：对应entity_id及用于在天气实体上显示的名称
- **城市选择**：选择唯一确认的要查询城市

### 配置选项:
> [⚙️ 配置](https://my.home-assistant.io/redirect/config) > 设备与服务 > [🧩 集成](https://my.home-assistant.io/redirect/integrations) > HeWeather > 选项

- **天气预报**：选择天气预报的类型:24小时, 3天, 7天。因API KEY权限不同，选项也会不同。默认3天
- **刷新时间**：后台自动刷新获取天气预报数据的时间间隔


