import request from './request'

export const askQuestion = (data) => {
    return request.post('/api/v1/chat/ask', data)
}