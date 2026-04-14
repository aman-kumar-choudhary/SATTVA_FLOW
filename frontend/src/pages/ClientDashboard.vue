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
            <button class="logout-btn" @click="logout" title="Logout">
              <span class="logout-icon">⏻</span>
              <span class="logout-label">Logout</span>
            </button>
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
              @click="markRead(n._id)">
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
        <div v-if="trainer" class="trainer-banner mb-4">
          <div class="trainer-avatar-lg">{{ trainer.name?.charAt(0) || '?' }}</div>
          <div class="trainer-banner-info">
            <div class="trainer-banner-label">Your Trainer</div>
            <div class="trainer-banner-name">{{ trainer.name }}</div>
            <div class="trainer-banner-spec">{{ trainer.trainer_details?.specialization || 'Yoga Trainer' }}</div>
            <div class="trainer-banner-stats">
              <span>⭐ {{ trainer.avg_rating || 'New' }}</span>
              <span>📅 {{ trainer.trainer_details?.experience || 0 }} yrs exp</span>
            </div>
          </div>
        </div>
        <div v-else class="info-banner mb-4">
          <span>ℹ</span><span>No trainer assigned yet. Admin will assign one soon!</span>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#eff6ff"><span>📅</span></div>
            <div class="stat-body"><div class="stat-number">{{ sessions.length }}</div><div class="stat-label">Total Sessions</div></div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f0fdf4"><span>✅</span></div>
            <div class="stat-body"><div class="stat-number">{{ completedSessions }}</div><div class="stat-label">Completed</div></div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fdf8f0"><span>📋</span></div>
            <div class="stat-body"><div class="stat-number">{{ plans.length }}</div><div class="stat-label">Active Plans</div></div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fdf4ff"><span>⭐</span></div>
            <div class="stat-body"><div class="stat-number">{{ myReviews.length }}</div><div class="stat-label">Reviews Given</div></div>
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

      <!-- ══════ SESSIONS ══════ -->
      <section v-if="activeSection === 'sessions'" class="page-section">
        <div class="empty-state" v-if="sessions.length === 0">No sessions yet.</div>
        <div v-else class="card">
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Title</th><th>Date</th><th>Duration</th><th>Status</th><th>Notes</th></tr></thead>
              <tbody>
                <tr v-for="s in sessions" :key="s._id">
                  <td class="font-medium">{{ s.title }}</td>
                  <td>{{ formatDate(s.scheduled_at) }}</td>
                  <td>{{ s.duration || 60 }}m</td>
                  <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                  <td class="text-muted text-sm">{{ s.notes || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

     

      <!-- ══════ PACKAGES ══════ -->
      <section v-if="activeSection === 'packages'" class="page-section">
        <div class="empty-state" v-if="packages.length === 0">No packages available. Check back soon!</div>
        <div v-else class="packages-grid">
          <div v-for="pkg in packages" :key="pkg._id"
            :class="['package-card', pkg.badge?.toLowerCase().includes('popular') ? 'package-card--featured' : '']">
            <div v-if="pkg.badge" class="pkg-badge">{{ pkg.badge }}</div>
            <div class="package-card-header">
              <h3 class="package-title">{{ pkg.title }}</h3>
              <span class="package-price">₹{{ pkg.price || 0 }}</span>
            </div>
            <p v-if="pkg.description" class="package-desc">{{ pkg.description }}</p>
            <div class="package-meta">
              <span v-if="pkg.sessions_count">🧘 {{ pkg.sessions_count }} sessions</span>
              <span v-if="pkg.duration_weeks">📅 {{ pkg.duration_weeks }} weeks</span>
            </div>
            <ul v-if="pkg.features?.length" class="pkg-features">
              <li v-for="f in pkg.features" :key="f">✓ {{ f }}</li>
            </ul>
            <button
              class="btn-primary w-full mt-auto"
              @click="expressInterest(pkg._id)"
              :disabled="selectedPackageId === pkg._id"
            >
              {{ selectedPackageId === pkg._id ? '✓ Current Selection' : (selectedPackageId ? 'Change Selection' : "Select This Package") }}
            </button>
            <p v-if="selectedPackageId === pkg._id" class="pkg-cta-note" style="color:#4a7c59; font-weight:600">Admin will contact you soon!</p>
            <p v-else class="pkg-cta-note">Admin will only see your latest choice</p>
          </div>
        </div>
      </section>

      <!-- ══════ QUERIES ══════ -->
      <section v-if="activeSection === 'queries'" class="page-section">
        <div class="list-toolbar">
          <h2 class="section-heading">My Queries</h2>
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
              <span class="query-response-label">Response: </span>{{ q.response }}
            </div>
            <div class="text-xs text-muted mt-2">{{ formatDate(q.created_at) }}</div>
          </div>
        </div>
      </section>

      <!-- ══════ REVIEWS ══════ -->
      <section v-if="activeSection === 'reviews'" class="page-section">
        <div class="list-toolbar">
          <h2 class="section-heading">My Reviews</h2>
          <button v-if="trainer && !hasReviewed" @click="showReviewModal = true" class="btn-primary">Write a Review</button>
        </div>
        <div class="empty-state" v-if="myReviews.length === 0">No reviews given yet.</div>
        <div v-else class="card">
          <div v-for="r in myReviews" :key="r._id" class="query-row">
            <div class="review-stars mb-1">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</div>
            <div class="font-medium mb-1">For: {{ trainer?.name || '—' }}</div>
            <p class="text-sm text-muted mb-1">{{ r.comment }}</p>
            <div class="flex-between">
              <span :class="statusPill(r.status)">{{ r.status }}</span>
              <span class="text-xs text-muted">{{ formatDate(r.created_at) }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ══════ PROFILE ══════ -->
      <section v-if="activeSection === 'profile'" class="page-section">
        <div class="card profile-card">
          <div class="detail-header mb-4">
            <div class="detail-avatar" style="background:#4a7c59">{{ profile?.name?.charAt(0) || 'C' }}</div>
            <div class="detail-info">
              <h2 class="detail-name">{{ profile?.name }}</h2>
              <div class="detail-tags">
                <span class="tag">{{ profile?.email }}</span>
                <span v-if="trainer" class="tag">Trainer: {{ trainer.name }}</span>
              </div>
            </div>
          </div>

          <!-- Personal Details -->
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
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">City / Location</label>
              <input type="text" v-model="profileForm.city" class="form-input" placeholder="e.g. Delhi, Mumbai" />
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Age</label>
              <input type="number" v-model="profileForm.age" class="form-input" min="10" max="100" placeholder="Your age" />
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Gender</label>
              <select v-model="profileForm.gender" class="form-input">
                <option value="">Prefer not to say</option>
                <option>Male</option>
                <option>Female</option>
                <option>Non-binary</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          <!-- Yoga Profile -->
          <div class="form-section-label">Yoga Profile</div>
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">Yoga Experience Level</label>
              <select v-model="profileForm.yoga_experience" class="form-input">
                <option value="">Select level</option>
                <option value="beginner">Beginner — No prior experience</option>
                <option value="some">Some — Tried a few classes</option>
                <option value="intermediate">Intermediate — 1–3 years</option>
                <option value="advanced">Advanced — 3+ years</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Health Goals</label>
            <textarea v-model="profileForm.health_goals" rows="3" class="form-input w-full resize-none"
              placeholder="e.g. Weight loss, flexibility, stress relief, back pain management…"></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">What do you expect from this class?</label>
            <textarea v-model="profileForm.expectations" rows="3" class="form-input w-full resize-none"
              placeholder="Tell your trainer what outcomes you're hoping for, your preferred pace, style preferences…"></textarea>
          </div>

          <!-- Health Information -->
          <div class="form-section-label">Health Information</div>
          <div class="form-group">
            <label class="form-label">Health Conditions / Injuries</label>
            <textarea v-model="profileForm.health_conditions" rows="3" class="form-input w-full resize-none"
              placeholder="e.g. Diabetes, lower back pain, knee injury, hypertension — your trainer will adapt sessions accordingly"></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Emergency Contact</label>
            <input type="text" v-model="profileForm.emergency_contact" class="form-input" placeholder="Name & phone, e.g. Raj Kumar +91 98765 43210" />
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
    <div v-if="showQueryModal" class="modal-backdrop" @click.self="showQueryModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <span class="modal-title">Submit a Query</span>
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

    <div v-if="showReviewModal" class="modal-backdrop" @click.self="showReviewModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <span class="modal-title">Review Your Trainer</span>
          <button class="modal-close" @click="showReviewModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Rating</label>
            <div style="display:flex;gap:8px;font-size:28px">
              <button v-for="star in 5" :key="star" @click="reviewForm.rating = star"
                style="background:none;border:none;cursor:pointer;transition:color .2s"
                :style="{ color: star <= reviewForm.rating ? '#f59e0b' : '#e5e7eb' }">★</button>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Your Review</label>
            <textarea v-model="reviewForm.comment" rows="5" class="form-input w-full resize-none" placeholder="Share your experience…"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showReviewModal = false" class="btn-cancel">Cancel</button>
          <button @click="submitReview" class="btn-primary">Submit Review</button>
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
      activeSection: 'overview',
      sidebarCollapsed: false,
      mobileSidebarOpen: false,
      showNotifications: false,
      navItems: [
        { id: 'overview',  icon: '🏠', label: 'Overview' },
        { id: 'sessions',  icon: '📅', label: 'My Sessions' },
        { id: 'packages',  icon: '🎁', label: 'Packages' },
        { id: 'queries',   icon: '💬', label: 'Queries' },
        { id: 'reviews',   icon: '⭐', label: 'Reviews' },
        { id: 'profile',   icon: '👤', label: 'Profile' },
      ],
      quickActions: [
        { id: 'sessions', icon: '📅', label: 'View My Sessions' },
        { id: 'packages', icon: '🎁', label: 'Browse Packages' },
        { id: 'queries',  icon: '💬', label: 'Submit a Query' },
        { id: 'reviews',  icon: '⭐', label: 'Write a Review' },
        { id: 'profile',  icon: '👤', label: 'Edit Profile' },
      ],
      pageTitles: {
        overview: 'My Dashboard', sessions: 'My Sessions',
        packages: 'Packages & Offers', queries: 'My Queries', reviews: 'My Reviews', profile: 'My Profile',
      },
      trainer: null, sessions: [], plans: [], packages: [],
      queries: [], myReviews: [], notifications: [],
      selectedPackageId: null,
      profile: null,
      profileForm: {
        name: '', phone: '',
        city: '', age: '', gender: '',
        yoga_experience: '', health_goals: '',
        expectations: '', health_conditions: '',
        emergency_contact: ''
      },
      profileSaving: false, profileSuccess: '',
      showQueryModal: false, showReviewModal: false,
      queryForm: { subject: '', message: '' },
      reviewForm: { rating: 5, comment: '' },
      pollInterval: null
    }
  },
  computed: {
    completedSessions() { return this.sessions.filter(s => s.status === 'completed').length },
    hasReviewed() { return this.myReviews.some(r => r.status === 'approved' || r.status === 'pending') },
    unreadCount() { return this.notifications.filter(n => !n.read).length }
  },
  async mounted() { await this.loadData(); await this.loadProfile(); this.startPolling() },
  beforeUnmount() { if (this.pollInterval) clearInterval(this.pollInterval) },
  methods: {
    logout() { localStorage.clear(); this.$router.push('/') },
    navigate(section) { this.activeSection = section; this.mobileSidebarOpen = false },
    statusPill(status) {
      const base = 'status-pill '
      const map = { active: base+'status-active', completed: base+'status-completed', scheduled: base+'status-scheduled', cancelled: base+'status-cancelled', pending: base+'status-pending', resolved: base+'status-active', approved: base+'status-active', rejected: base+'status-blocked' }
      return map[status] || base+'status-default'
    },
    async loadData() {
      const r = await api.getDashboardSummary()
      if (r.success) {
        this.trainer = r.trainer
        this.sessions = r.sessions?.items || []
        this.plans = r.plans?.items || []
        this.packages = r.packages?.items || []
        this.queries = r.queries?.items || []
        this.myReviews = r.reviews?.items || []
        this.notifications = r.notifications?.items || []
        this.selectedPackageId = r.selected_package_id
      }
    },
    startPolling() {
      this.pollInterval = setInterval(async () => {
        const r = await api.getNotifications(true)
        if (r.success && (r.items || []).length > this.unreadCount) await this.loadData()
      }, 30000)
    },
    async expressInterest(pkgId) {
      const r = await api.expressInterest(pkgId)
      if (r.success) {
        this.selectedPackageId = pkgId
      } else {
        alert(r.error || 'Failed to record selection')
      }
    },
    async submitQuery() {
      if (!this.queryForm.subject || !this.queryForm.message) { alert('Please fill in all fields'); return }
      const r = await api.createQuery(this.queryForm.subject, this.queryForm.message)
      if (r.success) { this.showQueryModal = false; this.queryForm = { subject: '', message: '' }; await this.loadData() }
      else alert(r.error || 'Failed to submit query')
    },
    async submitReview() {
      if (!this.reviewForm.rating) { alert('Please select a rating'); return }
      const r = await api.createReview(this.reviewForm.rating, this.reviewForm.comment)
      if (r.success) { this.showReviewModal = false; this.reviewForm = { rating: 5, comment: '' }; await this.loadData() }
      else alert(r.error || 'Failed to submit review')
    },
    async markRead(id) { await api.markNotificationRead(id); this.notifications = this.notifications.map(n => n._id === id ? { ...n, read: true } : n) },
    async markAllRead() { await api.markAllRead(); this.notifications = this.notifications.map(n => ({ ...n, read: true })) },
    async loadProfile() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) { const user = JSON.parse(stored); this.profile = user; this._fillProfileForm(user) }
        const res = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
        if (res.ok) {
          const user = await res.json()
          this.profile = user
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('userName', user.name)
          this._fillProfileForm(user)
        }
      } catch (e) {}
    },
    _fillProfileForm(user) {
      this.profileForm.name = user.name || ''
      this.profileForm.phone = user.phone || ''
      this.profileForm.city = user.city || ''
      this.profileForm.age = user.age || ''
      this.profileForm.gender = user.gender || ''
      this.profileForm.yoga_experience = user.yoga_experience || ''
      this.profileForm.health_goals = user.health_goals || ''
      this.profileForm.expectations = user.expectations || ''
      this.profileForm.health_conditions = user.health_conditions || ''
      this.profileForm.emergency_contact = user.emergency_contact || ''
    },
    async saveProfile() {
      this.profileSaving = true; this.profileSuccess = ''
      try {
        const payload = {
          name: this.profileForm.name,
          phone: this.profileForm.phone,
          city: this.profileForm.city,
          age: this.profileForm.age ? parseInt(this.profileForm.age) : null,
          gender: this.profileForm.gender,
          yoga_experience: this.profileForm.yoga_experience,
          health_goals: this.profileForm.health_goals,
          expectations: this.profileForm.expectations,
          health_conditions: this.profileForm.health_conditions,
          emergency_contact: this.profileForm.emergency_contact
        }
        const res = await fetch('/api/auth/profile', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
          body: JSON.stringify(payload)
        })
        if (res.ok) {
          const data = await res.json()
          if (data.user) { localStorage.setItem('user', JSON.stringify(data.user)); this._fillProfileForm(data.user) }
          localStorage.setItem('userName', this.profileForm.name)
          this.userName = this.profileForm.name
          this.profileSuccess = 'Profile updated!'
          setTimeout(() => this.profileSuccess = '', 3000)
        }
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
.user-avatar { width: 32px; height: 32px; border-radius: 50%; background: #4a7c59; color: white; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; }
.user-name { font-size: 13px; color: #6b7280; }

.page-section { padding: 24px; flex: 1; }
.card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; box-shadow: 0 1px 4px rgba(0,0,0,0.04); padding: 20px; }
.card-title { font-family: 'Lora', serif; font-size: 16px; color: #1f2937; font-weight: 500; margin-bottom: 16px; }
.section-heading { font-family: 'Lora', serif; font-size: 18px; color: #1f2937; font-weight: 500; }

.trainer-banner { background: linear-gradient(135deg, #1a1f1a, #4a7c59); border-radius: 16px; padding: 24px; display: flex; gap: 20px; color: white; align-items: center; }
.trainer-avatar-lg { width: 72px; height: 72px; border-radius: 50%; background: #c9a84c; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 700; color: #1a1f1a; flex-shrink: 0; }
.trainer-banner-info { flex: 1; }
.trainer-banner-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.6; margin-bottom: 4px; }
.trainer-banner-name { font-family: 'Lora', serif; font-size: 22px; margin-bottom: 2px; }
.trainer-banner-spec { font-size: 13px; opacity: 0.75; margin-bottom: 8px; }
.trainer-banner-stats { display: flex; gap: 20px; font-size: 12px; opacity: 0.85; }

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

.packages-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.package-card { background: white; border-radius: 16px; border: 1px solid #f0f0ee; box-shadow: 0 1px 4px rgba(0,0,0,0.04); padding: 24px; display: flex; flex-direction: column; gap: 10px; position: relative; transition: box-shadow 0.15s; }
.package-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.package-card--featured { border-color: #4a7c59; box-shadow: 0 4px 20px rgba(74,124,89,0.15); }
.pkg-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #4a7c59; color: white; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding: 4px 14px; border-radius: 20px; }
.package-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-top: 8px; }
.package-title { font-family: 'Lora', serif; font-size: 18px; color: #111827; font-weight: 500; }
.package-price { font-family: 'Lora', serif; font-size: 22px; color: #4a7c59; font-weight: 600; }
.package-desc { font-size: 12px; color: #9ca3af; line-height: 1.5; }
.package-meta { display: flex; flex-direction: column; gap: 4px; }
.package-meta span { font-size: 12px; color: #6b7280; }
.pkg-features { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 4px; }
.pkg-features li { font-size: 12px; color: #4b5563; }
.pkg-cta-note { font-size: 11px; color: #9ca3af; text-align: center; }
.mt-auto { margin-top: auto; }

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
.modal-box { background: white; border-radius: 18px; width: 480px; max-width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.15); animation: modal-in 0.2s ease; }
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

.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 9px 18px; background: #4a7c59; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: background 0.15s; white-space: nowrap; font-family: 'Inter', sans-serif; }
.btn-primary:hover:not(:disabled) { background: #3a6147; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-cancel { display: inline-flex; align-items: center; padding: 9px 18px; background: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; font-family: 'Inter', sans-serif; }
.btn-cancel:hover { background: #e5e7eb; }
.btn-link { background: none; border: none; color: #4a7c59; cursor: pointer; font-size: 13px; font-weight: 500; }

.info-banner { display: flex; align-items: center; gap: 10px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #92400e; }
.info-banner-blue { display: flex; align-items: center; gap: 8px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #1d4ed8; }
.empty-state { text-align: center; padding: 48px 20px; color: #9ca3af; font-size: 13px; background: white; border-radius: 16px; }
.flex-between { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.text-muted { color: #9ca3af; }
.text-xs { font-size: 11px; }
.text-sm { font-size: 13px; }
.font-medium { font-weight: 500; }
.w-full { width: 100%; }
.mb-1 { margin-bottom: 4px; }
.mb-2 { margin-bottom: 8px; }
.mb-3 { margin-bottom: 12px; }
.mb-4 { margin-bottom: 16px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }

.profile-card { max-width: 680px; }
.form-section-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #4a7c59; margin: 20px 0 12px; font-weight: 500; border-bottom: 1px solid #f0f0ee; padding-bottom: 6px; }
.form-row { display: flex; gap: 14px; flex-wrap: wrap; }
.form-row .form-group { min-width: 0; }
.flex-1 { flex: 1; min-width: 140px; }

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
  .packages-grid { grid-template-columns: 1fr; }
  .trainer-banner { flex-direction: column; text-align: center; }
  .trainer-banner-stats { justify-content: center; }
  .notif-dropdown { right: 8px; width: calc(100vw - 16px); }
  .list-toolbar { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
  .quick-actions-grid { grid-template-columns: 1fr 1fr; }
  .page-section { padding: 10px; }
}

/* ═══ LOGOUT BUTTON ═══ */
.logout-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px; border-radius: 8px;
  border: 1px solid #e5e7eb; background: white;
  cursor: pointer; font-size: 13px; font-weight: 500;
  color: #6b7280; transition: all 0.15s;
}
.logout-btn:hover { background: #fef2f2; border-color: #fca5a5; color: #dc2626; }
.logout-icon { font-size: 14px; }
@media (max-width: 640px) { .logout-label { display: none; } }
</style>