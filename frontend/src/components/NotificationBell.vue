<template>
  <div class="notification-bell" @click="toggleNotifications">
    <span class="bell-icon">🔔</span>
    <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
    
    <div v-if="isOpen" class="notifications-dropdown">
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
  name: 'NotificationBell',
  data() {
    return {
      isOpen: false,
      notifications: []
    }
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.read).length
    }
  },
  async mounted() {
    await this.loadNotifications()
    this.startPolling()
  },
  methods: {
    async loadNotifications() {
      const result = await api.getNotifications()
      if (result.success) {
        this.notifications = result
      }
    },
    
    startPolling() {
      setInterval(async () => {
        const result = await api.getNotifications(true)
        if (result.success && result.length > 0) {
          await this.loadNotifications()
        }
      }, 30000)
    },
    
    toggleNotifications() {
      this.isOpen = !this.isOpen
    },
    
    async markRead(notificationId) {
      await api.markNotificationRead(notificationId)
      await this.loadNotifications()
    },
    
    async markAllRead() {
      await api.markAllRead()
      await this.loadNotifications()
    },
    
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return 'Just now'
      if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.notification-bell {
  position: relative;
  cursor: pointer;
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
  position: absolute;
  top: 40px;
  right: 0;
  width: 350px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
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
  margin: 0;
}

.btn-link {
  background: none;
  border: none;
  color: var(--sage);
  cursor: pointer;
  font-size: 12px;
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
</style>