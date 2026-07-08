import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/chat',
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/ChatView.vue'),
    meta: { title: '智能问答' },
  },
  {
    path: '/documents',
    name: 'Documents',
    component: () => import('@/views/DocumentsView.vue'),
    meta: { title: '知识库管理' },
  },
  {
    path: '/conversations',
    name: 'Conversations',
    component: () => import('@/views/ConversationsView.vue'),
    meta: { title: '会话历史' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router