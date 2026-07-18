<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  Document,
  Delete,
  Link,
  View,
} from '@element-plus/icons-vue'
import { useDocumentsStore } from '@/stores/documents'

const documentsStore = useDocumentsStore()

/** 搜索文本 */
const searchText = ref('')

/** 搜索处理 */
const handleSearch = () => {
  documentsStore.searchQuery = searchText.value
}

/** 清除搜索 */
const handleClearSearch = () => {
  searchText.value = ''
  documentsStore.searchQuery = ''
}

/** 删除确认 */
const handleDelete = (doc) => {
  ElMessageBox.confirm(
      `确定要删除「${doc.name}」吗？此操作不可撤销。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
      }
  ).then(() => {
    documentsStore.removeDocument(doc.id)
    ElMessage.success('文档已删除')
  }).catch(() => {})
}

/** 复制链接 */
const handleCopyLink = async (doc) => {
  try {
    await navigator.clipboard.writeText(doc.url || `${window.location.origin}/api/documents/${doc.id}/download`)
    ElMessage.success('链接已复制到剪贴板')
  } catch {
    ElMessage.info(`文档链接: ${doc.url}`)
  }
}

/** 查看详情 */
const handleViewDetail = (doc) => {
  ElMessage.info(`查看文档详情: ${doc.name}`)
  // TODO: Phase 3 实现文档详情页
}

/** 文件类型标签颜色 */
const getTypeColor = (type) => {
  const map = {
    pdf: '#EF4444',
    word: '#3B82F6',
    markdown: '#8B5CF6',
    txt: '#6B7280',
  }
  return map[type] || '#6B7280'
}
</script>

<template>
  <div class="document-list">
    <!-- 搜索栏 -->
    <div class="list-toolbar">
      <el-input
          v-model="searchText"
          placeholder="搜索文档名称..."
          :prefix-icon="Search"
          clearable
          class="search-input"
          @input="handleSearch"
          @clear="handleClearSearch"
      />
      <div class="toolbar-info">
        <span class="toolbar-count">
          {{ documentsStore.filteredDocuments.length }} 个文档
        </span>
      </div>
    </div>

    <!-- 文档卡片列表 -->
    <div v-if="documentsStore.filteredDocuments.length > 0" class="documents-grid">
      <div
          v-for="doc in documentsStore.filteredDocuments"
          :key="doc.id"
          class="doc-card"
      >
        <!-- 文件类型标识 -->
        <div class="doc-card-header">
          <div class="doc-type-icon" :style="{ background: getTypeColor(doc.type) + '15', color: getTypeColor(doc.type) }">
            <el-icon :size="20"><Document /></el-icon>
          </div>
          <div class="doc-card-meta">
            <span class="doc-type-badge" :style="{ color: getTypeColor(doc.type) }">
              {{ doc.type.toUpperCase() }}
            </span>
            <el-tag
                :type="documentsStore.getStatusConfig(doc.status).type"
                size="small"
                effect="plain"
            >
              {{ documentsStore.getStatusConfig(doc.status).label }}
            </el-tag>
          </div>
        </div>

        <!-- 文件名 -->
        <h3 class="doc-name" :title="doc.name">{{ doc.name }}</h3>

        <!-- 文件信息 -->
        <div class="doc-info">
          <span class="doc-info-item">{{ documentsStore.formatFileSize(doc.size) }}</span>
          <span class="doc-info-sep">·</span>
          <span class="doc-info-item">{{ documentsStore.formatTime(doc.uploadTime) }}</span>
        </div>

        <!-- 操作按钮 -->
        <div class="doc-actions">
          <el-button
              link
              type="primary"
              :icon="View"
              size="small"
              @click="handleViewDetail(doc)"
          >
            详情
          </el-button>
          <el-button
              link
              type="primary"
              :icon="Link"
              size="small"
              @click="handleCopyLink(doc)"
          >
            复制链接
          </el-button>
          <el-button
              link
              type="danger"
              :icon="Delete"
              size="small"
              @click="handleDelete(doc)"
          >
            删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="documents-empty">
      <el-empty :image-size="100" description="暂无文档">
        <template #image>
          <el-icon :size="56" color="#9ca3af"><Document /></el-icon>
        </template>
        <template #description>
          <p class="empty-text">
            {{ searchText ? '没有找到匹配的文档' : '还没有上传任何文档' }}
          </p>
        </template>
      </el-empty>
    </div>
  </div>
</template>

<style scoped>
.document-list {
  display: flex;
  flex-direction: column;
}

/* ---- Toolbar ---- */
.list-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.search-input {
  max-width: 320px;
}

.toolbar-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-count {
  font-size: 13px;
  color: #6b7280;
}

/* ---- Documents Grid ---- */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* ---- Document Card ---- */
.doc-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doc-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.doc-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.doc-type-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.doc-card-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.doc-type-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.doc-name {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a2e;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-all;
  margin: 0;
}

.doc-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.doc-info-sep {
  color: #d1d5db;
}

.doc-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

/* ---- Empty ---- */
.documents-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.empty-text {
  font-size: 14px;
  color: #6b7280;
}
</style>