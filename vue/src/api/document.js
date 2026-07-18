/**
 * 文档管理 API
 * 位置： src/api/document.js
 */

import request from './request'

/**
 * 上传文档
 * @param {FormData} formData - 包含文件的 FormData
 * @param {Function} onProgress - 进度回调函数
 * @returns {Promise}
 */
export const uploadDocument = (formData, onProgress) => {
    return request.post('/api/v1/documents/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
            if (onProgress && progressEvent.total) {
                const percent = Math.round((progressEvent.loaded / progressEvent.total) * 100)
                onProgress(percent)
            }
        }
    })
}

/**
 * 获取文档列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.size - 每页大小
 * @param {string} params.keyword - 搜索关键词
 * @returns {Promise}
 */
export const getDocumentList = (params) => {
    return request.get('/api/v1/documents/list', { params })
}

/**
 * 获取文档详情
 * @param {number} id - 文档 ID
 * @returns {Promise}
 */
export const getDocumentDetail = (id) => {
    return request.get(`/api/v1/documents/${id}`)
}

/**
 * 删除文档
 * @param {number} id - 文档 ID
 * @returns {Promise}
 */
export const deleteDocument = (id) => {
    return request.delete(`/api/v1/documents/${id}`)
}

/**
 * 获取文档的访问链接（签名 URL）
 * @param {number} id - 文档 ID
 * @returns {Promise}
 */
export const getDocumentUrl = (id) => {
    return request.get(`/api/v1/documents/${id}/url`)
}