# Go AI Agent Harness

一个基于Go语言的AI代理框架，支持多种AI任务类型的异步处理和管理。

## 项目概述

Go AI Agent Harness是一个轻量级的AI代理服务框架，旨在简化AI任务的提交、执行和监控流程。它提供了统一的API接口来处理各种AI任务，包括文本生成、代码生成、数据分析和图像描述等。

## 功能特性

### 核心功能
- **多任务类型支持**: 支持文本生成、代码生成、数据分析、图像描述等多种AI任务
- **异步任务处理**: 基于Go协程的任务处理机制，支持高并发处理
- **任务状态管理**: 完整的任务生命周期管理(pending → processing → completed/failed)
- **RESTful API**: 提供标准的HTTP接口进行任务管理和状态查询
- **超时控制**: 内置任务超时机制防止长时间阻塞

### 技术架构
- **Gin框架**: 高性能HTTP Web框架
- **UUID生成**: 唯一任务标识符生成
- **内存存储**: 临时任务状态存储
- **上下文控制**: 请求级别的超时和取消控制

## API接口文档

### 1. 提交任务
```
POST /api/v1/agent/tasks
```
**请求体**:
```json
{
  "task": "text_generation",
  "model": "gpt-3.5-turbo",
  "params": {
    "prompt": "请帮我写一段关于人工智能的文章"
  },
  "priority": 1
}
```

**响应**:
```json
{
  "request_id": "uuid-string",
  "status": "pending",
  "created_at": "2026-03-22T11:06:58Z"
}
```

### 2. 查询任务状态
```
GET /api/v1/agent/tasks/{id}
```

**响应**:
```json
{
  "request_id": "uuid-string",
  "status": "completed",
  "result": {...},
  "created_at": "2026-03-22T11:06:58Z",
  "finished_at": "2026-03-22T11:07:00Z"
}
```

### 3. 列出所有任务
```
GET /api/v1/agent/tasks
```

### 4. 取消任务
```
DELETE /api/v1/agent/tasks/{id}
```

## 支持的任务类型

### 文本生成 (text_generation)
根据提供的提示词生成文本内容
```json
{
  "task": "text_generation",
  "params": {
    "prompt": "文章主题或问题描述"
  }
}
```

### 代码生成 (code_generation)
根据自然语言描述生成对应编程语言代码
```json
{
  "task": "code_generation",
  "params": {
    "description": "功能需求描述",
    "language": "python|javascript|java"
  }
}
```

### 数据分析 (data_analysis)
对输入数据集进行基础统计分析
```json
{
  "task": "data_analysis",
  "params": {
    "data": [1, 2, 3, 4, 5]
  }
}
```

### 图像描述 (image_description)
分析图像URL并返回图像内容描述
```json
{
  "task": "image_description",
  "params": {
    "image_url": "http://example.com/image.jpg"
  }
}
```

## 部署指南

### 本地运行
```bash
go run main.go
```

### 构建二进制文件
```bash
CGO_ENABLED=0 GOOS=linux go build -o ai-agent main.go
```

### Docker部署
```dockerfile
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

### Kubernetes部署
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent
  template:
    metadata:
      labels:
        app: ai-agent
    spec:
      containers:
      - name: ai-agent
        image: your-registry/ai-agent:latest
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: ai-agent-service
spec:
  selector:
    app: ai-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 性能优化建议

1. **水平扩展**: 通过增加副本数提高并发处理能力
2. **缓存策略**: 对频繁请求的结果实施缓存机制
3. **负载均衡**: 在前置网关层实现请求分流
4. **监控告警**: 集成Prometheus等监控解决方案

## 扩展开发

### 新增任务类型
1. 在`processTask`方法中注册新的任务处理器
2. 实现对应的处理函数
3. 更新API文档说明

### 集成真实AI模型
1. 替换模拟处理函数为真实的AI API调用
2. 添加认证和授权机制
3. 实施重试和熔断策略

## 故障排除

常见问题及解决方案:
- 任务卡住: 检查是否有死锁或无限循环
- 内存泄漏: 查看goroutine数量是否持续增长
- 接口超时: 调整context timeout参数

## 许可证

MIT License

## 联系方式

技术支持邮箱: support@example.com
