<template>
  <div class="dashboard-root">

    <!-- Mobile overlay -->
    <div v-if="mobileSidebarOpen" class="sidebar-overlay" @click="mobileSidebarOpen = false"></div>

    <!-- ═══ SIDEBAR ═══ -->
    <aside :class="['sidebar', sidebarCollapsed ? 'sidebar--collapsed' : '', mobileSidebarOpen ? 'sidebar--mobile-open' : '']">
      <div class="sidebar-brand">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 100" fill="none">
            <defs>
              <linearGradient id="appCG" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#7c9a6e"/><stop offset="100%" style="stop-color:#4a6640"/>
              </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="44" fill="url(#appCG)"/>
            <circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
            <path d="M50 68 Q42 73 38 80 Q44 75 50 73 Q56 75 62 80 Q58 73 50 68Z" fill="#e5b029" opacity="0.9"/>
            <path d="M50 68 Q35 72 30 78 Q38 73 50 71Z" fill="#e5b029" opacity="0.5"/>
            <path d="M50 68 Q65 72 70 78 Q62 73 50 71Z" fill="#e5b029" opacity="0.5"/>
            <circle cx="50" cy="28" r="7" fill="rgba(255,255,255,0.92)"/>
            <line x1="50" y1="35" x2="50" y2="56" stroke="rgba(255,255,255,0.92)" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M50 42 Q40 40 36 44" stroke="rgba(255,255,255,0.85)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M50 42 Q60 40 64 44" stroke="rgba(255,255,255,0.85)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M50 56 Q42 60 38 66" stroke="rgba(255,255,255,0.85)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M50 56 Q58 60 62 66" stroke="rgba(255,255,255,0.85)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <text x="108" y="42" font-family="Georgia, serif" font-size="26" font-weight="500" fill="#2C3E2D" letter-spacing="0.5">SattvaFlow</text>
            <text x="110" y="62" font-family="Georgia, serif" font-size="14" font-weight="300" fill="#c9a84c" letter-spacing="5">YOGA</text>
            <line x1="108" y1="69" x2="290" y2="69" stroke="#d4c9a8" stroke-width="0.75"/>
            <text x="110" y="81" font-family="Arial, sans-serif" font-size="9" fill="#9aab8a" letter-spacing="3">FIND YOUR FLOW</text>
          </svg>
      </div>
      <nav class="sidebar-nav">
        <button
          v-for="item in navItems" :key="item.id"
          @click="navigate(item.id)" :title="item.label"
          :class="['nav-item', activeSection === item.id ? 'nav-item--active' : '']"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
        </button>
      </nav>
      <button class="sidebar-toggle" @click="sidebarCollapsed = !sidebarCollapsed">
        {{ sidebarCollapsed ? '›' : '‹' }}
      </button>
    </aside>

    <!-- ═══ MAIN CONTENT ═══ -->
    <main :class="['main-content', sidebarCollapsed ? 'main-content--collapsed' : '']">

      <!-- Topbar -->
      <header class="topbar">
        <div class="topbar-inner">
          <div class="topbar-left">
            <button class="hamburger-btn" @click="mobileSidebarOpen = !mobileSidebarOpen" aria-label="Toggle menu">
              <span class="hamburger-line"></span>
              <span class="hamburger-line"></span>
              <span class="hamburger-line"></span>
            </button>
            <h1 class="page-title">{{ pageTitles[activeSection] || 'Dashboard' }}</h1>
          </div>
          <div class="topbar-right">
            <div class="notif-btn" @click="showNotifications = !showNotifications">
              <span>🔔</span>
              <span v-if="unreadCount > 0" class="notif-dot">{{ unreadCount }}</span>
            </div>
            <div class="user-chip">
              <div class="user-avatar">{{ userName.charAt(0).toUpperCase() }}</div>
              <span class="user-name">{{ userName }}</span>
            </div>
          </div>
        </div>
        <div v-if="showNotifications" class="notif-dropdown">
          <div class="notif-header">
            <span class="notif-title">Notifications</span>
            <button class="btn-link" @click="markAllRead">Mark all read</button>
          </div>
          <div class="notif-list">
            <div v-for="n in notifications" :key="n._id"
              :class="['notif-item', !n.read ? 'notif-item--unread' : '']"
              @click="markNotifRead(n._id)">
              <div class="notif-item-title">{{ n.title }}</div>
              <div class="notif-item-msg">{{ n.message }}</div>
              <div class="notif-item-time">{{ formatDate(n.created_at) }}</div>
            </div>
            <div v-if="!notifications.length" class="empty-state" style="padding:24px">No notifications</div>
          </div>
        </div>
      </header>

      <!-- ══════ OVERVIEW ══════ -->
      <section v-if="activeSection === 'overview'" class="page-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f0f9f4"><span>👥</span></div>
            <div class="stat-body"><div class="stat-number">{{ clients.length }}</div><div class="stat-label">My Clients</div></div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#eff6ff"><span>📅</span></div>
            <div class="stat-body"><div class="stat-number">{{ sessions.length }}</div><div class="stat-label">Total Sessions</div></div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fdf4ff"><span>⭐</span></div>
            <div class="stat-body"><div class="stat-number">{{ avgRating }}</div><div class="stat-label">Avg Rating</div></div>
          </div>
        </div>

        <div class="card">
          <h3 class="card-title">Quick Actions</h3>
          <div class="quick-actions-grid">
            <button v-for="qa in quickActions" :key="qa.id" @click="navigate(qa.id)" class="quick-action-btn">
              <span class="qa-icon">{{ qa.icon }}</span>
              <span class="qa-label">{{ qa.label }}</span>
            </button>
          </div>
        </div>
      </section>

      <!-- ══════ MY CLIENTS ══════ -->
      <section v-if="activeSection === 'clients'" class="page-section">
        <div class="empty-state" v-if="clients.length === 0">No clients assigned yet.</div>
        <div v-else>
          <!-- Selected client detail panel -->
          <div v-if="selectedClient" class="client-detail-panel mb-4">
            <div class="cdp-header">
              <div class="cdp-avatar">{{ selectedClient.name?.charAt(0) || '?' }}</div>
              <div class="cdp-header-info">
                <h3 class="cdp-name">{{ selectedClient.name }}</h3>
                <div class="cdp-meta">
                  <span v-if="selectedClient.email">✉ {{ selectedClient.email }}</span>
                  <span v-if="selectedClient.phone">📞 {{ selectedClient.phone }}</span>
                  <span v-if="selectedClient.city">📍 {{ selectedClient.city }}</span>
                  <span>Sessions completed: <strong>{{ selectedClient.sessions_completed || 0 }}</strong></span>
                </div>
              </div>
              <button class="cdp-close" @click="selectedClient = null">×</button>
            </div>

            <div class="cdp-tabs">
              <button v-for="tab in clientTabs" :key="tab.id"
                :class="['cdp-tab', clientDetailTab === tab.id ? 'cdp-tab--active' : '']"
                @click="clientDetailTab = tab.id">{{ tab.label }}</button>
            </div>

            <!-- Tab: Overview -->
            <div v-if="clientDetailTab === 'overview'" class="cdp-body">
              <div class="cdp-grid">
                <div class="cdp-field" v-if="selectedClient.age">
                  <span class="cdp-field-label">Age</span>
                  <span class="cdp-field-value">{{ selectedClient.age }}</span>
                </div>
                <div class="cdp-field" v-if="selectedClient.gender">
                  <span class="cdp-field-label">Gender</span>
                  <span class="cdp-field-value">{{ selectedClient.gender }}</span>
                </div>
                <div class="cdp-field" v-if="selectedClient.yoga_experience">
                  <span class="cdp-field-label">Experience</span>
                  <span class="cdp-field-value cdp-badge-exp">{{ selectedClient.yoga_experience }}</span>
                </div>
                <div class="cdp-field" v-if="selectedClient.emergency_contact">
                  <span class="cdp-field-label">Emergency Contact</span>
                  <span class="cdp-field-value">{{ selectedClient.emergency_contact }}</span>
                </div>
              </div>
            </div>

            <!-- Tab: Goals & Expectations -->
            <div v-if="clientDetailTab === 'goals'" class="cdp-body">
              <div class="cdp-block" v-if="selectedClient.health_goals">
                <div class="cdp-block-label">🎯 Health Goals</div>
                <p class="cdp-block-text">{{ selectedClient.health_goals }}</p>
              </div>
              <div class="cdp-block" v-if="selectedClient.expectations">
                <div class="cdp-block-label">💬 Expectations from Class</div>
                <p class="cdp-block-text">{{ selectedClient.expectations }}</p>
              </div>
              <div class="empty-state" style="padding:24px" v-if="!selectedClient.health_goals && !selectedClient.expectations">
                Client hasn't filled in goals yet.
              </div>
            </div>

            <!-- Tab: Health -->
            <div v-if="clientDetailTab === 'health'" class="cdp-body">
              <div class="cdp-block" v-if="selectedClient.health_conditions">
                <div class="cdp-block-label">⚕️ Health Conditions / Injuries</div>
                <p class="cdp-block-text cdp-block-text--warn">{{ selectedClient.health_conditions }}</p>
              </div>
              <div class="empty-state" style="padding:24px" v-else>
                No health conditions reported. Great!
              </div>
            </div>

            <!-- Tab: Sessions -->
            <div v-if="clientDetailTab === 'sessions'" class="cdp-body">
              <div v-if="getClientSessions(selectedClient._id).length === 0" class="empty-state" style="padding:24px">No sessions yet.</div>
              <div v-else class="table-wrap">
                <table class="data-table">
                  <thead><tr><th>Title</th><th>Date</th><th>Status</th><th>Attended</th></tr></thead>
                  <tbody>
                    <tr v-for="s in getClientSessions(selectedClient._id)" :key="s._id">
                      <td class="font-medium">{{ s.title }}</td>
                      <td>{{ formatDate(s.scheduled_at) }}</td>
                      <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                      <td><span v-if="s.attendance_marked" style="color:#16a34a">✓</span><span v-else class="text-muted">—</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Client cards grid -->
          <div class="clients-grid">
            <div :class="['client-card', selectedClient?._id === client._id ? 'client-card--selected' : '']"
              v-for="client in clients" :key="client._id"
              @click="openClientDetail(client)">
              <div class="client-avatar">{{ client.name?.charAt(0) || '?' }}</div>
              <div class="client-info">
                <h4 class="font-medium">{{ client.name }}</h4>
                <p class="text-sm text-muted">{{ client.email || client.phone || '—' }}</p>
                <div class="client-tags mt-1">
                  <span v-if="client.yoga_experience" class="cdp-badge-exp" style="font-size:10px;padding:2px 7px">{{ client.yoga_experience }}</span>
                  <span v-if="client.city" class="tag" style="font-size:10px">📍 {{ client.city }}</span>
                </div>
                <div class="text-xs text-muted mt-1">Sessions: {{ client.sessions_completed || 0 }} done</div>
                <div v-if="client.health_conditions" class="health-warn mt-1">
                  ⚠ {{ client.health_conditions.substring(0, 50) }}{{ client.health_conditions.length > 50 ? '…' : '' }}
                </div>
              </div>
              <button class="view-detail-btn">{{ selectedClient?._id === client._id ? '▲ Less' : '▼ View' }}</button>
            </div>
          </div>
        </div>
      </section>

      <!-- ══════ SESSIONS ══════ -->
      <section v-if="activeSection === 'sessions'" class="page-section">
        <div class="info-banner mb-4">
          <span>ℹ</span><span>Sessions are created by admin. You can mark attendance below.</span>
        </div>
        <div class="empty-state" v-if="sessions.length === 0">No sessions scheduled yet.</div>
        <div v-else class="card">
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Title</th><th>Client</th><th>Date</th><th>Duration</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="s in sessions" :key="s._id">
                  <td class="font-medium">{{ s.title }}</td>
                  <td>{{ getClientName(s.client_id) }}</td>
                  <td>{{ formatDate(s.scheduled_at) }}</td>
                  <td>{{ s.duration || 60 }}m</td>
                  <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                  <td>
                    <button v-if="s.status === 'scheduled'" @click="markAttendance(s._id)" class="micro-approve">✓ Attended</button>
                    <span v-else class="text-muted text-xs">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ══════ REVIEWS ══════ -->
      <section v-if="activeSection === 'reviews'" class="page-section">
        <div class="empty-state" v-if="reviews.length === 0">No reviews yet.</div>
        <div v-else class="card">
          <div v-for="r in reviews" :key="r._id" class="query-row">
            <div class="review-stars mb-1">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</div>
            <div class="font-medium mb-1">{{ r.client?.name || '—' }}</div>
            <p class="text-sm text-muted mb-1" style="font-style:italic">{{ r.comment }}</p>
            <div class="text-xs text-muted">{{ formatDate(r.created_at) }}</div>
          </div>
        </div>
      </section>

      <!-- ══════ QUERIES ══════ -->
      <section v-if="activeSection === 'queries'" class="page-section">
        <div class="list-toolbar">
          <h2 class="section-heading">Queries to Admin</h2>
          <button @click="showQueryModal = true" class="btn-primary">+ New Query</button>
        </div>
        <div class="empty-state" v-if="queries.length === 0">No queries submitted yet.</div>
        <div v-else class="card">
          <div v-for="q in queries" :key="q._id" class="query-row">
            <div class="flex-between mb-2">
              <strong class="font-medium">{{ q.subject }}</strong>
              <span :class="statusPill(q.status)">{{ q.status }}</span>
            </div>
            <p class="text-sm text-muted mb-2">{{ q.message }}</p>
            <div v-if="q.response" class="query-response">
              <span class="query-response-label">Admin Response: </span>{{ q.response }}
            </div>
            <div class="text-xs text-muted mt-2">{{ formatDate(q.created_at) }}</div>
          </div>
        </div>
      </section>

      <!-- ══════ PROFILE ══════ -->
      <section v-if="activeSection === 'profile'" class="page-section">
        <div class="card" style="max-width:620px">
          <div class="detail-header mb-4">
            <div class="detail-avatar" style="background:#7c6a4a">{{ profile?.name?.charAt(0) || 'T' }}</div>
            <div class="detail-info">
              <h2 class="detail-name">{{ profile?.name }}</h2>
              <div class="detail-tags">
                <span class="tag">{{ profile?.email }}</span>
                <span :class="['status-pill', profile?.status === 'active' ? 'status-active' : 'status-pending']">
                  {{ profile?.status === 'active' ? '✓ Active' : '⏳ Pending Approval' }}
                </span>
              </div>
            </div>
          </div>

          <div class="form-section-label">Personal Details</div>
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">Full Name</label>
              <input type="text" v-model="profileForm.name" class="form-input" placeholder="Your full name" />
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Phone / WhatsApp</label>
              <input type="tel" v-model="profileForm.phone" class="form-input" placeholder="+91 98765 43210" />
            </div>
          </div>

          <div class="form-section-label">Trainer Details</div>
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">Specialization</label>
              <input type="text" v-model="profileForm.specialization" class="form-input" placeholder="e.g. Hatha Yoga, Vinyasa" />
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Years of Experience</label>
              <input type="number" v-model="profileForm.experience" class="form-input" min="0" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Certifications (comma separated)</label>
            <input type="text" v-model="profileForm.certifications" class="form-input" placeholder="e.g. RYT-200, YAI" />
          </div>
          <div class="form-group">
            <label class="form-label">Bio</label>
            <textarea v-model="profileForm.bio" rows="4" class="form-input w-full resize-none" placeholder="Tell clients about yourself…"></textarea>
          </div>

          <div v-if="profileSuccess" class="info-banner-blue mb-3">✓ {{ profileSuccess }}</div>
          <div style="display:flex;justify-content:flex-end">
            <button class="btn-primary" :disabled="profileSaving" @click="saveProfile">
              {{ profileSaving ? 'Saving…' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </section>

    </main>

    <!-- ══════ MODALS ══════ -->

    <!-- Query Modal -->
    <div v-if="showQueryModal" class="modal-backdrop" @click.self="showQueryModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <span class="modal-title">Submit Query to Admin</span>
          <button class="modal-close" @click="showQueryModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Subject</label>
            <input type="text" v-model="queryForm.subject" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Message</label>
            <textarea v-model="queryForm.message" rows="5" class="form-input w-full resize-none"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showQueryModal = false" class="btn-cancel">Cancel</button>
          <button @click="submitQuery" class="btn-primary">Submit</button>
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
      activeSection: 'overview',
      sidebarCollapsed: false,
      mobileSidebarOpen: false,
      showNotifications: false,
      navItems: [
        { id: 'overview',  icon: '🏠', label: 'Overview' },
        { id: 'clients',   icon: '👥', label: 'My Clients' },
        { id: 'sessions',  icon: '📅', label: 'Sessions' },
        { id: 'reviews',   icon: '⭐', label: 'Reviews' },
        { id: 'queries',   icon: '💬', label: 'Queries' },
        { id: 'profile',   icon: '👤', label: 'Profile' },
      ],
      quickActions: [
        { id: 'clients',  icon: '👥', label: 'View My Clients' },
        { id: 'sessions', icon: '📅', label: 'View Sessions' },
        { id: 'reviews',  icon: '⭐', label: 'Client Reviews' },
        { id: 'queries',  icon: '💬', label: 'Submit Query' },
        { id: 'profile',  icon: '👤', label: 'Edit Profile' },
      ],
      pageTitles: {
        overview: 'Trainer Dashboard', clients: 'My Clients', sessions: 'My Sessions',
        plans: 'Yoga Plans', reviews: 'Client Reviews', queries: 'Queries', profile: 'My Profile',
      },
      clients: [], sessions: [], plans: [], reviews: [], queries: [], notifications: [],
      selectedClient: null,
      clientDetailTab: 'overview',
      clientTabs: [
        { id: 'overview',  label: '👤 Overview' },
        { id: 'goals',     label: '🎯 Goals & Expectations' },
        { id: 'health',    label: '⚕️ Health' },
        { id: 'sessions',  label: '📅 Sessions' },
      ],
      profile: null,
      profileForm: { name: '', phone: '', specialization: '', experience: '', certifications: '', bio: '' },
      profileSaving: false, profileSuccess: '',
      showPlanModal: false, showQueryModal: false,
      planForm: { client_id: '', title: '', description: '', weeks: 4, sessions_per_week: 3, focus_areas_str: '' },
      queryForm: { subject: '', message: '' },
      pollInterval: null
    }
  },
  computed: {
    avgRating() {
      if (!this.reviews.length) return 'N/A'
      return (this.reviews.reduce((a, r) => a + r.rating, 0) / this.reviews.length).toFixed(1)
    },
    unreadCount() { return this.notifications.filter(n => !n.read).length }
  },
  async mounted() { await this.loadData(); await this.loadProfile(); this.startPolling() },
  beforeUnmount() { if (this.pollInterval) clearInterval(this.pollInterval) },
  methods: {
    navigate(section) { this.activeSection = section; this.mobileSidebarOpen = false; this.selectedClient = null },
    openClientDetail(client) {
      if (this.selectedClient?._id === client._id) { this.selectedClient = null; return }
      this.selectedClient = client
      this.clientDetailTab = 'overview'
    },
    getClientSessions(clientId) {
      return this.sessions.filter(s => s.client_id === clientId || s.client?.id === clientId)
    },
    statusPill(status) {
      const base = 'status-pill '
      const map = { active: base+'status-active', completed: base+'status-completed', scheduled: base+'status-scheduled', cancelled: base+'status-cancelled', pending: base+'status-pending', resolved: base+'status-active', approved: base+'status-active', rejected: base+'status-blocked' }
      return map[status] || base+'status-default'
    },
    getClientName(clientId) { const c = this.clients.find(c => c._id === clientId); return c ? c.name : 'Unknown' },
    async loadData() {
      const [clientsR, sessionsR, plansR, reviewsR, queriesR, notifsR] = await Promise.all([
        api.getTrainerClients(), api.getTrainerSessions(), api.getTrainerPlans(),
        api.getTrainerReviews(), api.getTrainerQueries(), api.getNotifications()
      ])
      this.clients = clientsR.items || []; this.sessions = sessionsR.items || []
      this.plans = plansR.items || []; this.reviews = reviewsR.items || []
      this.queries = queriesR.items || []; this.notifications = notifsR.items || []
    },
    startPolling() {
      this.pollInterval = setInterval(async () => {
        const r = await api.getNotifications(true)
        if (r.success && (r.items || []).length > this.unreadCount) await this.loadData()
      }, 30000)
    },
    async markAttendance(sessionId) {
      const r = await api.markAttendance(sessionId)
      if (r.success) await this.loadData()
      else alert(r.error || 'Failed to mark attendance')
    },
    openPlanModal(client) {
      this.planForm = { client_id: client ? client._id : '', title: '', description: '', weeks: 4, sessions_per_week: 3, focus_areas_str: '' }
      this.showPlanModal = true
    },
    async createPlan() {
      if (!this.planForm.client_id || !this.planForm.title) { alert('Please fill in required fields'); return }
      const data = { ...this.planForm, focus_areas: this.planForm.focus_areas_str.split(',').map(s => s.trim()).filter(Boolean) }
      const r = await api.createPlan(data)
      if (r.success) { this.showPlanModal = false; await this.loadData() }
      else alert(r.error || 'Failed to create plan')
    },
    async updateProgress(planId, currentProgress) {
      const input = prompt('Enter progress percentage (0–100):', currentProgress || 0)
      if (input === null) return
      const progress = parseInt(input)
      if (isNaN(progress) || progress < 0 || progress > 100) { alert('Please enter a number between 0 and 100'); return }
      const r = await api.updatePlanProgress(planId, progress)
      if (r.success) await this.loadData()
      else alert(r.error || 'Failed to update progress')
    },
    async submitQuery() {
      if (!this.queryForm.subject || !this.queryForm.message) { alert('Please fill in all fields'); return }
      const r = await api.createTrainerQuery(this.queryForm.subject, this.queryForm.message)
      if (r.success) { this.showQueryModal = false; this.queryForm = { subject: '', message: '' }; await this.loadData() }
      else alert(r.error || 'Failed to submit query')
    },
    async markNotifRead(id) { await api.markNotificationRead(id); this.notifications = this.notifications.map(n => n._id === id ? { ...n, read: true } : n) },
    async markAllRead() { await api.markAllRead(); this.notifications = this.notifications.map(n => ({ ...n, read: true })) },
    async loadProfile() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) { const user = JSON.parse(stored); this.profile = user; this._fillProfileForm(user) }
        const res = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
        if (res.ok) { const user = await res.json(); this.profile = user; localStorage.setItem('user', JSON.stringify(user)); localStorage.setItem('userName', user.name); this._fillProfileForm(user) }
      } catch (e) {}
    },
    _fillProfileForm(user) {
      this.profileForm.name = user.name || ''; this.profileForm.phone = user.phone || ''
      const td = user.trainer_details || {}
      this.profileForm.specialization = td.specialization || ''; this.profileForm.experience = td.experience || ''
      this.profileForm.certifications = Array.isArray(td.certifications) ? td.certifications.join(', ') : (td.certifications || '')
      this.profileForm.bio = td.bio || ''
    },
    async saveProfile() {
      this.profileSaving = true; this.profileSuccess = ''
      try {
        const payload = { name: this.profileForm.name, phone: this.profileForm.phone, specialization: this.profileForm.specialization, experience: parseInt(this.profileForm.experience) || 0, certifications: this.profileForm.certifications, bio: this.profileForm.bio }
        const res = await fetch('/api/auth/profile', { method: 'PUT', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` }, body: JSON.stringify(payload) })
        if (res.ok) { const data = await res.json(); localStorage.setItem('userName', data.user.name); this.userName = data.user.name; this.profileSuccess = 'Profile updated!'; setTimeout(() => this.profileSuccess = '', 3000) }
      } catch (e) {} finally { this.profileSaving = false }
    },
    formatDate(d) { if (!d) return '—'; return new Date(d).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }) }
  }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 45; backdrop-filter: blur(2px); }
.hamburger-btn { display: none; flex-direction: column; justify-content: center; gap: 5px; background: none; border: none; cursor: pointer; padding: 6px; border-radius: 8px; flex-shrink: 0; transition: background 0.15s; }
.hamburger-btn:hover { background: #f3f4f6; }
.hamburger-line { display: block; width: 20px; height: 2px; background: #374151; border-radius: 2px; }

.dashboard-root { display: flex; min-height: 100vh; background: #f5f4f0; font-family: 'Inter', sans-serif; }

.sidebar { position: fixed; top: 0; left: 0; bottom: 0; width: 220px; background: #1a1f1a; display: flex; flex-direction: column; z-index: 50; transition: width 0.25s ease; overflow: hidden; }
.sidebar--collapsed { width: 64px; }
.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.08); flex-shrink: 0; }
.sidebar-logo { font-size: 20px; flex-shrink: 0; }
.sidebar-name { color: white; font-family: 'Lora', serif; font-size: 17px; white-space: nowrap; }
.sidebar-nav { flex: 1; padding: 10px 8px; display: flex; flex-direction: column; gap: 2px; overflow-y: auto; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px; border-radius: 8px; cursor: pointer; font-size: 13px; color: rgba(255,255,255,0.5); background: none; border: none; width: 100%; text-align: left; transition: background 0.15s, color 0.15s; white-space: nowrap; }
.nav-item:hover { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.85); }
.nav-item--active { background: #4a7c59; color: white; }
.nav-icon { font-size: 16px; flex-shrink: 0; }
.nav-label { flex: 1; }
.sidebar-toggle { background: none; border: none; border-top: 1px solid rgba(255,255,255,0.08); color: rgba(255,255,255,0.3); font-size: 18px; cursor: pointer; padding: 12px; text-align: right; transition: color 0.15s; flex-shrink: 0; }
.sidebar-toggle:hover { color: rgba(255,255,255,0.6); }

.main-content { margin-left: 220px; flex: 1; display: flex; flex-direction: column; min-height: 100vh; transition: margin-left 0.25s ease; }
.main-content--collapsed { margin-left: 64px; }

.topbar { position: sticky; top: 0; z-index: 40; background: white; border-bottom: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.topbar-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; padding: 0 24px; gap: 16px; }
.topbar-left { display: flex; align-items: center; gap: 12px; }
.page-title { font-family: 'Lora', serif; font-size: 20px; color: #111827; font-weight: 500; }
.topbar-right { display: flex; align-items: center; gap: 14px; flex-shrink: 0; }
.notif-btn { position: relative; cursor: pointer; font-size: 20px; padding: 4px; }
.notif-dot { position: absolute; top: -4px; right: -4px; background: #ef4444; color: white; font-size: 10px; font-weight: 600; min-width: 16px; height: 16px; border-radius: 99px; display: flex; align-items: center; justify-content: center; padding: 0 3px; }
.notif-dropdown { position: absolute; top: 64px; right: 16px; width: 340px; background: white; border: 1px solid #e5e7eb; border-radius: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); z-index: 200; overflow: hidden; }
.notif-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid #f3f4f6; }
.notif-title { font-size: 14px; font-weight: 600; color: #1f2937; }
.notif-list { max-height: 360px; overflow-y: auto; }
.notif-item { padding: 12px 16px; border-bottom: 1px solid #f9fafb; cursor: pointer; transition: background 0.15s; }
.notif-item:hover { background: #fafaf8; }
.notif-item--unread { background: #f0f9f4; border-left: 3px solid #4a7c59; }
.notif-item-title { font-size: 13px; font-weight: 600; color: #1f2937; margin-bottom: 2px; }
.notif-item-msg { font-size: 12px; color: #6b7280; margin-bottom: 4px; }
.notif-item-time { font-size: 11px; color: #9ca3af; }
.user-chip { display: flex; align-items: center; gap: 8px; }
.user-avatar { width: 32px; height: 32px; border-radius: 50%; background: #7c6a4a; color: white; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; }
.user-name { font-size: 13px; color: #6b7280; }

.page-section { padding: 24px; flex: 1; }
.card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; box-shadow: 0 1px 4px rgba(0,0,0,0.04); padding: 20px; }
.card-title { font-family: 'Lora', serif; font-size: 16px; color: #1f2937; font-weight: 500; margin-bottom: 16px; }
.section-heading { font-family: 'Lora', serif; font-size: 18px; color: #1f2937; font-weight: 500; }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.stat-card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; box-shadow: 0 1px 4px rgba(0,0,0,0.04); padding: 18px; display: flex; flex-direction: column; gap: 10px; }
.stat-icon-wrap { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.stat-number { font-family: 'Lora', serif; font-size: 28px; color: #111827; font-weight: 500; }
.stat-label { font-size: 12px; color: #9ca3af; margin-top: 3px; }

.quick-actions-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.quick-action-btn { display: flex; align-items: center; gap: 10px; padding: 14px; border-radius: 10px; border: 1px solid #f0f0ee; background: white; cursor: pointer; text-align: left; transition: border-color 0.15s, background 0.15s; }
.quick-action-btn:hover { border-color: rgba(74,124,89,0.3); background: rgba(74,124,89,0.04); }
.qa-icon { font-size: 22px; }
.qa-label { font-size: 13px; font-weight: 500; color: #374151; }

.clients-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.client-card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; align-items: flex-start; gap: 16px; cursor: pointer; transition: border-color 0.15s, box-shadow 0.15s; }
.client-card:hover { border-color: rgba(74,124,89,0.3); box-shadow: 0 4px 12px rgba(74,124,89,0.08); }
.client-card--selected { border-color: #4a7c59; box-shadow: 0 4px 16px rgba(74,124,89,0.15); }
.client-avatar { width: 48px; height: 48px; border-radius: 50%; background: rgba(124,106,74,0.15); color: #7c6a4a; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; flex-shrink: 0; }
.client-info { flex: 1; min-width: 0; }
.client-actions { flex-shrink: 0; }
.client-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.health-warn { font-size: 11px; color: #b45309; background: #fef3c7; border-radius: 6px; padding: 3px 8px; line-height: 1.4; }
.view-detail-btn { flex-shrink: 0; padding: 5px 10px; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb; color: #6b7280; font-size: 11px; cursor: pointer; align-self: flex-start; transition: all 0.15s; }
.view-detail-btn:hover { background: #4a7c59; color: white; border-color: #4a7c59; }

/* ── CLIENT DETAIL PANEL ── */
.client-detail-panel { background: white; border-radius: 16px; border: 2px solid #4a7c59; box-shadow: 0 4px 20px rgba(74,124,89,0.12); overflow: hidden; }
.cdp-header { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: linear-gradient(135deg, #1a1f1a, #2d4a38); }
.cdp-avatar { width: 56px; height: 56px; border-radius: 50%; background: #c9a84c; color: #1a1f1a; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; flex-shrink: 0; }
.cdp-header-info { flex: 1; }
.cdp-name { font-family: 'Lora', serif; font-size: 20px; color: white; margin-bottom: 6px; }
.cdp-meta { display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px; color: rgba(255,255,255,0.6); }
.cdp-close { background: rgba(255,255,255,0.1); border: none; color: white; font-size: 20px; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: background 0.15s; }
.cdp-close:hover { background: rgba(255,255,255,0.2); }
.cdp-tabs { display: flex; border-bottom: 1px solid #f0f0ee; padding: 0 16px; gap: 4px; background: #fafaf8; }
.cdp-tab { background: none; border: none; padding: 12px 14px; font-size: 12px; font-weight: 500; color: #9ca3af; cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.15s; white-space: nowrap; }
.cdp-tab:hover { color: #374151; }
.cdp-tab--active { color: #4a7c59; border-bottom-color: #4a7c59; }
.cdp-body { padding: 20px; }
.cdp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
.cdp-field { background: #f9fafb; border-radius: 10px; padding: 12px 14px; }
.cdp-field-label { display: block; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 4px; }
.cdp-field-value { font-size: 14px; color: #1f2937; font-weight: 500; }
.cdp-badge-exp { display: inline-block; background: #eff6ff; color: #2563eb; font-size: 11px; padding: 3px 10px; border-radius: 99px; font-weight: 500; text-transform: capitalize; }
.cdp-block { margin-bottom: 16px; }
.cdp-block:last-child { margin-bottom: 0; }
.cdp-block-label { font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
.cdp-block-text { font-size: 14px; color: #374151; line-height: 1.7; background: #f9fafb; border-radius: 10px; padding: 14px; border-left: 3px solid #4a7c59; }
.cdp-block-text--warn { border-left-color: #f59e0b; background: #fffbeb; color: #92400e; }

.plans-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.plan-card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.plan-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.plan-title { font-family: 'Lora', serif; font-size: 16px; color: #111827; font-weight: 500; }
.plan-pct { background: #f0fdf4; color: #16a34a; font-size: 12px; font-weight: 600; padding: 3px 8px; border-radius: 99px; }
.plan-desc { font-size: 12px; color: #9ca3af; margin-bottom: 10px; line-height: 1.5; }
.plan-meta { display: flex; gap: 12px; font-size: 12px; color: #6b7280; margin-bottom: 8px; }
.plan-focus { font-size: 12px; color: #4a7c59; margin-bottom: 8px; }
.progress-bar-bg { height: 8px; background: #f3f4f6; border-radius: 99px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: #4a7c59; border-radius: 99px; transition: width 0.4s ease; }
.progress-note { font-size: 11px; color: #9ca3af; margin-top: 6px; }

.list-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.query-row { padding: 16px 0; border-bottom: 1px solid #f3f4f6; }
.query-row:last-child { border-bottom: none; }
.query-response { background: rgba(74,124,89,0.06); border-left: 2px solid #4a7c59; border-radius: 6px; padding: 10px 12px; font-size: 13px; color: #374151; margin-top: 8px; }
.query-response-label { font-size: 11px; font-weight: 600; color: #4a7c59; text-transform: uppercase; letter-spacing: 0.05em; }
.review-stars { font-size: 18px; letter-spacing: 1px; color: #f59e0b; }

.detail-header { display: flex; align-items: flex-start; gap: 16px; flex-wrap: wrap; }
.detail-avatar { width: 60px; height: 60px; border-radius: 14px; color: white; font-family: 'Lora', serif; font-size: 24px; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.detail-info { flex: 1; }
.detail-name { font-family: 'Lora', serif; font-size: 22px; color: #111827; margin-bottom: 8px; }
.detail-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.tag { display: inline-block; background: #f3f4f6; color: #6b7280; font-size: 12px; padding: 3px 10px; border-radius: 99px; }

.form-section-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #4a7c59; margin: 20px 0 12px; font-weight: 500; }
.form-row { display: flex; gap: 14px; flex-wrap: wrap; }
.form-row .form-group { min-width: 0; }
.flex-1 { flex: 1; min-width: 120px; }

.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { background: #f9fafb; padding: 10px 16px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #9ca3af; border-bottom: 1px solid #f3f4f6; }
.data-table td { padding: 12px 16px; color: #4b5563; border-bottom: 1px solid #f9fafb; vertical-align: middle; }
.data-table tr:last-child td { border-bottom: none; }

.status-pill { display: inline-block; font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 99px; white-space: nowrap; }
.status-active { background: #f0fdf4; color: #16a34a; }
.status-pending { background: #fef3c7; color: #d97706; }
.status-blocked { background: #fef2f2; color: #dc2626; }
.status-completed { background: #eff6ff; color: #2563eb; }
.status-scheduled { background: #f5f3ff; color: #7c3aed; }
.status-cancelled { background: #f9fafb; color: #9ca3af; }
.status-default { background: #f9fafb; color: #6b7280; }

.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.modal-box { background: white; border-radius: 18px; width: 520px; max-width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.15); animation: modal-in 0.2s ease; }
@keyframes modal-in { from { transform: scale(0.96) translateY(8px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 22px; border-bottom: 1px solid #f3f4f6; }
.modal-title { font-family: 'Lora', serif; font-size: 18px; color: #111827; }
.modal-close { background: none; border: none; font-size: 22px; cursor: pointer; color: #9ca3af; padding: 0 4px; }
.modal-close:hover { color: #374151; }
.modal-body { padding: 22px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 14px 22px; border-top: 1px solid #f3f4f6; }

.form-input { width: 100%; padding: 9px 12px; border: 1px solid #e5e7eb; border-radius: 7px; font-size: 13px; font-family: 'Inter', sans-serif; outline: none; transition: border-color 0.15s; background: white; color: #1f2937; }
.form-input:focus { border-color: #4a7c59; }
.form-group { margin-bottom: 14px; }
.form-label { display: block; font-size: 12px; font-weight: 500; color: #6b7280; margin-bottom: 5px; }
.resize-none { resize: none; }
.w-full { width: 100%; }

.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 9px 18px; background: #4a7c59; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: background 0.15s; white-space: nowrap; font-family: 'Inter', sans-serif; }
.btn-primary:hover:not(:disabled) { background: #3a6147; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-cancel { display: inline-flex; align-items: center; padding: 9px 18px; background: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; font-family: 'Inter', sans-serif; }
.btn-cancel:hover { background: #e5e7eb; }
.btn-link { background: none; border: none; color: #4a7c59; cursor: pointer; font-size: 13px; font-weight: 500; text-decoration: underline; }
.micro-approve { padding: 5px 12px; border: none; border-radius: 5px; cursor: pointer; font-size: 11px; font-weight: 500; background: #f0fdf4; color: #16a34a; font-family: 'Inter', sans-serif; transition: all 0.12s; }
.micro-approve:hover { background: #16a34a; color: white; }

.info-banner { display: flex; align-items: center; gap: 10px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #92400e; }
.info-banner-blue { display: flex; align-items: center; gap: 8px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #1d4ed8; }
.empty-state { text-align: center; padding: 48px 20px; color: #9ca3af; font-size: 13px; background: white; border-radius: 16px; }
.flex-between { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.text-muted { color: #9ca3af; }
.text-xs { font-size: 11px; }
.text-sm { font-size: 13px; }
.font-medium { font-weight: 500; }
.mb-1 { margin-bottom: 4px; }
.mb-2 { margin-bottom: 8px; }
.mb-3 { margin-bottom: 12px; }
.mb-4 { margin-bottom: 16px; }
.mt-1 { margin-top: 4px; }
.mt-3 { margin-top: 12px; }

@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }

@media (max-width: 768px) {
  .sidebar-overlay { display: block; }
  .hamburger-btn { display: flex; }
  .sidebar { transform: translateX(-100%); transition: transform 0.25s ease; width: 220px !important; }
  .sidebar--mobile-open { transform: translateX(0); }
  .main-content { margin-left: 0 !important; }
  .sidebar-toggle { display: none; }
  .topbar-inner { padding: 0 14px; }
  .user-name { display: none; }
  .page-title { font-size: 16px; }
  .page-section { padding: 14px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .quick-actions-grid { grid-template-columns: repeat(2, 1fr); }
  .clients-grid { grid-template-columns: 1fr; }
  .cdp-tabs { overflow-x: auto; }
  .cdp-grid { grid-template-columns: repeat(2, 1fr); }
  .notif-dropdown { right: 8px; width: calc(100vw - 16px); }
  .list-toolbar { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
  .quick-actions-grid { grid-template-columns: 1fr 1fr; }
  .page-section { padding: 10px; }
}
</style>