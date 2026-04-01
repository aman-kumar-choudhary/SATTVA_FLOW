<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>Admin Dashboard</h1>
      <p>Welcome back, {{ userName }}</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_trainers || 0 }}</div>
          <div class="stat-label">Total Trainers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🧘</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.active_trainers || 0 }}</div>
          <div class="stat-label">Active Trainers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🙋</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_clients || 0 }}</div>
          <div class="stat-label">Total Clients</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.active_clients || 0 }}</div>
          <div class="stat-label">Active Clients</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_sessions || 0 }}</div>
          <div class="stat-label">Total Sessions</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pending_queries || 0 }}</div>
          <div class="stat-label">Pending Queries</div>
        </div>
      </div>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="loading-bar">Loading dashboard data…</div>

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

    <!-- ══ TRAINERS TAB ══ -->
    <div v-if="activeTab === 'trainers'" class="tab-content">
      <div class="section-header">
        <h2>Trainer Management</h2>
        <div class="filter-buttons">
          <button
            v-for="status in ['all', 'pending', 'active', 'rejected']"
            :key="status"
            :class="{ active: trainerFilter === status }"
            @click="trainerFilter = status"
          >{{ status.toUpperCase() }}</button>
        </div>
      </div>
      <div class="empty-state" v-if="filteredTrainers.length === 0">No trainers found.</div>
      <div class="trainers-table" v-else>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email / Phone</th>
              <th>Specialization</th>
              <th>Experience</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trainer in filteredTrainers" :key="trainer._id">
              <td>{{ trainer.name }}</td>
              <td>{{ trainer.email || trainer.phone || '—' }}</td>
              <td>{{ trainer.trainer_details?.specialization || trainer.specialization || '—' }}</td>
              <td>{{ trainer.trainer_details?.experience || trainer.experience || 0 }} yrs</td>
              <td><span :class="['status-badge', trainer.status]">{{ trainer.status }}</span></td>
              <td class="actions">
                <button v-if="trainer.status === 'pending'" class="btn-approve" @click="approveTrainer(trainer._id)">Approve</button>
                <button v-if="trainer.status === 'pending'" class="btn-reject"  @click="rejectTrainer(trainer._id)">Reject</button>
                <button v-if="trainer.status === 'active'"  class="btn-block"   @click="blockTrainer(trainer._id)">Block</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ══ CLIENTS TAB ══ -->
    <div v-if="activeTab === 'clients'" class="tab-content">
      <div class="section-header">
        <h2>Client Management</h2>
        <button class="btn-primary" @click="showAssignModal = true">+ Assign Client to Trainer</button>
      </div>
      <div class="empty-state" v-if="clients.length === 0">No clients found.</div>
      <div class="clients-grid" v-else>
        <div class="client-card" v-for="client in clients" :key="client._id">
          <div class="client-avatar">{{ client.name ? client.name.charAt(0) : '?' }}</div>
          <div class="client-info">
            <h4>{{ client.name }}</h4>
            <p>{{ client.email || client.phone || '—' }}</p>
            <span class="status-badge small" :class="client.status">{{ client.status }}</span>
          </div>
          <div class="client-assignment">
            <strong>Trainer:</strong>
            <span v-if="getTrainerForClient(client._id)">{{ getTrainerForClient(client._id) }}</span>
            <button v-else class="btn-link" @click="openAssignForClient(client)">Assign</button>
          </div>
          <div class="client-actions-col">
            <button v-if="client.status === 'pending'" class="btn-approve small" @click="activateClient(client._id)">Activate</button>
            <button v-if="client.status === 'active'"  class="btn-block small"   @click="blockClient(client._id)">Block</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ ASSIGNMENTS TAB ══ -->
    <div v-if="activeTab === 'assignments'" class="tab-content">
      <div class="section-header"><h2>Trainer–Client Assignments</h2></div>
      <div class="empty-state" v-if="assignments.length === 0">No assignments yet.</div>
      <div class="assignments-table" v-else>
        <table>
          <thead>
            <tr><th>Trainer</th><th>Client</th><th>Assigned Date</th><th>Sessions Completed</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="a in assignments" :key="a._id">
              <td>{{ a.trainer?.name || '—' }}</td>
              <td>{{ a.client?.name  || '—' }}</td>
              <td>{{ formatDate(a.created_at) }}</td>
              <td>{{ a.sessions_completed || 0 }}</td>
              <td>
                <button class="btn-link" @click="openReassign(a)">Reassign</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ══ SESSIONS TAB (Admin-only create) ══ -->
    <div v-if="activeTab === 'sessions'" class="tab-content">
      <div class="section-header">
        <h2>Session Management</h2>
        <button class="btn-primary" @click="openSessionModal(null)">+ New Session</button>
      </div>
      <div class="empty-state" v-if="sessions.length === 0">No sessions yet.</div>
      <div class="sessions-list" v-else>
        <div class="session-card" v-for="s in sessions" :key="s._id">
          <div class="session-header">
            <div class="session-title">{{ s.title }}</div>
            <div class="session-status" :class="s.status">{{ s.status }}</div>
          </div>
          <div class="session-meta">
            <span>👤 Client: {{ s.client?.name || '—' }}</span>
            <span>🏋️ Trainer: {{ s.trainer?.name || '—' }}</span>
            <span v-if="s.scheduled_at">📅 {{ formatDate(s.scheduled_at) }}</span>
            <span>⏱️ {{ s.duration || 60 }} min</span>
          </div>
          <div class="session-actions">
            <button class="btn-link"   @click="openSessionModal(s)">Edit</button>
            <button class="btn-reject small" @click="deleteSession(s._id)">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ PACKAGES / OFFERS TAB ══ -->
    <div v-if="activeTab === 'packages'" class="tab-content">
      <div class="section-header">
        <h2>Packages & Offers</h2>
        <button class="btn-primary" @click="openPackageModal(null)">+ New Package</button>
      </div>
      <div class="empty-state" v-if="packages.length === 0">No packages yet. Create one to show offers to clients.</div>
      <div class="packages-grid" v-else>
        <div class="package-card" v-for="pkg in packages" :key="pkg._id" :class="{ inactive: !pkg.is_active }">
          <div class="package-header">
            <div class="package-title">{{ pkg.title }}</div>
            <div class="package-price">₹{{ pkg.price || 0 }}</div>
          </div>
          <div class="package-desc">{{ pkg.description }}</div>
          <div class="package-details">
            <span v-if="pkg.duration_weeks">📅 {{ pkg.duration_weeks }} weeks</span>
            <span v-if="pkg.sessions_count">🧘 {{ pkg.sessions_count }} sessions</span>
            <span v-if="pkg.features?.length">✅ {{ pkg.features.length }} features</span>
          </div>
          <div class="package-interests" v-if="pkg.interested_clients?.length">
            🙋 {{ pkg.interested_clients.length }} interested client(s)
          </div>
          <div class="package-status">
            <span :class="['status-badge', pkg.is_active ? 'active' : 'inactive-badge']">
              {{ pkg.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div class="package-actions">
            <button class="btn-link"   @click="openPackageModal(pkg)">Edit</button>
            <button class="btn-block small" @click="togglePackage(pkg._id)">{{ pkg.is_active ? 'Deactivate' : 'Activate' }}</button>
            <button class="btn-reject small" @click="deletePackage(pkg._id)">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ QUERIES TAB ══ -->
    <div v-if="activeTab === 'queries'" class="tab-content">
      <div class="section-header"><h2>Client &amp; Trainer Queries</h2></div>
      <div class="empty-state" v-if="queries.length === 0">No pending queries.</div>
      <div class="queries-list" v-else>
        <div class="query-card" v-for="query in queries" :key="query._id">
          <div class="query-header">
            <div class="query-sender">
              <strong>{{ query.sender?.name || 'Unknown' }}</strong>
              <span class="query-role">{{ query.sender_role }}</span>
            </div>
            <div class="query-date">{{ formatDate(query.created_at) }}</div>
          </div>
          <div class="query-subject">{{ query.subject }}</div>
          <div class="query-message">{{ query.message }}</div>
          <div v-if="query.status === 'resolved'" class="query-response">
            <strong>Response:</strong> {{ query.response }}
          </div>
          <div v-else class="query-actions">
            <textarea v-model="query.responseText" placeholder="Type your response…" rows="2"></textarea>
            <button @click="respondToQuery(query._id, query.responseText)" class="btn-primary small">Send Response</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ REVIEWS TAB ══ -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="section-header"><h2>Review Moderation</h2></div>
      <div class="empty-state" v-if="pendingReviews.length === 0">No reviews pending approval.</div>
      <div class="reviews-list" v-else>
        <div class="review-card" v-for="review in pendingReviews" :key="review._id">
          <div class="review-header">
            <div class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</div>
            <div class="review-date">{{ formatDate(review.created_at) }}</div>
          </div>
          <div class="review-client">Client: {{ review.client?.name || '—' }}</div>
          <div class="review-trainer">Trainer: {{ review.trainer?.name || '—' }}</div>
          <div class="review-comment">{{ review.comment }}</div>
          <div class="review-actions">
            <button @click="approveReview(review._id)" class="btn-approve">Approve</button>
            <button @click="rejectReview(review._id)"  class="btn-reject">Reject</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════ MODALS ══════ -->

    <!-- Assign / Reassign Modal -->
    <div v-if="showAssignModal" class="modal-overlay" @click="showAssignModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ reassignMode ? 'Reassign Client' : 'Assign Client to Trainer' }}</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Select Trainer</label>
            <select v-model="assignData.trainer_id">
              <option value="">— choose trainer —</option>
              <option v-for="t in activeTrainers" :key="t._id" :value="t._id">
                {{ t.name }} — {{ t.trainer_details?.specialization || t.specialization || 'General' }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Select Client</label>
            <select v-model="assignData.client_id" :disabled="reassignMode">
              <option value="">— choose client —</option>
              <option v-for="c in (reassignMode ? clients : unassignedClients)" :key="c._id" :value="c._id">
                {{ c.name }} — {{ c.email || c.phone }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitAssign" class="btn-primary">{{ reassignMode ? 'Reassign' : 'Assign' }}</button>
          <button @click="showAssignModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Session Modal (admin creates session) -->
    <div v-if="showSessionModal" class="modal-overlay" @click="showSessionModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingSession ? 'Edit Session' : 'Create New Session' }}</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Trainer</label>
            <select v-model="sessionForm.trainer_id">
              <option value="">— select trainer —</option>
              <option v-for="t in activeTrainers" :key="t._id" :value="t._id">{{ t.name }}</option>
            </select>
          </div>
          <div class="input-group">
            <label>Client</label>
            <select v-model="sessionForm.client_id">
              <option value="">— select client —</option>
              <option v-for="c in activeClients" :key="c._id" :value="c._id">{{ c.name }}</option>
            </select>
          </div>
          <div class="input-group">
            <label>Session Title</label>
            <input type="text" v-model="sessionForm.title" placeholder="e.g. Morning Flow" />
          </div>
          <div class="input-group">
            <label>Scheduled Date &amp; Time</label>
            <input type="datetime-local" v-model="sessionForm.scheduled_at" />
          </div>
          <div class="input-group">
            <label>Duration (minutes)</label>
            <input type="number" v-model="sessionForm.duration" min="15" />
          </div>
          <div class="input-group">
            <label>Notes</label>
            <textarea v-model="sessionForm.notes" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitSession" class="btn-primary">{{ editingSession ? 'Update' : 'Create' }}</button>
          <button @click="showSessionModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Package Modal -->
    <div v-if="showPackageModal" class="modal-overlay" @click="showPackageModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingPackage ? 'Edit Package' : 'Create New Package / Offer' }}</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Package Title *</label>
            <input type="text" v-model="packageForm.title" placeholder="e.g. Beginner's 12-Week Journey" />
          </div>
          <div class="input-group">
            <label>Description</label>
            <textarea v-model="packageForm.description" rows="3" placeholder="What's included in this package…"></textarea>
          </div>
          <div class="pkg-grid">
            <div class="input-group">
              <label>Price (₹)</label>
              <input type="number" v-model="packageForm.price" placeholder="0" min="0" />
            </div>
            <div class="input-group">
              <label>Duration (weeks)</label>
              <input type="number" v-model="packageForm.duration_weeks" placeholder="8" min="1" />
            </div>
            <div class="input-group">
              <label>Number of Sessions</label>
              <input type="number" v-model="packageForm.sessions_count" placeholder="24" min="1" />
            </div>
            <div class="input-group">
              <label>Sessions / Week</label>
              <input type="number" v-model="packageForm.sessions_per_week" placeholder="3" min="1" />
            </div>
          </div>
          <div class="input-group">
            <label>Features (comma separated)</label>
            <input type="text" v-model="packageForm.features_str" placeholder="e.g. Personalized plan, WhatsApp support, Diet guide" />
          </div>
          <div class="input-group">
            <label>Badge / Tag (optional)</label>
            <input type="text" v-model="packageForm.badge" placeholder="e.g. Most Popular, New, Limited Offer" />
          </div>
        </div>
        <div class="modal-actions">
          <button @click="submitPackage" class="btn-primary">{{ editingPackage ? 'Update' : 'Create Package' }}</button>
          <button @click="showPackageModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      userName: localStorage.getItem('userName') || 'Admin',
      loading: false,
      activeTab: 'trainers',
      tabs: [
        { id: 'trainers',  name: 'Trainers' },
        { id: 'clients',   name: 'Clients' },
        { id: 'assignments', name: 'Assignments' },
        { id: 'sessions',  name: 'Sessions' },
        { id: 'packages',  name: '🎁 Packages & Offers' },
        { id: 'queries',   name: 'Queries' },
        { id: 'reviews',   name: 'Reviews' }
      ],
      stats: {},
      trainers: [],
      trainerFilter: 'all',
      clients: [],
      assignments: [],
      sessions: [],
      packages: [],
      queries: [],
      pendingReviews: [],
      // Assign modal
      showAssignModal: false,
      reassignMode: false,
      assignData: { trainer_id: '', client_id: '' },
      // Session modal
      showSessionModal: false,
      editingSession: null,
      sessionForm: { trainer_id: '', client_id: '', title: '', scheduled_at: '', duration: 60, notes: '' },
      // Package modal
      showPackageModal: false,
      editingPackage: null,
      packageForm: { title: '', description: '', price: '', duration_weeks: '', sessions_count: '', sessions_per_week: '', features_str: '', badge: '' }
    }
  },
  computed: {
    filteredTrainers() {
      if (this.trainerFilter === 'all') return this.trainers
      return this.trainers.filter(t => t.status === this.trainerFilter)
    },
    activeTrainers() {
      return this.trainers.filter(t => t.status === 'active')
    },
    activeClients() {
      return this.clients.filter(c => c.status === 'active')
    },
    unassignedClients() {
      const assigned = new Set(this.assignments.map(a => a.client_id || a.client?._id))
      return this.activeClients.filter(c => !assigned.has(c._id))
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [statsR, trainersR, clientsR, assignmentsR, sessionsR, packagesR, queriesR, reviewsR] = await Promise.all([
          api.getStats(),
          api.getTrainers(),
          api.getClients(),
          api.getAssignments(),
          api.adminGetSessions(),
          api.getPackages(),
          api.getQueries(),
          api.getReviews()
        ])

        if (statsR.success) this.stats = statsR
        // All list calls return { success, items }
        this.trainers      = trainersR.items      || []
        this.clients       = clientsR.items       || []
        this.assignments   = assignmentsR.items   || []
        this.sessions      = sessionsR.items      || []
        this.packages      = packagesR.items      || []
        this.queries       = queriesR.items       || []
        this.pendingReviews = reviewsR.items      || []
      } finally {
        this.loading = false
      }
    },

    // ── Trainer actions ──
    async approveTrainer(id) {
      const r = await api.approveTrainer(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async rejectTrainer(id) {
      const reason = prompt('Enter rejection reason:')
      if (!reason) return
      const r = await api.rejectTrainer(id, reason)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async blockTrainer(id) {
      if (!confirm('Block this trainer?')) return
      const r = await api.blockTrainer(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },

    // ── Client actions ──
    async activateClient(id) {
      const r = await api.activateClient(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async blockClient(id) {
      if (!confirm('Block this client?')) return
      const r = await api.blockClient(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },

    // ── Assign helpers ──
    getTrainerForClient(clientId) {
      const a = this.assignments.find(a => (a.client_id === clientId || a.client?._id === clientId))
      return a?.trainer?.name || null
    },
    openAssignForClient(client) {
      this.reassignMode = false
      this.assignData = { trainer_id: '', client_id: client._id }
      this.showAssignModal = true
    },
    openReassign(assignment) {
      this.reassignMode = true
      this.assignData = {
        trainer_id: '',
        client_id: assignment.client_id || assignment.client?._id || ''
      }
      this.showAssignModal = true
    },
    async submitAssign() {
      if (!this.assignData.trainer_id || !this.assignData.client_id) {
        alert('Please select both trainer and client')
        return
      }
      let r
      if (this.reassignMode) {
        r = await api.reassignClient(this.assignData.client_id, this.assignData.trainer_id)
      } else {
        r = await api.assignClient(this.assignData.trainer_id, this.assignData.client_id)
      }
      if (r.success) {
        this.showAssignModal = false
        this.assignData = { trainer_id: '', client_id: '' }
        await this.loadData()
      } else {
        alert(r.error || 'Failed to assign')
      }
    },

    // ── Session actions ──
    openSessionModal(session) {
      if (session) {
        this.editingSession = session
        this.sessionForm = {
          trainer_id:   session.trainer_id || session.trainer?._id || '',
          client_id:    session.client_id  || session.client?._id  || '',
          title:        session.title       || '',
          scheduled_at: session.scheduled_at ? session.scheduled_at.slice(0, 16) : '',
          duration:     session.duration    || 60,
          notes:        session.notes       || ''
        }
      } else {
        this.editingSession = null
        this.sessionForm = { trainer_id: '', client_id: '', title: '', scheduled_at: '', duration: 60, notes: '' }
      }
      this.showSessionModal = true
    },
    async submitSession() {
      if (!this.sessionForm.trainer_id || !this.sessionForm.client_id || !this.sessionForm.title || !this.sessionForm.scheduled_at) {
        alert('Please fill in all required fields')
        return
      }
      let r
      if (this.editingSession) {
        r = await api.adminUpdateSession(this.editingSession._id, this.sessionForm)
      } else {
        r = await api.adminCreateSession(this.sessionForm)
      }
      if (r.success) {
        this.showSessionModal = false
        await this.loadData()
      } else {
        alert(r.error || 'Failed to save session')
      }
    },
    async deleteSession(id) {
      if (!confirm('Delete this session?')) return
      const r = await api.adminDeleteSession(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },

    // ── Package actions ──
    openPackageModal(pkg) {
      if (pkg) {
        this.editingPackage = pkg
        this.packageForm = {
          title:             pkg.title            || '',
          description:       pkg.description      || '',
          price:             pkg.price            || '',
          duration_weeks:    pkg.duration_weeks   || '',
          sessions_count:    pkg.sessions_count   || '',
          sessions_per_week: pkg.sessions_per_week|| '',
          features_str:      Array.isArray(pkg.features) ? pkg.features.join(', ') : (pkg.features || ''),
          badge:             pkg.badge            || ''
        }
      } else {
        this.editingPackage = null
        this.packageForm = { title: '', description: '', price: '', duration_weeks: '', sessions_count: '', sessions_per_week: '', features_str: '', badge: '' }
      }
      this.showPackageModal = true
    },
    async submitPackage() {
      if (!this.packageForm.title.trim()) {
        alert('Package title is required')
        return
      }
      const data = {
        title:             this.packageForm.title,
        description:       this.packageForm.description,
        price:             parseFloat(this.packageForm.price) || 0,
        duration_weeks:    parseInt(this.packageForm.duration_weeks)    || null,
        sessions_count:    parseInt(this.packageForm.sessions_count)    || null,
        sessions_per_week: parseInt(this.packageForm.sessions_per_week) || null,
        features:          this.packageForm.features_str.split(',').map(s => s.trim()).filter(Boolean),
        badge:             this.packageForm.badge
      }
      let r
      if (this.editingPackage) {
        r = await api.updatePackage(this.editingPackage._id, data)
      } else {
        r = await api.createPackage(data)
      }
      if (r.success) {
        this.showPackageModal = false
        await this.loadData()
      } else {
        alert(r.error || 'Failed to save package')
      }
    },
    async togglePackage(id) {
      const r = await api.togglePackage(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async deletePackage(id) {
      if (!confirm('Delete this package? This cannot be undone.')) return
      const r = await api.deletePackage(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },

    // ── Query / Review ──
    async respondToQuery(queryId, response) {
      if (!response) { alert('Please enter a response'); return }
      const r = await api.respondToQuery(queryId, response)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async approveReview(id) {
      const r = await api.approveReview(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },
    async rejectReview(id) {
      const r = await api.rejectReview(id)
      if (r.success) { await this.loadData() } else { alert(r.error || 'Failed') }
    },

    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
  margin: 100px auto 60px;
  padding: 0 40px;
}

.loading-bar {
  text-align: center;
  padding: 12px;
  background: #fff8e1;
  color: #f57c00;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 13px;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
  color: var(--text-soft);
  font-size: 14px;
  background: white;
  border-radius: 8px;
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
  background: white;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
  transition: transform .3s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.08); }
.stat-icon  { font-size: 32px; }
.stat-value { font-size: 28px; font-weight: 600; color: var(--sage); font-family: 'Cormorant Garamond', serif; }
.stat-label { font-size: 12px; color: var(--text-soft); text-transform: uppercase; letter-spacing: 1px; }

.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid #e0e0d8;
  margin-bottom: 32px;
  flex-wrap: wrap;
}
.tabs button {
  padding: 12px 20px;
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-soft);
  cursor: pointer;
  transition: all .3s;
  position: relative;
  white-space: nowrap;
}
.tabs button.active { color: var(--sage); }
.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 2px;
  background: var(--sage);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.section-header h2 { font-size: 24px; font-family: 'Cormorant Garamond', serif; }

.filter-buttons { display: flex; gap: 8px; }
.filter-buttons button {
  padding: 6px 12px;
  background: #f5f5f0;
  border: 1px solid #e0e0d8;
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
  text-transform: uppercase;
  transition: all .3s;
}
.filter-buttons button.active { background: var(--sage); color: white; border-color: var(--sage); }

.trainers-table, .assignments-table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
th, td { padding: 16px; text-align: left; border-bottom: 1px solid #f0f0e8; }
th { background: #fafaf5; font-weight: 600; font-size: 13px; color: var(--text-mid); }

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  text-transform: uppercase;
}
.status-badge.active       { background: #e8f5e9; color: #2e7d32; }
.status-badge.pending      { background: #fff3e0; color: #f57c00; }
.status-badge.rejected     { background: #ffebee; color: #c62828; }
.status-badge.inactive-badge { background: #eeeeee; color: #666; }
.status-badge.small        { font-size: 9px; padding: 2px 6px; }

.actions { display: flex; gap: 8px; align-items: center; }

.btn-approve, .btn-reject, .btn-block {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
  transition: all .3s;
}
.btn-approve { background: var(--sage); color: white; }
.btn-approve:hover { background: var(--sage-dark); }
.btn-reject  { background: #f44336; color: white; }
.btn-reject:hover { background: #d32f2f; }
.btn-block   { background: #ff9800; color: white; }
.btn-block:hover { background: #f57c00; }
.small { padding: 4px 8px !important; font-size: 10px !important; }

.btn-primary {
  background: var(--sage);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s;
}
.btn-primary:hover { background: var(--sage-dark); }
.btn-primary.small { padding: 6px 12px; font-size: 12px; }

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
  text-decoration: underline;
}

/* Clients grid */
.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}
.client-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.client-avatar {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: white; flex-shrink: 0;
}
.client-info  { flex: 1; }
.client-info h4 { margin-bottom: 4px; }
.client-info p  { font-size: 12px; color: var(--text-soft); margin-bottom: 6px; }
.client-assignment { font-size: 12px; text-align: right; min-width: 80px; }
.client-assignment strong { display: block; margin-bottom: 4px; }
.client-actions-col { display: flex; flex-direction: column; gap: 6px; }

/* Sessions */
.sessions-list { display: flex; flex-direction: column; gap: 16px; }
.session-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.session-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.session-title  { font-weight: 600; font-size: 16px; }
.session-status { padding: 4px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; }
.session-status.scheduled { background: #fff3e0; color: #f57c00; }
.session-status.completed { background: #e8f5e9; color: #2e7d32; }
.session-status.cancelled { background: #ffebee; color: #c62828; }
.session-meta   { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-soft); margin-bottom: 12px; }
.session-actions { display: flex; gap: 8px; }

/* Packages grid */
.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}
.package-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
  border: 1px solid #f0f0e8;
  transition: transform .2s, box-shadow .2s;
}
.package-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.1); }
.package-card.inactive { opacity: 0.6; }
.package-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.package-title  { font-size: 18px; font-weight: 600; color: var(--text-dark); }
.package-price  { font-size: 22px; font-weight: 700; color: var(--sage); font-family: 'Cormorant Garamond', serif; }
.package-desc   { font-size: 13px; color: var(--text-mid); margin-bottom: 12px; line-height: 1.5; }
.package-details{ display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: var(--text-soft); margin-bottom: 8px; }
.package-interests { font-size: 12px; color: var(--sage); margin-bottom: 10px; }
.package-status { margin-bottom: 12px; }
.package-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.pkg-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

/* Queries / reviews */
.queries-list, .reviews-list { display: flex; flex-direction: column; gap: 20px; }
.query-card, .review-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.query-header, .review-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.query-sender { display: flex; align-items: center; gap: 8px; }
.query-role   { font-size: 11px; padding: 2px 6px; background: #f5f5f0; border-radius: 4px; color: var(--text-soft); }
.query-subject { font-weight: 600; margin-bottom: 8px; }
.query-message { color: var(--text-mid); margin-bottom: 16px; }
.query-date, .review-date { font-size: 11px; color: var(--text-soft); }
.query-response { background: #f8f9fa; padding: 12px; border-radius: 4px; margin-top: 12px; }
.query-actions textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e0d8;
  border-radius: 4px;
  margin-bottom: 8px;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}
.review-rating  { color: var(--gold); font-size: 18px; }
.review-client, .review-trainer { font-size: 12px; color: var(--text-soft); margin-bottom: 6px; }
.review-comment { font-style: italic; margin: 12px 0; }
.review-actions { display: flex; gap: 8px; }

/* Modal */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 32px;
  border-radius: 12px;
  min-width: 420px;
  max-width: 560px;
  max-height: 85vh;
  overflow-y: auto;
  width: 100%;
}
.modal-content h3 { margin-bottom: 24px; font-size: 20px; }
.modal-body { margin-bottom: 24px; }
.input-group { margin-bottom: 16px; }
.input-group label { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 500; color: var(--text-mid); }
.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0d8;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
}
.input-group input:focus, .input-group select:focus, .input-group textarea:focus {
  outline: none; border-color: var(--sage);
}
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

@media (max-width: 768px) {
  .admin-dashboard { padding: 80px 20px 40px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .clients-grid, .packages-grid { grid-template-columns: 1fr; }
  .modal-content { min-width: 300px; margin: 20px; }
  .pkg-grid { grid-template-columns: 1fr; }
}
</style>