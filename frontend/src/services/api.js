import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 博主管理API
export const bloggerApi = {
  getList: (params) => api.get('/bloggers', { params }),
  getById: (id) => api.get(`/bloggers/${id}`),
  create: (data) => api.post('/bloggers', data),
  update: (id, data) => api.put(`/bloggers/${id}`, data),
  delete: (id) => api.delete(`/bloggers/${id}`),
  sync: (id) => api.post(`/bloggers/${id}/sync`),
  syncWeibo: (id) => api.post(`/bloggers/${id}/sync-weibo`)
}

// 微博数据API
export const weiboApi = {
  getList: (params) => api.get('/weibo', { params }),
  getById: (id) => api.get(`/weibo/${id}`),
  delete: (id) => api.delete(`/weibo/${id}`),
  batchDelete: (ids) => api.post('/weibo/batch-delete', { ids }),
  syncAll: (bloggerId) => api.post('/weibo/sync-all', { blogger_id: bloggerId }),
  syncByTimeRange: (data) => api.post('/weibo/sync-time-range', data),
  getLogs: (params) => api.get('/weibo/spider-logs', { params }),
  updatePrediction: (id, prediction) => api.put(`/weibo/${id}/prediction`, { prediction })
}

// 竞猜分析API
export const guessApi = {
  getAnalysis: (params) => api.get('/guess/analysis', { params }),
  getLeaderboard: (params) => api.get('/guess/leaderboard', { params }),
  getBloggerStats: (id, params) => api.get(`/guess/blogger/${id}/stats`, { params }),
  updateStats: (data) => api.post('/guess/stats/update', data),
  getHistory: (params) => api.get('/guess/history', { params })
}

// 官方结果API
export const officialApi = {
  getList: (params) => api.get('/official', { params }),
  getById: (id) => api.get(`/official/${id}`),
  create: (data) => api.post('/official', data),
  update: (id, data) => api.put(`/official/${id}`, data),
  delete: (id) => api.delete(`/official/${id}`),
  batchCreate: (data) => api.post('/official/batch', data),
  getDates: () => api.get('/official/dates')
}

// 系统管理API
export const systemApi = {
  getConfigs: () => api.get('/system/config'),
  getConfig: (key) => api.get(`/system/config/${key}`),
  updateConfig: (key, value) => api.put(`/system/config/${key}`, { value }),
  updateCookie: (cookie) => api.post('/system/cookie', { cookie }),
  checkCookie: () => api.get('/system/cookie/check'),
  getJobs: () => api.get('/system/jobs'),
  pauseJob: (id) => api.post(`/system/jobs/${id}/pause`),
  resumeJob: (id) => api.post(`/system/jobs/${id}/resume`),
  runSpiderNow: () => api.post('/system/jobs/run-now'),
  getStats: () => api.get('/system/stats')
}

export default api
