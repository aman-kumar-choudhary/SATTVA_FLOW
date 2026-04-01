// api.js - Centralized API module for SattvaFlow
// Fixes: correct response parsing for paginated and non-paginated endpoints

const BASE_URL = import.meta.env.VITE_API_URL || ''

function getToken() {
  return localStorage.getItem('token')
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
  }
}

async function request(method, path, body = null) {
  try {
    const options = {
      method,
      headers: authHeaders()
    }
    if (body) options.body = JSON.stringify(body)

    const res = await fetch(`${BASE_URL}${path}`, options)

    if (res.status === 401) {
      localStorage.clear()
      window.location.href = '/login'
      return { success: false, error: 'Unauthorized' }
    }

    const data = await res.json()

    if (!res.ok) {
      return { success: false, error: data.error || 'Request failed' }
    }

    return { success: true, data }
  } catch (err) {
    console.error(`API error [${method} ${path}]:`, err)
    return { success: false, error: 'Network error' }
  }
}

// ── helpers to unwrap paginated vs flat responses ──────────────────────────
// Backend returns either:
//   • paginated: { items: [...], total, page, pages }
//   • flat array: [...]
//   • single object: { ... }

function unwrapList(result) {
  // Returns array on success, [] on failure
  if (!result.success) return []
  const d = result.data
  if (Array.isArray(d)) return d
  if (d && Array.isArray(d.items)) return d.items
  return []
}

function unwrapItem(result) {
  if (!result.success) return null
  return result.data
}

// ══════════════════════════════════════════════════════════════════
//  ADMIN API
// ══════════════════════════════════════════════════════════════════

export const adminApi = {
  // Stats
  async getStats() {
    const r = await request('GET', '/api/admin/stats')
    if (!r.success) return { success: false }
    return { success: true, ...r.data }
  },

  // Trainers
  async getTrainers(status = null) {
    const qs = status ? `?status=${status}` : ''
    const r = await request('GET', `/api/admin/trainers${qs}`)
    return { success: r.success, items: unwrapList(r) }
  },
  async approveTrainer(id) {
    const r = await request('PUT', `/api/admin/trainers/${id}/approve`)
    return { success: r.success, error: r.error }
  },
  async rejectTrainer(id, reason) {
    const r = await request('PUT', `/api/admin/trainers/${id}/reject`, { reason })
    return { success: r.success, error: r.error }
  },
  async blockTrainer(id) {
    const r = await request('PUT', `/api/admin/trainers/${id}/block`)
    return { success: r.success, error: r.error }
  },

  // Clients
  async getClients(status = null) {
    const qs = status ? `?status=${status}` : ''
    const r = await request('GET', `/api/admin/clients${qs}`)
    return { success: r.success, items: unwrapList(r) }
  },
  async activateClient(id) {
    const r = await request('PUT', `/api/admin/clients/${id}/activate`)
    return { success: r.success, error: r.error }
  },
  async blockClient(id) {
    const r = await request('PUT', `/api/admin/clients/${id}/block`)
    return { success: r.success, error: r.error }
  },

  // Assignments
  async getAssignments() {
    const r = await request('GET', '/api/admin/assignments')
    return { success: r.success, items: unwrapList(r) }
  },
  async assignClient(trainer_id, client_id) {
    const r = await request('POST', '/api/admin/assignments', { trainer_id, client_id })
    return { success: r.success, error: r.error }
  },
  async reassignClient(client_id, new_trainer_id) {
    const r = await request('PUT', '/api/admin/assignments/reassign', { client_id, new_trainer_id })
    return { success: r.success, error: r.error }
  },

  // Sessions (admin-only create/update/delete)
  async getSessions() {
    const r = await request('GET', '/api/admin/sessions')
    return { success: r.success, items: unwrapList(r) }
  },
  async createSession(data) {
    const r = await request('POST', '/api/admin/sessions', data)
    return { success: r.success, error: r.error, session: r.data?.session }
  },
  async updateSession(id, data) {
    const r = await request('PUT', `/api/admin/sessions/${id}`, data)
    return { success: r.success, error: r.error }
  },
  async deleteSession(id) {
    const r = await request('DELETE', `/api/admin/sessions/${id}`)
    return { success: r.success, error: r.error }
  },

  // Packages / Offers
  async getPackages() {
    const r = await request('GET', '/api/admin/packages')
    return { success: r.success, items: unwrapList(r) }
  },
  async createPackage(data) {
    const r = await request('POST', '/api/admin/packages', data)
    return { success: r.success, error: r.error, pkg: r.data?.package }
  },
  async updatePackage(id, data) {
    const r = await request('PUT', `/api/admin/packages/${id}`, data)
    return { success: r.success, error: r.error }
  },
  async togglePackage(id) {
    const r = await request('PUT', `/api/admin/packages/${id}/toggle`)
    return { success: r.success, error: r.error }
  },
  async deletePackage(id) {
    const r = await request('DELETE', `/api/admin/packages/${id}`)
    return { success: r.success, error: r.error }
  },

  // Queries
  async getQueries(status = null) {
    const qs = status ? `?status=${status}` : ''
    const r = await request('GET', `/api/admin/queries${qs}`)
    return { success: r.success, items: unwrapList(r) }
  },
  async respondToQuery(id, response) {
    const r = await request('POST', `/api/admin/queries/${id}/respond`, { response })
    return { success: r.success, error: r.error }
  },

  // Reviews
  async getReviews() {
    const r = await request('GET', '/api/admin/reviews')
    return { success: r.success, items: unwrapList(r) }
  },
  async approveReview(id) {
    const r = await request('PUT', `/api/admin/reviews/${id}/approve`)
    return { success: r.success, error: r.error }
  },
  async rejectReview(id) {
    const r = await request('PUT', `/api/admin/reviews/${id}/reject`)
    return { success: r.success, error: r.error }
  },

  // Broadcast
  async broadcast(title, message, target_role = 'all') {
    const r = await request('POST', '/api/admin/broadcast', { title, message, target_role })
    return { success: r.success, error: r.error }
  }
}

// ══════════════════════════════════════════════════════════════════
//  TRAINER API
// ══════════════════════════════════════════════════════════════════

export const trainerApi = {
  async getClients() {
    const r = await request('GET', '/api/trainer/clients')
    return { success: r.success, items: unwrapList(r) }
  },
  async getSessions() {
    const r = await request('GET', '/api/trainer/sessions')
    return { success: r.success, items: unwrapList(r) }
  },
  async markAttendance(sessionId) {
    const r = await request('PUT', `/api/trainer/sessions/${sessionId}/attendance`)
    return { success: r.success, error: r.error }
  },
  async getPlans(clientId = null) {
    const qs = clientId ? `?client_id=${clientId}` : ''
    const r = await request('GET', `/api/trainer/plans${qs}`)
    return { success: r.success, items: unwrapList(r) }
  },
  async createPlan(data) {
    const r = await request('POST', '/api/trainer/plans', data)
    return { success: r.success, error: r.error, plan: r.data?.plan }
  },
  async updatePlanProgress(planId, progress) {
    const r = await request('PUT', `/api/trainer/plans/${planId}/progress`, { progress })
    return { success: r.success, error: r.error }
  },
  async getReviews() {
    const r = await request('GET', '/api/trainer/reviews')
    return { success: r.success, items: unwrapList(r) }
  },
  async getQueries() {
    const r = await request('GET', '/api/trainer/queries')
    return { success: r.success, items: unwrapList(r) }
  },
  async createQuery(subject, message) {
    const r = await request('POST', '/api/trainer/queries', { subject, message })
    return { success: r.success, error: r.error }
  },
  async getPackages() {
    const r = await request('GET', '/api/trainer/packages')
    return { success: r.success, items: unwrapList(r) }
  }
}

// ══════════════════════════════════════════════════════════════════
//  CLIENT API
// ══════════════════════════════════════════════════════════════════

export const clientApi = {
  async getMyTrainer() {
    const r = await request('GET', '/api/client/trainer')
    if (!r.success) return { success: false }
    // Backend returns trainer object directly or { trainer: null }
    const d = r.data
    if (d && d.trainer === null) return { success: true, trainer: null }
    return { success: true, trainer: d }
  },
  async getMySessions() {
    const r = await request('GET', '/api/client/sessions')
    return { success: r.success, items: unwrapList(r) }
  },
  async getMyPlans() {
    const r = await request('GET', '/api/client/plans')
    return { success: r.success, items: unwrapList(r) }
  },
  async getMyPackages() {
    const r = await request('GET', '/api/client/packages')
    return { success: r.success, items: unwrapList(r) }
  },
  async expressInterest(packageId) {
    const r = await request('POST', `/api/client/packages/${packageId}/interest`)
    return { success: r.success, error: r.error }
  },
  async getMyQueries() {
    const r = await request('GET', '/api/client/queries')
    return { success: r.success, items: unwrapList(r) }
  },
  async createQuery(subject, message) {
    const r = await request('POST', '/api/client/queries', { subject, message })
    return { success: r.success, error: r.error }
  },
  async getMyReviews() {
    const r = await request('GET', '/api/client/reviews')
    return { success: r.success, items: unwrapList(r) }
  },
  async createReview(rating, comment) {
    const r = await request('POST', '/api/client/reviews', { rating, comment })
    return { success: r.success, error: r.error }
  }
}

// ══════════════════════════════════════════════════════════════════
//  NOTIFICATIONS API (shared across all roles)
// ══════════════════════════════════════════════════════════════════

export const notificationApi = {
  async getAll(unreadOnly = false) {
    const qs = unreadOnly ? '?unread=true' : ''
    const r = await request('GET', `/api/notifications${qs}`)
    return { success: r.success, items: unwrapList(r) }
  },
  async markRead(id) {
    const r = await request('PUT', `/api/notifications/${id}/read`)
    return { success: r.success }
  },
  async markAllRead() {
    const r = await request('PUT', '/api/notifications/read-all')
    return { success: r.success }
  },
  async getUnreadCount() {
    const r = await request('GET', '/api/notifications/unread-count')
    if (!r.success) return 0
    return r.data?.unread_count || 0
  }
}

// ══════════════════════════════════════════════════════════════════
//  AUTH API
// ══════════════════════════════════════════════════════════════════

export const authApi = {
  async getMe() {
    const r = await request('GET', '/api/auth/me')
    return r.success ? r.data : null
  },
  async updateProfile(data) {
    const r = await request('PUT', '/api/auth/profile', data)
    return { success: r.success, user: r.data?.user, error: r.error }
  }
}

// Legacy default export kept for backward compat - maps old api.X() calls
// to new structured api. Dashboards that import `api from '../api'` still work.
const api = {
  // Admin
  getStats: adminApi.getStats.bind(adminApi),
  getTrainers: (s) => adminApi.getTrainers(s),
  approveTrainer: (id) => adminApi.approveTrainer(id),
  rejectTrainer: (id, reason) => adminApi.rejectTrainer(id, reason),
  blockTrainer: (id) => adminApi.blockTrainer(id),
  getClients: (s) => adminApi.getClients(s),
  activateClient: (id) => adminApi.activateClient(id),
  blockClient: (id) => adminApi.blockClient(id),
  getAssignments: () => adminApi.getAssignments(),
  assignClient: (tid, cid) => adminApi.assignClient(tid, cid),
  reassignClient: (cid, ntid) => adminApi.reassignClient(cid, ntid),
  // Admin sessions
  adminGetSessions: () => adminApi.getSessions(),
  adminCreateSession: (d) => adminApi.createSession(d),
  adminUpdateSession: (id, d) => adminApi.updateSession(id, d),
  adminDeleteSession: (id) => adminApi.deleteSession(id),
  // Packages
  getPackages: () => adminApi.getPackages(),
  createPackage: (d) => adminApi.createPackage(d),
  updatePackage: (id, d) => adminApi.updatePackage(id, d),
  togglePackage: (id) => adminApi.togglePackage(id),
  deletePackage: (id) => adminApi.deletePackage(id),
  // Queries/reviews
  getQueries: (s) => adminApi.getQueries(s),
  respondToQuery: (id, r) => adminApi.respondToQuery(id, r),
  getReviews: () => adminApi.getReviews(),
  approveReview: (id) => adminApi.approveReview(id),
  rejectReview: (id) => adminApi.rejectReview(id),
  // Trainer
  getTrainerClients: () => trainerApi.getClients(),
  getTrainerSessions: () => trainerApi.getSessions(),
  getTrainerPlans: (cid) => trainerApi.getPlans(cid),
  createPlan: (d) => trainerApi.createPlan(d),
  updatePlanProgress: (id, p) => trainerApi.updatePlanProgress(id, p),
  getTrainerReviews: () => trainerApi.getReviews(),
  getTrainerQueries: () => trainerApi.getQueries(),
  createTrainerQuery: (s, m) => trainerApi.createQuery(s, m),
  markAttendance: (id) => trainerApi.markAttendance(id),
  // Client
  getMyTrainer: () => clientApi.getMyTrainer(),
  getMySessions: () => clientApi.getMySessions(),
  getMyPlans: () => clientApi.getMyPlans(),
  getMyPackages: () => clientApi.getMyPackages(),
  expressInterest: (id) => clientApi.expressInterest(id),
  getMyQueries: () => clientApi.getMyQueries(),
  createQuery: (s, m) => clientApi.createQuery(s, m),
  getMyReviews: () => clientApi.getMyReviews(),
  createReview: (r, c) => clientApi.createReview(r, c),
  // Notifications
  getNotifications: (unreadOnly) => notificationApi.getAll(unreadOnly),
  markNotificationRead: (id) => notificationApi.markRead(id),
  markAllRead: () => notificationApi.markAllRead()
}

export default api