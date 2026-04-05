<template>
  <div class="dashboard-root">

    <!-- Mobile overlay -->
    <div v-if="mobileSidebarOpen" class="sidebar-overlay" @click="mobileSidebarOpen = false"></div>

    <!-- ═══ SIDEBAR ═══ -->
    <aside :class="['sidebar', sidebarCollapsed ? 'sidebar--collapsed' : '', mobileSidebarOpen ? 'sidebar--mobile-open' : '']">
      <!-- Brand -->
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

      <!-- Nav -->
      <nav class="sidebar-nav">
        <button
          v-for="item in navItems"
          :key="item.id"
          @click="navigate(item.id)"
          :title="item.label"
          :class="['nav-item', activeSection === item.id ? 'nav-item--active' : '']"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          <span
            v-if="item.badge && getBadge(item.badge) > 0 && !sidebarCollapsed"
            class="nav-badge"
          >{{ getBadge(item.badge) }}</span>
          <span
            v-if="item.badge && getBadge(item.badge) > 0 && sidebarCollapsed"
            class="nav-badge nav-badge--dot"
          ></span>
        </button>
      </nav>

      <!-- Toggle -->
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
            <h1 class="page-title">{{ currentPageTitle }}</h1>
            <div v-if="breadcrumb.length" class="breadcrumb">
              <span v-for="(crumb, i) in breadcrumb" :key="i" class="breadcrumb-item">
                <button v-if="crumb.action" @click="crumb.action" class="breadcrumb-link">{{ crumb.label }}</button>
                <span v-else class="breadcrumb-text">{{ crumb.label }}</span>
                <span v-if="i < breadcrumb.length - 1" class="breadcrumb-sep">›</span>
              </span>
            </div>
          </div>
          <div class="topbar-right">
            <div class="search-wrap">
              <span class="search-icon">🔍</span>
              <input
                v-model="globalSearch"
                placeholder="Search users, sessions… (Enter to jump)"
                class="search-input"
                @keyup.enter="handleSearch"
                @input="handleSearch"
              />
              <button v-if="globalSearch" class="search-clear" @click="globalSearch = ''">×</button>
            </div>
            <div class="user-chip">
              <div class="user-avatar">A</div>
              <span class="user-name">Admin</span>
            </div>
          </div>
        </div>
        <div v-if="loading" class="loading-bar-wrap">
          <div class="loading-bar"></div>
        </div>
      </header>

      <!-- ══════════════ OVERVIEW ══════════════ -->
      <section v-if="activeSection === 'overview'" class="page-section">

        <!-- Stat Cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f0f9f4">
              <span>👤</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.clients?.total || 0 }}</div>
              <div class="stat-label">Total Clients</div>
            </div>
            <span v-if="stats.clients?.pending" class="stat-badge">{{ stats.clients.pending }} pending</span>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fdf8f0">
              <span>🧘</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.trainers?.total || 0 }}</div>
              <div class="stat-label">Total Trainers</div>
            </div>
            <span v-if="stats.trainers?.pending" class="stat-badge">{{ stats.trainers.pending }} pending</span>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#eff6ff">
              <span>📅</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.sessions?.total || 0 }}</div>
              <div class="stat-label">All Sessions</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f0fdf4">
              <span>✅</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.sessions?.completed || 0 }}</div>
              <div class="stat-label">Completed</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f5f3ff">
              <span>🔗</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.assignments || 0 }}</div>
              <div class="stat-label">Active Assignments</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fef2f2">
              <span>💬</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.pending_queries || 0 }}</div>
              <div class="stat-label">Open Queries</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#fdf4ff">
              <span>⭐</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.pending_reviews || 0 }}</div>
              <div class="stat-label">Reviews Pending</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrap" style="background:#f0f9ff">
              <span>📦</span>
            </div>
            <div class="stat-body">
              <div class="stat-number">{{ stats.packages || 0 }}</div>
              <div class="stat-label">Active Packages</div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <h3 class="card-title">Quick Actions</h3>
          <div class="quick-actions-grid">
            <button
              v-for="qa in quickActions" :key="qa.id"
              @click="navigate(qa.id)"
              class="quick-action-btn"
            >
              <span class="qa-icon">{{ qa.icon }}</span>
              <div class="qa-body">
                <div class="qa-label">{{ qa.label }}</div>
                <div v-if="qa.badge && getBadge(qa.badge) > 0" class="qa-sub">{{ getBadge(qa.badge) }} pending</div>
              </div>
            </button>
          </div>
        </div>
      </section>

      <!-- ══════════════ CLIENTS ══════════════ -->
      <section v-if="activeSection === 'clients'" class="page-section">

        <!-- Client Detail -->
        <div v-if="selectedClient">
          <div class="card mb-4">
            <div class="detail-header">
              <div class="detail-avatar" style="background:#4a7c59">
                {{ selectedClient.name?.charAt(0) || '?' }}
              </div>
              <div class="detail-info">
                <h2 class="detail-name">{{ selectedClient.name }}</h2>
                <div class="detail-tags">
                  <span class="tag">{{ selectedClient.email || '—' }}</span>
                  <span class="tag">{{ selectedClient.phone || '—' }}</span>
                  <span :class="statusPill(selectedClient.status)">{{ selectedClient.status }}</span>
                </div>
              </div>
              <div class="detail-actions">
                <button v-if="selectedClient.status === 'pending'" class="btn-approve" @click="activateClient(selectedClient._id)" :disabled="actionLoading">✓ Activate</button>
                <button v-if="selectedClient.status === 'active'" class="btn-block" @click="blockClient(selectedClient._id)" :disabled="actionLoading">⊘ Block</button>
                <button v-if="selectedClient.status === 'blocked'" class="btn-approve" @click="unblockClient(selectedClient._id)" :disabled="actionLoading">↺ Unblock</button>
                <button class="btn-danger" @click="confirmDelete('client', selectedClient._id, selectedClient.name)" :disabled="actionLoading">🗑 Remove</button>
              </div>
            </div>
          </div>

          <!-- Inner Tabs -->
          <div class="tab-strip mb-4">
            <button
              v-for="t in clientDetailTabs" :key="t.id"
              @click="clientDetailTab = t.id"
              :class="['tab-btn', clientDetailTab === t.id ? 'tab-btn--active' : '']"
            >{{ t.label }}</button>
          </div>

          <!-- Progress Tab -->
          <div v-if="clientDetailTab === 'progress'">
            <div v-if="selectedClientDetail.subscription" class="card mb-4">
              <div class="flex-between mb-4">
                <h3 class="card-title">📦 {{ selectedClientDetail.subscription.package_title }}</h3>
                <span class="text-xs text-muted">Enrolled: {{ formatDate(selectedClientDetail.subscription.enrolled_at) }}</span>
              </div>

              <!-- Progress Stats Grid -->
              <div class="sub-stats-grid">
                <div class="sub-stat sub-stat--green">
                  <div class="sub-stat-val">{{ selectedClientDetail.subscription.total_sessions }}</div>
                  <div class="sub-stat-label">Total Sessions</div>
                </div>
                <div class="sub-stat sub-stat--green">
                  <div class="sub-stat-val">{{ selectedClientDetail.subscription.completed_sessions }}</div>
                  <div class="sub-stat-label">Completed</div>
                </div>
                <div class="sub-stat sub-stat--orange">
                  <div class="sub-stat-val">{{ selectedClientDetail.subscription.pending_sessions }}</div>
                  <div class="sub-stat-label">Remaining</div>
                </div>
                <div class="sub-stat">
                  <div class="sub-stat-val">{{ selectedClientDetail.subscription.sessions_per_week || '—' }}</div>
                  <div class="sub-stat-label">Sessions/Week</div>
                </div>
                <div class="sub-stat">
                  <div class="sub-stat-val">{{ selectedClientDetail.subscription.total_weeks }}</div>
                  <div class="sub-stat-label">Total Weeks</div>
                </div>
                <div :class="['sub-stat', selectedClientDetail.progress?.weeks_remaining === 0 ? 'sub-stat--orange' : '']">
                  <div class="sub-stat-val">{{ selectedClientDetail.progress?.weeks_remaining ?? '—' }}</div>
                  <div class="sub-stat-label">Weeks Remaining</div>
                </div>
              </div>

              <!-- Deadline & On-Track Row -->
              <div v-if="selectedClientDetail.progress" class="deadline-row mt-4">
                <div class="deadline-item">
                  <span class="deadline-label">📅 Deadline</span>
                  <span class="deadline-value">{{ formatDate(selectedClientDetail.progress.deadline) }}</span>
                </div>
                <div class="deadline-item">
                  <span class="deadline-label">⏱ Weeks Elapsed</span>
                  <span class="deadline-value">{{ selectedClientDetail.progress.weeks_elapsed }}</span>
                </div>
                <div class="deadline-item">
                  <span :class="selectedClientDetail.progress.is_on_track ? 'badge-yes' : 'badge-warn'">
                    {{ selectedClientDetail.progress.is_on_track ? '✓ On Track' : '⚠ Behind Schedule' }}
                  </span>
                  <span class="text-xs text-muted ml-2">
                    (expected {{ selectedClientDetail.progress.expected_done }} done by now)
                  </span>
                </div>
              </div>

              <!-- Completion Bar -->
              <div class="progress-wrap mt-4">
                <div class="progress-header">
                  <span>Class Completion Progress</span>
                  <span class="progress-pct">{{ completionPct(selectedClientDetail.subscription) }}%</span>
                </div>
                <div class="progress-bar-bg">
                  <div class="progress-bar-fill" :style="{ width: completionPct(selectedClientDetail.subscription) + '%' }"></div>
                </div>
                <div class="progress-note">
                  {{ selectedClientDetail.subscription.completed_sessions }} of
                  {{ selectedClientDetail.subscription.total_sessions }} classes completed ·
                  {{ selectedClientDetail.subscription.pending_sessions }} remaining
                </div>
              </div>
            </div>
            <div v-else class="info-banner mb-4">
              <span>ℹ</span>
              <span>No active package. Client must select one from the packages page.</span>
            </div>
            <div v-if="!selectedClientDetail.subscription" class="card">
              <h4 class="font-medium mb-3">Assign a Package (Admin Override)</h4>
              <div class="row-gap">
                <select v-model="packageToAssign" class="form-input flex-1">
                  <option value="">— Select Package —</option>
                  <option v-for="pkg in packages" :key="pkg._id" :value="pkg._id">
                    {{ pkg.title }} ({{ pkg.duration_weeks }}w · {{ pkg.sessions_per_week }}/wk · {{ pkg.sessions_count }} sessions)
                  </option>
                </select>
                <button class="btn-approve" @click="assignPackageToClient" :disabled="!packageToAssign || actionLoading">Assign</button>
              </div>
            </div>
          </div>

          <!-- Sessions Tab -->
          <div v-if="clientDetailTab === 'sessions'" class="card">
            <div class="card-header">
              <h3 class="card-title">Sessions ({{ selectedClientDetail.sessions?.length || 0 }})</h3>
              <button class="btn-primary" @click="openScheduleSession(selectedClient)">+ Schedule Session</button>
            </div>
            <div v-if="!selectedClientDetail.sessions?.length" class="empty-state">No sessions yet.</div>
            <div v-else class="table-wrap">
              <table class="data-table">
                <thead><tr><th>#</th><th>Title</th><th>Scheduled</th><th>Duration</th><th>Status</th><th>Attended</th><th>Actions</th></tr></thead>
                <tbody>
                  <tr v-for="(s, idx) in selectedClientDetail.sessions" :key="s._id">
                    <td class="text-muted">{{ idx + 1 }}</td>
                    <td class="font-medium">{{ s.title }}</td>
                    <td>{{ formatDateTime(s.scheduled_at) }}</td>
                    <td>{{ s.duration_minutes || 60 }}m</td>
                    <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                    <td><span v-if="s.attendance_marked" class="badge-yes">✓ Yes</span><span v-else class="badge-no">—</span></td>
                    <td>
                      <div class="action-row">
                        <button class="micro-edit" @click="editSession(s)">Edit</button>
                        <button class="micro-del" @click="confirmDeleteSession(s._id)">Delete</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Info Tab -->
          <div v-if="clientDetailTab === 'info'" class="card">
            <div class="info-grid">
              <div v-for="field in clientInfoFields(selectedClient, selectedClientDetail)" :key="field.label">
                <label class="field-label">{{ field.label }}</label>
                <p class="field-value" v-html="field.value"></p>
              </div>
            </div>
            <div v-if="activeTrainers.length" class="divider-top mt-4 pt-4">
              <h4 class="font-medium mb-3">Assign / Reassign Trainer</h4>
              <div class="row-gap">
                <select v-model="trainerToAssign" class="form-input flex-1">
                  <option value="">— Select Trainer —</option>
                  <option v-for="t in activeTrainers" :key="t._id" :value="t._id">{{ t.name }} · {{ t.specialization }}</option>
                </select>
                <button class="btn-approve" :disabled="!trainerToAssign || actionLoading" @click="assignTrainer">
                  {{ selectedClientDetail.trainer ? 'Reassign' : 'Assign' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Queries Tab -->
          <div v-if="clientDetailTab === 'queries'">
            <div v-if="!selectedClientDetail.queries?.length" class="empty-state">No queries from this client.</div>
            <div v-for="q in selectedClientDetail.queries" :key="q._id" class="card mb-3">
              <div class="flex-between mb-2">
                <strong>{{ q.subject }}</strong>
                <span :class="statusPill(q.status)">{{ q.status }}</span>
              </div>
              <p class="text-sm text-muted mb-2">{{ q.message }}</p>
              <div v-if="q.response" class="query-response">
                <span class="query-response-label">Response: </span>{{ q.response }}
              </div>
              <div v-if="q.status === 'pending'" class="mt-2">
                <textarea v-model="q._replyText" rows="3" class="form-input w-full resize-none mb-2" placeholder="Type your response…"></textarea>
                <button class="btn-primary" @click="respondQuery(q)" :disabled="!q._replyText || actionLoading">📧 Send Reply</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Client List -->
        <div v-else>
          <div class="list-toolbar">
            <div class="filter-chips">
              <button v-for="s in ['all','active','pending','blocked']" :key="s"
                :class="['filter-chip', clientFilter === s ? 'filter-chip--active' : '']"
                @click="clientFilter = s; fetchClients()">{{ s }}</button>
            </div>
            <div class="search-field-wrap">
              <span class="search-field-icon">🔍</span>
              <input v-model="clientSearch" placeholder="Search clients…" class="form-input search-field" />
            </div>
          </div>
          <div class="card">
            <div v-if="filteredClients.length === 0" class="empty-state">No clients found.</div>
            <div v-else class="table-wrap">
              <table class="data-table">
                <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                  <tr v-for="c in filteredClients" :key="c._id" class="row-clickable" @click="openClientDetail(c)">
                    <td>
                      <div class="user-row">
                        <div class="user-initial" style="background:rgba(74,124,89,0.15);color:#4a7c59">{{ c.name?.charAt(0) }}</div>
                        <span class="font-medium">{{ c.name }}</span>
                      </div>
                    </td>
                    <td class="text-muted">{{ c.email }}</td>
                    <td class="text-muted">{{ c.phone || '—' }}</td>
                    <td><span :class="statusPill(c.status)">{{ c.status }}</span></td>
                    <td @click.stop>
                      <div class="action-row">
                        <button v-if="c.status === 'pending'" class="micro-approve" @click="activateClient(c._id)">Activate</button>
                        <button v-if="c.status === 'active'" class="micro-block" @click="blockClient(c._id)">Block</button>
                        <button v-if="c.status === 'blocked'" class="micro-approve" @click="unblockClient(c._id)">Unblock</button>
                        <button class="micro-del" @click="confirmDelete('client', c._id, c.name)">Delete</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-if="clientPages > 1" class="pagination">
            <button :disabled="clientPage === 1" @click="clientPage--; fetchClients()" class="pagination-btn">‹ Prev</button>
            <span class="pagination-info">{{ clientPage }} / {{ clientPages }}</span>
            <button :disabled="clientPage === clientPages" @click="clientPage++; fetchClients()" class="pagination-btn">Next ›</button>
          </div>
        </div>
      </section>

      <!-- ══════════════ TRAINERS ══════════════ -->
      <section v-if="activeSection === 'trainers'" class="page-section">

        <div v-if="selectedTrainer">
          <div class="card mb-4">
            <div class="detail-header">
              <div class="detail-avatar" style="background:#7c6a4a">
                {{ selectedTrainer.name?.charAt(0) || '?' }}
              </div>
              <div class="detail-info">
                <h2 class="detail-name">{{ selectedTrainer.name }}</h2>
                <div class="detail-tags">
                  <span class="tag">{{ selectedTrainer.email }}</span>
                  <span class="tag">{{ selectedTrainer.specialization || '—' }}</span>
                  <span :class="statusPill(selectedTrainer.status)">{{ selectedTrainer.status }}</span>
                </div>
              </div>
              <div class="detail-actions">
                <button v-if="selectedTrainer.status === 'pending'" class="btn-approve" @click="approveTrainer(selectedTrainer._id)" :disabled="actionLoading">✓ Approve</button>
                <button v-if="selectedTrainer.status === 'pending'" class="btn-danger" @click="rejectTrainer(selectedTrainer._id)" :disabled="actionLoading">✗ Reject</button>
                <button v-if="selectedTrainer.status === 'active'" class="btn-block" @click="blockTrainer(selectedTrainer._id)" :disabled="actionLoading">⊘ Block</button>
                <button v-if="selectedTrainer.status === 'blocked'" class="btn-approve" @click="unblockTrainer(selectedTrainer._id)" :disabled="actionLoading">↺ Unblock</button>
                <button class="btn-danger" @click="confirmDelete('trainer', selectedTrainer._id, selectedTrainer.name)" :disabled="actionLoading">🗑 Remove</button>
              </div>
            </div>
          </div>

          <div class="tab-strip mb-4">
            <button v-for="t in trainerDetailTabs" :key="t.id" @click="trainerDetailTab = t.id"
              :class="['tab-btn', trainerDetailTab === t.id ? 'tab-btn--active' : '']">{{ t.label }}</button>
          </div>

          <div v-if="trainerDetailTab === 'info'" class="card">
            <div class="info-grid">
              <div><label class="field-label">Full Name</label><p class="field-value">{{ selectedTrainer.name || '—' }}</p></div>
              <div><label class="field-label">Email</label><p class="field-value">{{ selectedTrainer.email || '—' }}</p></div>
              <div><label class="field-label">Specialization</label><p class="field-value">{{ selectedTrainer.specialization || '—' }}</p></div>
              <div><label class="field-label">Experience</label><p class="field-value">{{ selectedTrainer.experience_years ? selectedTrainer.experience_years + ' yrs' : '—' }}</p></div>
              <div><label class="field-label">Status</label><p class="field-value"><span :class="statusPill(selectedTrainer.status)">{{ selectedTrainer.status }}</span></p></div>
              <div><label class="field-label">Registered</label><p class="field-value">{{ formatDate(selectedTrainer.created_at) }}</p></div>
            </div>
          </div>

          <div v-if="trainerDetailTab === 'clients'" class="card">
            <h3 class="card-title mb-3">Assigned Clients ({{ selectedTrainerDetail.clients?.length || 0 }})</h3>
            <div v-if="!selectedTrainerDetail.clients?.length" class="empty-state">No assigned clients.</div>
            <div v-else class="table-wrap">
              <table class="data-table">
                <thead><tr><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                  <tr v-for="c in selectedTrainerDetail.clients" :key="c._id">
                    <td class="font-medium">{{ c.name }}</td>
                    <td class="text-muted">{{ c.email }}</td>
                    <td><span :class="statusPill(c.status)">{{ c.status }}</span></td>
                    <td><button class="micro-edit" @click="openClientFromTrainer(c)">View</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="trainerDetailTab === 'sessions'" class="card">
            <h3 class="card-title mb-3">Sessions ({{ selectedTrainerDetail.sessions?.length || 0 }})</h3>
            <div v-if="!selectedTrainerDetail.sessions?.length" class="empty-state">No sessions yet.</div>
            <div v-else class="table-wrap">
              <table class="data-table">
                <thead><tr><th>Title</th><th>Client</th><th>Date</th><th>Status</th></tr></thead>
                <tbody>
                  <tr v-for="s in selectedTrainerDetail.sessions" :key="s._id">
                    <td class="font-medium">{{ s.title }}</td>
                    <td>{{ s.client?.name || '—' }}</td>
                    <td>{{ formatDateTime(s.scheduled_at) }}</td>
                    <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Trainer List -->
        <div v-else>
          <div class="list-toolbar">
            <div class="filter-chips">
              <button v-for="s in ['all','active','pending','blocked']" :key="s"
                :class="['filter-chip', trainerFilter === s ? 'filter-chip--active' : '']"
                @click="trainerFilter = s; fetchTrainers()">{{ s }}</button>
            </div>
            <div class="search-field-wrap">
              <span class="search-field-icon">🔍</span>
              <input v-model="trainerSearch" placeholder="Search trainers…" class="form-input search-field" />
            </div>
          </div>
          <div class="card">
            <div v-if="filteredTrainers.length === 0" class="empty-state">No trainers found.</div>
            <div v-else class="table-wrap">
              <table class="data-table">
                <thead><tr><th>Name</th><th>Email</th><th>Specialization</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                  <tr v-for="t in filteredTrainers" :key="t._id" class="row-clickable" @click="openTrainerDetail(t)">
                    <td>
                      <div class="user-row">
                        <div class="user-initial" style="background:rgba(124,106,74,0.15);color:#7c6a4a">{{ t.name?.charAt(0) }}</div>
                        <span class="font-medium">{{ t.name }}</span>
                      </div>
                    </td>
                    <td class="text-muted">{{ t.email }}</td>
                    <td class="text-muted">{{ t.specialization || '—' }}</td>
                    <td><span :class="statusPill(t.status)">{{ t.status }}</span></td>
                    <td @click.stop>
                      <div class="action-row">
                        <button v-if="t.status === 'pending'" class="micro-approve" @click="approveTrainer(t._id)">Approve</button>
                        <button v-if="t.status === 'active'" class="micro-block" @click="blockTrainer(t._id)">Block</button>
                        <button v-if="t.status === 'blocked'" class="micro-approve" @click="unblockTrainer(t._id)">Unblock</button>
                        <button class="micro-del" @click="confirmDelete('trainer', t._id, t.name)">Delete</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-if="trainerPages > 1" class="pagination">
            <button :disabled="trainerPage === 1" @click="trainerPage--; fetchTrainers()" class="pagination-btn">‹ Prev</button>
            <span class="pagination-info">{{ trainerPage }} / {{ trainerPages }}</span>
            <button :disabled="trainerPage === trainerPages" @click="trainerPage++; fetchTrainers()" class="pagination-btn">Next ›</button>
          </div>
        </div>
      </section>

      <!-- ══════════════ SESSIONS ══════════════ -->
      <section v-if="activeSection === 'sessions'" class="page-section">
        <div class="list-toolbar">
          <div class="filter-chips">
            <button v-for="s in ['all','scheduled','completed','cancelled']" :key="s"
              :class="['filter-chip', sessionFilter === s ? 'filter-chip--active' : '']"
              @click="sessionFilter = s; fetchSessions()">{{ s }}</button>
          </div>
          <button class="btn-primary" @click="openScheduleSession(null)">+ New Session</button>
        </div>
        <div class="card">
          <div v-if="sessions.length === 0 && !loading" class="empty-state">No sessions found.</div>
          <div v-else class="table-wrap">
            <table class="data-table">
              <thead><tr><th>#</th><th>Title</th><th>Client</th><th>Trainer</th><th>Date & Time</th><th>Dur.</th><th>Status</th><th>Attended</th><th>Actions</th></tr></thead>
              <tbody>
                <tr v-for="(s, i) in filteredSessions" :key="s._id">
                  <td class="text-muted">{{ (sessionPage - 1) * 20 + i + 1 }}</td>
                  <td class="font-medium">{{ s.title }}</td>
                  <td>{{ s.client?.name || '—' }}</td>
                  <td>{{ s.trainer?.name || '—' }}</td>
                  <td>{{ formatDateTime(s.scheduled_at) }}</td>
                  <td>{{ s.duration_minutes || 60 }}m</td>
                  <td><span :class="statusPill(s.status)">{{ s.status }}</span></td>
                  <td><span v-if="s.attendance_marked" class="badge-yes">✓</span><span v-else class="badge-no">—</span></td>
                  <td>
                    <div class="action-row">
                      <button class="micro-edit" @click="editSession(s)">Edit</button>
                      <button class="micro-del" @click="confirmDeleteSession(s._id)">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="sessionPages > 1" class="pagination">
          <button :disabled="sessionPage === 1" @click="sessionPage--; fetchSessions()" class="pagination-btn">‹ Prev</button>
          <span class="pagination-info">{{ sessionPage }} / {{ sessionPages }}</span>
          <button :disabled="sessionPage === sessionPages" @click="sessionPage++; fetchSessions()" class="pagination-btn">Next ›</button>
        </div>
      </section>

      <!-- ══════════════ PACKAGES ══════════════ -->
      <section v-if="activeSection === 'packages'" class="page-section">
        <div class="list-toolbar">
          <h2 class="section-heading">Package Management</h2>
          <button class="btn-primary" @click="openPackageModal(null)">+ New Package</button>
        </div>
        <div class="packages-grid">
          <div v-for="pkg in packages" :key="pkg._id"
            :class="['package-card', !pkg.is_active ? 'package-card--inactive' : '']">
            <div class="package-card-header">
              <h3 class="package-title">{{ pkg.title }}</h3>
              <span class="package-price">₹{{ pkg.price }}</span>
            </div>
            <p class="package-desc">{{ pkg.description }}</p>
            <div class="package-meta">
              <span>📅 {{ pkg.duration_weeks }} weeks</span>
              <span>🔁 {{ pkg.sessions_count }} sessions total</span>
              <span>📆 {{ pkg.sessions_per_week || Math.round(pkg.sessions_count / pkg.duration_weeks) }}/week</span>
            </div>
            <div v-if="pkg.enrolled_count !== undefined" class="package-enrolled">
              <span class="tag">{{ pkg.enrolled_count || 0 }} enrolled</span>
            </div>
            <div class="package-actions">
              <button class="micro-edit" @click="openPackageModal(pkg)">Edit</button>
              <button :class="pkg.is_active ? 'micro-block' : 'micro-approve'" @click="togglePackage(pkg._id)">{{ pkg.is_active ? 'Deactivate' : 'Activate' }}</button>
              <button class="micro-del" @click="confirmDeletePackage(pkg._id)">Delete</button>
            </div>
          </div>
        </div>

        <div v-if="subscriptions.length" class="card mt-6">
          <div class="card-header"><h3 class="card-title">All Package Subscriptions</h3></div>
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Client</th><th>Package</th><th>Total</th><th>Completed</th><th>Pending</th><th>Progress</th><th>Enrolled</th></tr></thead>
              <tbody>
                <tr v-for="sub in subscriptions" :key="sub._id">
                  <td class="font-medium">{{ sub.client_name }}</td>
                  <td>{{ sub.package_title }}</td>
                  <td>{{ sub.total_sessions }}</td>
                  <td><span class="badge-yes">{{ sub.completed_sessions }}</span></td>
                  <td><span class="badge-no">{{ sub.pending_sessions }}</span></td>
                  <td>
                    <div class="progress-mini-wrap">
                      <div class="progress-mini-bg"><div class="progress-mini-fill" :style="{ width: completionPct(sub) + '%' }"></div></div>
                      <span class="text-xs text-muted">{{ completionPct(sub) }}%</span>
                    </div>
                  </td>
                  <td>{{ formatDate(sub.enrolled_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ══════════════ QUERIES ══════════════ -->
      <section v-if="activeSection === 'queries'" class="page-section">
        <div class="filter-chips mb-5">
          <button v-for="s in ['all','pending','resolved']" :key="s"
            :class="['filter-chip', queryFilter === s ? 'filter-chip--active' : '']"
            @click="queryFilter = s; fetchQueries()">{{ s }}</button>
        </div>
        <div v-if="queries.length === 0 && !loading" class="empty-state">No queries.</div>
        <div v-for="q in filteredQueries" :key="q._id" class="card mb-3">
          <div class="flex-between mb-2">
            <strong>{{ q.subject }}</strong>
            <div class="action-row">
              <span class="sender-chip">
                <span class="sender-avatar">{{ (q.sender?.name || q.sender_role || '?').charAt(0).toUpperCase() }}</span>
                <span class="sender-name">{{ q.sender?.name || 'Unknown' }}</span>
                <span class="tag" :style="q.sender_role === 'trainer' ? 'background:#fef3c7;color:#92400e' : ''">{{ q.sender_role }}</span>
              </span>
              <span :class="statusPill(q.status)">{{ q.status }}</span>
              <span class="text-xs text-muted">{{ formatDate(q.created_at) }}</span>
            </div>
          </div>
          <p class="text-sm text-muted mb-2">{{ q.message }}</p>
          <div v-if="q.response" class="query-response">
            <span class="query-response-label">Response: </span>{{ q.response }}
          </div>
          <div v-if="q.status === 'pending'" class="mt-3">
            <textarea v-model="q._replyText" rows="3" class="form-input w-full resize-none mb-2" placeholder="Type your response and hit Send — an email will be sent automatically…"></textarea>
            <button class="btn-primary" @click="respondQuery(q)" :disabled="!q._replyText || actionLoading">📧 Send Reply</button>
          </div>
        </div>
      </section>

      <!-- ══════════════ REVIEWS ══════════════ -->
      <section v-if="activeSection === 'reviews'" class="page-section">
        <div v-if="reviews.length === 0 && !loading" class="empty-state">No pending reviews.</div>
        <div v-for="r in reviews" :key="r._id" class="card mb-3">
          <div class="flex-between mb-2">
            <span class="review-stars">{{ '★'.repeat(r.rating) }}<span class="review-stars--empty">{{ '★'.repeat(5 - r.rating) }}</span></span>
            <span :class="statusPill(r.status)">{{ r.status }}</span>
          </div>
          <p class="text-sm text-muted mb-2">{{ r.comment || '(no comment)' }}</p>
          <p class="text-xs text-muted mb-3">Client: {{ r.client_name || r.client_id }} · Trainer: {{ r.trainer_name || r.trainer_id }}</p>
          <div v-if="r.status === 'pending'" class="action-row">
            <button class="btn-approve" @click="approveReview(r._id)" :disabled="actionLoading">✓ Approve</button>
            <button class="btn-danger" @click="rejectReview(r._id)" :disabled="actionLoading">✗ Reject</button>
          </div>
        </div>
      </section>

    </main>

    <!-- ═══ MODALS ═══ -->

    <!-- Schedule Session Modal -->
    <div v-if="showSessionModal" class="modal-backdrop" @click.self="showSessionModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h3 class="modal-title">{{ editingSession?._id ? 'Edit Session' : 'Schedule Session' }}</h3>
          <button @click="showSessionModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group"><label class="form-label">Title *</label><input v-model="sessionForm.title" class="form-input" placeholder="e.g. Morning Flow Session" /></div>
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">Client *</label>
              <select v-model="sessionForm.client_id" @change="onSessionClientChange" class="form-input">
                <option value="">— Select Client —</option>
                <option v-for="c in activeClients" :key="c._id" :value="c._id">{{ c.name }}</option>
              </select>
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Trainer *</label>
              <select v-model="sessionForm.trainer_id" class="form-input">
                <option value="">— Select Trainer —</option>
                <option v-for="t in activeTrainers" :key="t._id" :value="t._id">{{ t.name }}</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group flex-1"><label class="form-label">Date & Time *</label><input type="datetime-local" v-model="sessionForm.scheduled_at" class="form-input" /></div>
            <div class="form-group flex-1"><label class="form-label">Duration (min)</label><input type="number" v-model="sessionForm.duration_minutes" min="15" step="15" class="form-input" /></div>
          </div>
          <div class="form-group"><label class="form-label">Session Type</label>
            <select v-model="sessionForm.session_type" class="form-input">
              <option value="regular">Regular</option>
              <option value="assessment">Assessment</option>
              <option value="makeup">Makeup</option>
            </select>
          </div>
          <div class="form-group"><label class="form-label">Notes</label><textarea v-model="sessionForm.notes" rows="2" class="form-input resize-none w-full" placeholder="Optional notes…"></textarea></div>
          <div v-if="sessionForm.client_id && selectedClientPending !== null" class="info-banner-blue">
            <span>ℹ</span> This client has <strong>{{ selectedClientPending }}</strong> pending sessions remaining.
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showSessionModal = false">Cancel</button>
          <button class="btn-primary" @click="submitSession" :disabled="!sessionForm.title || !sessionForm.client_id || !sessionForm.trainer_id || !sessionForm.scheduled_at || actionLoading">
            {{ editingSession?._id ? 'Update Session' : 'Schedule & Notify' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Package Modal -->
    <div v-if="showPackageModal" class="modal-backdrop" @click.self="showPackageModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h3 class="modal-title">{{ editingPackage?._id ? 'Edit Package' : 'New Package' }}</h3>
          <button @click="showPackageModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group"><label class="form-label">Title *</label><input v-model="packageForm.title" class="form-input" /></div>
          <div class="form-group"><label class="form-label">Description</label><textarea v-model="packageForm.description" rows="2" class="form-input resize-none w-full"></textarea></div>
          <div class="form-row">
            <div class="form-group flex-1"><label class="form-label">Price (₹)</label><input type="number" v-model.number="packageForm.price" min="0" class="form-input" /></div>
            <div class="form-group flex-1"><label class="form-label">Duration (weeks) *</label><input type="number" v-model.number="packageForm.duration_weeks" min="1" class="form-input" /></div>
          </div>
          <div class="form-row">
            <div class="form-group flex-1">
              <label class="form-label">Sessions / Week *</label>
              <input type="number" v-model.number="packageForm.sessions_per_week" min="1" class="form-input"
                     placeholder="e.g. 3" />
            </div>
            <div class="form-group flex-1">
              <label class="form-label">Total Sessions (auto-calculated)</label>
              <input type="number" :value="computedTotalSessions" disabled
                     class="form-input" style="background:#f9fafb;cursor:not-allowed;font-weight:600;color:#2c3e2d" />
            </div>
          </div>
          <div class="info-banner-blue" style="margin-top:4px" v-if="packageForm.sessions_per_week && packageForm.duration_weeks">
            <span>📊</span>
            <strong>{{ packageForm.sessions_per_week }}</strong> sessions/week ×
            <strong>{{ packageForm.duration_weeks }}</strong> weeks =
            <strong>{{ computedTotalSessions }}</strong> total sessions
          </div>
          <label class="checkbox-label" style="margin-top:12px">
            <input type="checkbox" v-model="packageForm.is_featured" class="checkbox-input" />
            Featured package
          </label>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showPackageModal = false">Cancel</button>
          <button class="btn-primary" @click="submitPackage"
            :disabled="!packageForm.title || !packageForm.duration_weeks || !packageForm.sessions_per_week || actionLoading">
            {{ editingPackage?._id ? 'Update' : 'Create Package' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="confirmModal.show" class="modal-backdrop" @click.self="confirmModal.show = false">
      <div class="modal-box" style="max-width:400px">
        <div class="modal-header" style="background:#fef2f2">
          <h3 class="modal-title" style="color:#dc2626">⚠ Confirm Deletion</h3>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to permanently remove <strong>{{ confirmModal.name }}</strong>?</p>
          <p class="text-xs text-muted mt-1">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="confirmModal.show = false">Cancel</button>
          <button class="btn-danger" @click="executeDelete" :disabled="actionLoading">Yes, Delete</button>
        </div>
      </div>
    </div>

    <!-- Toast notifications -->
    <div class="toast-container">
      <div v-for="toast in toasts" :key="toast.id"
        :class="['toast', toast.type === 'success' ? 'toast--success' : toast.type === 'error' ? 'toast--error' : 'toast--info']">
        <span>{{ toast.message }}</span>
        <button @click="removeToast(toast.id)" class="toast-close">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted, onUnmounted, reactive } from 'vue'

const API = (path, opts = {}) => {
  const token = localStorage.getItem('token')
  return fetch(`/api${path}`, {
    ...opts,
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', ...(opts.headers || {}) }
  }).then(async r => {
    const data = await r.json()
    if (!r.ok) throw new Error(data.error || `HTTP ${r.status}`)
    return data
  })
}

export default defineComponent({
  name: 'AdminDashboard',
  setup() {
    const activeSection = ref('overview')
    const sidebarCollapsed = ref(false)
    const mobileSidebarOpen = ref(false)
    const loading = ref(false)
    const actionLoading = ref(false)
    const globalSearch = ref('')
    const toasts = ref([])
    const stats = ref({})

    const clients = ref([])
    const clientFilter = ref('all')
    const clientSearch = ref('')
    const clientPage = ref(1)
    const clientPages = ref(1)
    const clientFilterCounts = ref({})
    const selectedClient = ref(null)
    const selectedClientDetail = ref({ sessions: [], queries: [], trainer: null, subscription: null })
    const clientDetailTab = ref('progress')
    const trainerToAssign = ref('')
    const packageToAssign = ref('')
    const selectedClientPending = ref(null)

    const trainers = ref([])
    const trainerFilter = ref('all')
    const trainerSearch = ref('')
    const trainerPage = ref(1)
    const trainerPages = ref(1)
    const selectedTrainer = ref(null)
    const selectedTrainerDetail = ref({ clients: [], sessions: [] })
    const trainerDetailTab = ref('info')

    const sessions = ref([])
    const sessionFilter = ref('all')
    const sessionPage = ref(1)
    const sessionPages = ref(1)
    const showSessionModal = ref(false)
    const editingSession = ref(null)
    const sessionForm = reactive({ title: '', client_id: '', trainer_id: '', scheduled_at: '', duration_minutes: 60, session_type: 'regular', notes: '' })

    const packages = ref([])
    const subscriptions = ref([])
    const showPackageModal = ref(false)
    const editingPackage = ref(null)
    const packageForm = reactive({ title: '', description: '', price: 0, duration_weeks: 4, sessions_per_week: 3, sessions_count: 0, is_featured: false })

    const queries = ref([])
    const queryFilter = ref('all')
    const reviews = ref([])

    const confirmModal = reactive({ show: false, type: '', id: '', name: '' })

    const navItems = [
      { id: 'overview', icon: '🏠', label: 'Overview' },
      { id: 'clients', icon: '👤', label: 'Clients', badge: 'pending_clients' },
      { id: 'trainers', icon: '🧘', label: 'Trainers', badge: 'pending_trainers' },
      { id: 'sessions', icon: '📅', label: 'Sessions' },
      { id: 'packages', icon: '📦', label: 'Packages' },
      { id: 'queries', icon: '💬', label: 'Queries', badge: 'pending_queries' },
      { id: 'reviews', icon: '⭐', label: 'Reviews', badge: 'pending_reviews' },
    ]

    const quickActions = [
      { id: 'clients', icon: '👤', label: 'Manage Clients', badge: 'pending_clients' },
      { id: 'trainers', icon: '🧘', label: 'Manage Trainers', badge: 'pending_trainers' },
      { id: 'sessions', icon: '📅', label: 'Schedule Session' },
      { id: 'packages', icon: '📦', label: 'Manage Packages' },
      { id: 'queries', icon: '💬', label: 'Answer Queries', badge: 'pending_queries' },
      { id: 'reviews', icon: '⭐', label: 'Moderate Reviews', badge: 'pending_reviews' },
    ]

    const clientDetailTabs = [
      { id: 'progress', label: '📊 Progress' },
      { id: 'sessions', label: '📅 Sessions' },
      { id: 'info', label: '👤 Info' },
      { id: 'queries', label: '💬 Queries' },
    ]

    const trainerDetailTabs = [
      { id: 'info', label: '👤 Info' },
      { id: 'clients', label: '👥 Clients' },
      { id: 'sessions', label: '📅 Sessions' },
    ]

    const currentPageTitle = computed(() => {
      if (selectedClient.value && activeSection.value === 'clients') return selectedClient.value.name
      if (selectedTrainer.value && activeSection.value === 'trainers') return selectedTrainer.value.name
      const m = { overview: 'Dashboard Overview', clients: 'Client Management', trainers: 'Trainer Management', sessions: 'Session Management', packages: 'Packages', queries: 'Queries & Complaints', reviews: 'Review Moderation' }
      return m[activeSection.value] || ''
    })

    const breadcrumb = computed(() => {
      if (selectedClient.value && activeSection.value === 'clients')
        return [{ label: 'Clients', action: () => { selectedClient.value = null } }, { label: selectedClient.value.name }]
      if (selectedTrainer.value && activeSection.value === 'trainers')
        return [{ label: 'Trainers', action: () => { selectedTrainer.value = null } }, { label: selectedTrainer.value.name }]
      return []
    })

    const filteredClients = computed(() => {
      if (!clientSearch.value) return clients.value
      const q = clientSearch.value.toLowerCase()
      return clients.value.filter(c => c.name?.toLowerCase().includes(q) || c.email?.toLowerCase().includes(q) || c.phone?.includes(q))
    })

    const filteredTrainers = computed(() => {
      if (!trainerSearch.value) return trainers.value
      const q = trainerSearch.value.toLowerCase()
      return trainers.value.filter(t => t.name?.toLowerCase().includes(q) || t.specialization?.toLowerCase().includes(q))
    })

    const activeTrainers = computed(() => trainers.value.filter(t => t.status === 'active'))
    const activeClients = computed(() => clients.value.filter(c => c.status === 'active'))

    const completionPct = (sub) => {
      if (!sub || !sub.total_sessions) return 0
      return Math.round((sub.completed_sessions / sub.total_sessions) * 100)
    }

    const computedTotalSessions = computed(() =>
      (packageForm.sessions_per_week || 0) * (packageForm.duration_weeks || 0)
    )

    const getBadge = (key) => {
      if (key === 'pending_clients') return stats.value.clients?.pending || 0
      if (key === 'pending_trainers') return stats.value.trainers?.pending || 0
      if (key === 'pending_queries') return stats.value.pending_queries || 0
      if (key === 'pending_reviews') return stats.value.pending_reviews || 0
      return 0
    }

    const statusPill = (status) => {
      const base = 'status-pill '
      const map = {
        active: base + 'status-active',
        pending: base + 'status-pending',
        blocked: base + 'status-blocked',
        completed: base + 'status-completed',
        scheduled: base + 'status-scheduled',
        cancelled: base + 'status-cancelled',
        pending_approval: base + 'status-pending',
        resolved: base + 'status-active',
        rejected: base + 'status-blocked',
        approved: base + 'status-active',
      }
      return map[status] || base + 'status-default'
    }

    const clientSubStats = (sub) => [
      { label: 'Total Weeks', value: sub.total_weeks },
      { label: 'Sessions/Week', value: sub.sessions_per_week },
      { label: 'Total Sessions', value: sub.total_sessions },
      { label: 'Completed', value: sub.completed_sessions, highlight: true },
      { label: 'Pending', value: sub.pending_sessions, orange: true },
    ]

    const clientInfoFields = (client, detail) => [
      { label: 'Full Name', value: client.name || '—' },
      { label: 'Email', value: client.email || '—' },
      { label: 'Phone', value: client.phone || '—' },
      { label: 'Status', value: `<span class="${statusPill(client.status)}">${client.status}</span>` },
      { label: 'Registered', value: formatDate(client.created_at) },
      { label: 'Assigned Trainer', value: detail.trainer?.name || '—' },
    ]

    const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'
    const formatDateTime = (d) => d ? new Date(d).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—'

    let toastId = 0
    const toast = (message, type = 'success') => {
      const id = ++toastId
      toasts.value.push({ id, message, type })
      setTimeout(() => removeToast(id), 4000)
    }
    const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

    const navigate = (section) => {
      activeSection.value = section
      selectedClient.value = null
      selectedTrainer.value = null
      mobileSidebarOpen.value = false
      if (section === 'clients') fetchClients()
      if (section === 'trainers') fetchTrainers()
      if (section === 'sessions') fetchSessions()
      if (section === 'packages') { fetchPackages(); fetchSubscriptions() }
      if (section === 'queries') fetchQueries()
      if (section === 'reviews') fetchReviews()
    }

    const fetchStats = async () => {
      try { stats.value = await API('/admin/stats') } catch (e) { toast('Failed to load stats', 'error') }
    }

    const fetchClients = async () => {
      loading.value = true
      try {
        const status = clientFilter.value === 'all' ? '' : clientFilter.value
        const data = await API(`/admin/clients?page=${clientPage.value}&per_page=20${status ? '&status=' + status : ''}`)
        clients.value = data.items; clientPages.value = data.pages
      } catch (e) { toast('Failed to load clients', 'error') }
      loading.value = false
    }

    const fetchTrainers = async () => {
      loading.value = true
      try {
        const status = trainerFilter.value === 'all' ? '' : trainerFilter.value
        const data = await API(`/admin/trainers?page=${trainerPage.value}&per_page=20${status ? '&status=' + status : ''}`)
        trainers.value = data.items; trainerPages.value = data.pages
      } catch (e) { toast('Failed to load trainers', 'error') }
      loading.value = false
    }

    const fetchSessions = async () => {
      loading.value = true
      try {
        const status = sessionFilter.value === 'all' ? '' : sessionFilter.value
        const data = await API(`/admin/sessions?page=${sessionPage.value}&per_page=20${status ? '&status=' + status : ''}`)
        sessions.value = data.items; sessionPages.value = data.pages
      } catch (e) { toast('Failed to load sessions', 'error') }
      loading.value = false
    }

    const fetchPackages = async () => {
      try { const data = await API('/admin/packages'); packages.value = data.items || data } catch (e) { toast('Failed to load packages', 'error') }
    }

    const fetchSubscriptions = async () => {
      try { const data = await API('/admin/subscriptions'); subscriptions.value = data.items || data } catch (e) { console.warn('Subscriptions not ready') }
    }

    const fetchQueries = async () => {
      loading.value = true
      try {
        const status = queryFilter.value === 'all' ? '' : queryFilter.value
        const data = await API(`/admin/queries${status ? '?status=' + status : ''}`)
        queries.value = (data.items || data).map(q => ({ ...q, _replyText: '' }))
      } catch (e) { toast('Failed to load queries', 'error') }
      loading.value = false
    }

    const fetchReviews = async () => {
      try { const data = await API('/admin/reviews?status=pending'); reviews.value = data.items || data } catch (e) { toast('Failed to load reviews', 'error') }
    }

    const openClientDetail = async (client) => {
      selectedClient.value = client; clientDetailTab.value = 'progress'
      await loadClientDetail(client._id)
    }

    const openClientFromTrainer = async (client) => {
      activeSection.value = 'clients'; selectedTrainer.value = null
      selectedClient.value = client; clientDetailTab.value = 'progress'
      await loadClientDetail(client._id)
    }

    const loadClientDetail = async (clientId) => {
      loading.value = true
      try { const data = await API(`/admin/clients/${clientId}/detail`); selectedClientDetail.value = data; trainerToAssign.value = data.trainer?._id || '' }
      catch (e) { toast('Failed to load client details', 'error') }
      loading.value = false
    }

    const openTrainerDetail = async (trainer) => {
      selectedTrainer.value = trainer; trainerDetailTab.value = 'info'; loading.value = true
      try {
        const data = await API(`/admin/trainers/${trainer._id}`)
        selectedTrainerDetail.value = { clients: data.assigned_clients || [], sessions: data.sessions || [] }
      } catch (e) { toast('Failed to load trainer details', 'error') }
      loading.value = false
    }

    const approveTrainer = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/trainers/${id}/approve`, { method: 'PUT' }); toast('Trainer approved!'); selectedTrainer.value = null; fetchTrainers(); fetchStats() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const rejectTrainer = async (id) => {
      const reason = prompt('Rejection reason:'); if (!reason) return
      actionLoading.value = true
      try { await API(`/admin/trainers/${id}/reject`, { method: 'PUT', body: JSON.stringify({ reason }) }); toast('Trainer rejected'); selectedTrainer.value = null; fetchTrainers(); fetchStats() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const blockTrainer = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/trainers/${id}/block`, { method: 'PUT' }); toast('Trainer blocked'); selectedTrainer.value = null; fetchTrainers() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const unblockTrainer = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/trainers/${id}/unblock`, { method: 'PUT' }); toast('Trainer unblocked'); selectedTrainer.value = null; fetchTrainers() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const activateClient = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/clients/${id}/activate`, { method: 'PUT' }); toast('Client activated!'); fetchClients(); fetchStats(); if (selectedClient.value) selectedClient.value.status = 'active' }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const blockClient = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/clients/${id}/block`, { method: 'PUT' }); toast('Client blocked'); fetchClients(); if (selectedClient.value) selectedClient.value.status = 'blocked' }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const unblockClient = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/clients/${id}/unblock`, { method: 'PUT' }); toast('Client unblocked'); fetchClients(); if (selectedClient.value) selectedClient.value.status = 'active' }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const assignTrainer = async () => {
      if (!trainerToAssign.value) return; actionLoading.value = true
      try {
        await API(`/admin/clients/${selectedClient.value._id}/assign-trainer`, { method: 'POST', body: JSON.stringify({ trainer_id: trainerToAssign.value }) })
        toast('Trainer assigned!'); await loadClientDetail(selectedClient.value._id)
      } catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const assignPackageToClient = async () => {
      if (!packageToAssign.value) return; actionLoading.value = true
      try { await API(`/admin/clients/${selectedClient.value._id}/assign-package`, { method: 'POST', body: JSON.stringify({ package_id: packageToAssign.value }) }); toast('Package assigned!'); packageToAssign.value = ''; await loadClientDetail(selectedClient.value._id) }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const openScheduleSession = (client) => {
      editingSession.value = null
      Object.assign(sessionForm, { title: '', client_id: client?._id || '', trainer_id: '', scheduled_at: '', duration_minutes: 60, session_type: 'regular', notes: '' })
      if (client?._id) computePending(client._id)
      showSessionModal.value = true
    }

    const editSession = (s) => {
      editingSession.value = s
      const dt = s.scheduled_at ? new Date(s.scheduled_at).toISOString().slice(0, 16) : ''
      Object.assign(sessionForm, { title: s.title, client_id: s.client_id, trainer_id: s.trainer_id, scheduled_at: dt, duration_minutes: s.duration_minutes || 60, session_type: s.session_type || 'regular', notes: s.notes || '' })
      showSessionModal.value = true
    }

    const onSessionClientChange = () => {
      if (sessionForm.client_id) computePending(sessionForm.client_id)
      const c = clients.value.find(x => x._id === sessionForm.client_id)
      if (c?.assigned_trainer?._id) sessionForm.trainer_id = c.assigned_trainer._id
    }

    const computePending = (clientId) => {
      const c = clients.value.find(x => x._id === clientId)
      selectedClientPending.value = c?.subscription ? c.subscription.pending_sessions : null
    }

    const submitSession = async () => {
      actionLoading.value = true
      try {
        if (editingSession.value?._id) { await API(`/admin/sessions/${editingSession.value._id}`, { method: 'PUT', body: JSON.stringify(sessionForm) }); toast('Session updated!') }
        else { await API('/admin/sessions', { method: 'POST', body: JSON.stringify(sessionForm) }); toast('Session scheduled!') }
        showSessionModal.value = false; fetchSessions()
        if (selectedClient.value) await loadClientDetail(selectedClient.value._id)
      } catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const confirmDeleteSession = (id) => { confirmModal.show = true; confirmModal.type = 'session'; confirmModal.id = id; confirmModal.name = 'this session' }

    const openPackageModal = (pkg) => {
      editingPackage.value = pkg || null
      const defaults = { title: '', description: '', price: 0, duration_weeks: 4, sessions_per_week: 3, sessions_count: 0, is_featured: false }
      Object.assign(packageForm, pkg ? {
        ...defaults, ...pkg,
        sessions_per_week: pkg.sessions_per_week || Math.max(1, Math.round((pkg.sessions_count || 1) / (pkg.duration_weeks || 1)))
      } : defaults)
      showPackageModal.value = true
    }

    const submitPackage = async () => {
      actionLoading.value = true
      try {
        const payload = {
          ...packageForm,
          sessions_count: packageForm.sessions_per_week * packageForm.duration_weeks
        }
        if (editingPackage.value?._id) {
          await API(`/admin/packages/${editingPackage.value._id}`, { method: 'PUT', body: JSON.stringify(payload) })
          toast('Package updated!')
        } else {
          await API('/admin/packages', { method: 'POST', body: JSON.stringify(payload) })
          toast('Package created!')
        }
        showPackageModal.value = false; fetchPackages()
      } catch (e) { toast(e.message, 'error') }
      actionLoading.value = false
    }

    const togglePackage = async (id) => {
      try { await API(`/admin/packages/${id}/toggle`, { method: 'PUT' }); toast('Package status updated'); fetchPackages() }
      catch (e) { toast(e.message, 'error') }
    }

    const confirmDeletePackage = (id) => { confirmModal.show = true; confirmModal.type = 'package'; confirmModal.id = id; confirmModal.name = 'this package' }

    const respondQuery = async (q) => {
      if (!q._replyText) return; actionLoading.value = true
      try { await API(`/admin/queries/${q._id}/respond`, { method: 'PUT', body: JSON.stringify({ response: q._replyText }) }); toast('Reply sent!'); q.status = 'resolved'; q.response = q._replyText; q._replyText = '' }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const approveReview = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/reviews/${id}/approve`, { method: 'PUT' }); toast('Review approved'); fetchReviews() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const rejectReview = async (id) => {
      actionLoading.value = true
      try { await API(`/admin/reviews/${id}/reject`, { method: 'PUT', body: JSON.stringify({ reason: 'Does not meet guidelines' }) }); toast('Review rejected'); fetchReviews() }
      catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const confirmDelete = (type, id, name) => { confirmModal.show = true; confirmModal.type = type; confirmModal.id = id; confirmModal.name = name }

    const executeDelete = async () => {
      actionLoading.value = true
      try {
        const { type, id } = confirmModal
        if (type === 'client') await API(`/admin/clients/${id}`, { method: 'DELETE' })
        else if (type === 'trainer') await API(`/admin/trainers/${id}`, { method: 'DELETE' })
        else if (type === 'session') await API(`/admin/sessions/${id}`, { method: 'DELETE' })
        else if (type === 'package') await API(`/admin/packages/${id}`, { method: 'DELETE' })
        toast(`${type} removed`); confirmModal.show = false
        if (type === 'client') { selectedClient.value = null; fetchClients() }
        if (type === 'trainer') { selectedTrainer.value = null; fetchTrainers() }
        if (type === 'session') { fetchSessions(); if (selectedClient.value) loadClientDetail(selectedClient.value._id) }
        if (type === 'package') fetchPackages()
        fetchStats()
      } catch (e) { toast(e.message, 'error') }; actionLoading.value = false
    }

    const filteredQueries = computed(() => {
      const q = globalSearch.value.toLowerCase()
      if (!q) return queries.value
      return queries.value.filter(item =>
        item.subject?.toLowerCase().includes(q) ||
        item.message?.toLowerCase().includes(q) ||
        item.sender?.name?.toLowerCase().includes(q) ||
        item.sender_role?.toLowerCase().includes(q)
      )
    })

    const filteredSessions = computed(() => {
      const q = globalSearch.value.toLowerCase()
      if (!q) return sessions.value
      return sessions.value.filter(s =>
        s.title?.toLowerCase().includes(q) ||
        s.client?.name?.toLowerCase().includes(q) ||
        s.trainer?.name?.toLowerCase().includes(q) ||
        s.status?.toLowerCase().includes(q)
      )
    })

    // ── GLOBAL SEARCH: jump to section if term matches a section keyword ──
    const handleSearch = () => {
      const q = globalSearch.value.toLowerCase()
      if (!q) return
      if (['client', 'user'].some(k => q.includes(k))) { activeSection.value = 'clients'; fetchClients() }
      else if (['trainer'].some(k => q.includes(k))) { activeSection.value = 'trainers'; fetchTrainers() }
      else if (['session'].some(k => q.includes(k))) { activeSection.value = 'sessions'; fetchSessions() }
      else if (['query', 'complaint'].some(k => q.includes(k))) { activeSection.value = 'queries'; fetchQueries() }
      else if (['review'].some(k => q.includes(k))) { activeSection.value = 'reviews'; fetchReviews() }
      // else filter in current section — reactive computed handles it
    }

    // ── AUTO-REFRESH: re-fetch active section every 60 s ──
    let autoRefreshTimer = null
    const startAutoRefresh = () => {
      autoRefreshTimer = setInterval(() => {
        const s = activeSection.value
        if (s === 'overview') fetchStats()
        else if (s === 'clients') fetchClients()
        else if (s === 'trainers') fetchTrainers()
        else if (s === 'sessions') fetchSessions()
        else if (s === 'packages') { fetchPackages(); fetchSubscriptions() }
        else if (s === 'queries') fetchQueries()
        else if (s === 'reviews') fetchReviews()
      }, 60000)
    }

    onMounted(() => {
      fetchStats(); fetchTrainers(); fetchClients(); fetchPackages()
      startAutoRefresh()
    })

    onUnmounted(() => { if (autoRefreshTimer) clearInterval(autoRefreshTimer) })

    return {
      activeSection, sidebarCollapsed, mobileSidebarOpen, loading, actionLoading, globalSearch, toasts,
      stats, navItems, quickActions, currentPageTitle, breadcrumb,
      clients, clientFilter, clientSearch, clientPage, clientPages, clientFilterCounts,
      filteredClients, selectedClient, selectedClientDetail, clientDetailTab, clientDetailTabs,
      trainerToAssign, packageToAssign, selectedClientPending,
      trainers, trainerFilter, trainerSearch, trainerPage, trainerPages, filteredTrainers,
      selectedTrainer, selectedTrainerDetail, trainerDetailTab, trainerDetailTabs,
      activeTrainers, activeClients,
      sessions, sessionFilter, sessionPage, sessionPages,
      showSessionModal, editingSession, sessionForm,
      packages, subscriptions, showPackageModal, editingPackage, packageForm,
      queries, queryFilter, reviews, confirmModal,
      completionPct, getBadge, statusPill, clientSubStats, clientInfoFields, computedTotalSessions,
      formatDate, formatDateTime,
      navigate, handleSearch,
      filteredQueries, filteredSessions,
      openClientDetail, openClientFromTrainer, openTrainerDetail,
      activateClient, blockClient, unblockClient, assignTrainer, assignPackageToClient,
      approveTrainer, rejectTrainer, blockTrainer, unblockTrainer,
      openScheduleSession, editSession, onSessionClientChange, submitSession, confirmDeleteSession,
      openPackageModal, submitPackage, togglePackage, confirmDeletePackage,
      respondQuery, approveReview, rejectReview,
      confirmDelete, executeDelete, removeToast,
      fetchClients, fetchTrainers, fetchSessions, fetchQueries, fetchReviews
    }
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ═══ SIDEBAR OVERLAY (mobile) ═══ */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 45;
  backdrop-filter: blur(2px);
}

/* ═══ HAMBURGER ═══ */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
  flex-shrink: 0;
  transition: background 0.15s;
}
.hamburger-btn:hover { background: #f3f4f6; }
.hamburger-line {
  display: block;
  width: 20px;
  height: 2px;
  background: #374151;
  border-radius: 2px;
  transition: all 0.2s;
}

/* ═══ MOBILE RESPONSIVE ═══ */
@media (max-width: 768px) {
  .sidebar-overlay { display: block; }
  .hamburger-btn { display: flex; }

  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.25s ease, width 0.25s ease;
    width: 220px !important;
  }
  .sidebar--mobile-open {
    transform: translateX(0);
  }

  .main-content {
    margin-left: 0 !important;
  }
  .main-content--collapsed {
    margin-left: 0 !important;
  }

  .sidebar-toggle { display: none; }

  .topbar-inner {
    padding: 0 14px;
    gap: 10px;
  }

  .search-wrap { display: none; }
  .user-name { display: none; }

  .page-title { font-size: 16px; }

  .page-section { padding: 14px; }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .topbar-left {
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }

  .list-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-field { width: 100% !important; }
  .search-field-wrap { width: 100%; }

  .form-row { flex-direction: column; }

  .tab-strip {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
  }

  .detail-header { flex-direction: column; }
  .detail-actions { width: 100%; }

  .data-table th, .data-table td { padding: 8px 10px; font-size: 12px; }

  .modal-box { border-radius: 12px; }

  .sub-stats-grid { grid-template-columns: repeat(2, 1fr); }

  .packages-grid { grid-template-columns: 1fr; }

  .card { padding: 14px; }

  .topbar-right { gap: 8px; }
}

@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat-number { font-size: 22px; }
  .quick-actions-grid { grid-template-columns: 1fr 1fr; }
  .filter-chips { gap: 4px; }
  .filter-chip { padding: 5px 10px; font-size: 11px; }
  .page-section { padding: 10px; }
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body { font-family: 'Inter', sans-serif; background: #f5f4f0; }

/* ═══ LAYOUT ═══ */
.dashboard-root {
  display: flex;
  min-height: 100vh;
  background: #f5f4f0;
  font-family: 'Inter', sans-serif;
}

/* ═══ SIDEBAR ═══ */
.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: 220px;
  background: #1a1f1a;
  display: flex;
  flex-direction: column;
  z-index: 50;
  transition: width 0.25s ease;
  overflow: hidden;
}
.sidebar--collapsed { width: 64px; }

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  flex-shrink: 0;
}
.sidebar-logo { font-size: 20px; flex-shrink: 0; }
.sidebar-name {
  color: white;
  font-family: 'Lora', serif;
  font-size: 17px;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.sidebar-nav {
  flex: 1;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  transition: background 0.15s, color 0.15s;
  position: relative;
  white-space: nowrap;
}
.nav-item:hover { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.85); }
.nav-item--active { background: #4a7c59; color: white; }
.nav-icon { font-size: 16px; flex-shrink: 0; }
.nav-label { flex: 1; }
.nav-badge {
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 99px;
  min-width: 18px;
  text-align: center;
  flex-shrink: 0;
}
.nav-badge--dot {
  width: 8px; height: 8px;
  padding: 0; border-radius: 50%;
  position: absolute; top: 6px; right: 6px;
}

.sidebar-toggle {
  background: none;
  border: none;
  border-top: 1px solid rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.3);
  font-size: 18px;
  cursor: pointer;
  padding: 12px;
  text-align: right;
  transition: color 0.15s;
  flex-shrink: 0;
}
.sidebar-toggle:hover { color: rgba(255,255,255,0.6); }

/* ═══ MAIN ═══ */
.main-content {
  margin-left: 220px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.25s ease;
}
.main-content--collapsed { margin-left: 64px; }

/* ═══ TOPBAR ═══ */
.topbar {
  position: sticky;
  top: 0;
  z-index: 40;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  gap: 16px;
}
.topbar-left { display: flex; flex-direction: column; gap: 2px; }
.page-title {
  font-family: 'Lora', serif;
  font-size: 20px;
  color: #111827;
  font-weight: 500;
  line-height: 1.2;
}
.breadcrumb { display: flex; align-items: center; gap: 4px; }
.breadcrumb-item { display: flex; align-items: center; gap: 4px; font-size: 12px; }
.breadcrumb-link { color: #4a7c59; background: none; border: none; cursor: pointer; font-size: 12px; padding: 0; text-decoration: underline; }
.breadcrumb-text { color: #6b7280; }
.breadcrumb-sep { color: #d1d5db; }

.topbar-right { display: flex; align-items: center; gap: 14px; flex-shrink: 0; }
.search-wrap { position: relative; }
.search-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 13px; }
.search-input {
  padding: 8px 14px 8px 34px;
  font-size: 13px;
  border: 1px solid #e5e7eb;
  border-radius: 99px;
  width: 220px;
  background: #f9fafb;
  outline: none;
  transition: border-color 0.15s, background 0.15s;
  font-family: 'Inter', sans-serif;
}
.search-input:focus { border-color: #4a7c59; background: white; }
.search-clear { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #9ca3af; font-size: 16px; line-height: 1; padding: 0 2px; }
.search-clear:hover { color: #374151; }
.sender-chip { display: inline-flex; align-items: center; gap: 6px; background: #f9fafb; border: 1px solid #f0f0ee; border-radius: 99px; padding: 3px 10px 3px 4px; }
.sender-avatar { width: 20px; height: 20px; border-radius: 50%; background: #4a7c59; color: white; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; }
.sender-name { font-size: 12px; font-weight: 500; color: #374151; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.user-chip { display: flex; align-items: center; gap: 8px; }
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: #4a7c59;
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600;
}
.user-name { font-size: 13px; color: #6b7280; }

.loading-bar-wrap { height: 2px; background: #f3f4f6; overflow: hidden; }
.loading-bar { height: 100%; background: #4a7c59; animation: loading 1.5s infinite ease-in-out; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(400%); } }

/* ═══ PAGE SECTION ═══ */
.page-section { padding: 24px; flex: 1; }

/* ═══ CARDS ═══ */
.card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f0f0ee;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 20px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 4px;
}
.card-title {
  font-family: 'Lora', serif;
  font-size: 16px;
  color: #1f2937;
  font-weight: 500;
}
.section-heading {
  font-family: 'Lora', serif;
  font-size: 18px;
  color: #1f2937;
  font-weight: 500;
}
.mb-3 { margin-bottom: 12px; }
.mb-4 { margin-bottom: 16px; }
.mb-5 { margin-bottom: 20px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }
.mt-4 { margin-top: 16px; }
.mt-6 { margin-top: 24px; }
.ml-auto { margin-left: auto; }
.pt-4 { padding-top: 16px; }
.flex-1 { flex: 1; }

/* ═══ STATS GRID ═══ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}
@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .stats-grid { grid-template-columns: 1fr; } }

.stat-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f0f0ee;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: box-shadow 0.15s;
  position: relative;
}
.stat-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.stat-icon-wrap {
  width: 40px; height: 40px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.stat-body {}
.stat-number {
  font-family: 'Lora', serif;
  font-size: 28px;
  color: #111827;
  font-weight: 500;
  line-height: 1;
}
.stat-label { font-size: 12px; color: #9ca3af; margin-top: 3px; }
.stat-badge {
  position: absolute;
  top: 14px; right: 14px;
  background: #fef3c7;
  color: #92400e;
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 99px;
}

/* ═══ QUICK ACTIONS ═══ */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
@media (max-width: 700px) { .quick-actions-grid { grid-template-columns: repeat(2, 1fr); } }

.quick-action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #f0f0ee;
  background: white;
  cursor: pointer;
  text-align: left;
  transition: border-color 0.15s, background 0.15s;
}
.quick-action-btn:hover { border-color: rgba(74,124,89,0.3); background: rgba(74,124,89,0.04); }
.qa-icon { font-size: 22px; }
.qa-label { font-size: 13px; font-weight: 500; color: #374151; }
.qa-sub { font-size: 11px; color: #d97706; font-weight: 600; margin-top: 2px; }

/* ═══ DETAIL HEADER ═══ */
.detail-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}
.detail-avatar {
  width: 60px; height: 60px;
  border-radius: 14px;
  color: white;
  font-family: 'Lora', serif;
  font-size: 24px;
  font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.detail-info { flex: 1; min-width: 0; }
.detail-name { font-family: 'Lora', serif; font-size: 22px; color: #111827; margin-bottom: 8px; }
.detail-tags { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.detail-actions { display: flex; flex-wrap: wrap; gap: 8px; flex-shrink: 0; }

/* ═══ TABS ═══ */
.tab-strip {
  display: inline-flex;
  background: white;
  border: 1px solid #f0f0ee;
  border-radius: 10px;
  padding: 4px;
  gap: 2px;
}
.tab-btn {
  padding: 7px 16px;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  background: none;
  border: none;
  color: #6b7280;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}
.tab-btn:hover { color: #111827; }
.tab-btn--active { background: #4a7c59; color: white; }

/* ═══ TABLE ═══ */
.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th {
  background: #f9fafb;
  padding: 10px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #9ca3af;
  border-bottom: 1px solid #f3f4f6;
}
.data-table td {
  padding: 12px 16px;
  color: #4b5563;
  border-bottom: 1px solid #f9fafb;
  vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover td { background: #fafaf8; }
.row-clickable { cursor: pointer; }

/* ═══ TOOLBAR ═══ */
.list-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.filter-chips { display: flex; gap: 6px; flex-wrap: wrap; }
.filter-chip {
  padding: 6px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  text-transform: capitalize;
  font-family: 'Inter', sans-serif;
}
.filter-chip:hover { border-color: #4a7c59; color: #4a7c59; }
.filter-chip--active { background: #4a7c59; color: white; border-color: #4a7c59; }

.search-field-wrap { position: relative; }
.search-field-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 12px; }
.search-field { padding-left: 32px !important; width: 200px; }

/* ═══ PAGINATION ═══ */
.pagination { display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 20px; }
.pagination-btn {
  padding: 7px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}
.pagination-btn:hover:not(:disabled) { border-color: #4a7c59; color: #4a7c59; }
.pagination-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination-info { font-size: 13px; color: #9ca3af; }

/* ═══ PACKAGES GRID ═══ */
.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 8px;
}
.package-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f0f0ee;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 20px;
  transition: box-shadow 0.15s;
}
.package-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.package-card--inactive { opacity: 0.55; }
.package-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.package-title { font-family: 'Lora', serif; font-size: 16px; color: #111827; font-weight: 500; }
.package-price { font-family: 'Lora', serif; font-size: 18px; color: #4a7c59; font-weight: 600; flex-shrink: 0; }
.package-desc { font-size: 12px; color: #9ca3af; margin-bottom: 12px; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.package-meta { display: flex; flex-direction: column; gap: 3px; margin-bottom: 12px; }
.package-meta span { font-size: 12px; color: #6b7280; }
.package-enrolled { margin-bottom: 12px; }
.package-actions { display: flex; gap: 6px; flex-wrap: wrap; padding-top: 12px; border-top: 1px solid #f3f4f6; }

/* ═══ BUTTONS ═══ */
.btn-primary {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 18px; background: #4a7c59; color: white;
  border: none; border-radius: 8px; font-size: 13px; font-weight: 500;
  cursor: pointer; transition: background 0.15s; white-space: nowrap;
  font-family: 'Inter', sans-serif;
}
.btn-primary:hover:not(:disabled) { background: #3a6147; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-approve {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 7px 14px; background: #f0fdf4; color: #16a34a;
  border: 1px solid #bbf7d0; border-radius: 7px; font-size: 12px;
  font-weight: 500; cursor: pointer; transition: all 0.15s; white-space: nowrap;
  font-family: 'Inter', sans-serif;
}
.btn-approve:hover:not(:disabled) { background: #16a34a; color: white; border-color: #16a34a; }
.btn-approve:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-block {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 7px 14px; background: #fffbeb; color: #d97706;
  border: 1px solid #fde68a; border-radius: 7px; font-size: 12px;
  font-weight: 500; cursor: pointer; transition: all 0.15s; white-space: nowrap;
  font-family: 'Inter', sans-serif;
}
.btn-block:hover:not(:disabled) { background: #d97706; color: white; border-color: #d97706; }
.btn-block:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-danger {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 7px 14px; background: #fff1f2; color: #dc2626;
  border: 1px solid #fecaca; border-radius: 7px; font-size: 12px;
  font-weight: 500; cursor: pointer; transition: all 0.15s; white-space: nowrap;
  font-family: 'Inter', sans-serif;
}
.btn-danger:hover:not(:disabled) { background: #dc2626; color: white; border-color: #dc2626; }
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-cancel {
  display: inline-flex; align-items: center;
  padding: 9px 18px; background: #f3f4f6; color: #6b7280;
  border: 1px solid #e5e7eb; border-radius: 8px; font-size: 13px;
  font-weight: 500; cursor: pointer; transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}
.btn-cancel:hover { background: #e5e7eb; }

.micro-edit, .micro-del, .micro-approve, .micro-block {
  padding: 4px 10px; border: none; border-radius: 5px; cursor: pointer;
  font-size: 11px; font-weight: 500; transition: all 0.12s;
  font-family: 'Inter', sans-serif;
}
.micro-edit { background: #eff6ff; color: #2563eb; }
.micro-edit:hover { background: #2563eb; color: white; }
.micro-del { background: #fff1f2; color: #dc2626; }
.micro-del:hover { background: #dc2626; color: white; }
.micro-approve { background: #f0fdf4; color: #16a34a; }
.micro-approve:hover { background: #16a34a; color: white; }
.micro-block { background: #fffbeb; color: #d97706; }
.micro-block:hover { background: #d97706; color: white; }

/* ═══ STATUS PILLS ═══ */
.status-pill {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 99px;
  white-space: nowrap;
}
.status-active { background: #f0fdf4; color: #16a34a; }
.status-pending { background: #fef3c7; color: #d97706; }
.status-blocked { background: #fef2f2; color: #dc2626; }
.status-completed { background: #eff6ff; color: #2563eb; }
.status-scheduled { background: #f5f3ff; color: #7c3aed; }
.status-cancelled { background: #f9fafb; color: #9ca3af; }
.status-default { background: #f9fafb; color: #6b7280; }

/* ═══ MISC ═══ */
.tag {
  display: inline-block;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 99px;
}
.text-muted { color: #9ca3af; }
.text-xs { font-size: 11px; }
.text-sm { font-size: 13px; }
.font-medium { font-weight: 500; }
.flex-between { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.action-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.row-gap { display: flex; gap: 8px; align-items: center; }
.user-row { display: flex; align-items: center; gap: 10px; }
.user-initial {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600;
  flex-shrink: 0;
}
.divider-top { border-top: 1px solid #f3f4f6; }
.w-full { width: 100%; }
.resize-none { resize: none; }

/* ═══ INFO GRID ═══ */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}
.field-label { display: block; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.field-value { font-size: 13px; color: #374151; }

/* ═══ PROGRESS ═══ */
.sub-stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}
@media (max-width: 700px) { .sub-stats-grid { grid-template-columns: repeat(2, 1fr); } }
.sub-stat {
  background: #f9fafb;
  border-radius: 10px;
  padding: 14px;
  text-align: center;
}
.sub-stat--green { background: rgba(74,124,89,0.08); }
.sub-stat--orange { background: #fffbeb; }
.sub-stat-val { font-family: 'Lora', serif; font-size: 22px; font-weight: 600; color: #1f2937; }
.sub-stat--green .sub-stat-val { color: #4a7c59; }
.sub-stat--orange .sub-stat-val { color: #d97706; }
.sub-stat-label { font-size: 11px; color: #9ca3af; margin-top: 4px; }

.progress-wrap {}
.progress-header { display: flex; justify-content: space-between; font-size: 13px; color: #4b5563; margin-bottom: 8px; }
.progress-pct { font-weight: 600; color: #4a7c59; }
.progress-bar-bg { height: 8px; background: #f3f4f6; border-radius: 99px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: #4a7c59; border-radius: 99px; transition: width 0.4s ease; }
.progress-note { font-size: 11px; color: #9ca3af; margin-top: 6px; }

.progress-mini-wrap { display: flex; align-items: center; gap: 8px; }
.progress-mini-bg { width: 80px; height: 5px; background: #f3f4f6; border-radius: 99px; overflow: hidden; }
.progress-mini-fill { height: 100%; background: #4a7c59; border-radius: 99px; }

.badge-warn {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 600;
  background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa;
}

.deadline-row {
  display: flex; flex-wrap: wrap; align-items: center; gap: 16px;
  padding: 12px 16px; background: #f9fafb; border-radius: 10px;
  border: 1px solid #e5e7eb;
}
.deadline-item { display: flex; align-items: center; gap: 8px; }
.deadline-label { font-size: 12px; color: #6b7280; font-weight: 500; }
.deadline-value { font-size: 13px; color: #111827; font-weight: 600; }

/* ═══ BADGES ═══ */
.badge-yes { color: #16a34a; font-weight: 600; font-size: 12px; }
.badge-no { color: #d1d5db; font-size: 12px; }

/* ═══ QUERY / REVIEW ═══ */
.query-response {
  background: rgba(74,124,89,0.06);
  border-left: 2px solid #4a7c59;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 13px;
  color: #374151;
  margin-top: 8px;
}
.query-response-label { font-size: 11px; font-weight: 600; color: #4a7c59; text-transform: uppercase; letter-spacing: 0.05em; }
.review-stars { font-size: 18px; letter-spacing: 1px; color: #f59e0b; }
.review-stars--empty { color: #e5e7eb; }

/* ═══ INFO BANNERS ═══ */
.info-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13px;
  color: #92400e;
}
.info-banner-blue {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  color: #1d4ed8;
}

/* ═══ EMPTY STATE ═══ */
.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: #9ca3af;
  font-size: 13px;
}

/* ═══ MODALS ═══ */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}
.modal-box {
  background: white;
  border-radius: 18px;
  width: 540px;
  max-width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: modal-in 0.2s ease;
}
@keyframes modal-in {
  from { transform: scale(0.96) translateY(8px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid #f3f4f6;
}
.modal-title { font-family: 'Lora', serif; font-size: 18px; color: #111827; }
.modal-close {
  background: none; border: none; font-size: 22px;
  cursor: pointer; color: #9ca3af; padding: 0 4px; transition: color 0.15s;
}
.modal-close:hover { color: #374151; }
.modal-body { padding: 22px; }
.modal-footer {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 14px 22px; border-top: 1px solid #f3f4f6;
}

/* ═══ FORMS ═══ */
.form-input {
  width: 100%; padding: 9px 12px;
  border: 1px solid #e5e7eb; border-radius: 7px;
  font-size: 13px; font-family: 'Inter', sans-serif;
  outline: none; transition: border-color 0.15s; background: white;
  color: #1f2937;
}
.form-input:focus { border-color: #4a7c59; }
.form-group { margin-bottom: 14px; }
.form-label { display: block; font-size: 12px; font-weight: 500; color: #6b7280; margin-bottom: 5px; }
.form-row { display: flex; gap: 14px; margin-bottom: 0; }
.form-row .form-group { margin-bottom: 14px; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; color: #4b5563; }
.checkbox-input { width: 15px; height: 15px; accent-color: #4a7c59; }

/* ═══ TOASTS ═══ */
.toast-container {
  position: fixed;
  bottom: 24px; right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  min-width: 260px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  animation: toast-in 0.2s ease;
}
@keyframes toast-in { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.toast--success { background: #1f5c2e; color: white; }
.toast--error { background: #b91c1c; color: white; }
.toast--info { background: #1e40af; color: white; }
.toast-close {
  background: none; border: none; font-size: 18px;
  cursor: pointer; color: rgba(255,255,255,0.6); transition: color 0.15s;
}
.toast-close:hover { color: white; }
</style>