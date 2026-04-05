const API_BASE_URL = (import.meta.env.VITE_API_URL || 'https://sattva-flow-nv6n.onrender.com') + '/api'

const api = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('token')
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'API request failed')
      }
      
      return data  // Return just the data, not { success: true, ...data }
    } catch (error) {
      console.error('API Error:', error)
      throw error  // Throw the error so it can be caught
    }
  },
  
  // Convenience methods
  get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  },
  
  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },
  
  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },
  
  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  },
  
  // Auth (update these to use the new methods)
  async sendOTP(identifier, method) {
    return this.post('/auth/send-otp', { identifier, method })
  },
  
  async verifyOTP(identifier, otp, role, name) {
    return this.post('/auth/verify-otp', { identifier, otp, role, name })
  },
  
  getCurrentUser() {
    return this.get('/auth/me')
  },
  
  // Admin
  getTrainers(status) {
    const query = status ? `?status=${status}` : ''
    return this.get(`/admin/trainers${query}`)
  },
  
  approveTrainer(trainerId) {
    return this.put(`/admin/trainers/${trainerId}/approve`)
  },
  
  rejectTrainer(trainerId, reason) {
    return this.put(`/admin/trainers/${trainerId}/reject`, { reason })
  },
  
  getClients() {
    return this.get('/admin/clients')
  },
  
  assignClient(trainerId, clientId) {
    return this.post('/admin/assignments', { trainer_id: trainerId, client_id: clientId })
  },
  
  getAssignments() {
    return this.get('/admin/assignments')
  },
  
  getQueries(status) {
    const query = status ? `?status=${status}` : ''
    return this.get(`/admin/queries${query}`)
  },
  
  respondToQuery(queryId, response) {
    return this.post(`/admin/queries/${queryId}/respond`, { response })
  },
  
  getReviews(status) {
    const query = status ? `?status=${status}` : ''
    return this.get(`/admin/reviews${query}`)
  },
  
  approveReview(reviewId) {
    return this.put(`/admin/reviews/${reviewId}/approve`)
  },
  
  rejectReview(reviewId) {
    return this.delete(`/admin/reviews/${reviewId}/reject`)
  },
  
  getStats() {
    return this.get('/admin/stats')
  },
  
  // Trainer
  getTrainerClients() {
    return this.get('/trainer/clients')
  },
  
  getTrainerSessions() {
    return this.get('/trainer/sessions')
  },
  
  createSession(sessionData) {
    return this.post('/trainer/sessions', sessionData)
  },
  
  getTrainerPlans(clientId) {
    const query = clientId ? `?client_id=${clientId}` : ''
    return this.get(`/trainer/plans${query}`)
  },
  
  createPlan(planData) {
    return this.post('/trainer/plans', planData)
  },
  
  updatePlanProgress(planId, progress) {
    return this.put(`/trainer/plans/${planId}/progress`, { progress })
  },
  
  getTrainerReviews() {
    return this.get('/trainer/reviews')
  },
  
  // Client
  getMyTrainer() {
    return this.get('/client/trainer')
  },
  
  getMySessions() {
    return this.get('/client/sessions')
  },
  
  getMyPlans() {
    return this.get('/client/plans')
  },
  
  createQuery(subject, message) {
    return this.post('/client/queries', { subject, message })
  },
  
  getMyQueries() {
    return this.get('/client/queries')
  },
  
  createReview(rating, comment) {
    return this.post('/client/reviews', { rating, comment })
  },
  
  getMyReviews() {
    return this.get('/client/reviews')
  },
  
  // Notifications
  getNotifications(unreadOnly = false) {
    const query = unreadOnly ? '?unread=true' : ''
    return this.get(`/notifications${query}`)
  },
  
  markNotificationRead(notificationId) {
    return this.put(`/notifications/${notificationId}/read`)
  },
  
  markAllRead() {
    return this.put('/notifications/read-all')
  },
  
  // Public
  getFeaturedTrainers() {
    return this.get('/public/trainers')
  },
  
  getPublicReviews() {
    return this.get('/public/reviews')
  }
}

export default api