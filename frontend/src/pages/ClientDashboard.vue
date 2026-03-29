<template>
  <div class="client-dashboard">
    <div class="dashboard-header">
      <h1>My Yoga Journey</h1>
      <p>Welcome back, {{ userName }}</p>
    </div>
    
    <!-- Trainer Card -->
    <div class="trainer-section" v-if="trainer">
      <div class="trainer-card">
        <div class="trainer-avatar">{{ trainer.name.charAt(0) }}</div>
        <div class="trainer-info">
          <h3>{{ trainer.name }}</h3>
          <p class="trainer-spec">{{ trainer.trainer_details?.specialization || 'Yoga Trainer' }}</p>
          <p class="trainer-bio">{{ trainer.trainer_details?.bio || 'Your dedicated yoga guide' }}</p>
          <div class="trainer-stats">
            <span>⭐ {{ trainer.avg_rating || 'New' }} rating</span>
            <span>📅 {{ trainer.experience || 0 }} years exp</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="no-trainer">
      <p>No trainer assigned yet. Our admin will assign a trainer to you soon!</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ sessions.length }}</div>
          <div class="stat-label">Total Sessions</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ completedSessions }}</div>
          <div class="stat-label">Completed</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <div class="stat-value">{{ plans.length }}</div>
          <div class="stat-label">Active Plans</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <div class="stat-value">{{ myReviews.length }}</div>
          <div class="stat-label">Reviews Given</div>
        </div>
      </div>
    </div>
    
    <!-- Tabs -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.name }}
      </button>
    </div>
    
    <!-- Sessions Tab -->
    <div v-if="activeTab === 'sessions'" class="tab-content">
      <div class="section-header">
        <h2>My Sessions</h2>
      </div>
      
      <div class="sessions-list">
        <div class="session-card" v-for="session in sessions" :key="session._id">
          <div class="session-header">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-status" :class="session.status">{{ session.status }}</div>
          </div>
          <div class="session-description" v-if="session.description">{{ session.description }}</div>
          <div class="session-date" v-if="session.scheduled_at">
            📅 {{ formatDate(session.scheduled_at) }}
          </div>
          <div class="session-duration">⏱️ {{ session.duration }} minutes</div>
          <div class="session-notes" v-if="session.notes">{{ session.notes }}</div>
        </div>
      </div>
    </div>
    
    <!-- Plans Tab -->
    <div v-if="activeTab === 'plans'" class="tab-content">
      <div class="section-header">
        <h2>My Yoga Plans</h2>
      </div>
      
      <div class="plans-list">
        <div class="plan-card" v-for="plan in plans" :key="plan._id">
          <div class="plan-header">
            <div class="plan-title">{{ plan.title }}</div>
            <div class="plan-progress">{{ plan.progress }}% Complete</div>
          </div>
          <div class="plan-description" v-if="plan.description">{{ plan.description }}</div>
          <div class="plan-details">
            <span>📅 {{ plan.weeks }} weeks</span>
            <span>🏋️ {{ plan.sessions_per_week }} sessions/week</span>
          </div>
          <div class="plan-focus" v-if="plan.focus_areas?.length">
            🎯 Focus: {{ plan.focus_areas.join(', ') }}
          </div>
          <div class="plan-exercises" v-if="plan.exercises?.length">
            <strong>Exercises:</strong>
            <ul>
              <li v-for="exercise in plan.exercises" :key="exercise.name">{{ exercise.name }} - {{ exercise.sets }} sets</li>
            </ul>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: plan.progress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Queries Tab -->
    <div v-if="activeTab === 'queries'" class="tab-content">
      <div class="section-header">
        <h2>My Queries</h2>
        <button @click="showQueryModal = true" class="btn-primary">+ New Query</button>
      </div>
      
      <div class="queries-list">
        <div class="query-card" v-for="query in queries" :key="query._id">
          <div class="query-header">
            <div class="query-subject">{{ query.subject }}</div>
            <div class="query-status" :class="query.status">{{ query.status }}</div>
          </div>
          <div class="query-message">{{ query.message }}</div>
          <div v-if="query.response" class="query-response">
            <strong>Response:</strong> {{ query.response }}
          </div>
          <div class="query-date">{{ formatDate(query.created_at) }}</div>
        </div>
      </div>
    </div>
    
    <!-- Reviews Tab -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="section-header">
        <h2>My Reviews</h2>
        <button 
          v-if="trainer && !hasReviewed" 
          @click="showReviewModal = true" 
          class="btn-primary"
        >
          Write a Review
        </button>
      </div>
      
      <div class="reviews-list">
        <div class="review-card" v-for="review in myReviews" :key="review._id">
          <div class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</div>
          <div class="review-trainer">For: {{ trainer?.name }}</div>
          <div class="review-comment">{{ review.comment }}</div>
          <div class="review-status" :class="review.status">
            Status: {{ review.status }}
          </div>
          <div class="review-date">{{ formatDate(review.created_at) }}</div>
        </div>
      </div>
    </div>
    
    <!-- Query Modal -->
    <div v-if="showQueryModal" class="modal-overlay" @click="showQueryModal = false">
      <div class="modal-content" @click.stop>
        <h3>Submit a Query</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Subject</label>
            <input type="text" v-model="queryForm.subject" required />
          </div>
          <div class="input-group">
            <label>Message</label>
            <textarea v-model="queryForm.message" rows="5" required></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitQuery" class="btn-primary">Submit</button>
          <button @click="showQueryModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
    

    <!-- Profile Tab -->
    <div v-if="activeTab === 'profile'" class="tab-content">
      <div class="section-header">
        <h2>My Profile</h2>
      </div>

      <div class="profile-card">
        <div class="profile-avatar-row">
          <img v-if="profile && profile.picture" :src="profile.picture" class="profile-avatar-img" alt="avatar" />
          <div v-else class="profile-avatar-fallback">{{ (profile && profile.name) ? profile.name.charAt(0) : 'C' }}</div>
          <div class="profile-meta">
            <div class="profile-name">{{ profile && profile.name }}</div>
            <div class="profile-email">{{ profile && profile.email }}</div>
            <div class="profile-trainer-info" v-if="trainer">
              <span class="trainer-assigned-label">Assigned Trainer:</span>
              <span class="trainer-assigned-name">{{ trainer.name }}</span>
            </div>
            <div v-else class="profile-no-trainer">No trainer assigned yet</div>
          </div>
        </div>

        <div class="profile-form">
          <div class="profile-section-label">Personal Details</div>
          <div class="pf-grid">
            <div class="pf-group">
              <label>Full Name</label>
              <input type="text" v-model="profileForm.name" placeholder="Your full name" />
            </div>
            <div class="pf-group">
              <label>Phone / WhatsApp</label>
              <input type="tel" v-model="profileForm.phone" placeholder="+91 98765 43210" />
            </div>
          </div>

          <div v-if="profileSuccess" class="profile-success">✓ {{ profileSuccess }}</div>

          <div class="pf-actions">
            <button class="btn-primary" :disabled="profileSaving" @click="saveProfile">
              {{ profileSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div v-if="showReviewModal" class="modal-overlay" @click="showReviewModal = false">
      <div class="modal-content" @click.stop>
        <h3>Review Your Trainer</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Rating</label>
            <div class="rating-selector">
              <button 
                v-for="star in 5" 
                :key="star"
                @click="reviewForm.rating = star"
                class="star-btn"
                :class="{ active: star <= reviewForm.rating }"
              >
                ★
              </button>
            </div>
          </div>
          <div class="input-group">
            <label>Your Review</label>
            <textarea v-model="reviewForm.comment" rows="5" placeholder="Share your experience..."></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitReview" class="btn-primary">Submit Review</button>
          <button @click="showReviewModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
    
    <!-- Notifications -->
    <div class="notification-bell" @click="showNotifications = !showNotifications">
      <span class="bell-icon">🔔</span>
      <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
    </div>
    
    <div v-if="showNotifications" class="notifications-dropdown">
      <div class="notifications-header">
        <h4>Notifications</h4>
        <button @click="markAllRead" class="btn-link">Mark all read</button>
      </div>
      <div class="notifications-list">
        <div 
          v-for="notification in notifications" 
          :key="notification._id"
          class="notification-item"
          :class="{ unread: !notification.read }"
          @click="markRead(notification._id)"
        >
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
          <div class="notification-time">{{ formatDate(notification.created_at) }}</div>
        </div>
        <div v-if="!notifications.length" class="no-notifications">
          No notifications
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'ClientDashboard',
  data() {
    return {
      userName: localStorage.getItem('userName') || 'Client',
      activeTab: 'sessions',
      tabs: [
        { id: 'sessions', name: 'My Sessions' },
        { id: 'plans', name: 'Yoga Plans' },
        { id: 'queries', name: 'Queries' },
        { id: 'reviews', name: 'Reviews' },
        { id: 'profile', name: '👤 Profile' }
      ],
      trainer: null,
      sessions: [],
      plans: [],
      queries: [],
      myReviews: [],
      notifications: [],
      profile: null,
      profileForm: { name: '', phone: '' },
      profileSaving: false,
      profileSuccess: '',
      showNotifications: false,
      showQueryModal: false,
      showReviewModal: false,
      queryForm: {
        subject: '',
        message: ''
      },
      reviewForm: {
        rating: 5,
        comment: ''
      }
    }
  },
  computed: {
    completedSessions() {
      return this.sessions.filter(s => s.status === 'completed').length
    },
    hasReviewed() {
      return this.myReviews.some(r => r.status === 'approved' || r.status === 'pending')
    },
    unreadCount() {
      return this.notifications.filter(n => !n.read).length
    }
  },
  async mounted() {
    await this.loadData()
    await this.loadProfile()
    this.startPolling()
  },
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval)
  },
  methods: {
    async loadData() {
      const trainerResult = await api.getMyTrainer()
      if (trainerResult.success) this.trainer = trainerResult
      
      const sessionsResult = await api.getMySessions()
      if (sessionsResult.success) this.sessions = sessionsResult
      
      const plansResult = await api.getMyPlans()
      if (plansResult.success) this.plans = plansResult
      
      const queriesResult = await api.getMyQueries()
      if (queriesResult.success) this.queries = queriesResult
      
      const reviewsResult = await api.getMyReviews()
      if (reviewsResult.success) this.myReviews = reviewsResult
      
      const notificationsResult = await api.getNotifications()
      if (notificationsResult.success) this.notifications = notificationsResult
    },
    
    startPolling() {
      this.pollInterval = setInterval(async () => {
        const notificationsResult = await api.getNotifications(true)
        if (notificationsResult.success && notificationsResult.length > this.notifications.filter(n => !n.read).length) {
          await this.loadData()
        }
      }, 30000) // Poll every 30 seconds
    },
    
    async submitQuery() {
      if (!this.queryForm.subject || !this.queryForm.message) {
        alert('Please fill in all fields')
        return
      }
      
      const result = await api.createQuery(this.queryForm.subject, this.queryForm.message)
      if (result.success) {
        await this.loadData()
        this.showQueryModal = false
        this.queryForm = { subject: '', message: '' }
      } else {
        alert(result.error || 'Failed to submit query')
      }
    },
    
    async submitReview() {
      if (!this.reviewForm.rating) {
        alert('Please select a rating')
        return
      }
      
      const result = await api.createReview(this.reviewForm.rating, this.reviewForm.comment)
      if (result.success) {
        await this.loadData()
        this.showReviewModal = false
        this.reviewForm = { rating: 5, comment: '' }
      } else {
        alert(result.error || 'Failed to submit review')
      }
    },
    
    async markRead(notificationId) {
      await api.markNotificationRead(notificationId)
      await this.loadData()
    },
    
    async markAllRead() {
      await api.markAllRead()
      await this.loadData()
    },
    
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleString()
    },

    async loadProfile() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) {
          const user = JSON.parse(stored)
          this.profile = user
          this.profileForm.name  = user.name  || ''
          this.profileForm.phone = user.phone || ''
        }
        const res = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
        if (res.ok) {
          const user = await res.json()
          this.profile = user
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('userName', user.name)
          this.profileForm.name  = user.name  || ''
          this.profileForm.phone = user.phone || ''
        }
      } catch (e) { /* silent */ }
    },

    async saveProfile() {
      this.profileSaving = true
      this.profileSuccess = ''
      try {
        const res = await fetch('/api/auth/profile', {
          method:  'PUT',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
          body:    JSON.stringify({ name: this.profileForm.name, phone: this.profileForm.phone })
        })
        if (res.ok) {
          const data = await res.json()
          localStorage.setItem('userName', data.user.name)
          this.userName       = data.user.name
          this.profileSuccess = 'Profile updated successfully!'
          setTimeout(() => this.profileSuccess = '', 3000)
        }
      } catch (e) { /* silent */ } finally {
        this.profileSaving = false
      }
    }
  }
}
</script>

<style scoped>
.client-dashboard {
  max-width: 1400px;
  margin: 100px auto 60px;
  padding: 0 40px;
}

.dashboard-header {
  margin-bottom: 40px;
}

.dashboard-header h1 {
  font-size: 36px;
  font-family: 'Cormorant Garamond', serif;
  color: var(--text-dark);
  margin-bottom: 8px;
}

.dashboard-header p {
  color: var(--text-soft);
}

.trainer-section {
  margin-bottom: 40px;
}

.trainer-card {
  background: linear-gradient(135deg, var(--deep), var(--sage-dark));
  border-radius: 16px;
  padding: 32px;
  display: flex;
  gap: 24px;
  color: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.trainer-avatar {
  width: 80px;
  height: 80px;
  background: var(--gold);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: bold;
  color: var(--deep);
}

.trainer-info {
  flex: 1;
}

.trainer-info h3 {
  font-size: 28px;
  margin-bottom: 8px;
}

.trainer-spec {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 8px;
}

.trainer-bio {
  font-size: 13px;
  opacity: 0.7;
  margin-bottom: 12px;
}

.trainer-stats {
  display: flex;
  gap: 20px;
  font-size: 12px;
}

.no-trainer {
  background: #f5f5f0;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  color: var(--text-soft);
  margin-bottom: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  font-size: 32px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: var(--sage);
  font-family: 'Cormorant Garamond', serif;
}

.stat-label {
  font-size: 12px;
  color: var(--text-soft);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.tabs {
  display: flex;
  gap: 12px;
  border-bottom: 1px solid #e0e0d8;
  margin-bottom: 32px;
}

.tabs button {
  padding: 12px 24px;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-soft);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.tabs button.active {
  color: var(--sage);
}

.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--sage);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 24px;
  font-family: 'Cormorant Garamond', serif;
}

.btn-primary {
  background: var(--sage);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: var(--sage-dark);
}

.btn-secondary {
  background: #f5f5f0;
  border: 1px solid #e0e0d8;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-link {
  background: none;
  border: none;
  color: var(--sage);
  cursor: pointer;
  font-size: 12px;
}

.sessions-list,
.plans-list,
.queries-list,
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.session-card,
.plan-card,
.query-card,
.review-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.session-header,
.plan-header,
.query-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.session-title,
.plan-title,
.query-subject {
  font-weight: 600;
  font-size: 18px;
  color: var(--text-dark);
}

.session-status,
.query-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  text-transform: uppercase;
}

.session-status.scheduled,
.query-status.pending {
  background: #fff3e0;
  color: #f57c00;
}

.session-status.completed {
  background: #e8f5e9;
  color: #2e7d32;
}

.session-status.cancelled {
  background: #ffebee;
  color: #c62828;
}

.query-status.resolved {
  background: #e8f5e9;
  color: #2e7d32;
}

.plan-progress {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.session-description,
.plan-description,
.query-message {
  font-size: 13px;
  color: var(--text-mid);
  margin-bottom: 8px;
}

.session-date,
.session-duration,
.plan-details,
.plan-focus,
.query-date,
.review-date {
  font-size: 12px;
  color: var(--text-soft);
  margin-bottom: 4px;
}

.session-notes {
  font-size: 12px;
  color: var(--sage);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f0f0e8;
}

.progress-bar {
  height: 6px;
  background: #f0f0e8;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 12px;
}

.progress-fill {
  height: 100%;
  background: var(--sage);
  transition: width 0.3s;
}

.query-response {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 4px;
  margin: 12px 0;
}

.review-rating {
  color: var(--gold);
  font-size: 18px;
  margin-bottom: 8px;
}

.review-trainer {
  font-weight: 500;
  margin-bottom: 8px;
}

.review-comment {
  font-style: italic;
  margin-bottom: 8px;
}

.review-status {
  font-size: 11px;
  margin-bottom: 8px;
}

.review-status.approved {
  color: #2e7d32;
}

.review-status.pending {
  color: #f57c00;
}

.notification-bell {
  position: fixed;
  top: 100px;
  right: 40px;
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  z-index: 100;
}

.notification-bell:hover {
  transform: scale(1.05);
}

.bell-icon {
  font-size: 24px;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #f44336;
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
}

.notifications-dropdown {
  position: fixed;
  top: 160px;
  right: 40px;
  width: 350px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 101;
  overflow: hidden;
}

.notifications-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notifications-header h4 {
  font-size: 16px;
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0e8;
  cursor: pointer;
  transition: background 0.3s;
}

.notification-item:hover {
  background: #fafaf5;
}

.notification-item.unread {
  background: #f0f7ef;
  border-left: 3px solid var(--sage);
}

.notification-title {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 4px;
}

.notification-message {
  font-size: 12px;
  color: var(--text-mid);
  margin-bottom: 4px;
}

.notification-time {
  font-size: 10px;
  color: var(--text-soft);
}

.no-notifications {
  padding: 40px;
  text-align: center;
  color: var(--text-soft);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  padding: 32px;
  border-radius: 12px;
  min-width: 450px;
  max-width: 550px;
}

.modal-content h3 {
  margin-bottom: 24px;
}

.modal-body {
  margin-bottom: 24px;
}

.input-group {
  margin-bottom: 16px;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-mid);
}

.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0d8;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.input-group input:focus,
.input-group select:focus,
.input-group textarea:focus {
  outline: none;
  border-color: var(--sage);
}

.rating-selector {
  display: flex;
  gap: 8px;
}

.star-btn {
  font-size: 28px;
  background: none;
  border: none;
  cursor: pointer;
  color: #ddd;
  transition: color 0.3s;
}

.star-btn.active {
  color: var(--gold);
}

.star-btn:hover {
  color: var(--gold);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .client-dashboard {
    padding: 80px 20px 40px;
  }
  
  .trainer-card {
    flex-direction: column;
    text-align: center;
  }
  
  .trainer-avatar {
    margin: 0 auto;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .notifications-dropdown {
    width: calc(100% - 40px);
    right: 20px;
    left: 20px;
  }
  
  .notification-bell {
    right: 20px;
  }
  
  .modal-content {
    min-width: 300px;
    margin: 20px;
  }
}

/* ── PROFILE TAB ── */
.profile-card {
  background: white; border-radius: 12px;
  padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.profile-avatar-row {
  display: flex; align-items: center; gap: 20px; margin-bottom: 32px;
  padding-bottom: 24px; border-bottom: 1px solid rgba(0,0,0,0.06);
}
.profile-avatar-img {
  width: 72px; height: 72px; border-radius: 50%; object-fit: cover;
  border: 3px solid rgba(124,154,109,0.2);
}
.profile-avatar-fallback {
  width: 72px; height: 72px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; color: white; font-family: 'Cormorant Garamond', serif;
}
.profile-meta { flex: 1; }
.profile-name { font-size: 22px; font-weight: 600; color: var(--text-dark); margin-bottom: 4px; }
.profile-email { font-size: 13px; color: var(--text-soft); margin-bottom: 10px; }
.trainer-assigned-label { font-size: 12px; color: var(--text-soft); margin-right: 6px; }
.trainer-assigned-name { font-size: 13px; font-weight: 500; color: var(--sage-dark); }
.profile-no-trainer { font-size: 12px; color: var(--text-soft); font-style: italic; }

.profile-section-label {
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--sage); margin: 0 0 16px; font-weight: 500;
}
.pf-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pf-group { display: flex; flex-direction: column; gap: 6px; }
.pf-group.pf-full { grid-column: 1 / -1; }
.pf-group label {
  font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--text-mid); font-weight: 500;
}
.pf-group input {
  padding: 10px 12px; border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;
  font-size: 14px; font-family: inherit; color: var(--text-dark); transition: border-color 0.2s;
}
.pf-group input:focus {
  outline: none; border-color: var(--sage); box-shadow: 0 0 0 3px rgba(124,154,109,0.1);
}
.profile-success {
  margin: 16px 0; padding: 10px 14px; background: #e8f5e9; color: #2e7d32;
  border-radius: 6px; font-size: 13px;
}
.pf-actions { margin-top: 24px; display: flex; justify-content: flex-end; }

</style>