# Yiri Backend

包名 `yiri_be`，pip 名 `yiri-be`。[YiriMirai][yiri] 的后端服务。支持管理机器人。

## 接口

`GET` 请求使用 query 参数，`POST` 请求使用 Json 请求体。

返回格式也是 Json，格式为

| 参数    | 类型             |
| ------- | ---------------- |
| code    | integer          |
| message | string           |
| data    | 返回数据 \| null |

其中，`code` 为 0 代表一切正常，如果不为 0，则错误信息在 `message` 中。`data` 包含了返回数据，具体见以下请求返回数据。

### 机器人状态

#### 获取机器人状态

`GET /bot/status`

- 请求参数

无

- 返回数据

| 参数    | 类型   |
| ------- | ------ |
| version | string |

### Handlers

#### 新建 handler

`POST /bot/handler/new`

- 请求参数

| 参数 | 类型   | 可选 | 描述             |
| ---- | ------ | ---- | ---------------- |
| name | string |      | 名称             |
| type | string |      | 监听消息的类型   |
| code | string |      | 要执行的代码片段 |

- 返回数据

无

#### 获取 handler

`GET /bot/handler/get`

- 请求参数

| 参数 | 类型   | 可选 | 描述 |
| ---- | ------ | ---- | ---- |
| name | string |      | 名称 |

- 返回数据

| 参数 | 类型   |
| ---- | ------ |
| name | string |
| type | string |
| code | string |

#### 修改 handler

`POST /bot/handler/update`

- 请求参数

| 参数 | 类型   | 可选 | 描述             |
| ---- | ------ | ---- | ---------------- |
| name | string |      | 名称             |
| code | string | Y    | 要修改的代码片段 |

- 返回数据

无

#### 删除 handler

`POST /bot/handler/delete`

- 请求参数

| 参数 | 类型   | 可选 | 描述 |
| ---- | ------ | ---- | ---- |
| name | string |      | 名称 |

- 返回数据

无


[yiri]: https://github.com/YiriMiraiProject/YiriMirai
