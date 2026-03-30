<template>
  <div class="login-page">

    <!-- Left decorative panel -->
    <div class="auth-panel">
      <div class="panel-bg"></div>
      <div class="panel-orb po1"></div>
      <div class="panel-orb po2"></div>

      <div class="panel-content">
        <div class="panel-illustration">
          <svg viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg" width="220" height="220">
            <circle cx="120" cy="120" r="90" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
            <circle cx="120" cy="120" r="70" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="4 8"/>
            <ellipse cx="120" cy="165" rx="30" ry="7" fill="rgba(201,168,76,0.2)"/>
            <path d="M120 158 Q104 148 100 135 Q108 132 120 135 Q132 132 140 135 Q136 148 120 158Z" fill="#c9a84c" opacity="0.6"/>
            <path d="M120 158 Q90 142 86 124 Q102 122 120 135Z" fill="#c9a84c" opacity="0.3"/>
            <path d="M120 158 Q150 142 154 124 Q138 122 120 135Z" fill="#c9a84c" opacity="0.3"/>
            <circle cx="120" cy="76" r="14" fill="rgba(255,255,255,0.15)"/>
            <circle cx="120" cy="76" r="14" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
            <line x1="120" y1="90" x2="120" y2="128" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round"/>
            <path d="M120 100 Q103 92 90 84" stroke="rgba(255,255,255,0.35)" stroke-width="3" stroke-linecap="round" fill="none"/>
            <path d="M120 100 Q137 92 150 84" stroke="rgba(255,255,255,0.35)" stroke-width="3" stroke-linecap="round" fill="none"/>
            <circle cx="88" cy="83" r="3.5" fill="rgba(201,168,76,0.7)"/>
            <circle cx="152" cy="83" r="3.5" fill="rgba(201,168,76,0.7)"/>
            <path d="M120 128 Q104 138 94 148" stroke="rgba(255,255,255,0.35)" stroke-width="3" stroke-linecap="round" fill="none"/>
            <path d="M120 128 Q136 138 146 148" stroke="rgba(255,255,255,0.35)" stroke-width="3" stroke-linecap="round" fill="none"/>
            <circle cx="120" cy="76" r="22" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1">
              <animate attributeName="r" values="22;30;22" dur="3s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.2;0;0.2" dur="3s" repeatCount="indefinite"/>
            </circle>
          </svg>
        </div>

        <div class="panel-tagline">
          <div class="panel-tagline-label">✦ Welcome Back</div>
          <h2 class="panel-tagline-title">Your journey<br><em>continues here</em></h2>
          <p class="panel-tagline-sub">Sign in to your existing account below.</p>
        </div>

        <div class="panel-stats">
          <div class="panel-stat">
            <div class="panel-stat-num">2,400+</div>
            <div class="panel-stat-label">Active Members</div>
          </div>
          <div class="panel-stat-divider"></div>
          <div class="panel-stat">
            <div class="panel-stat-num">48</div>
            <div class="panel-stat-label">Expert Trainers</div>
          </div>
          <div class="panel-stat-divider"></div>
          <div class="panel-stat">
            <div class="panel-stat-num">4.9★</div>
            <div class="panel-stat-label">Avg Rating</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right login form -->
    <div class="auth-form-wrap">
      <div class="auth-form-inner">

        <div class="form-header">
          <span class="form-label">✦ Secure Login</span>
          <h1 class="form-title">Welcome<br><em>Back</em></h1>
          <p class="form-sub">Sign in with your Google account to continue</p>
        </div>

        <div class="google-section">
          <button class="btn-google" :disabled="loading" @click="handleGoogleSignIn">
            <span v-if="!loading" class="btn-google-inner">
              <svg class="google-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Continue with Google
            </span>
            <span v-else class="loading-dots">Signing in<span>.</span><span>.</span><span>.</span></span>
          </button>

          <div class="divider">
            <span class="divider-line"></span>
            <span class="divider-text">secure · private · instant</span>
            <span class="divider-line"></span>
          </div>

          <div class="google-info">
            <span class="info-icon">🔒</span>
            We use Google Sign-In — no passwords stored, no data shared.
          </div>
        </div>

        <div v-if="error" class="form-error">
          <span>⚠</span> {{ error }}
        </div>

        <div class="form-footer">
          Don't have an account?
          <router-link to="/signup" class="form-link">Begin your journey →</router-link>
        </div>

        <div class="form-footer-note">
          <span style="color:var(--gold)">🔒</span>
          Google OAuth · No passwords · Privacy-first
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import api from '../api'
import { auth, provider, signInWithGoogle, handleRedirectResult, signInWithPopup } from '../firebase'

export default {
  name: 'LoginPage',
  data() {
    return {
      loading: false,
      error: '',
      isRedirecting: false
    }
  },
  async mounted() {
    const token = localStorage.getItem('token')
    const role  = localStorage.getItem('userRole')
    if (token && role) {
      this.redirectToDashboard(role)
      return
    }
    
    // Check if this is a redirect from Google Sign-In
    await this.checkRedirectResult()
  },
  methods: {
    async checkRedirectResult() {
      try {
        const result = await handleRedirectResult()
        if (result) {
          // We have a redirect result, process it
          await this.processGoogleSignIn(result)
        }
      } catch (error) {
        console.error('Redirect sign-in error:', error)
        this.error = 'Sign-in failed. Please try again.'
      }
    },
    
    async processGoogleSignIn(result) {
      try {
        const idToken = await result.user.getIdToken()
        const res = await api.post('/auth/google', { token: idToken })
        
        if (res.needs_profile) {
          this.error = 'No account found. Please sign up first.'
          setTimeout(() => {
            this.$router.push({
              path: '/signup',
              query: {
                prefill_google_id: res.google_data.google_id,
                prefill_email:     res.google_data.email,
                prefill_name:      res.google_data.name,
                prefill_picture:   res.google_data.picture
              }
            })
          }, 1500)
          return
        }
        
        this.saveUserSession(res.token, res.user)
        this.redirectToDashboard(res.user.role)
      } catch (err) {
        throw err
      }
    },
    
    async handleGoogleSignIn() {
      this.loading = true
      this.error = ''
      
      try {
        const result = await signInWithGoogle()
        
        // If redirecting, don't process further
        if (result?.isRedirecting) {
          this.isRedirecting = true
          this.loading = false
          return
        }
        
        // Normal popup flow
        await this.processGoogleSignIn(result)
        
      } catch (err) {
        if (err.code === 'auth/popup-closed-by-user' || err.code === 'auth/cancelled-popup-request') {
          this.error = 'Sign-in cancelled. Please try again.'
        } else if (err.code === 'auth/popup-blocked') {
          this.error = 'Popup was blocked. Redirecting to Google Sign-In page...'
          // Try redirect method as last resort
          try {
            const { signInWithRedirect } = await import('../firebase')
            await signInWithRedirect(auth, provider)
          } catch (redirectErr) {
            this.error = 'Please allow popups for this site to sign in with Google.'
          }
        } else {
          this.error = err.response?.data?.error || err.message || 'Sign-in failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
    
    saveUserSession(token, user) {
      localStorage.setItem('token', token)
      localStorage.setItem('userRole', user.role)
      localStorage.setItem('userName', user.name)
      localStorage.setItem('userId', user.id)
      localStorage.setItem('user', JSON.stringify(user))
    },
    
    redirectToDashboard(role) {
      if (role === 'admin') this.$router.push('/admin')
      else if (role === 'trainer') this.$router.push('/trainer')
      else this.$router.push('/client')
    }
  }
}
</script>

<style scoped>
/* ── LAYOUT ── */
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* ── LEFT PANEL ── */
.auth-panel {
  position: relative;
  background: var(--deep);
  overflow: hidden;
  display: flex; align-items: center; justify-content: center;
  padding: 80px 60px;
}
.panel-bg {
  position: absolute; inset: 0;
  background: linear-gradient(160deg, #2F4F4F 0%, #1a3030 50%, #0d1f1f 100%);
}
.panel-orb {
  position: absolute; border-radius: 50%; filter: blur(60px); pointer-events: none;
}
.po1 { width: 400px; height: 400px; background: rgba(124,154,109,0.15); top: -100px; right: -100px; }
.po2 { width: 250px; height: 250px; background: rgba(201,168,76,0.08); bottom: -50px; left: -50px; }

.panel-content {
  position: relative; z-index: 1;
  display: flex; flex-direction: column;
  align-items: flex-start; gap: 40px; width: 100%;
}
.panel-illustration {
  display: flex; align-items: center; justify-content: center; width: 100%;
  opacity: 0.85;
}
.panel-tagline-label {
  font-size: 10px; letter-spacing: 4px; color: var(--gold);
  text-transform: uppercase; margin-bottom: 12px;
}
.panel-tagline-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(28px, 3vw, 42px); font-weight: 300;
  color: white; line-height: 1.15; margin-bottom: 12px;
}
.panel-tagline-title em { font-style: italic; color: var(--gold); }
.panel-tagline-sub { font-size: 13px; color: rgba(255,255,255,0.4); font-weight: 300; line-height: 1.7; }

.panel-stats { display: flex; align-items: center; gap: 20px; width: 100%; }
.panel-stat-num {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 22px; font-weight: 300; color: white; line-height: 1;
}
.panel-stat-label { font-size: 10px; letter-spacing: 2px; color: rgba(255,255,255,0.3); text-transform: uppercase; }
.panel-stat-divider { width: 1px; height: 32px; background: rgba(255,255,255,0.1); }

/* ── RIGHT FORM ── */
.auth-form-wrap {
  display: flex; align-items: center; justify-content: center;
  background: var(--cream); padding: 80px 60px;
  overflow-y: auto;
}
.auth-form-inner { width: 100%; max-width: 420px; }

.form-header { margin-bottom: 40px; }
.form-label {
  font-size: 10px; letter-spacing: 4px; color: var(--sage);
  text-transform: uppercase; display: block; margin-bottom: 12px;
}
.form-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(36px, 4vw, 56px); font-weight: 300;
  color: var(--text-dark); line-height: 1.05; margin-bottom: 10px;
}
.form-title em { font-style: italic; color: var(--sage-dark); }
.form-sub { font-size: 14px; color: var(--text-soft); font-weight: 300; }

/* ── GOOGLE BUTTON ── */
.google-section { display: flex; flex-direction: column; gap: 24px; }

.btn-google {
  width: 100%; padding: 15px 20px;
  background: white; border: 1.5px solid rgba(0,0,0,0.12);
  border-radius: 2px; cursor: pointer; font-family: inherit;
  font-size: 15px; font-weight: 500; color: var(--text-dark);
  transition: all 0.25s ease; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  min-height: 52px; touch-action: manipulation;
}
.btn-google:hover:not(:disabled) {
  border-color: var(--sage); box-shadow: 0 4px 20px rgba(47,79,79,0.12);
  transform: translateY(-1px);
}
.btn-google:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }
.btn-google-inner { display: flex; align-items: center; justify-content: center; gap: 12px; }
.google-icon { width: 20px; height: 20px; flex-shrink: 0; }

.divider { display: flex; align-items: center; gap: 12px; }
.divider-line { flex: 1; height: 1px; background: rgba(0,0,0,0.07); }
.divider-text {
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--text-soft); white-space: nowrap;
}

.google-info {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 16px; background: rgba(124,154,109,0.05);
  border: 1px solid rgba(124,154,109,0.12);
  border-radius: 4px; font-size: 12px; color: var(--text-mid); line-height: 1.5;
}
.info-icon { font-size: 14px; flex-shrink: 0; }

/* ── LOADING ── */
.loading-dots span { animation: blink 1.2s ease-in-out infinite; display: inline-block; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80%,100% { opacity: 0; } 40% { opacity: 1; } }

/* ── ERROR ── */
.form-error {
  margin-top: 16px; padding: 12px 16px;
  background: rgba(200,50,50,0.06); border: 1px solid rgba(200,50,50,0.15);
  border-radius: 4px; font-size: 13px; color: #c33;
  display: flex; align-items: center; gap: 8px;
}

/* ── FOOTER ── */
.form-footer {
  margin-top: 32px; padding-top: 24px;
  border-top: 1px solid rgba(0,0,0,0.06);
  font-size: 13px; color: var(--text-soft); text-align: center;
}
.form-link { color: var(--sage); text-decoration: none; margin-left: 4px; font-weight: 500; }
.form-link:hover { color: var(--sage-dark); }
.form-footer-note {
  margin-top: 16px; text-align: center;
  font-size: 11px; letter-spacing: 1.5px; color: var(--text-soft);
  display: flex; align-items: center; justify-content: center; gap: 6px;
}

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
  .login-page { grid-template-columns: 1fr; }
  .auth-panel { display: none; }
  .auth-form-wrap { padding: 100px 32px 60px; }
}
@media (max-width: 480px) {
  .auth-form-wrap { padding: 80px 20px 40px; }
  .btn-google { font-size: 14px; padding: 14px 16px; }
}
</style>