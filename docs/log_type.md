# 日志记录说明
本文件说明程序运行时所有可能的`log_type`所对应的含义。

## 1. SERVER
本部分输出的日志为与服务器生命周期相关的日志。

### 1.1 STARTED

- 等级: `INFO`
- 描述：Socket服务器启动成功。
- message：包含两个字段。`port`与`ip`，表示服务器监听的IP地址与端口。

### 1.2 STOPPING_SERVER
- 等级: `INFO`
- 描述：开始执行关闭服务器的操作。
- message：无。

### 1.3 STOPPING_SOCKET_THREADS
- 等级: `INFO`
- 描述：开始关闭所有的socket线程。
- message：无。

### 1.4 STOPPED
- 等级: `INFO`
- 描述：服务器关闭成功。
- message：无。

## 2. 

