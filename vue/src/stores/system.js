import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 系统健康状态 Store
 * 数据来源：后端 Actuator /health 接口（Phase 1 使用 Mock）
 */
export const useSystemStore = defineStore('system', () => {
  /** 各组件健康状态列表 */
  const components = ref([
    { key: 'ai-service', label: 'AI Service', status: 'up' },
    { key: 'embedding', label: 'Embedding', status: 'up' },
    { key: 'milvus', label: 'Milvus', status: 'up' },
    { key: 'redis', label: 'Redis', status: 'up' },
    { key: 'llm', label: 'LLM', status: 'up' },
  ])

  /** 系统整体健康状态 */
  const overallStatus = computed(() => {
    const allUp = components.value.every((c) => c.status === 'up')
    const anyDown = components.value.some((c) => c.status === 'down')
    if (allUp) return 'healthy'
    if (anyDown) return 'degraded'
    return 'unknown'
  })

  /** 从后端 /health 接口更新状态（预留） */
  const fetchHealthStatus = async () => {
    // TODO: Phase 2 接入真实 Actuator /health 接口
    // const { data } = await axios.get('/actuator/health')
    // components.value = parseHealthResponse(data)
  }

  return {
    components,
    overallStatus,
    fetchHealthStatus,
  }
})