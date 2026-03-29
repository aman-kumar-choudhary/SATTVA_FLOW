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
          <div class="stat-value">{{ stats.total_trainers }}</div>
          <div class="stat-label">Total Trainers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🧘</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.active_trainers }}</div>
          <div class="stat-label">Active Trainers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🙋</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_clients }}</div>
          <div class="stat-label">Total Clients</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.active_clients }}</div>
          <div class="stat-label">Active Clients</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_sessions }}</div>
          <div class="stat-label">Total Sessions</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pending_queries }}</div>
          <div class="stat-label">Pending Queries</div>
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
    
    <!-- Trainers Tab -->
    <div v-if="activeTab === 'trainers'" class="tab-content">
      <div class="section-header">
        <h2>Trainer Management</h2>
        <div class="filter-buttons">
          <button 
            v-for="status in ['all', 'pending', 'active', 'rejected']"
            :key="status"
            :class="{ active: trainerFilter === status }"
            @click="trainerFilter = status"
          >
            {{ status.toUpperCase() }}
          </button>
        </div>
      </div>
      
      <div class="trainers-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email/Phone</th>
              <th>Specialization</th>
              <th>Experience</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trainer in filteredTrainers" :key="trainer._id">
              <td>{{ trainer.name }}</td>
              <td>{{ trainer.email || trainer.phone }}</td>
              <td>{{ trainer.trainer_details?.specialization || '-' }}</td>
              <td>{{ trainer.trainer_details?.experience || 0 }} years</td>
              <td>
                <span :class="['status-badge', trainer.status]">
                  {{ trainer.status }}
                </span>
              </td>
              <td class="actions">
                <button 
                  v-if="trainer.status === 'pending'"
                  class="btn-approve"
                  @click="approveTrainer(trainer._id)"
                >
                  Approve
                </button>
                <button 
                  v-if="trainer.status === 'pending'"
                  class="btn-reject"
                  @click="rejectTrainer(trainer._id)"
                >
                  Reject
                </button>
                <button 
                  v-if="trainer.status === 'active'"
                  class="btn-block"
                  @click="blockTrainer(trainer._id)"
                >
                  Block
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Clients Tab -->
    <div v-if="activeTab === 'clients'" class="tab-content">
      <div class="section-header">
        <h2>Client Management</h2>
        <button class="btn-primary" @click="showAssignModal = true">
          + Assign Client to Trainer
        </button>
      </div>
      
      <div class="clients-grid">
        <div class="client-card" v-for="client in clients" :key="client._id">
          <div class="client-avatar">{{ client.name.charAt(0) }}</div>
          <div class="client-info">
            <h4>{{ client.name }}</h4>
            <p>{{ client.email || client.phone }}</p>
            <span class="status-badge small" :class="client.status">{{ client.status }}</span>
          </div>
          <div class="client-assignment">
            <strong>Trainer:</strong>
            <span v-if="getTrainerForClient(client._id)">
              {{ getTrainerForClient(client._id) }}
            </span>
            <button 
              v-else
              class="btn-link"
              @click="openAssignForClient(client)"
            >
              Assign
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Assignments Tab -->
    <div v-if="activeTab === 'assignments'" class="tab-content">
      <div class="section-header">
        <h2>Trainer-Client Assignments</h2>
      </div>
      
      <div class="assignments-table">
        <table>
          <thead>
            <tr>
              <th>Trainer</th>
              <th>Client</th>
              <th>Assigned Date</th>
              <th>Sessions Completed</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="assignment in assignments" :key="assignment._id">
              <td>{{ assignment.trainer?.name || 'Unknown' }}</td>
              <td>{{ assignment.client?.name || 'Unknown' }}</td>
              <td>{{ formatDate(assignment.created_at) }}</td>
              <td>{{ assignment.sessions_completed || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Queries Tab -->
    <div v-if="activeTab === 'queries'" class="tab-content">
      <div class="section-header">
        <h2>Client & Trainer Queries</h2>
      </div>
      
      <div class="queries-list">
        <div class="query-card" v-for="query in queries" :key="query._id">
          <div class="query-header">
            <div class="query-sender">
              <strong>{{ query.sender?.name }}</strong>
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
            <textarea 
              v-model="query.responseText" 
              placeholder="Type your response..."
              rows="2"
            ></textarea>
            <button @click="respondToQuery(query._id, query.responseText)" class="btn-primary small">
              Send Response
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Reviews Tab -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="section-header">
        <h2>Review Moderation</h2>
      </div>
      
      <div class="reviews-list">
        <div class="review-card" v-for="review in pendingReviews" :key="review._id">
          <div class="review-header">
            <div class="review-rating">★★★★★</div>
            <div class="review-date">{{ formatDate(review.created_at) }}</div>
          </div>
          <div class="review-client">Client: {{ review.client?.name }}</div>
          <div class="review-trainer">Trainer: {{ review.trainer?.name }}</div>
          <div class="review-comment">{{ review.comment }}</div>
          <div class="review-actions">
            <button @click="approveReview(review._id)" class="btn-approve">Approve</button>
            <button @click="rejectReview(review._id)" class="btn-reject">Reject</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Assign Modal -->
    <div v-if="showAssignModal" class="modal-overlay" @click="showAssignModal = false">
      <div class="modal-content" @click.stop>
        <h3>Assign Client to Trainer</h3>
        <div class="modal-body">
          <div class="input-group">
            <label>Select Trainer</label>
            <select v-model="assignData.trainer_id">
              <option v-for="trainer in activeTrainers" :key="trainer._id" :value="trainer._id">
                {{ trainer.name }} - {{ trainer.trainer_details?.specialization }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Select Client</label>
            <select v-model="assignData.client_id">
              <option v-for="client in unassignedClients" :key="client._id" :value="client._id">
                {{ client.name }} - {{ client.email || client.phone }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="assignClient" class="btn-primary">Assign</button>
          <button @click="showAssignModal = false" class="btn-secondary">Cancel</button>
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
      activeTab: 'trainers',
      tabs: [
        { id: 'trainers', name: 'Trainers' },
        { id: 'clients', name: 'Clients' },
        { id: 'assignments', name: 'Assignments' },
        { id: 'queries', name: 'Queries' },
        { id: 'reviews', name: 'Reviews' }
      ],
      stats: {
        total_trainers: 0,
        active_trainers: 0,
        total_clients: 0,
        active_clients: 0,
        total_sessions: 0,
        pending_queries: 0,
        pending_reviews: 0
      },
      trainers: [],
      trainerFilter: 'all',
      clients: [],
      assignments: [],
      queries: [],
      pendingReviews: [],
      showAssignModal: false,
      assignData: {
        trainer_id: '',
        client_id: ''
      }
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
    unassignedClients() {
      const assignedClientIds = this.assignments.map(a => a.client_id)
      return this.clients.filter(c => !assignedClientIds.includes(c._id) && c.status === 'active')
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      const statsResult = await api.getStats()
      if (statsResult.success) this.stats = statsResult
      
      const trainersResult = await api.getTrainers()
      if (trainersResult.success) this.trainers = trainersResult
      
      const clientsResult = await api.getClients()
      if (clientsResult.success) this.clients = clientsResult
      
      const assignmentsResult = await api.getAssignments()
      if (assignmentsResult.success) this.assignments = assignmentsResult
      
      const queriesResult = await api.getQueries()
      if (queriesResult.success) this.queries = queriesResult
      
      const reviewsResult = await api.getReviews('pending')
      if (reviewsResult.success) this.pendingReviews = reviewsResult
    },
    
    async approveTrainer(trainerId) {
      const result = await api.approveTrainer(trainerId)
      if (result.success) {
        await this.loadData()
      } else {
        alert('Failed to approve trainer')
      }
    },
    
    async rejectTrainer(trainerId) {
      const reason = prompt('Enter rejection reason:')
      if (reason) {
        const result = await api.rejectTrainer(trainerId, reason)
        if (result.success) {
          await this.loadData()
        } else {
          alert('Failed to reject trainer')
        }
      }
    },
    
    async blockTrainer(trainerId) {
      if (confirm('Are you sure you want to block this trainer?')) {
        // Implement block functionality
        alert('Feature coming soon')
      }
    },
    
    getTrainerForClient(clientId) {
      const assignment = this.assignments.find(a => a.client_id === clientId)
      if (assignment && assignment.trainer) {
        return assignment.trainer.name
      }
      return null
    },
    
    openAssignForClient(client) {
      this.assignData.client_id = client._id
      this.showAssignModal = true
    },
    
    async assignClient() {
      if (!this.assignData.trainer_id || !this.assignData.client_id) {
        alert('Please select both trainer and client')
        return
      }
      
      const result = await api.assignClient(this.assignData.trainer_id, this.assignData.client_id)
      if (result.success) {
        await this.loadData()
        this.showAssignModal = false
        this.assignData = { trainer_id: '', client_id: '' }
      } else {
        alert(result.error || 'Failed to assign client')
      }
    },
    
    async respondToQuery(queryId, response) {
      if (!response) {
        alert('Please enter a response')
        return
      }
      
      const result = await api.respondToQuery(queryId, response)
      if (result.success) {
        await this.loadData()
      } else {
        alert('Failed to send response')
      }
    },
    
    async approveReview(reviewId) {
      const result = await api.approveReview(reviewId)
      if (result.success) {
        await this.loadData()
      } else {
        alert('Failed to approve review')
      }
    },
    
    async rejectReview(reviewId) {
      const result = await api.rejectReview(reviewId)
      if (result.success) {
        await this.loadData()
      } else {
        alert('Failed to reject review')
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString()
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

.filter-buttons {
  display: flex;
  gap: 8px;
}

.filter-buttons button {
  padding: 6px 12px;
  background: #f5f5f0;
  border: 1px solid #e0e0d8;
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
  text-transform: uppercase;
  transition: all 0.3s;
}

.filter-buttons button.active {
  background: var(--sage);
  color: white;
  border-color: var(--sage);
}

.trainers-table,
.assignments-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0e8;
}

th {
  background: #fafaf5;
  font-weight: 600;
  font-size: 13px;
  color: var(--text-mid);
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  text-transform: uppercase;
}

.status-badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.status-badge.rejected {
  background: #ffebee;
  color: #c62828;
}

.status-badge.small {
  font-size: 9px;
  padding: 2px 6px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-approve, .btn-reject, .btn-block {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.3s;
}

.btn-approve {
  background: var(--sage);
  color: white;
}

.btn-approve:hover {
  background: var(--sage-dark);
}

.btn-reject {
  background: #f44336;
  color: white;
}

.btn-reject:hover {
  background: #d32f2f;
}

.btn-block {
  background: #ff9800;
  color: white;
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
  margin-bottom: 8px;
}

.client-assignment {
  font-size: 12px;
  text-align: right;
}

.client-assignment strong {
  display: block;
  margin-bottom: 4px;
}

.queries-list,
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.query-card,
.review-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.query-header,
.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.query-sender {
  display: flex;
  align-items: center;
  gap: 8px;
}

.query-role {
  font-size: 11px;
  padding: 2px 6px;
  background: #f5f5f0;
  border-radius: 4px;
  color: var(--text-soft);
}

.query-subject {
  font-weight: 600;
  margin-bottom: 8px;
}

.query-message {
  color: var(--text-mid);
  margin-bottom: 16px;
}

.query-response {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 4px;
  margin-top: 12px;
}

.query-actions textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e0d8;
  border-radius: 4px;
  margin-bottom: 8px;
  font-family: inherit;
}

.review-rating {
  color: var(--gold);
}

.review-client,
.review-trainer {
  font-size: 12px;
  color: var(--text-soft);
  margin-bottom: 8px;
}

.review-comment {
  font-style: italic;
  margin: 12px 0;
}

.review-actions {
  display: flex;
  gap: 8px;
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
  min-width: 400px;
  max-width: 500px;
}

.modal-content h3 {
  margin-bottom: 24px;
}

.modal-body {
  margin-bottom: 24px;
}

.modal-body select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0d8;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .admin-dashboard {
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