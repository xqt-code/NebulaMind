/**
 * Axios 请求封装
 * 统一 baseURL、超时、拦截器、TraceID、TenantID
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 生成 UUID v4（用于 X-Trace-ID）
 */
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/** 租户 ID */
const TENANT_ID = import.meta.env.VITE_TENANT_ID || 'default'

// ==================== 请求拦截器 ====================
request.interceptors.request.use(
    (config) => {
      // 自动添加 TraceID
      config.headers['X-Trace-ID'] = generateUUID()
      // 自动添加 TenantID
      config.headers['X-Tenant-ID'] = TENANT_ID

      // 从 localStorage 获取 token（如果有）
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }

      return config
    },
    (error) => {
      return Promise.reject(error)
    }
)

// ==================== 响应拦截器 ====================
request.interceptors.response.use(
    (response) => {
      const data = response.data

      // 统一处理 Result<T> 格式：{ code, data, message }
      // 如果响应数据没有 code 字段，说明是原始数据，直接返回
      if (data && typeof data.code !== 'undefined') {
        // 成功：code 为 200 或 '200'
        if (data.code === 200 || data.code === '200') {
          // 如果存在 data.data，返回 data.data；否则返回整个 data
          return data.data !== undefined ? data.data : data
        }

        // 业务错误（code 不为 200）
        const errorMsg = data.msg || data.message || '请求失败'
        ElMessage.error(errorMsg)
        return Promise.reject(new Error(errorMsg))
      }

      // 非标准格式（没有 code 字段）直接返回
      return data
    },
    (error) => {
      // 网络错误处理
      if (error.code === 'ECONNABORTED') {
        ElMessage.error('请求超时，请稍后重试')
      } else if (error.message === 'Network Error') {
        ElMessage.error('网络连接失败，请检查网络')
      } else if (error.response) {
        const { status, data } = error.response
        switch (status) {
          case 401:
            ElMessage.error('登录已过期，请重新登录')
            break
          case 403:
            ElMessage.error('没有访问权限')
            break
          case 404:
            ElMessage.error('请求的资源不存在')
            break
          case 500:
            ElMessage.error('服务器内部错误')
            break
          default:
            ElMessage.error(data?.message || `请求失败 (${status})`)
        }
      } else {
        ElMessage.error('请求发送失败')
      }
      return Promise.reject(error)
    }
)

export default request