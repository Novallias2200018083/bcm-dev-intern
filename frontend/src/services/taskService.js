import api from './api'

export const taskService = {
  /**
   * Fetch all tasks with optional filters
   */
  async getTasks(params = {}) {
    const response = await api.get('/tasks', { params })
    return response.data
  },

  /**
   * Fetch task summary statistics
   */
  async getStats() {
    const response = await api.get('/tasks/stats')
    return response.data
  },

  /**
   * Fetch list of task categories
   */
  async getCategories() {
    const response = await api.get('/tasks/categories')
    return response.data
  },

  /**
   * Fetch a single task by ID
   */
  async getTask(id) {
    const response = await api.get(`/tasks/${id}`)
    return response.data
  },

  /**
   * Create a new task
   */
  async createTask(taskData) {
    const response = await api.post('/tasks', taskData)
    return response.data
  },

  /**
   * Update an existing task
   */
  async updateTask(id, taskData) {
    const response = await api.put(`/tasks/${id}`, taskData)
    return response.data
  },

  /**
   * Quick status toggle (pending, in_progress, completed)
   */
  async updateStatus(id, status) {
    const response = await api.patch(`/tasks/${id}/status`, { status })
    return response.data
  },

  /**
   * Delete a task
   */
  async deleteTask(id) {
    await api.delete(`/tasks/${id}`)
    return true
  },

  /**
   * Upload an attachment file (image or document) for a task
   */
  async uploadAttachment(id, file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post(`/tasks/${id}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Delete the attachment of a task
   */
  async deleteAttachment(id) {
    const response = await api.delete(`/tasks/${id}/attachment`)
    return response.data
  },
}

export default taskService

