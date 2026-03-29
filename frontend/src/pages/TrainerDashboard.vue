<template>
  <div class="trainer-dashboard">
    <div class="dashboard-header">
      <h1>Trainer Dashboard</h1>
      <p>Welcome back, {{ userName }}</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ clients.length }}</div>
          <div class="stat-label">Assigned Clients</div>
        </div>
      </div>
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
          <div class="stat-value">{{ reviews.length }}</div>
          <div class="stat-label">Reviews</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <div class="stat-value">{{ avgRating }}</div>
          <div class="stat-label">Avg Rating</div>
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
    
    <!-- Clients Tab -->
    <div v-if="activeTab === 'clients'" class="tab-content">
      <div class="section-header">
        <h2>My Clients</h2>
      </div>
      
      <div class="clients-grid">
        <div class="client-card" v-for="client in clients" :key="client._id">
          <div class="client-avatar">{{ client.name.charAt(0) }}</div>
          <div class="client-info">
            <h4>{{ client.name }}</h4>
            <p>{{ client.email || client.phone }}</p>
            <div class="client-stats">
              <span>Sessions: {{ client.sessions_completed || 0 }}</span>
            </div>
          </div>
          <div class="client-actions">
            <button @click="viewClientDetails(client)" class="btn-link">View Plans</button>
            <button @click="openSessionModal(client)" class="btn-primary small">Add Session</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Sessions Tab -->
    <div v-if="activeTab === 'sessions'" class="tab-content">
      <div class="section-header">
        <h2>All Sessions</h2>
        <button @click="openSessionModal(null)" class="btn-primary">+ New Session</button>
      </div>
      
      <div class="sessions-list">
        <div class="session-card" v-for="session in sessions" :key="session._id">
          <div class="session-header">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-status" :class="session.status">{{ session.status }}</div>
          </div>
          <div class="session-client">Client: {{ getClientName(session.client_id) }}</div>
          <div class="session-date" v-if="session.scheduled_at">
            Scheduled: {{ formatDate(session.scheduled_at) }}
          </div>
          <div class="session-duration">Duration: {{ session.duration }} minutes</div>
          <div class="session-notes" v-if="session.notes">{{ session.notes }}</div>
          <div class="session-actions" v-if="session.status === 'scheduled'">
            <button @click="updateSessionStatus(session._id, 'completed')" class="btn-approve small">Mark Completed</button>
            <button @click="updateSessionStatus(session._id, 'cancelled')" class="btn-reject small">Cancel</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Plans Tab -->
    <div v-if="activeTab === 'plans'" class="tab-content">
      <div class="section-header">
        <h2>Yoga Plans</h2>
        <button @click="openPlanModal(null)" class="btn-primary">+ New Plan</button>
      </div>
      
      <div class="plans-list">
        <div class="plan-card" v-for="plan in plans" :key="plan._id">
          <div class="plan-header">
            <div class="plan-title">{{ plan.title }}</div>
            <div class="plan-progress">{{ plan.progress }}% Complete</div>
          </div>
          <div class="plan-client">Client: {{ getClientName(plan.client_id) }}</div>
          <div class="plan-details">
            <span>{{ plan.weeks }} weeks</span>
            <span>{{ plan.sessions_per_week }} sessions/week</span>
          </div>
          <div class="plan-focus" v-if="plan.focus_areas?.length">
            Focus: {{ plan.focus_areas.join(', ') }}
          </div>
          <div class="plan-description" v-if="plan.description">{{ plan.description }}</div>
          <div class="plan-actions">
            <button @click="updateProgress(plan._id)" class="btn-link">Update Progress</button>
            <button @click="viewPlanDetails(plan)" class="btn-link">View Details</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Reviews Tab -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="section-header">
        <h2>Client Reviews</h2>
      </div>
      
      <div class="reviews-list">
        <div class="review-card" v-for="review in reviews" :key="review._id">
          <div class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</div>
          <div class="review-client">{{ review.client?.name }}</div>
          <div class="review-comment">{{ review.comment }}</div>
          <div class="review-date">{{ formatDate(review.created_at) }}</div>
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
          <div v-else class="profile-avatar-fallback">{{ (profile && profile.name) ? profile.name.charAt(0) : 'T' }}</div>
          <div class="profile-meta">
            <div class="profile-name">{{ profile && profile.name }}</div>
            <div class="profile-email">{{ profile && profile.email }}</div>
            <div class="profile-status-badge" :class="profile && profile.status">
              {{ profile && profile.status === 'active' ? '✓ Active' : '⏳ Pending Approval' }}
            </div>
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

          <div class="profile-section-label">Trainer Details</div>
          <div class="pf-grid">
            <div class="pf-group">
              <label>Specialization</label>
              <input type="text" v-model="profileForm.specialization" placeholder="e.g. Hatha Yoga, Vinyasa" />
            </div>
            <div class="pf-group">
              <label>Years of Experience</label>
              <input type="number" v-model="profileForm.experience" placeholder="Years" min="0" />
            </div>
            <div class="pf-group pf-full">
              <label>Certifications (comma separated)</label>
              <input type="text" v-model="profileForm.certifications" placeholder="e.g. RYT-200, YAI" />
            </div>
            <div class="pf-group pf-full">
              <label>Bio</label>
              <textarea v-model="profileForm.bio" rows="4" placeholder="Tell clients about yourself..."></textarea>
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

    <!-- Session Modal -->
    <div v-if="showSessionModal" class="modal-overlay" @click="showSessionModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingSession ? 'Edit Session' : 'Create New Session' }}</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Client</label>
            <select v-model="sessionForm.client_id">
              <option v-for="client in clients" :key="client._id" :value="client._id">
                {{ client.name }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Session Title</label>
            <input type="text" v-model="sessionForm.title" required />
          </div>
          <div class="input-group">
            <label>Description</label>
            <textarea v-model="sessionForm.description" rows="3"></textarea>
          </div>
          <div class="input-group">
            <label>Scheduled Date & Time</label>
            <input type="datetime-local" v-model="sessionForm.scheduled_at" />
          </div>
          <div class="input-group">
            <label>Duration (minutes)</label>
            <input type="number" v-model="sessionForm.duration" />
          </div>
          <div class="input-group">
            <label>Notes</label>
            <textarea v-model="sessionForm.notes" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="createSession" class="btn-primary">{{ editingSession ? 'Update' : 'Create' }}</button>
          <button @click="showSessionModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
    
    <!-- Plan Modal -->
    <div v-if="showPlanModal" class="modal-overlay" @click="showPlanModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingPlan ? 'Edit Plan' : 'Create New Yoga Plan' }}</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Client</label>
            <select v-model="planForm.client_id">
              <option v-for="client in clients" :key="client._id" :value="client._id">
                {{ client.name }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Plan Title</label>
            <input type="text" v-model="planForm.title" required />
          </div>
          <div class="input-group">
            <label>Description</label>
            <textarea v-model="planForm.description" rows="3"></textarea>
          </div>
          <div class="input-group">
            <label>Duration (weeks)</label>
            <input type="number" v-model="planForm.weeks" />
          </div>
          <div class="input-group">
            <label>Sessions per Week</label>
            <input type="number" v-model="planForm.sessions_per_week" />
          </div>
          <div class="input-group">
            <label>Focus Areas (comma separated)</label>
            <input type="text" v-model="planForm.focus_areas_str" placeholder="e.g., Flexibility, Strength, Balance" />
          </div>
        </div>
        <div class="modal-actions">
          <button @click="createPlan" class="btn-primary">{{ editingPlan ? 'Update' : 'Create' }}</button>
          <button @click="showPlanModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'TrainerDashboard',
  data() {
    return {
      userName: localStorage.getItem('userName') || 'Trainer',
      activeTab: 'clients',
      tabs: [
        { id: 'clients', name: 'My Clients' },
        { id: 'sessions', name: 'Sessions' },
        { id: 'plans', name: 'Yoga Plans' },
        { id: 'reviews', name: 'Reviews' },
        { id: 'profile', name: '👤 Profile' }
      ],
      clients: [],
      sessions: [],
      plans: [],
      reviews: [],
      profile: null,
      profileForm: { name: '', phone: '', specialization: '', experience: '', certifications: '', bio: '' },
      profileSaving: false,
      profileSuccess: '',
      showSessionModal: false,
      showPlanModal: false,
      editingSession: false,
      editingPlan: false,
      sessionForm: {
        client_id: '',
        title: '',
        description: '',
        scheduled_at: '',
        duration: 60,
        notes: ''
      },
      planForm: {
        client_id: '',
        title: '',
        description: '',
        weeks: 4,
        sessions_per_week: 3,
        focus_areas_str: ''
      }
    }
  },
  computed: {
    avgRating() {
      if (!this.reviews.length) return 'N/A'
      const sum = this.reviews.reduce((acc, r) => acc + r.rating, 0)
      return (sum / this.reviews.length).toFixed(1)
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      const clientsResult = await api.getTrainerClients()
      if (clientsResult.success) this.clients = clientsResult
      
      const sessionsResult = await api.getTrainerSessions()
      if (sessionsResult.success) this.sessions = sessionsResult
      
      const plansResult = await api.getTrainerPlans()
      if (plansResult.success) this.plans = plansResult
      
      const reviewsResult = await api.getTrainerReviews()
      if (reviewsResult.success) this.reviews = reviewsResult
      await this.loadProfile()
    },
    
    getClientName(clientId) {
      const client = this.clients.find(c => c._id === clientId)
      return client ? client.name : 'Unknown'
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Not scheduled'
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    
    viewClientDetails(client) {
      // Filter plans for this client
      const clientPlans = this.plans.filter(p => p.client_id === client._id)
      alert(`Client: ${client.name}\nPlans: ${clientPlans.length}\nSessions: ${client.sessions_completed || 0}`)
    },
    
    openSessionModal(client) {
      this.editingSession = false
      this.sessionForm = {
        client_id: client ? client._id : '',
        title: '',
        description: '',
        scheduled_at: '',
        duration: 60,
        notes: ''
      }
      this.showSessionModal = true
    },
    
    async createSession() {
      if (!this.sessionForm.client_id || !this.sessionForm.title) {
        alert('Please fill in required fields')
        return
      }
      
      const result = await api.createSession(this.sessionForm)
      if (result.success) {
        await this.loadData()
        this.showSessionModal = false
      } else {
        alert(result.error || 'Failed to create session')
      }
    },
    
    async updateSessionStatus(sessionId, status) {
      // Implement session status update
      alert('Feature coming soon')
    },
    
    openPlanModal(client) {
      this.editingPlan = false
      this.planForm = {
        client_id: client ? client._id : '',
        title: '',
        description: '',
        weeks: 4,
        sessions_per_week: 3,
        focus_areas_str: ''
      }
      this.showPlanModal = true
    },
    
    async createPlan() {
      if (!this.planForm.client_id || !this.planForm.title) {
        alert('Please fill in required fields')
        return
      }
      
      const planData = {
        ...this.planForm,
        focus_areas: this.planForm.focus_areas_str.split(',').map(s => s.trim()).filter(s => s)
      }
      
      const result = await api.createPlan(planData)
      if (result.success) {
        await this.loadData()
        this.showPlanModal = false
      } else {
        alert(result.error || 'Failed to create plan')
      }
    },
    
    async updateProgress(planId) {
      const progress = prompt('Enter progress percentage (0-100):')
      if (progress !== null && !isNaN(progress)) {
        const result = await api.updatePlanProgress(planId, parseInt(progress))
        if (result.success) {
          await this.loadData()
        } else {
          alert('Failed to update progress')
        }
      }
    },
    
    viewPlanDetails(plan) {
      alert(`Plan: ${plan.title}\nProgress: ${plan.progress}%\nWeeks: ${plan.weeks}\nSessions/week: ${plan.sessions_per_week}`)
    },

    async loadProfile() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) {
          const user = JSON.parse(stored)
          this.profile = user
          this.profileForm.name   = user.name  || ''
          this.profileForm.phone  = user.phone || ''
          const td = user.trainer_details || {}
          this.profileForm.specialization = td.specialization || ''
          this.profileForm.experience     = td.experience     || ''
          this.profileForm.certifications = Array.isArray(td.certifications) ? td.certifications.join(', ') : (td.certifications || '')
          this.profileForm.bio            = td.bio            || ''
        }
        // Fetch fresh from API
        const res = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
        if (res.ok) {
          const user = await res.json()
          this.profile = user
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('userName', user.name)
          this.profileForm.name   = user.name  || ''
          this.profileForm.phone  = user.phone || ''
          const td = user.trainer_details || {}
          this.profileForm.specialization = td.specialization || ''
          this.profileForm.experience     = td.experience     || ''
          this.profileForm.certifications = Array.isArray(td.certifications) ? td.certifications.join(', ') : (td.certifications || '')
          this.profileForm.bio            = td.bio            || ''
        }
      } catch (e) { /* silent */ }
    },

    async saveProfile() {
      this.profileSaving = true
      this.profileSuccess = ''
      try {
        const payload = {
          name:           this.profileForm.name,
          phone:          this.profileForm.phone,
          specialization: this.profileForm.specialization,
          experience:     parseInt(this.profileForm.experience) || 0,
          certifications: this.profileForm.certifications,
          bio:            this.profileForm.bio
        }
        const res = await fetch('/api/auth/profile', {
          method:  'PUT',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
          body:    JSON.stringify(payload)
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
.trainer-dashboard {
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

.btn-primary.small {
  padding: 6px 12px;
  font-size: 12px;
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
  margin-right: 8px;
}

.btn-approve, .btn-reject {
  padding: 4px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
}

.btn-approve {
  background: var(--sage);
  color: white;
}

.btn-reject {
  background: #f44336;
  color: white;
}

.small {
  padding: 4px 8px;
  font-size: 11px;
}

.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.client-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.client-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.client-info {
  flex: 1;
}

.client-info h4 {
  margin-bottom: 4px;
}

.client-info p {
  font-size: 12px;
  color: var(--text-soft);
  margin-bottom: 4px;
}

.client-stats {
  font-size: 11px;
  color: var(--text-mid);
}

.client-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sessions-list,
.plans-list,
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.session-card,
.plan-card,
.review-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.session-header,
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.session-title,
.plan-title {
  font-weight: 600;
  font-size: 18px;
  color: var(--text-dark);
}

.session-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  text-transform: uppercase;
}

.session-status.scheduled {
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

.plan-progress {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.session-client,
.plan-client {
  font-size: 13px;
  color: var(--text-mid);
  margin-bottom: 8px;
}

.session-date,
.session-duration {
  font-size: 12px;
  color: var(--text-soft);
  margin-bottom: 4px;
}

.plan-details {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-soft);
  margin-bottom: 8px;
}

.plan-focus {
  font-size: 12px;
  color: var(--sage);
  margin-bottom: 8px;
}

.plan-description,
.session-notes {
  font-size: 13px;
  color: var(--text-mid);
  margin: 8px 0;
}

.session-actions,
.plan-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.review-rating {
  color: var(--gold);
  font-size: 14px;
  margin-bottom: 8px;
}

.review-client {
  font-weight: 500;
  margin-bottom: 8px;
}

.review-comment {
  font-style: italic;
  margin-bottom: 8px;
}

.review-date {
  font-size: 11px;
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
  max-height: 80vh;
  overflow-y: auto;
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

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
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
.profile-status-badge {
  display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 500;
}
.profile-status-badge.active { background: #e8f5e9; color: #2e7d32; }
.profile-status-badge.pending { background: #fff3e0; color: #f57c00; }

.profile-section-label {
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--sage); margin: 24px 0 16px; font-weight: 500;
}
.pf-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pf-group { display: flex; flex-direction: column; gap: 6px; }
.pf-group.pf-full { grid-column: 1 / -1; }
.pf-group label {
  font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--text-mid); font-weight: 500;
}
.pf-group input, .pf-group textarea {
  padding: 10px 12px; border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;
  font-size: 14px; font-family: inherit; color: var(--text-dark); transition: border-color 0.2s;
}
.pf-group input:focus, .pf-group textarea:focus {
  outline: none; border-color: var(--sage); box-shadow: 0 0 0 3px rgba(124,154,109,0.1);
}
.pf-group textarea { resize: vertical; min-height: 100px; }

.profile-success {
  margin: 16px 0; padding: 10px 14px; background: #e8f5e9; color: #2e7d32;
  border-radius: 6px; font-size: 13px;
}
.pf-actions { margin-top: 24px; display: flex; justify-content: flex-end; }

@media (max-width: 768px) {
  .trainer-dashboard {
    padding: 80px 20px 40px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .clients-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    min-width: 300px;
    margin: 20px;
  }
}
</style>