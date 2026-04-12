import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'

import HomePage from './pages/HomePage.vue'
import LoginPage from './pages/LoginPage.vue'
import SignupPage from './pages/SignupPage.vue'
import AdminDashboard from './pages/AdminDashboard.vue'
import TrainerDashboard from './pages/TrainerDashboard.vue'
import ClientDashboard from './pages/ClientDashboard.vue'

const routes = [
  { path: '/', component: HomePage, name: 'Home' },
  { path: '/login', component: LoginPage, name: 'Login' },
  { path: '/signup', component: SignupPage, name: 'Signup' },
  { path: '/admin', component: AdminDashboard, name: 'Admin', meta: { requiresAuth: true, role: 'admin' } },
  { path: '/trainer', component: TrainerDashboard, name: 'Trainer', meta: { requiresAuth: true, role: 'trainer' } },
  { path: '/client', component: ClientDashboard, name: 'Client', meta: { requiresAuth: true, role: 'client' } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')
  // const token = sessionStorage.getItem('token')
  // const userRole = sessionStorage.getItem('userRole')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && userRole !== to.meta.role) {
    next('/')
  } else {
    next()
  }
})

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.mount('#app')