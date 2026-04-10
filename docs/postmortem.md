# Incident Postmortem

## 1. Incident Summary
在本地 Kubernetes 部署 FastAPI 服务时，Pod 处于 Running 但一直未 Ready，导致 Service 无法正常转发流量，应用无法通过端口转发稳定访问。

## 2. Impact
- 应用无法正常提供服务
- `/health` 检查失败
- 本地验证和后续监控接入被阻塞

## 3. Timeline
- 14:00 修改 deployment.yaml，新增 readinessProbe
- 14:05 apply 后发现 Pod 未 Ready
- 14:08 使用 kubectl get pods 查看状态
- 14:10 使用 kubectl describe pod 查看 Events
- 14:12 发现 readinessProbe 路径写成了 /wrong-health
- 14:15 修正为 /health 并重新 apply
- 14:18 Pod 恢复 Ready，服务访问正常

## 4. Root Cause
readinessProbe 的 HTTP 路径配置错误，Kubernetes 持续探测失败，因此 Pod 被判定为 Not Ready，未加入 Service 后端。

## 5. Detection
通过以下方式定位问题：
- kubectl get pods
- kubectl describe pod <pod-name>
- 查看 probe failed 相关 Events

## 6. Resolution
将 readinessProbe 的 path 从 /wrong-health 改为 /health，并重新部署。

## 7. Prevention / Action Items
- 提交 YAML 前先人工检查 probe 路径是否与应用实际接口一致
- 将 /health 保持为固定健康检查入口
- 后续在 CI 中加入更基础的接口测试