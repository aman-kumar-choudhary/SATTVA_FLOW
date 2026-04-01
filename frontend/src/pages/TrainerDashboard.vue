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
      >{{ tab.name }}</button>
    </div>

    <!-- ══ MY CLIENTS TAB ══ -->
    <div v-if="activeTab === 'clients'" class="tab-content">
      <div class="section-header"><h2>My Clients</h2></div>
      <div class="empty-state" v-if="clients.length === 0">No clients assigned yet.</div>
      <div class="clients-grid" v-else>
        <div class="client-card" v-for="client in clients" :key="client._id">
          <div class="client-avatar">{{ client.name ? client.name.charAt(0) : '?' }}</div>
          <div class="client-info">
            <h4>{{ client.name }}</h4>
            <p>{{ client.email || client.phone || '—' }}</p>
            <div class="client-stats">
              <span>Sessions completed: {{ client.sessions_completed || 0 }}</span>
            </div>
          </div>
          <div class="client-actions">
            <button @click="openPlanModal(client)" class="btn-primary small">+ Yoga Plan</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ SESSIONS TAB (view-only — admin creates sessions) ══ -->
    <div v-if="activeTab === 'sessions'" class="tab-content">
      <div class="section-header">
        <h2>My Sessions</h2>
        <div class="info-notice">ℹ️ Sessions are created by admin. You can mark attendance below.</div>
      </div>
      <div class="empty-state" v-if="sessions.length === 0">No sessions scheduled yet.</div>
      <div class="sessions-list" v-else>
        <div class="session-card" v-for="session in sessions" :key="session._id">
          <div class="session-header">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-status" :class="session.status">{{ session.status }}</div>
          </div>
          <div class="session-client">👤 Client: {{ getClientName(session.client_id) }}</div>
          <div class="session-date" v-if="session.scheduled_at">📅 {{ formatDate(session.scheduled_at) }}</div>
          <div class="session-duration">⏱️ {{ session.duration || 60 }} minutes</div>
          <div class="session-notes" v-if="session.notes">📝 {{ session.notes }}</div>
          <div class="session-actions" v-if="session.status === 'scheduled'">
            <button @click="markAttendance(session._id)" class="btn-approve small">✓ Mark Attended</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ YOGA PLANS TAB (trainer creates plans for clients) ══ -->
    <div v-if="activeTab === 'plans'" class="tab-content">
      <div class="section-header">
        <h2>Yoga Plans</h2>
        <button @click="openPlanModal(null)" class="btn-primary">+ New Plan</button>
      </div>
      <div class="empty-state" v-if="plans.length === 0">No yoga plans yet. Create one for your clients.</div>
      <div class="plans-list" v-else>
        <div class="plan-card" v-for="plan in plans" :key="plan._id">
          <div class="plan-header">
            <div class="plan-title">{{ plan.title }}</div>
            <div class="plan-progress">{{ plan.progress || 0 }}% Complete</div>
          </div>
          <div class="plan-client">👤 Client: {{ getClientName(plan.client_id) }}</div>
          <div class="plan-details">
            <span>📅 {{ plan.weeks }} weeks</span>
            <span>🏋️ {{ plan.sessions_per_week }} sessions/week</span>
          </div>
          <div class="plan-focus" v-if="plan.focus_areas?.length">
            🎯 Focus: {{ plan.focus_areas.join(', ') }}
          </div>
          <div class="plan-description" v-if="plan.description">{{ plan.description }}</div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: (plan.progress || 0) + '%' }"></div>
          </div>
          <div class="plan-actions">
            <button @click="updateProgress(plan._id, plan.progress)" class="btn-link">Update Progress</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ REVIEWS TAB ══ -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="section-header"><h2>Client Reviews</h2></div>
      <div class="empty-state" v-if="reviews.length === 0">No reviews yet.</div>
      <div class="reviews-list" v-else>
        <div class="review-card" v-for="review in reviews" :key="review._id">
          <div class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</div>
          <div class="review-client">{{ review.client?.name || '—' }}</div>
          <div class="review-comment">{{ review.comment }}</div>
          <div class="review-date">{{ formatDate(review.created_at) }}</div>
        </div>
      </div>
    </div>

    <!-- ══ QUERIES TAB ══ -->
    <div v-if="activeTab === 'queries'" class="tab-content">
      <div class="section-header">
        <h2>My Queries to Admin</h2>
        <button @click="showQueryModal = true" class="btn-primary">+ New Query</button>
      </div>
      <div class="empty-state" v-if="queries.length === 0">No queries submitted yet.</div>
      <div class="queries-list" v-else>
        <div class="query-card" v-for="query in queries" :key="query._id">
          <div class="query-header">
            <div class="query-subject">{{ query.subject }}</div>
            <div class="query-status" :class="query.status">{{ query.status }}</div>
          </div>
          <div class="query-message">{{ query.message }}</div>
          <div v-if="query.response" class="query-response"><strong>Admin Response:</strong> {{ query.response }}</div>
          <div class="query-date">{{ formatDate(query.created_at) }}</div>
        </div>
      </div>
    </div>

    <!-- ══ PROFILE TAB ══ -->
    <div v-if="activeTab === 'profile'" class="tab-content">
      <div class="section-header"><h2>My Profile</h2></div>
      <div class="profile-card">
        <div class="profile-avatar-row">
          <img v-if="profile && profile.picture" :src="profile.picture" class="profile-avatar-img" alt="avatar" />
          <div v-else class="profile-avatar-fallback">{{ profile?.name ? profile.name.charAt(0) : 'T' }}</div>
          <div class="profile-meta">
            <div class="profile-name">{{ profile?.name }}</div>
            <div class="profile-email">{{ profile?.email }}</div>
            <div class="profile-status-badge" :class="profile?.status">
              {{ profile?.status === 'active' ? '✓ Active' : '⏳ Pending Approval' }}
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
              <input type="number" v-model="profileForm.experience" min="0" />
            </div>
            <div class="pf-group pf-full">
              <label>Certifications (comma separated)</label>
              <input type="text" v-model="profileForm.certifications" placeholder="e.g. RYT-200, YAI" />
            </div>
            <div class="pf-group pf-full">
              <label>Bio</label>
              <textarea v-model="profileForm.bio" rows="4" placeholder="Tell clients about yourself…"></textarea>
            </div>
          </div>

          <div v-if="profileSuccess" class="profile-success">✓ {{ profileSuccess }}</div>
          <div class="pf-actions">
            <button class="btn-primary" :disabled="profileSaving" @click="saveProfile">
              {{ profileSaving ? 'Saving…' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ Notifications Bell ══ -->
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
          v-for="n in notifications"
          :key="n._id"
          class="notification-item"
          :class="{ unread: !n.read }"
          @click="markNotifRead(n._id)"
        >
          <div class="notification-title">{{ n.title }}</div>
          <div class="notification-message">{{ n.message }}</div>
          <div class="notification-time">{{ formatDate(n.created_at) }}</div>
        </div>
        <div v-if="!notifications.length" class="no-notifications">No notifications</div>
      </div>
    </div>

    <!-- ══ MODALS ══ -->

    <!-- Query Modal -->
    <div v-if="showQueryModal" class="modal-overlay" @click="showQueryModal = false">
      <div class="modal-content" @click.stop>
        <h3>Submit Query to Admin</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Subject</label>
            <input type="text" v-model="queryForm.subject" />
          </div>
          <div class="input-group">
            <label>Message</label>
            <textarea v-model="queryForm.message" rows="5"></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitQuery" class="btn-primary">Submit</button>
          <button @click="showQueryModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Plan Modal -->
    <div v-if="showPlanModal" class="modal-overlay" @click="showPlanModal = false">
      <div class="modal-content" @click.stop>
        <h3>Create Yoga Plan</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Client *</label>
            <select v-model="planForm.client_id">
              <option value="">— select client —</option>
              <option v-for="c in clients" :key="c._id" :value="c._id">{{ c.name }}</option>
            </select>
          </div>
          <div class="input-group">
            <label>Plan Title *</label>
            <input type="text" v-model="planForm.title" placeholder="e.g. 4-Week Flexibility Journey" />
          </div>
          <div class="input-group">
            <label>Description</label>
            <textarea v-model="planForm.description" rows="3"></textarea>
          </div>
          <div class="input-group">
            <label>Duration (weeks)</label>
            <input type="number" v-model="planForm.weeks" min="1" />
          </div>
          <div class="input-group">
            <label>Sessions per Week</label>
            <input type="number" v-model="planForm.sessions_per_week" min="1" />
          </div>
          <div class="input-group">
            <label>Focus Areas (comma separated)</label>
            <input type="text" v-model="planForm.focus_areas_str" placeholder="e.g. Flexibility, Strength, Balance" />
          </div>
        </div>
        <div class="modal-actions">
          <button @click="createPlan" class="btn-primary">Create Plan</button>
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
        { id: 'clients',  name: 'My Clients' },
        { id: 'sessions', name: 'Sessions' },
        { id: 'plans',    name: 'Yoga Plans' },
        { id: 'reviews',  name: 'Reviews' },
        { id: 'queries',  name: 'Queries' },
        { id: 'profile',  name: '👤 Profile' }
      ],
      clients:       [],
      sessions:      [],
      plans:         [],
      reviews:       [],
      queries:       [],
      notifications: [],
      showNotifications: false,
      profile:       null,
      profileForm:   { name: '', phone: '', specialization: '', experience: '', certifications: '', bio: '' },
      profileSaving: false,
      profileSuccess: '',
      showPlanModal:   false,
      showQueryModal:  false,
      planForm: {
        client_id: '',
        title: '',
        description: '',
        weeks: 4,
        sessions_per_week: 3,
        focus_areas_str: ''
      },
      queryForm: { subject: '', message: '' },
      pollInterval: null
    }
  },
  computed: {
    avgRating() {
      if (!this.reviews.length) return 'N/A'
      const sum = this.reviews.reduce((acc, r) => acc + r.rating, 0)
      return (sum / this.reviews.length).toFixed(1)
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
      const [clientsR, sessionsR, plansR, reviewsR, queriesR, notifsR] = await Promise.all([
        api.getTrainerClients(),
        api.getTrainerSessions(),
        api.getTrainerPlans(),
        api.getTrainerReviews(),
        api.getTrainerQueries(),
        api.getNotifications()
      ])

      // All return { success, items }
      this.clients       = clientsR.items   || []
      this.sessions      = sessionsR.items  || []
      this.plans         = plansR.items     || []
      this.reviews       = reviewsR.items   || []
      this.queries       = queriesR.items   || []
      this.notifications = notifsR.items    || []
    },

    startPolling() {
      this.pollInterval = setInterval(async () => {
        const r = await api.getNotifications(true)
        if (r.success) {
          const newUnread = (r.items || []).length
          if (newUnread > this.unreadCount) {
            await this.loadData()
          }
        }
      }, 30000)
    },

    getClientName(clientId) {
      const c = this.clients.find(c => c._id === clientId)
      return c ? c.name : 'Unknown'
    },

    // Sessions — mark attendance only (no create)
    async markAttendance(sessionId) {
      const r = await api.markAttendance(sessionId)
      if (r.success) {
        await this.loadData()
      } else {
        alert(r.error || 'Failed to mark attendance')
      }
    },

    // Yoga plans
    openPlanModal(client) {
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
      const data = {
        ...this.planForm,
        focus_areas: this.planForm.focus_areas_str.split(',').map(s => s.trim()).filter(Boolean)
      }
      const r = await api.createPlan(data)
      if (r.success) {
        this.showPlanModal = false
        await this.loadData()
      } else {
        alert(r.error || 'Failed to create plan')
      }
    },
    async updateProgress(planId, currentProgress) {
      const input = prompt('Enter progress percentage (0–100):', currentProgress || 0)
      if (input === null) return
      const progress = parseInt(input)
      if (isNaN(progress) || progress < 0 || progress > 100) {
        alert('Please enter a number between 0 and 100')
        return
      }
      const r = await api.updatePlanProgress(planId, progress)
      if (r.success) {
        await this.loadData()
      } else {
        alert(r.error || 'Failed to update progress')
      }
    },

    // Queries
    async submitQuery() {
      if (!this.queryForm.subject || !this.queryForm.message) {
        alert('Please fill in all fields')
        return
      }
      const r = await api.createTrainerQuery(this.queryForm.subject, this.queryForm.message)
      if (r.success) {
        this.showQueryModal = false
        this.queryForm = { subject: '', message: '' }
        await this.loadData()
      } else {
        alert(r.error || 'Failed to submit query')
      }
    },

    // Notifications
    async markNotifRead(id) {
      await api.markNotificationRead(id)
      this.notifications = this.notifications.map(n => n._id === id ? { ...n, read: true } : n)
    },
    async markAllRead() {
      await api.markAllRead()
      this.notifications = this.notifications.map(n => ({ ...n, read: true }))
    },

    // Profile
    async loadProfile() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) {
          const user = JSON.parse(stored)
          this.profile = user
          this._fillProfileForm(user)
        }
        const res = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        if (res.ok) {
          const user = await res.json()
          this.profile = user
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('userName', user.name)
          this._fillProfileForm(user)
        }
      } catch (e) { /* silent */ }
    },
    _fillProfileForm(user) {
      this.profileForm.name   = user.name  || ''
      this.profileForm.phone  = user.phone || ''
      const td = user.trainer_details || {}
      this.profileForm.specialization  = td.specialization || ''
      this.profileForm.experience      = td.experience     || ''
      this.profileForm.certifications  = Array.isArray(td.certifications)
        ? td.certifications.join(', ')
        : (td.certifications || '')
      this.profileForm.bio = td.bio || ''
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
          this.userName = data.user.name
          this.profileSuccess = 'Profile updated successfully!'
          setTimeout(() => this.profileSuccess = '', 3000)
        }
      } catch (e) { /* silent */ } finally {
        this.profileSaving = false
      }
    },

    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })
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

.empty-state {
  padding: 60px 0;
  text-align: center;
  color: var(--text-soft);
  font-size: 14px;
  background: white;
  border-radius: 8px;
}

.info-notice {
  font-size: 12px;
  color: var(--text-soft);
  background: #f0f7ef;
  border: 1px solid #c8e6c9;
  padding: 8px 14px;
  border-radius: 20px;
}

.dashboard-header { margin-bottom: 40px; }
.dashboard-header h1 { font-size: 36px; font-family: 'Cormorant Garamond', serif; color: var(--text-dark); margin-bottom: 8px; }
.dashboard-header p  { color: var(--text-soft); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}
.stat-card {
  background: white; padding: 24px; border-radius: 12px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04); transition: transform .3s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.08); }
.stat-icon  { font-size: 32px; }
.stat-value { font-size: 28px; font-weight: 600; color: var(--sage); font-family: 'Cormorant Garamond', serif; }
.stat-label { font-size: 12px; color: var(--text-soft); text-transform: uppercase; letter-spacing: 1px; }

.tabs {
  display: flex; gap: 4px; border-bottom: 1px solid #e0e0d8; margin-bottom: 32px; flex-wrap: wrap;
}
.tabs button {
  padding: 12px 20px; background: none; border: none;
  font-size: 13px; font-weight: 500; color: var(--text-soft);
  cursor: pointer; transition: all .3s; position: relative; white-space: nowrap;
}
.tabs button.active { color: var(--sage); }
.tabs button.active::after {
  content: ''; position: absolute; bottom: -1px; left: 0; right: 0;
  height: 2px; background: var(--sage);
}

.section-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;
}
.section-header h2 { font-size: 24px; font-family: 'Cormorant Garamond', serif; }

.clients-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px;
}
.client-card {
  background: white; padding: 20px; border-radius: 8px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.client-avatar {
  width: 48px; height: 48px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: white;
}
.client-info { flex: 1; }
.client-info h4 { margin-bottom: 4px; }
.client-info p  { font-size: 12px; color: var(--text-soft); margin-bottom: 4px; }
.client-stats   { font-size: 11px; color: var(--text-mid); }
.client-actions { display: flex; flex-direction: column; gap: 6px; }

.sessions-list, .plans-list, .reviews-list, .queries-list {
  display: flex; flex-direction: column; gap: 16px;
}
.session-card, .plan-card, .review-card, .query-card {
  background: white; padding: 20px; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.session-header, .plan-header, .query-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
}
.session-title, .plan-title, .query-subject {
  font-weight: 600; font-size: 16px; color: var(--text-dark);
}
.session-status {
  padding: 4px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase;
}
.session-status.scheduled { background: #fff3e0; color: #f57c00; }
.session-status.completed { background: #e8f5e9; color: #2e7d32; }
.session-status.cancelled { background: #ffebee; color: #c62828; }
.session-client, .session-date, .session-duration, .session-notes { font-size: 12px; color: var(--text-soft); margin-bottom: 4px; }
.session-actions { margin-top: 10px; display: flex; gap: 8px; }

.plan-progress { background: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
.plan-client   { font-size: 13px; color: var(--text-mid); margin-bottom: 8px; }
.plan-details  { display: flex; gap: 16px; font-size: 12px; color: var(--text-soft); margin-bottom: 6px; }
.plan-focus    { font-size: 12px; color: var(--sage); margin-bottom: 6px; }
.plan-description { font-size: 13px; color: var(--text-mid); margin-bottom: 8px; }
.plan-actions  { margin-top: 10px; display: flex; gap: 8px; }
.progress-bar  { height: 6px; background: #f0f0e8; border-radius: 3px; overflow: hidden; margin-top: 10px; }
.progress-fill { height: 100%; background: var(--sage); transition: width .3s; }

.query-status { padding: 4px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; }
.query-status.pending  { background: #fff3e0; color: #f57c00; }
.query-status.resolved { background: #e8f5e9; color: #2e7d32; }
.query-message  { font-size: 13px; color: var(--text-mid); margin-bottom: 8px; }
.query-response { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 8px 0; font-size: 13px; }
.query-date     { font-size: 11px; color: var(--text-soft); }

.review-rating  { color: var(--gold); font-size: 18px; margin-bottom: 6px; }
.review-client  { font-weight: 500; margin-bottom: 6px; }
.review-comment { font-style: italic; margin-bottom: 6px; }
.review-date    { font-size: 11px; color: var(--text-soft); }

/* Notification Bell */
.notification-bell {
  position: fixed; top: 100px; right: 40px;
  width: 48px; height: 48px; background: white; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,.1);
  transition: all .3s; z-index: 100;
}
.notification-bell:hover { transform: scale(1.05); }
.bell-icon { font-size: 24px; }
.notification-badge {
  position: absolute; top: -5px; right: -5px;
  background: #f44336; color: white; font-size: 11px;
  padding: 2px 6px; border-radius: 10px;
}
.notifications-dropdown {
  position: fixed; top: 160px; right: 40px; width: 350px;
  background: white; border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,.15); z-index: 101; overflow: hidden;
}
.notifications-header {
  padding: 16px; border-bottom: 1px solid #f0f0e8;
  display: flex; justify-content: space-between; align-items: center;
}
.notifications-header h4 { font-size: 16px; }
.notifications-list { max-height: 400px; overflow-y: auto; }
.notification-item {
  padding: 12px 16px; border-bottom: 1px solid #f0f0e8;
  cursor: pointer; transition: background .3s;
}
.notification-item:hover { background: #fafaf5; }
.notification-item.unread { background: #f0f7ef; border-left: 3px solid var(--sage); }
.notification-title   { font-weight: 600; font-size: 13px; margin-bottom: 4px; }
.notification-message { font-size: 12px; color: var(--text-mid); margin-bottom: 4px; }
.notification-time    { font-size: 10px; color: var(--text-soft); }
.no-notifications     { padding: 40px; text-align: center; color: var(--text-soft); }

/* Buttons */
.btn-primary { background: var(--sage); color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; transition: all .3s; }
.btn-primary:hover { background: var(--sage-dark); }
.btn-primary.small { padding: 6px 12px; font-size: 12px; }
.btn-secondary { background: #f5f5f0; border: 1px solid #e0e0d8; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
.btn-link { background: none; border: none; color: var(--sage); cursor: pointer; font-size: 12px; text-decoration: underline; }
.btn-approve { background: var(--sage); color: white; border: none; border-radius: 4px; cursor: pointer; }
.btn-approve.small { padding: 4px 10px; font-size: 11px; }

/* Modal */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.5);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-content {
  background: white; padding: 32px; border-radius: 12px;
  min-width: 450px; max-width: 550px; max-height: 80vh; overflow-y: auto; width: 100%;
}
.modal-content h3 { margin-bottom: 24px; font-size: 20px; }
.modal-body { margin-bottom: 24px; }
.input-group { margin-bottom: 16px; }
.input-group label { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 500; color: var(--text-mid); }
.input-group input, .input-group select, .input-group textarea {
  width: 100%; padding: 10px 12px; border: 1px solid #e0e0d8;
  border-radius: 6px; font-size: 14px; font-family: inherit; box-sizing: border-box;
}
.input-group input:focus, .input-group select:focus, .input-group textarea:focus {
  outline: none; border-color: var(--sage);
}
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

/* Profile */
.profile-card { background: white; border-radius: 12px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,.04); }
.profile-avatar-row { display: flex; align-items: center; gap: 20px; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid rgba(0,0,0,.06); }
.profile-avatar-img { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(124,154,109,.2); }
.profile-avatar-fallback {
  width: 72px; height: 72px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; color: white; font-family: 'Cormorant Garamond', serif;
}
.profile-meta { flex: 1; }
.profile-name  { font-size: 22px; font-weight: 600; color: var(--text-dark); margin-bottom: 4px; }
.profile-email { font-size: 13px; color: var(--text-soft); margin-bottom: 10px; }
.profile-status-badge { display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 500; }
.profile-status-badge.active  { background: #e8f5e9; color: #2e7d32; }
.profile-status-badge.pending { background: #fff3e0; color: #f57c00; }
.profile-section-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--sage); margin: 24px 0 16px; font-weight: 500; }
.pf-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pf-group { display: flex; flex-direction: column; gap: 6px; }
.pf-group.pf-full { grid-column: 1 / -1; }
.pf-group label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-mid); font-weight: 500; }
.pf-group input, .pf-group textarea {
  padding: 10px 12px; border: 1px solid rgba(0,0,0,.1); border-radius: 6px;
  font-size: 14px; font-family: inherit; color: var(--text-dark); transition: border-color .2s;
}
.pf-group input:focus, .pf-group textarea:focus { outline: none; border-color: var(--sage); box-shadow: 0 0 0 3px rgba(124,154,109,.1); }
.pf-group textarea { resize: vertical; min-height: 100px; }
.profile-success { margin: 16px 0; padding: 10px 14px; background: #e8f5e9; color: #2e7d32; border-radius: 6px; font-size: 13px; }
.pf-actions { margin-top: 24px; display: flex; justify-content: flex-end; }

@media (max-width: 768px) {
  .trainer-dashboard { padding: 80px 20px 40px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .clients-grid { grid-template-columns: 1fr; }
  .modal-content { min-width: 300px; margin: 20px; }
  .pf-grid { grid-template-columns: 1fr; }
  .notifications-dropdown { width: calc(100% - 40px); right: 20px; }
  .notification-bell { right: 20px; }
}
</style>