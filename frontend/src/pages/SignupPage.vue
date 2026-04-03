<template>
  <div class="signup-page">

    <!-- Left form panel -->
    <div class="auth-form-wrap">
      <div class="auth-form-inner">

        <div class="form-header">
          <span class="form-label">✦ Join SattvaFlow</span>
          <h1 class="form-title">Begin Your<br><em>Journey</em></h1>
          <p class="form-sub">Create your account and find your flow</p>
        </div>

        <!-- ══ STEP 1: Role selection + Google Sign-In ══ -->
        <div v-if="step === 'choose'">
          <div class="role-selector">
            <button :class="{ active: role === 'client' }" @click="role = 'client'">
              <span class="role-icon">🙋</span>
              <div>
                <div class="role-name">I'm a Client</div>
                <div class="role-desc">Looking for a trainer</div>
              </div>
            </button>
            <button :class="{ active: role === 'trainer' }" @click="role = 'trainer'">
              <span class="role-icon">🧘</span>
              <div>
                <div class="role-name">I'm a Trainer</div>
                <div class="role-desc">Want to teach yoga</div>
              </div>
            </button>
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
                Sign up with Google
              </span>
              <span v-else class="loading-dots">Signing up<span>.</span><span>.</span><span>.</span></span>
            </button>
          </div>

          <div v-if="error" class="form-error"><span>⚠</span> {{ error }}</div>
        </div>

        <!-- ══ STEP 2: Profile details after Google auth ══ -->
        <div v-if="step === 'details'" class="form-step">

          <!-- Google identity confirmation pill -->
          <div class="google-confirmed">
            <img v-if="googleData.picture" :src="googleData.picture" class="g-avatar" alt="avatar" />
            <div v-else class="g-avatar-fallback">{{ googleData.name?.charAt(0) }}</div>
            <div class="g-confirmed-text">
              <div class="g-confirmed-name">{{ googleData.name }}</div>
              <div class="g-confirmed-email">{{ googleData.email }}</div>
            </div>
            <span class="g-confirmed-tick">✓</span>
          </div>

          <div class="role-confirm">
            <span class="role-confirm-icon">{{ role === 'client' ? '🙋' : '🧘' }}</span>
            Registering as <strong>{{ role === 'client' ? 'Client' : 'Trainer' }}</strong>
            <span v-if="role === 'trainer'" class="role-note"> — pending admin approval</span>
          </div>

          <div class="form-grid">
            <!-- Phone -->
            <div class="input-group full">
              <label>Phone / WhatsApp <span class="optional-tag">(optional)</span></label>
              <div class="input-wrap">
                <span class="input-icon">📱</span>
                <input type="tel" v-model="phone" placeholder="+91 98765 43210" />
              </div>
            </div>

            <!-- Trainer-specific fields -->
            <template v-if="role === 'trainer'">
              <div class="trainer-section-label">Trainer Details</div>

              <div class="input-group full">
                <label>Specialization <span class="required-tag">*</span></label>
                <div class="input-wrap">
                  <span class="input-icon">🌿</span>
                  <input type="text" v-model="specialization" placeholder="e.g. Hatha Yoga, Vinyasa" />
                </div>
              </div>

              <div class="input-group half">
                <label>Years of Experience <span class="required-tag">*</span></label>
                <div class="input-wrap">
                  <span class="input-icon">⏱</span>
                  <input type="number" v-model="experience" placeholder="Years" min="0" max="50" />
                </div>
              </div>

              <div class="input-group half">
                <label>Certifications <span class="optional-tag">(optional)</span></label>
                <div class="input-wrap">
                  <span class="input-icon">🎓</span>
                  <input type="text" v-model="certifications" placeholder="e.g. RYT-200, YAI" />
                </div>
              </div>

              <div class="input-group full">
                <label>Bio <span class="optional-tag">(optional)</span></label>
                <textarea v-model="bio" placeholder="Tell your future clients about yourself..." rows="3"></textarea>
              </div>
            </template>
          </div>

          <div v-if="error" class="form-error"><span>⚠</span> {{ error }}</div>

          <button class="btn-submit" :disabled="loading || !canSubmit" @click="completeProfile">
            <span v-if="!loading">Complete Registration →</span>
            <span v-else class="loading-dots">Creating account<span>.</span><span>.</span><span>.</span></span>
          </button>

          <div class="form-row-actions">
            <button class="btn-ghost" @click="resetToChoose">← Choose a different role</button>
          </div>
        </div>

        <div class="form-footer">
          Already have an account?
          <router-link to="/login" class="form-link">Sign in →</router-link>
        </div>
      </div>
    </div>

    <!-- Right decorative panel -->
    <div class="auth-panel">
      <div class="panel-bg"></div>
      <div class="panel-orb po1"></div>
      <div class="panel-orb po2"></div>
      <div class="panel-orb po3"></div>

      <div class="panel-content">
        <div class="panel-badge">✦ Join SattvaFlow</div>
        <h2 class="panel-title">Find your flow.<br><em>Transform your life.</em></h2>
        <p class="panel-sub">Connect with certified yoga trainers, track your progress, and build a sustainable practice.</p>

        <div class="panel-features">
          <div class="feat-pill" v-for="f in features" :key="f.text">
            <span class="feat-icon">{{ f.icon }}</span>
            {{ f.text }}
          </div>
        </div>

        <div class="panel-visual">
          <div class="vis-ring r1"></div>
          <div class="vis-ring r2"></div>
          <div class="vis-ring r3"></div>
          <div class="vis-center">
            <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" width="80" height="80">
              <circle cx="40" cy="26" r="10" fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
              <line x1="40" y1="36" x2="40" y2="56" stroke="rgba(255,255,255,0.4)" stroke-width="3" stroke-linecap="round"/>
              <path d="M40 42 Q28 35 20 28" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M40 42 Q52 35 60 28" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M40 56 Q30 62 24 68" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M40 56 Q50 62 56 68" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            </svg>
          </div>
        </div>

        <div class="panel-testimonial">
          <div class="panel-stars">★★★★★</div>
          <p class="panel-quote">"SattvaFlow transformed my practice. My trainer understands exactly what I need."</p>
          <div class="panel-author">
            <div class="panel-avatar">P</div>
            <div>
              <div class="panel-author-name">Priya Sharma</div>
              <div class="panel-author-role">Client · Delhi</div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { authApi } from '../api'
import { auth, provider, signInWithGoogle, handleRedirectResult, signInWithRedirect } from '../firebase'

export default {
  name: 'SignupPage',
  data() {
    return {
      step: 'choose',
      role: 'client',
      loading: false,
      error: '',
      isRedirecting: false,
      googleData: {
        google_id: '',
        email: '',
        name: '',
        picture: ''
      },
      phone: '',
      specialization: '',
      experience: '',
      certifications: '',
      bio: '',
      features: [
        { icon: '🧘', text: 'Expert Trainers' },
        { icon: '📅', text: 'Flexible Scheduling' },
        { icon: '📊', text: 'Progress Tracking' },
        { icon: '💬', text: 'Direct Messaging' },
        { icon: '🏆', text: 'Certified Programs' },
        { icon: '🌿', text: 'Holistic Wellness' }
      ]
    }
  },
  computed: {
    canSubmit() {
      if (this.role === 'trainer') {
        return this.specialization.trim() && this.experience !== ''
      }
      return true
    }
  },
  async mounted() {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('userRole')
    if (token && role) {
      this.redirectToDashboard(role)
      return
    }

    // Pre-fill Google data when redirected from login page (new user flow)
    const q = this.$route.query
    if (q.prefill_google_id) {
      this.googleData = {
        google_id: q.prefill_google_id,
        email: q.prefill_email || '',
        name: q.prefill_name || '',
        picture: q.prefill_picture || ''
      }
      this.$router.replace({ path: '/signup' })
      this.step = 'details'
    }

    // Check for redirect return from Google Sign-In
    await this.checkRedirectResult()
  },
  methods: {
    async checkRedirectResult() {
      try {
        const result = await handleRedirectResult()
        if (result) {
          await this.processGoogleSignIn(result)
        }
      } catch (error) {
        console.error('Redirect sign-in error:', error)
        this.error = 'Sign-up failed. Please try again.'
      }
    },

    /**
     * Takes a resolved Firebase popup/redirect result,
     * exchanges the ID token for a SattvaFlow JWT.
     * If the account already exists → save session and redirect.
     * If new user → advance to the profile details step.
     */
    async processGoogleSignIn(result) {
      const idToken = await result.user.getIdToken()

      // FIX: was `api.post(...)` — api has no .post() method.
      // authApi.googleLogin() routes through request() correctly.
      const res = await authApi.googleLogin(idToken)

      if (res.token) {
        // Existing user — log them straight in
        this.saveUserSession(res.token, res.user)
        this.redirectToDashboard(res.user.role)
        return
      }

      if (res.needs_profile) {
        // New user — collect profile details
        this.googleData = res.google_data
        this.step = 'details'
      }
    },

    async handleGoogleSignIn() {
      this.loading = true
      this.error = ''

      try {
        const result = await signInWithGoogle()

        // signInWithGoogle returns { isRedirecting: true } when popup is blocked
        if (result?.isRedirecting) {
          this.isRedirecting = true
          this.loading = false
          return
        }

        await this.processGoogleSignIn(result)

      } catch (err) {
        if (err.code === 'auth/popup-closed-by-user' || err.code === 'auth/cancelled-popup-request') {
          this.error = 'Sign-up cancelled. Please try again.'
        } else if (err.code === 'auth/popup-blocked') {
          this.error = 'Popup was blocked. Redirecting to Google Sign-In page...'
          try {
            await signInWithRedirect(auth, provider)
          } catch (redirectErr) {
            this.error = 'Please allow popups for this site to sign up with Google.'
          }
        } else {
          this.error = err.message || 'Google sign-up failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },

    async completeProfile() {
      this.loading = true
      this.error = ''
      try {
        const payload = {
          google_id: this.googleData.google_id,
          email: this.googleData.email,
          name: this.googleData.name,
          picture: this.googleData.picture,
          role: this.role,
          phone: this.phone || null
        }

        if (this.role === 'trainer') {
          payload.specialization = this.specialization
          payload.experience = parseInt(this.experience) || 0
          payload.certifications = this.certifications
          payload.bio = this.bio
        }

        // FIX: was `api.post(...)` — api has no .post() method.
        // authApi.completeRegistration() routes through request() correctly.
        const res = await authApi.completeRegistration(payload)
        this.saveUserSession(res.token, res.user)
        this.redirectToDashboard(res.user.role)
      } catch (err) {
        this.error = err.message || 'Registration failed. Please try again.'
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
    },

    resetToChoose() {
      this.step = 'choose'
      this.googleData = { google_id: '', email: '', name: '', picture: '' }
      this.error = ''
    }
  }
}
</script>

<style scoped>
/* ── LAYOUT ── */
.signup-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* ── LEFT FORM ── */
.auth-form-wrap {
  display: flex; align-items: center; justify-content: center;
  background: var(--cream); padding: 80px 60px;
  overflow-y: auto;
}
.auth-form-inner { width: 100%; max-width: 440px; }

.form-header { margin-bottom: 36px; }
.form-label {
  font-size: 10px; letter-spacing: 4px; color: var(--sage);
  text-transform: uppercase; display: block; margin-bottom: 12px;
}
.form-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(36px, 4vw, 52px); font-weight: 300;
  color: var(--text-dark); line-height: 1.05; margin-bottom: 10px;
}
.form-title em { font-style: italic; color: var(--sage-dark); }
.form-sub { font-size: 14px; color: var(--text-soft); font-weight: 300; }

/* ── ROLE SELECTOR ── */
.role-selector {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 12px; margin-bottom: 28px;
}
.role-selector button {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; background: white;
  border: 1.5px solid rgba(0,0,0,0.08); border-radius: 4px;
  cursor: pointer; font-family: inherit; transition: all 0.25s ease; text-align: left;
}
.role-selector button:hover { border-color: var(--sage); }
.role-selector button.active {
  border-color: var(--sage); background: rgba(124,154,109,0.05);
  box-shadow: 0 0 0 3px rgba(124,154,109,0.1);
}
.role-icon { font-size: 22px; flex-shrink: 0; }
.role-name { font-size: 13px; font-weight: 500; color: var(--text-dark); }
.role-desc { font-size: 11px; color: var(--text-soft); margin-top: 2px; }

/* ── GOOGLE SECTION ── */
.google-section { display: flex; flex-direction: column; gap: 20px; }
.btn-google {
  width: 100%; padding: 15px 20px; background: white;
  border: 1.5px solid rgba(0,0,0,0.12); border-radius: 2px;
  cursor: pointer; font-family: inherit; font-size: 15px; font-weight: 500;
  color: var(--text-dark); transition: all 0.25s ease;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06); min-height: 52px;
}
.btn-google:hover:not(:disabled) {
  border-color: var(--sage); box-shadow: 0 4px 20px rgba(47,79,79,0.12);
  transform: translateY(-1px);
}
.btn-google:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }
.btn-google-inner { display: flex; align-items: center; justify-content: center; gap: 12px; }
.google-icon { width: 20px; height: 20px; flex-shrink: 0; }

.google-info {
  display: flex; align-items: center; gap: 8px; padding: 12px 16px;
  background: rgba(124,154,109,0.05); border: 1px solid rgba(124,154,109,0.12);
  border-radius: 4px; font-size: 12px; color: var(--text-mid); line-height: 1.5;
}
.info-icon { font-size: 14px; flex-shrink: 0; }

/* ── GOOGLE CONFIRMED ── */
.google-confirmed {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; margin-bottom: 20px;
  background: rgba(124,154,109,0.06);
  border: 1px solid rgba(124,154,109,0.2); border-radius: 8px;
}
.g-avatar {
  width: 40px; height: 40px; border-radius: 50%; object-fit: cover;
  border: 2px solid rgba(124,154,109,0.25);
}
.g-avatar-fallback {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 18px;
  font-family: 'Cormorant Garamond', Georgia, serif; flex-shrink: 0;
}
.g-confirmed-text { flex: 1; min-width: 0; }
.g-confirmed-name { font-size: 14px; font-weight: 500; color: var(--text-dark); }
.g-confirmed-email { font-size: 11px; color: var(--text-soft); margin-top: 2px; }
.g-confirmed-tick { font-size: 16px; color: var(--sage); font-weight: 700; flex-shrink: 0; }

/* ── PROFILE FORM ── */
.form-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 16px; margin-bottom: 24px;
}
.input-group { display: flex; flex-direction: column; }
.input-group.full { grid-column: 1 / -1; }
.input-group.half { grid-column: span 1; }
.input-group label {
  display: block; margin-bottom: 7px;
  font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--text-mid); font-weight: 500;
}
.optional-tag { font-size: 10px; color: var(--text-soft); text-transform: none; letter-spacing: 0; }
.required-tag { color: #c44; }

.input-wrap { position: relative; }
.input-icon {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  font-size: 15px; pointer-events: none;
}
.input-wrap input {
  width: 100%; padding: 13px 14px 13px 40px;
  border: 1px solid rgba(0,0,0,0.1); border-radius: 2px;
  background: white; font-size: 14px; color: var(--text-dark);
  font-family: inherit; transition: all 0.3s; box-sizing: border-box;
}
.input-wrap input:focus {
  outline: none; border-color: var(--sage);
  box-shadow: 0 0 0 3px rgba(124,154,109,0.1);
}
textarea {
  width: 100%; padding: 12px 14px;
  border: 1px solid rgba(0,0,0,0.1); border-radius: 2px;
  background: white; font-size: 14px; color: var(--text-dark);
  font-family: inherit; transition: all 0.3s; resize: vertical; min-height: 80px;
  box-sizing: border-box;
}
textarea:focus {
  outline: none; border-color: var(--sage);
  box-shadow: 0 0 0 3px rgba(124,154,109,0.1);
}
.trainer-section-label {
  grid-column: 1 / -1; font-size: 10px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--sage); padding: 8px 0 4px;
  border-top: 1px solid rgba(0,0,0,0.06);
}

/* ── ROLE CONFIRM ── */
.role-confirm {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 14px; background: rgba(47,79,79,0.04);
  border-radius: 4px; font-size: 12px; color: var(--text-mid); margin-bottom: 20px;
}
.role-confirm-icon { font-size: 18px; }
.role-note { color: var(--text-soft); font-style: italic; }

/* ── SUBMIT ── */
.btn-submit {
  width: 100%; padding: 16px; background: var(--deep); color: white; border: none;
  font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  font-family: inherit; cursor: pointer; transition: all 0.4s ease;
  border-radius: 2px; position: relative; overflow: hidden; margin-top: 4px;
}
.btn-submit::before {
  content: ''; position: absolute; inset: 0;
  background: var(--sage); transform: translateX(-101%); transition: transform 0.4s ease;
}
.btn-submit:hover::before { transform: translateX(0); }
.btn-submit span { position: relative; z-index: 1; }
.btn-submit:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(47,79,79,0.25); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.btn-submit:disabled::before { display: none; }

/* ── GHOST ── */
.form-row-actions { display: flex; justify-content: flex-start; margin-top: 16px; }
.btn-ghost {
  background: none; border: none; cursor: pointer;
  font-size: 12px; color: var(--text-soft); font-family: inherit; padding: 0;
  transition: color 0.2s;
}
.btn-ghost:hover { color: var(--sage); }

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
  margin-top: 28px; padding-top: 20px;
  border-top: 1px solid rgba(0,0,0,0.06);
  font-size: 13px; color: var(--text-soft); text-align: center;
}
.form-link { color: var(--sage); text-decoration: none; margin-left: 4px; font-weight: 500; }
.form-link:hover { color: var(--sage-dark); }
.form-footer-note {
  margin-top: 12px; text-align: center;
  font-size: 11px; letter-spacing: 1.5px; color: var(--text-soft);
  display: flex; align-items: center; justify-content: center; gap: 6px;
}

/* ── RIGHT PANEL ── */
.auth-panel {
  position: relative; background: var(--deep);
  overflow: hidden; display: flex; align-items: center; justify-content: center;
  padding: 80px 60px;
}
.panel-bg {
  position: absolute; inset: 0;
  background: linear-gradient(160deg, #1a3030 0%, #2F4F4F 50%, #3a5a3a 100%);
}
.panel-orb { position: absolute; border-radius: 50%; filter: blur(60px); pointer-events: none; }
.po1 { width: 350px; height: 350px; background: rgba(124,154,109,0.2); top: -80px; left: -80px; }
.po2 { width: 250px; height: 250px; background: rgba(201,168,76,0.1); bottom: 80px; right: -60px; }
.po3 { width: 150px; height: 150px; background: rgba(255,255,255,0.04); top: 50%; left: 50%; }

.panel-content { position: relative; z-index: 1; display: flex; flex-direction: column; gap: 28px; width: 100%; }
.panel-badge {
  display: inline-block; font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--gold); border: 1px solid rgba(201,168,76,0.25); border-radius: 20px;
  padding: 5px 14px; width: fit-content;
}
.panel-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(30px, 3.5vw, 46px); font-weight: 300; color: white; line-height: 1.15;
}
.panel-title em { font-style: italic; color: var(--gold); }
.panel-sub { font-size: 13px; color: rgba(255,255,255,0.4); font-weight: 300; line-height: 1.8; }

.panel-features { display: flex; flex-wrap: wrap; gap: 10px; }
.feat-pill {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 7px 14px; font-size: 12px; color: rgba(255,255,255,0.5);
}
.feat-icon { font-size: 13px; }

.panel-visual {
  position: relative; display: flex; align-items: center; justify-content: center; height: 200px;
}
.vis-ring { position: absolute; border-radius: 50%; border: 1px solid rgba(255,255,255,0.06); }
.r1 { width: 180px; height: 180px; animation: ringR 20s linear infinite; }
.r2 { width: 140px; height: 140px; border-style: dashed; animation: ringR 30s linear infinite reverse; }
.r3 { width: 100px; height: 100px; animation: ringR 15s linear infinite 2s; }
@keyframes ringR { to { transform: rotate(360deg); } }
.vis-center { position: absolute; opacity: 0.7; }

.panel-testimonial {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 4px; padding: 24px;
}
.panel-stars { color: var(--gold); font-size: 13px; letter-spacing: 3px; margin-bottom: 12px; }
.panel-quote {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 16px; font-weight: 300; line-height: 1.7;
  color: rgba(255,255,255,0.65); font-style: italic; margin-bottom: 20px;
}
.panel-author { display: flex; align-items: center; gap: 12px; }
.panel-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 14px;
}
.panel-author-name { font-size: 13px; font-weight: 500; color: white; }
.panel-author-role { font-size: 11px; color: rgba(255,255,255,0.35); }

/* ── RESPONSIVE ── */
@media (max-width: 1000px) {
  .signup-page { grid-template-columns: 1fr; }
  .auth-panel { display: none; }
  .auth-form-wrap { padding: 100px 32px 60px; }
}
@media (max-width: 480px) {
  .auth-form-wrap { padding: 80px 20px 40px; }
  .role-selector { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .input-group.half { grid-column: 1 / -1; }
}
</style>