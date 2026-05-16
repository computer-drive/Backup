# 服务器配置文件说明

## 1. `server`

### 1.1 `server.address`
- 描述：服务器监听的IP地址。
- 类型：string。
- 默认值：`"0.0.0.0"`

### 1.2 `server.port`
- 描述：服务器监听的端口号。
- 类型：int。
- 默认值：`8080`    

## 2. `log`

### 2.1 `log.database`
- 描述：日志数据库文件名。
- 类型：string。
- 默认值：`"log.db"`

## 3. `storages`

### 3.1 `storages.storage`
- 描述：存储配置列表。
- 说明：每个存储配置中应该包含一个对象，包含path与max_size两个字段。
- 类型：array。
- 默认值：`[]`

## 3.2 `storage.instance_database`
- 描述：存储实例数据库路径。
- 类型：string。
- 默认值：`"storage.db"`

## 4. `handle_error`
本部分配置了服务器在遇到错误时的处理方式。strict表示已ERROR输出日志，并且停止服务器运行，ignore已WARNING输出日志，继续运行。
### 4.1 `handle_error.invalid_storage_path`
- 描述：当存储路径无效时的错误处理方式。
- 类型：int。
- 默认值：`1`
- 说明：1表示表示strict，0表示ignore。
