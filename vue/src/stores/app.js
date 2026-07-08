import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 应用全局设置 Store
 * 管理 Developer Mode 等全局状态
 */
export const useAppStore = defineStore('app', () => {
  /** 开发者模式：开启后启用调试面板、API 日志等 */
  const developerMode = ref(false)

  /** 切换开发者模式 */
  const toggleDeveloperMode = () => {
    developerMode.value = !developerMode.value
  }

  return {
    developerMode,
    toggleDeveloperMode,
  }
})