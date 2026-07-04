<script setup>
import { ref, computed } from 'vue'
import {
  Search,
  Document,
  Delete,
  Link,
  View,
  RefreshRight,
  WarningFilled,
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
          <el-icon :size="56" color="var(--color-text-disabled)"><Document /></el-icon>
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
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.search-input {
  max-width: 320px;
}

.toolbar-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.toolbar-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

/* ---- Documents Grid ---- */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-lg);
}

/* ---- Document Card ---- */
.doc-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  transition: all var(--transition-fast);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.doc-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow-md);
}

.doc-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.doc-type-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
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
  font-weight: var(--font-weight-bold);
  letter-spacing: 0.5px;
  font-family: var(--font-mono);
}

.doc-name {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  line-height: var(--line-height-normal);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-all;
}

.doc-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.doc-info-sep {
  color: var(--color-text-disabled);
}

.doc-actions {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-top: var(--space-sm);
  border-top: 1px solid var(--color-border-light);
}

/* ---- Empty ---- */
.documents-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
}

.empty-text {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
}
</style>