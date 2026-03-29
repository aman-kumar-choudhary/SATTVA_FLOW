const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

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
      
      return { success: true, ...data }
    } catch (error) {
      console.error('API Error:', error)
      return { success: false, error: error.message }
    }
  },
  
  // Auth
  sendOTP(identifier, method) {
    return this.request('/auth/send-otp', {
      method: 'POST',
      body: JSON.stringify({ identifier, method })
    })
  },
  
  verifyOTP(identifier, otp, role, name) {
    return this.request('/auth/verify-otp', {
      method: 'POST',
      body: JSON.stringify({ identifier, otp, role, name })
    })
  },
  
  getCurrentUser() {
    return this.request('/auth/me')
  },
  
  // Admin
  getTrainers(status) {
    const query = status ? `?status=${status}` : ''
    return this.request(`/admin/trainers${query}`)
  },
  
  approveTrainer(trainerId) {
    return this.request(`/admin/trainers/${trainerId}/approve`, { method: 'PUT' })
  },
  
  rejectTrainer(trainerId, reason) {
    return this.request(`/admin/trainers/${trainerId}/reject`, {
      method: 'PUT',
      body: JSON.stringify({ reason })
    })
  },
  
  getClients() {
    return this.request('/admin/clients')
  },
  
  assignClient(trainerId, clientId) {
    return this.request('/admin/assignments', {
      method: 'POST',
      body: JSON.stringify({ trainer_id: trainerId, client_id: clientId })
    })
  },
  
  getAssignments() {
    return this.request('/admin/assignments')
  },
  
  getQueries(status) {
    const query = status ? `?status=${status}` : ''
    return this.request(`/admin/queries${query}`)
  },
  
  respondToQuery(queryId, response) {
    return this.request(`/admin/queries/${queryId}/respond`, {
      method: 'POST',
      body: JSON.stringify({ response })
    })
  },
  
  getReviews(status) {
    const query = status ? `?status=${status}` : ''
    return this.request(`/admin/reviews${query}`)
  },
  
  approveReview(reviewId) {
    return this.request(`/admin/reviews/${reviewId}/approve`, { method: 'PUT' })
  },
  
  rejectReview(reviewId) {
    return this.request(`/admin/reviews/${reviewId}/reject`, { method: 'DELETE' })
  },
  
  getStats() {
    return this.request('/admin/stats')
  },
  
  // Trainer
  getTrainerClients() {
    return this.request('/trainer/clients')
  },
  
  getTrainerSessions() {
    return this.request('/trainer/sessions')
  },
  
  createSession(sessionData) {
    return this.request('/trainer/sessions', {
      method: 'POST',
      body: JSON.stringify(sessionData)
    })
  },
  
  getTrainerPlans(clientId) {
    const query = clientId ? `?client_id=${clientId}` : ''
    return this.request(`/trainer/plans${query}`)
  },
  
  createPlan(planData) {
    return this.request('/trainer/plans', {
      method: 'POST',
      body: JSON.stringify(planData)
    })
  },
  
  updatePlanProgress(planId, progress) {
    return this.request(`/trainer/plans/${planId}/progress`, {
      method: 'PUT',
      body: JSON.stringify({ progress })
    })
  },
  
  getTrainerReviews() {
    return this.request('/trainer/reviews')
  },
  
  // Client
  getMyTrainer() {
    return this.request('/client/trainer')
  },
  
  getMySessions() {
    return this.request('/client/sessions')
  },
  
  getMyPlans() {
    return this.request('/client/plans')
  },
  
  createQuery(subject, message) {
    return this.request('/client/queries', {
      method: 'POST',
      body: JSON.stringify({ subject, message })
    })
  },
  
  getMyQueries() {
    return this.request('/client/queries')
  },
  
  createReview(rating, comment) {
    return this.request('/client/reviews', {
      method: 'POST',
      body: JSON.stringify({ rating, comment })
    })
  },
  
  getMyReviews() {
    return this.request('/client/reviews')
  },
  
  // Notifications
  getNotifications(unreadOnly = false) {
    const query = unreadOnly ? '?unread=true' : ''
    return this.request(`/notifications${query}`)
  },
  
  markNotificationRead(notificationId) {
    return this.request(`/notifications/${notificationId}/read`, { method: 'PUT' })
  },
  
  markAllRead() {
    return this.request('/notifications/read-all', { method: 'PUT' })
  },
  
  // Public
  getFeaturedTrainers() {
    return this.request('/public/trainers')
  },
  
  getPublicReviews() {
    return this.request('/public/reviews')
  }
}

export default api