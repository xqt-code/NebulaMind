import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import '@/styles/global.css'

import App from './App.vue'
import router from './router'
import { setupGlobalErrorHandler, setupVueErrorHandler } from '@/utils/errorHandler'

const app = createApp(App)

// 注册所有 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局错误处理
setupGlobalErrorHandler()
setupVueErrorHandler(app)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')