/**
 * WebSocket 连接管理工具
 * 支持自动重连、心跳检测、事件订阅
 */

const DEFAULT_RECONNECT_DELAY = 2000
const DEFAULT_MAX_RECONNECT = 5
const DEFAULT_HEARTBEAT_INTERVAL = 15000
const DEFAULT_HEARTBEAT_TIMEOUT = 5000

/**
 * 创建 WebSocket 连接管理器
 * @param {string} url - WebSocket 地址
 * @param {object} options
 * @param {number} options.reconnectDelay - 重连间隔 ms
 * @param {number} options.maxReconnect - 最大重连次数
 * @param {number} options.heartbeatInterval - 心跳间隔 ms
 * @param {number} options.heartbeatTimeout - 心跳超时 ms
 * @param {function} options.onMessage - 消息回调
 * @param {function} options.onStatusChange - 连接状态变更回调
 * @returns {object} { connect, disconnect, send, status }
 */
export function createWebSocket(url, options = {}) {
  const {
    reconnectDelay = DEFAULT_RECONNECT_DELAY,
    maxReconnect = DEFAULT_MAX_RECONNECT,
    heartbeatInterval = DEFAULT_HEARTBEAT_INTERVAL,
    heartbeatTimeout = DEFAULT_HEARTBEAT_TIMEOUT,
    onMessage,
    onStatusChange,
  } = options

  let ws = null
  let reconnectCount = 0
  let reconnectTimer = null
  let heartbeatTimer = null
  let heartbeatTimeoutTimer = null
  let _status = 'disconnected'
  let destroyed = false

  // 状态 getter/setter
  const setStatus = (s) => {
    if (_status !== s) {
      _status = s
      if (onStatusChange) onStatusChange(s)
    }
  }

  const getStatus = () => _status

  // 心跳
  const startHeartbeat = () => {
    stopHeartbeat()
    heartbeatTimer = setInterval(() => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'PING' }))
        heartbeatTimeoutTimer = setTimeout(() => {
          // 心跳超时，认为连接断开
          if (ws) {
            ws.close()
          }
        }, heartbeatTimeout)
      }
    }, heartbeatInterval)
  }

  const stopHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
      heartbeatTimer = null
    }
    if (heartbeatTimeoutTimer) {
      clearTimeout(heartbeatTimeoutTimer)
      heartbeatTimeoutTimer = null
    }
  }

  // 连接
  const connect = () => {
    if (destroyed) return
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
      return
    }

    setStatus('connecting')

    try {
      ws = new WebSocket(url)
    } catch (error) {
      setStatus('error')
      scheduleReconnect()
      return
    }

    ws.onopen = () => {
      setStatus('connected')
      reconnectCount = 0
      startHeartbeat()
    }

    ws.onmessage = (event) => {
      // 心跳响应
      if (event.data === 'PONG' || (typeof event.data === 'string' && event.data.includes('"PONG"'))) {
        if (heartbeatTimeoutTimer) {
          clearTimeout(heartbeatTimeoutTimer)
          heartbeatTimeoutTimer = null
        }
        return
      }

      // 业务消息
      if (onMessage) {
        try {
          const data = JSON.parse(event.data)
          onMessage(data)
        } catch {
          onMessage(event.data)
        }
      }
    }

    ws.onerror = () => {
      setStatus('error')
    }

    ws.onclose = (event) => {
      stopHeartbeat()
      if (!event.wasClean) {
        setStatus('disconnected')
        scheduleReconnect()
      } else {
        setStatus('disconnected')
      }
    }
  }

  // 断线重连
  const scheduleReconnect = () => {
    if (destroyed) return
    if (reconnectCount >= maxReconnect) {
      setStatus('failed')
      return
    }

    reconnectCount++
    setStatus('reconnecting')

    reconnectTimer = setTimeout(() => {
      connect()
    }, reconnectDelay * Math.min(reconnectCount, 3))
  }

  // 断开连接
  const disconnect = () => {
    destroyed = true
    stopHeartbeat()
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    if (ws) {
      ws.onopen = null
      ws.onmessage = null
      ws.onerror = null
      ws.onclose = null
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close(1000, 'Client disconnect')
      }
      ws = null
    }
    setStatus('disconnected')
  }

  // 发送消息
  const send = (data) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(typeof data === 'string' ? data : JSON.stringify(data))
      return true
    }
    return false
  }

  return {
    connect,
    disconnect,
    send,
    get status() {
      return getStatus()
    },
  }
}

/**
 * 上传任务 WebSocket 客户端
 * 监听单个文档的处理进度
 */
export function createUploadTracker(taskId, url = '/ws/task-progress', options = {}) {
  const {
    onTaskStart,
    onParsing,
    onEmbedding,
    onIndexing,
    onSuccess,
    onError,
    onStatusChange,
  } = options

  // 使用查询参数传递 taskId
  const wsUrl = `${url}?taskId=${taskId}`

  const client = createWebSocket(wsUrl, {
    onMessage(data) {
      switch (data.type) {
        case 'TASK_START':
          if (onTaskStart) onTaskStart(data)
          break
        case 'PARSING':
          if (onParsing) onParsing(data)
          break
        case 'EMBEDDING':
          if (onEmbedding) onEmbedding(data)
          break
        case 'INDEXING':
          if (onIndexing) onIndexing(data)
          break
        case 'SUCCESS':
          if (onSuccess) onSuccess(data)
          break
        case 'ERROR':
          if (onError) onError(data)
          break
      }
    },
    onStatusChange(status) {
      if (onStatusChange) onStatusChange(status)
    },
  })

  client.connect()

  return client
}