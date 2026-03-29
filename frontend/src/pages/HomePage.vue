<template>
  <div class="home-page">

    <!-- Custom Cursor -->
    <div class="cursor" ref="cursor"></div>
    <div class="cursor-trail" ref="cursorTrail"></div>

    <!-- Particle Canvas -->
    <canvas ref="particleCanvas" class="particles-canvas"></canvas>

    <!-- Page Loader -->
    <div class="sf-loader" ref="loader">
      <svg class="loader-lotus" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="44" stroke="rgba(124,154,109,0.3)" stroke-width="1"/>
        <path d="M50 75 Q38 65 34 55 Q38 50 50 48 Q62 50 66 55 Q62 65 50 75Z" fill="rgba(201,168,76,0.6)"/>
        <path d="M50 75 Q28 62 24 48 Q34 44 50 48Z" fill="rgba(124,154,109,0.5)"/>
        <path d="M50 75 Q72 62 76 48 Q66 44 50 48Z" fill="rgba(124,154,109,0.5)"/>
        <path d="M50 75 Q40 55 38 40 Q44 36 50 34 Q56 36 62 40 Q60 55 50 75Z" fill="rgba(201,168,76,0.4)"/>
        <circle cx="50" cy="48" r="6" fill="#c9a84c" opacity="0.8"/>
      </svg>
      <div class="loader-text">SATTVAFLOW</div>
      <div class="loader-bar"><div class="loader-bar-fill"></div></div>
    </div>

    <!-- ── HERO ── -->
    <section id="hero">
      <div class="hero-bg"></div>
      <div class="hero-orb orb1"></div>
      <div class="hero-orb orb2"></div>
      <div class="hero-orb orb3"></div>

      <div class="hero-content">
        
        <h1 class="hero-title">
          Flow Into<br><em>Your Best</em><br><span class="gold">Self</span>
        </h1>
        <p class="hero-subtitle">
          A premium yoga management platform. Connect with expert trainers, follow personalised sessions, and track your transformation — all in one sacred space.
        </p>
        <div class="hero-actions">
          <a href="#cta" class="btn-primary">
            <span>Begin Your Journey</span>
            <span>→</span>
          </a>
          <a href="#how" class="btn-secondary">
            See How It Works <span class="btn-arrow">→</span>
          </a>
        </div>
      </div>

      <!-- Right Visual -->
      <div class="hero-visual">
        <div class="hero-circle-wrap">
          <div class="hero-circle-bg"></div>
          <div class="hero-circle-ring"></div>
          <div class="hero-circle-ring2"></div>
          <div class="hero-yoga-svg">
            <svg viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="140" cy="140" r="100" stroke="rgba(124,154,109,0.1)" stroke-width="1"/>
              <circle cx="140" cy="140" r="80" stroke="rgba(201,168,76,0.08)" stroke-width="1" stroke-dasharray="4 8"/>
              <ellipse cx="140" cy="185" rx="35" ry="8" fill="rgba(201,168,76,0.15)"/>
              <path d="M140 178 Q122 168 118 155 Q126 152 140 155 Q154 152 162 155 Q158 168 140 178Z" fill="#c9a84c" opacity="0.7"/>
              <path d="M140 178 Q108 162 102 144 Q118 142 140 155Z" fill="#c9a84c" opacity="0.4"/>
              <path d="M140 178 Q172 162 178 144 Q162 142 140 155Z" fill="#c9a84c" opacity="0.4"/>
              <path d="M140 178 Q128 158 126 140 Q132 137 140 136 Q148 137 154 140 Q152 158 140 178Z" fill="#c9a84c" opacity="0.35"/>
              <circle cx="140" cy="92" r="16" fill="rgba(124,154,109,0.8)"/>
              <circle cx="140" cy="92" r="16" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
              <line x1="140" y1="108" x2="140" y2="148" stroke="rgba(47,79,79,0.7)" stroke-width="5" stroke-linecap="round"/>
              <path d="M140 118 Q120 108 106 100" stroke="rgba(47,79,79,0.6)" stroke-width="4" stroke-linecap="round" fill="none"/>
              <path d="M140 118 Q160 108 174 100" stroke="rgba(47,79,79,0.6)" stroke-width="4" stroke-linecap="round" fill="none"/>
              <circle cx="104" cy="99" r="4" fill="rgba(201,168,76,0.6)"/>
              <circle cx="176" cy="99" r="4" fill="rgba(201,168,76,0.6)"/>
              <path d="M140 148 Q122 158 110 168" stroke="rgba(47,79,79,0.6)" stroke-width="4" stroke-linecap="round" fill="none"/>
              <path d="M140 148 Q158 158 170 168" stroke="rgba(47,79,79,0.6)" stroke-width="4" stroke-linecap="round" fill="none"/>
              <circle cx="140" cy="92" r="26" fill="none" stroke="rgba(124,154,109,0.2)" stroke-width="1">
                <animate attributeName="r" values="26;34;26" dur="3s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.3;0;0.3" dur="3s" repeatCount="indefinite"/>
              </circle>
              <circle cx="140" cy="92" r="22" fill="none" stroke="rgba(201,168,76,0.2)" stroke-width="1">
                <animate attributeName="r" values="22;30;22" dur="3s" begin="1s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.3;0;0.3" dur="3s" begin="1s" repeatCount="indefinite"/>
              </circle>
              <circle cx="90" cy="120" r="2" fill="rgba(201,168,76,0.6)"><animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/></circle>
              <circle cx="192" cy="115" r="1.5" fill="rgba(201,168,76,0.5)"><animate attributeName="opacity" values="0;1;0" dur="2.5s" begin="0.5s" repeatCount="indefinite"/></circle>
              <circle cx="115" cy="175" r="2" fill="rgba(124,154,109,0.7)"><animate attributeName="opacity" values="0;1;0" dur="1.8s" begin="1s" repeatCount="indefinite"/></circle>
              <circle cx="165" cy="172" r="1.5" fill="rgba(124,154,109,0.5)"><animate attributeName="opacity" values="0;1;0" dur="2.2s" begin="0.3s" repeatCount="indefinite"/></circle>
            </svg>
          </div>
          <div class="hero-float-tag t1">
            <div class="dot green"></div>
            <div>
              <div style="font-size:11px;font-weight:600;color:#1a2e1a">128 Active Sessions</div>
              <div style="font-size:10px;color:#7a8c7a">Right now</div>
            </div>
          </div>
          <div class="hero-float-tag t2">
            <div class="dot gold"></div>
            <div>
              <div style="font-size:11px;font-weight:600;color:#1a2e1a">OTP Login</div>
              <div style="font-size:10px;color:#7a8c7a">Passwordless security</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div class="hero-stats">
        <div class="stat-item">
          <div class="stat-num" ref="statClients">0</div>
          <div class="stat-label">Happy Clients</div>
        </div>
        <div class="stat-item">
          <div class="stat-num" ref="statTrainers">0</div>
          <div class="stat-label">Expert Trainers</div>
        </div>
        <div class="stat-item">
          <div class="stat-num" ref="statSessions">0</div>
          <div class="stat-label">Sessions Done</div>
        </div>
      </div>

      <div class="scroll-hint">
        <div class="scroll-line"></div>
        <span class="scroll-text">Scroll</span>
      </div>
    </section>

    <!-- ── FEATURES ── -->
    <section id="features">
      <div class="section-inner">
        <div class="reveal">
          <span class="section-label">✦ Platform Features</span>
          <h2 class="section-title">Everything You Need to<br><em>Thrive &amp; Grow</em></h2>
        </div>
        <div class="features-grid">
          <div class="feature-card reveal stagger-1">
            <div class="feature-num">01</div>
            <div class="feature-icon">🔐</div>
            <div class="feature-title">OTP-Based Login</div>
            <div class="feature-desc">No passwords, no hassle. Secure WhatsApp &amp; email OTP authentication for every user — trainers, clients, and admin alike.</div>
          </div>
          <div class="feature-card reveal stagger-2">
            <div class="feature-num">02</div>
            <div class="feature-icon">🧘</div>
            <div class="feature-title">Personalized Sessions</div>
            <div class="feature-desc">Each client gets custom yoga plans from their assigned trainer. Daily sessions tailored to body type, goals, and progress.</div>
          </div>
          <div class="feature-card reveal stagger-3">
            <div class="feature-num">03</div>
            <div class="feature-icon">📊</div>
            <div class="feature-title">Progress Analytics</div>
            <div class="feature-desc">Visual progress charts, attendance tracking, and performance metrics help clients and trainers see real transformation.</div>
          </div>
          <div class="feature-card reveal stagger-4">
            <div class="feature-num">04</div>
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Privacy-First Design</div>
            <div class="feature-desc">Strict role-based access control. Clients only see their trainer. Trainers only see assigned clients. Admin sees everything.</div>
          </div>
          <div class="feature-card reveal stagger-5">
            <div class="feature-num">05</div>
            <div class="feature-icon">💬</div>
            <div class="feature-title">Query &amp; Review System</div>
            <div class="feature-desc">Seamless communication channels. Clients rate trainers, send queries to admin, and get WhatsApp/email notifications instantly.</div>
          </div>
          <div class="feature-card reveal stagger-6">
            <div class="feature-num">06</div>
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Admin Super Control</div>
            <div class="feature-desc">One admin to rule them all. Approve trainers, assign clients, edit homepage, manage pricing — all from a beautiful dashboard.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── HOW IT WORKS ── -->
    <section id="how">
      <div class="how-bg-text">SATTVĀFLOW</div>
      <div class="section-inner">
        <div class="reveal">
          <span class="section-label">✦ Simple Process</span>
          <h2 class="section-title">Your Journey<br><em>in 4 Steps</em></h2>
        </div>
        <div class="how-grid">
          <div class="how-steps">
            <div class="how-step active reveal stagger-1">
              <div class="step-num">01</div>
              <div class="step-content">
                <div class="step-title">Sign Up with WhatsApp OTP</div>
                <div class="step-desc">Enter your WhatsApp number during signup. Receive an instant OTP. Verify and you're in — no password ever needed.</div>
              </div>
            </div>
            <div class="how-step reveal stagger-2">
              <div class="step-num">02</div>
              <div class="step-content">
                <div class="step-title">Admin Assigns Your Trainer</div>
                <div class="step-desc">After registration, our admin reviews and matches you with the perfect trainer based on your goals and preferences.</div>
              </div>
            </div>
            <div class="how-step reveal stagger-3">
              <div class="step-num">03</div>
              <div class="step-content">
                <div class="step-title">Start Your Yoga Sessions</div>
                <div class="step-desc">Access your personalized yoga plans, daily sessions, and track every milestone. Your trainer updates your progress in real-time.</div>
              </div>
            </div>
            <div class="how-step reveal stagger-4">
              <div class="step-num">04</div>
              <div class="step-content">
                <div class="step-title">Transform &amp; Get Notified</div>
                <div class="step-desc">Receive WhatsApp &amp; email notifications for sessions, reminders, and announcements. Never miss a flow.</div>
              </div>
            </div>
          </div>
          <div class="how-visual reveal-right">
            <div class="how-phone">
              <div class="phone-notch"></div>
              <div class="phone-screen">
                <div style="font-size:10px;letter-spacing:3px;color:rgba(255,255,255,0.3);margin-bottom:16px;text-transform:uppercase;">SattvaFlow</div>
                <div class="phone-card">
                  <div class="phone-card-label">Today's Session</div>
                  <div class="phone-card-text">Morning Vinyasa Flow · 7:00 AM</div>
                </div>
                <div class="phone-card">
                  <div class="phone-card-label">Your Trainer</div>
                  <div class="phone-card-text">Priya Sharma · Hatha Specialist</div>
                </div>
                <div class="phone-card">
                  <div class="phone-card-label">Progress</div>
                  <div class="phone-card-text">Week 3 · 12 sessions completed ✦</div>
                </div>
                <div style="margin-top:20px;font-size:10px;letter-spacing:2px;color:rgba(255,255,255,0.25);text-transform:uppercase;text-align:center;">Enter OTP</div>
                <div class="phone-otp">
                  <div class="otp-box">3</div>
                  <div class="otp-box">7</div>
                  <div class="otp-box">8</div>
                  <div class="otp-box">1</div>
                  <div class="otp-box">2</div>
                  <div class="otp-box">4</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── TRAINERS ── -->
    <section id="trainers">
      <div class="section-inner">
        <div class="trainers-header reveal">
          <div>
            <span class="section-label">✦ Our Experts</span>
            <h2 class="section-title">Meet Your<br><em>Guides</em></h2>
          </div>
          <a href="#cta" class="btn-secondary" style="color:var(--text-dark)">All Trainers <span class="btn-arrow">→</span></a>
        </div>
        <div class="trainers-grid">
          <div class="trainer-card reveal stagger-1">
            <div class="trainer-img" style="background:linear-gradient(135deg,#7C9A6D,#2F4F4F)">
              <div class="trainer-img-inner">🧘‍♀️</div>
              <div class="trainer-badge">Top Rated</div>
            </div>
            <div class="trainer-info">
              <div class="trainer-name">Priya Sharma</div>
              <div class="trainer-spec">Hatha &amp; Vinyasa</div>
              <div class="trainer-stats">
                <div class="trainer-stat"><div class="trainer-stat-num">4.9</div><div class="trainer-stat-label">Rating</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">148</div><div class="trainer-stat-label">Clients</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">6yr</div><div class="trainer-stat-label">Exp.</div></div>
              </div>
            </div>
          </div>
          <div class="trainer-card reveal stagger-2">
            <div class="trainer-img" style="background:linear-gradient(135deg,#4a6640,#7C9A6D)">
              <div class="trainer-img-inner">🧘</div>
            </div>
            <div class="trainer-info">
              <div class="trainer-name">Arjun Mehta</div>
              <div class="trainer-spec">Ashtanga &amp; Power</div>
              <div class="trainer-stats">
                <div class="trainer-stat"><div class="trainer-stat-num">4.8</div><div class="trainer-stat-label">Rating</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">112</div><div class="trainer-stat-label">Clients</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">8yr</div><div class="trainer-stat-label">Exp.</div></div>
              </div>
            </div>
          </div>
          <div class="trainer-card reveal stagger-3">
            <div class="trainer-img" style="background:linear-gradient(135deg,#c9a84c,#4a6640)">
              <div class="trainer-img-inner">🌿</div>
              <div class="trainer-badge">New</div>
            </div>
            <div class="trainer-info">
              <div class="trainer-name">Meera Nair</div>
              <div class="trainer-spec">Yin &amp; Restorative</div>
              <div class="trainer-stats">
                <div class="trainer-stat"><div class="trainer-stat-num">4.9</div><div class="trainer-stat-label">Rating</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">76</div><div class="trainer-stat-label">Clients</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">4yr</div><div class="trainer-stat-label">Exp.</div></div>
              </div>
            </div>
          </div>
          <div class="trainer-card reveal stagger-4">
            <div class="trainer-img" style="background:linear-gradient(135deg,#2F4F4F,#c9a84c)">
              <div class="trainer-img-inner">🌸</div>
            </div>
            <div class="trainer-info">
              <div class="trainer-name">Kavya Reddy</div>
              <div class="trainer-spec">Prenatal &amp; Gentle</div>
              <div class="trainer-stats">
                <div class="trainer-stat"><div class="trainer-stat-num">5.0</div><div class="trainer-stat-label">Rating</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">94</div><div class="trainer-stat-label">Clients</div></div>
                <div class="trainer-stat"><div class="trainer-stat-num">5yr</div><div class="trainer-stat-label">Exp.</div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── PRICING ── -->
    <section id="pricing">
      <div class="section-inner">
        <div class="reveal" style="text-align:center;max-width:500px;margin:0 auto">
          <span class="section-label">✦ Transparent Pricing</span>
          <h2 class="section-title">Simple Plans,<br><em>Profound Results</em></h2>
        </div>
        <div class="pricing-grid">
          <div class="pricing-card reveal stagger-1">
            <span class="pricing-plan">Seeker</span>
            <div class="pricing-price">₹999<span style="font-size:20px;color:var(--text-soft)">/mo</span></div>
            <div class="pricing-period">Perfect for beginners</div>
            <ul class="pricing-features">
              <li>1 Assigned Trainer</li>
              <li>8 Sessions per Month</li>
              <li>Progress Tracking</li>
              <li>WhatsApp Notifications</li>
              <li>OTP Secure Login</li>
            </ul>
            <a href="#cta" class="pricing-btn">Get Started</a>
          </div>
          <div class="pricing-card featured reveal stagger-2">
            <div class="pricing-tag">Most Popular</div>
            <span class="pricing-plan">Practitioner</span>
            <div class="pricing-price" style="color:white">₹1,999<span style="font-size:20px;color:rgba(255,255,255,0.4)">/mo</span></div>
            <div class="pricing-period">For serious yogis</div>
            <ul class="pricing-features">
              <li>1 Dedicated Trainer</li>
              <li>20 Sessions per Month</li>
              <li>Custom Yoga Plans</li>
              <li>Progress Analytics Charts</li>
              <li>Session Scheduling</li>
              <li>Priority Support</li>
            </ul>
            <a href="#cta" class="pricing-btn">Begin Journey</a>
          </div>
          <div class="pricing-card reveal stagger-3">
            <span class="pricing-plan">Master</span>
            <div class="pricing-price">₹3,499<span style="font-size:20px;color:var(--text-soft)">/mo</span></div>
            <div class="pricing-period">Unlimited transformation</div>
            <ul class="pricing-features">
              <li>2 Dedicated Trainers</li>
              <li>Unlimited Sessions</li>
              <li>AI Yoga Recommendations</li>
              <li>Video Session Integration</li>
              <li>Full Analytics + Reports</li>
              <li>Exclusive Content Library</li>
            </ul>
            <a href="#cta" class="pricing-btn">Go Master</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ── REVIEWS ── -->
    <section id="reviews">
      <div class="section-inner">
        <div class="reveal" style="text-align:center;max-width:400px;margin:0 auto">
          <span class="section-label">✦ Testimonials</span>
          <h2 class="section-title">Voices of<br><em>Transformation</em></h2>
        </div>
      </div>
      <div class="reviews-track-wrap">
        <div class="reviews-track">
          <div class="review-card" v-for="(r, i) in reviewsDouble" :key="i">
            <div class="review-stars">{{ r.stars }}</div>
            <div class="review-text">"{{ r.text }}"</div>
            <div class="review-author">
              <div class="review-avatar">{{ r.initial }}</div>
              <div>
                <div class="review-name">{{ r.name }}</div>
                <div class="review-role">{{ r.role }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ── -->
    <section id="cta">
      <svg class="cta-bg-lotus" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="200" cy="200" r="180" stroke="white" stroke-width="1"/>
        <path d="M200 360 Q140 300 120 240 Q160 220 200 220 Q240 220 280 240 Q260 300 200 360Z" fill="white"/>
        <path d="M200 360 Q80 280 60 200 Q120 180 200 220Z" fill="white" opacity="0.5"/>
        <path d="M200 360 Q320 280 340 200 Q280 180 200 220Z" fill="white" opacity="0.5"/>
        <path d="M200 220 Q180 160 180 100 Q190 90 200 88 Q210 90 220 100 Q220 160 200 220Z" fill="white" opacity="0.3"/>
      </svg>
      <div class="section-inner">
        <div class="cta-content reveal">
          <h2 class="cta-title">Ready to <em>Find<br>Your Flow?</em></h2>
          <p class="cta-sub">Join thousands of yogis transforming their lives with SattvaFlow.<br>No passwords. No complexity. Just pure practice.</p>
          <div class="cta-actions">
            <a href="/signup" class="btn-gold" @click.prevent="$router.push('/signup')">
              <span>Start Free Trial</span>
              <span>→</span>
            </a>
            <a href="#features" class="btn-outline-white">Explore Platform</a>
          </div>
          <div class="cta-trust">
            <div class="cta-trust-item"><span class="cta-check">✓</span> No credit card required</div>
            <div class="cta-trust-item"><span class="cta-check">✓</span> WhatsApp OTP login</div>
            <div class="cta-trust-item"><span class="cta-check">✓</span> Cancel anytime</div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  name: 'HomePage',

  data() {
    return {
      _rafCursor: null,
      _rafParticles: null,
      _mx: 0, _my: 0, _tx: 0, _ty: 0,
      _particles: [],
      _revealObserver: null,
      _statsObserver: null,
      _statsDone: false,
      reviews: [
        { stars: '★★★★★', text: 'SattvaFlow completely changed my mornings. My trainer Priya understands my body better than I do. Three months in and I\'ve never felt more alive.', initial: 'A', name: 'Ananya Singh', role: 'Client · Delhi' },
        { stars: '★★★★★', text: 'The OTP login is so smooth. No passwords to remember, just one tap on WhatsApp and I\'m in. The privacy design makes me feel totally safe.', initial: 'R', name: 'Rohit Verma', role: 'Client · Mumbai' },
        { stars: '★★★★★', text: 'As a trainer, the dashboard is my command center. I can track all my clients\' progress, send session reminders, and communicate directly — all in one place.', initial: 'P', name: 'Priya Sharma', role: 'Trainer · Certified Instructor' },
        { stars: '★★★★☆', text: 'I was skeptical at first, but the admin matched me with the perfect trainer for prenatal yoga. The session reminders on WhatsApp are a lifesaver.', initial: 'S', name: 'Sunita Kapoor', role: 'Client · Bengaluru' },
        { stars: '★★★★★', text: 'The progress charts blow my mind every week. Watching my flexibility scores go up is incredibly motivating. SattvaFlow made yoga a habit I love.', initial: 'K', name: 'Karan Patel', role: 'Client · Ahmedabad' },
      ]
    }
  },

  computed: {
    reviewsDouble() {
      return [...this.reviews, ...this.reviews]
    }
  },

  mounted() {
    // Cursor: none on body while on this page
    document.body.style.cursor = 'none'

    // Loader
    this._loaderTimeout = setTimeout(() => {
      if (this.$refs.loader) this.$refs.loader.classList.add('hide')
    }, 2600)

    // Init sub-systems
    this._initCursor()
    this._initParticles()
    this._initScrollReveal()
    this._initCounters()

    window.addEventListener('scroll', this._onScroll)
  },

  beforeUnmount() {
    document.body.style.cursor = ''
    clearTimeout(this._loaderTimeout)
    window.removeEventListener('scroll', this._onScroll)
    if (this._rafCursor) cancelAnimationFrame(this._rafCursor)
    if (this._rafParticles) cancelAnimationFrame(this._rafParticles)
    if (this._revealObserver) this._revealObserver.disconnect()
    if (this._statsObserver) this._statsObserver.disconnect()
    document.removeEventListener('mousemove', this._onMouseMove)
  },

  methods: {
    // ── CURSOR ──
    _initCursor() {
      this._onMouseMove = (e) => {
        this._mx = e.clientX
        this._my = e.clientY
        const c = this.$refs.cursor
        if (c) { c.style.left = this._mx - 6 + 'px'; c.style.top = this._my - 6 + 'px' }
      }
      document.addEventListener('mousemove', this._onMouseMove)

      const animTrail = () => {
        this._tx += (this._mx - this._tx) * 0.12
        this._ty += (this._my - this._ty) * 0.12
        const t = this.$refs.cursorTrail
        if (t) { t.style.left = this._tx - 18 + 'px'; t.style.top = this._ty - 18 + 'px' }
        this._rafCursor = requestAnimationFrame(animTrail)
      }
      animTrail()

      this.$nextTick(() => {
        document.querySelectorAll('a, button, .feature-card, .trainer-card, .pricing-card').forEach(el => {
          el.addEventListener('mouseenter', () => {
            const c = this.$refs.cursor; const t = this.$refs.cursorTrail
            if (c) c.style.transform = 'scale(2.5)'
            if (t) t.style.transform = 'scale(1.4)'
          })
          el.addEventListener('mouseleave', () => {
            const c = this.$refs.cursor; const t = this.$refs.cursorTrail
            if (c) c.style.transform = 'scale(1)'
            if (t) t.style.transform = 'scale(1)'
          })
        })
      })
    },

    // ── PARTICLES ──
    _initParticles() {
      const canvas = this.$refs.particleCanvas
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight }
      resize()
      window.addEventListener('resize', resize)

      this._particles = Array.from({ length: 55 }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2 + 0.5,
        vx: (Math.random() - 0.5) * 0.3,
        vy: -Math.random() * 0.4 - 0.1,
        opacity: Math.random() * 0.5 + 0.1,
        color: Math.random() > 0.5 ? '124,154,109' : '201,168,76'
      }))

      const draw = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        this._particles.forEach(p => {
          ctx.beginPath()
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(${p.color},${p.opacity})`
          ctx.fill()
          p.x += p.vx; p.y += p.vy
          if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width }
          if (p.x < -10) p.x = canvas.width + 10
          if (p.x > canvas.width + 10) p.x = -10
        })
        this._rafParticles = requestAnimationFrame(draw)
      }
      draw()
    },

    // ── SCROLL REVEAL ──
    _initScrollReveal() {
      this._revealObserver = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible') })
      }, { threshold: 0.12 })

      this.$nextTick(() => {
        document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
          this._revealObserver.observe(el)
        })
      })
    },

    // ── COUNTERS ──
    _initCounters() {
      const countUp = (el, target, suffix = '') => {
        let start = 0
        const step = target / 60
        const timer = setInterval(() => {
          start += step
          if (start >= target) { el.textContent = target + suffix; clearInterval(timer) }
          else el.textContent = Math.floor(start) + suffix
        }, 25)
      }

      this._statsObserver = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting && !this._statsDone) {
            this._statsDone = true
            if (this.$refs.statClients) countUp(this.$refs.statClients, 2400, '+')
            if (this.$refs.statTrainers) countUp(this.$refs.statTrainers, 48, '+')
            if (this.$refs.statSessions) countUp(this.$refs.statSessions, 18000, '+')
          }
        })
      }, { threshold: 0.5 })

      this.$nextTick(() => {
        const hero = document.getElementById('hero')
        if (hero) this._statsObserver.observe(hero)
      })
    },

    // ── SCROLL / PARALLAX ──
    _onScroll() {
      const scrollY = window.scrollY
      document.querySelectorAll('.hero-orb').forEach((orb, i) => {
        orb.style.transform = `translateY(${scrollY * (0.1 + i * 0.05)}px)`
      })
    }
  }
}
</script>

<style scoped>
/* ── CURSOR ── */
.cursor {
  position: fixed; width: 12px; height: 12px;
  background: var(--sage); border-radius: 50%;
  pointer-events: none; z-index: 9999;
  transition: transform 0.15s ease, opacity 0.15s;
  mix-blend-mode: multiply;
}
.cursor-trail {
  position: fixed; width: 36px; height: 36px;
  border: 1.5px solid var(--sage); border-radius: 50%;
  pointer-events: none; z-index: 9998;
  transition: transform 0.35s ease;
  opacity: 0.5;
}

/* ── PARTICLES ── */
.particles-canvas {
  position: fixed; inset: 0;
  pointer-events: none; z-index: 0; opacity: 0.4;
}

/* ── LOADER ── */
.sf-loader {
  position: fixed; inset: 0; z-index: 10000;
  background: var(--deep);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  transition: opacity 0.8s ease, visibility 0.8s ease;
}
.sf-loader.hide { opacity: 0; visibility: hidden; pointer-events: none; }
.loader-lotus {
  width: 80px; height: 80px;
  animation: loaderSpin 2s linear infinite, loaderPulse 1s ease-in-out infinite alternate;
}
@keyframes loaderSpin { to { transform: rotate(360deg); } }
@keyframes loaderPulse { from { opacity: 0.5; } to { opacity: 1; } }
.loader-text {
  margin-top: 24px; color: var(--beige);
  font-family: 'Cinzel', 'Georgia', serif; font-size: 11px;
  letter-spacing: 6px; opacity: 0.7;
  animation: loaderFade 1.5s ease-in-out infinite alternate;
}
@keyframes loaderFade { from { opacity: 0.3; } to { opacity: 0.8; } }
.loader-bar {
  margin-top: 20px; width: 160px; height: 1px;
  background: rgba(255,255,255,0.1); border-radius: 1px; overflow: hidden;
}
.loader-bar-fill {
  height: 100%; background: var(--gold);
  animation: loaderBar 2.5s ease forwards;
}
@keyframes loaderBar { from { width: 0; } to { width: 100%; } }

/* ── HOME PAGE ── */
.home-page { position: relative; overflow-x: hidden; }

/* ── HERO ── */
#hero {
  position: relative; min-height: 100vh;
  display: flex; align-items: center; overflow: hidden;
}
.hero-bg {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 70% 40%, rgba(124,154,109,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 50% at 20% 80%, rgba(201,168,76,0.06) 0%, transparent 50%),
    linear-gradient(160deg, #FAFAF5 0%, #F0EDE2 50%, #E8F0E4 100%);
}
.hero-orb {
  position: absolute; border-radius: 50%;
  filter: blur(60px); pointer-events: none;
}
.orb1 { width: 500px; height: 500px; background: rgba(124,154,109,0.15); top: -100px; right: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb2 { width: 300px; height: 300px; background: rgba(201,168,76,0.1); bottom: 100px; left: -50px; animation: orbFloat 10s ease-in-out infinite reverse; }
.orb3 { width: 200px; height: 200px; background: rgba(47,79,79,0.08); top: 50%; left: 40%; animation: orbFloat 6s ease-in-out infinite 2s; }
@keyframes orbFloat { 0%,100% { transform: translate(0,0) scale(1); } 33% { transform: translate(20px,-30px) scale(1.05); } 66% { transform: translate(-15px,15px) scale(0.97); } }

.hero-content {
  position: relative; z-index: 1;
  max-width: 680px; padding: 140px 60px 80px;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px; border: 1px solid rgba(124,154,109,0.3);
  border-radius: 20px; background: rgba(124,154,109,0.06);
  font-size: 11px; letter-spacing: 3px; color: var(--sage-dark);
  text-transform: uppercase; margin-bottom: 32px;
  opacity: 0; transform: translateY(20px);
  animation: fadeUp 0.8s ease 0.3s forwards;
}
.hero-badge::before {
  content: ''; width: 6px; height: 6px;
  background: var(--gold); border-radius: 50%;
  animation: pulse 2s ease infinite;
  display: inline-block;
}
@keyframes pulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.5); } }

.hero-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(52px, 7vw, 88px);
  font-weight: 300; line-height: 1.05;
  color: var(--text-dark); margin-bottom: 24px;
  opacity: 0; transform: translateY(30px);
  animation: fadeUp 0.9s ease 0.5s forwards;
}
.hero-title em { font-style: italic; color: var(--sage-dark); }
.hero-title .gold { color: var(--gold); }

.hero-subtitle {
  font-size: 15px; font-weight: 300; line-height: 1.8;
  color: var(--text-mid); max-width: 480px; margin-bottom: 44px;
  opacity: 0; transform: translateY(30px);
  animation: fadeUp 0.9s ease 0.7s forwards;
}
.hero-actions {
  display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
  opacity: 0; transform: translateY(30px);
  animation: fadeUp 0.9s ease 0.9s forwards;
}
.btn-primary {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--sage); color: white;
  padding: 16px 36px; border-radius: 2px;
  font-size: 12px; letter-spacing: 2.5px; text-transform: uppercase;
  text-decoration: none; font-weight: 500;
  transition: all 0.4s ease; position: relative; overflow: hidden;
}
.btn-primary::before {
  content: ''; position: absolute; inset: 0;
  background: var(--sage-dark); transform: translateX(-101%);
  transition: transform 0.4s ease;
}
.btn-primary:hover::before { transform: translateX(0); }
.btn-primary span { position: relative; z-index: 1; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(124,154,109,0.35); }

.btn-secondary {
  display: inline-flex; align-items: center; gap: 8px;
  color: var(--text-dark); text-decoration: none;
  font-size: 13px; font-weight: 400; letter-spacing: 0.5px;
  transition: gap 0.3s ease;
}
.btn-secondary:hover { gap: 14px; }
.btn-arrow { font-size: 18px; transition: transform 0.3s ease; }
.btn-secondary:hover .btn-arrow { transform: translateX(4px); }

.hero-stats {
  position: absolute; right: 60px; bottom: 80px;
  display: flex; flex-direction: column; gap: 24px;
  opacity: 0; animation: fadeUp 0.9s ease 1.2s forwards;
}
.stat-item { text-align: right; }
.stat-num {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 42px; font-weight: 300; color: var(--text-dark); line-height: 1;
}
.stat-label { font-size: 10px; letter-spacing: 3px; color: var(--text-soft); text-transform: uppercase; }

.hero-visual {
  position: absolute; right: 0; top: 0; bottom: 0;
  width: 50%; display: flex; align-items: center; justify-content: center;
  opacity: 0; animation: heroVisual 1.2s ease 0.6s forwards;
}
@keyframes heroVisual { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.hero-circle-wrap { position: relative; width: 460px; height: 460px; }
.hero-circle-bg {
  position: absolute; inset: 0; border-radius: 50%;
  background: radial-gradient(circle, rgba(124,154,109,0.12) 0%, transparent 70%);
  animation: circleBreath 4s ease-in-out infinite;
}
@keyframes circleBreath { 0%,100% { transform: scale(1); } 50% { transform: scale(1.06); } }
.hero-circle-ring {
  position: absolute; inset: 30px; border-radius: 50%;
  border: 1px solid rgba(124,154,109,0.2);
  animation: ringRotate 20s linear infinite;
}
.hero-circle-ring2 {
  position: absolute; inset: 70px; border-radius: 50%;
  border: 1px dashed rgba(201,168,76,0.2);
  animation: ringRotate 30s linear infinite reverse;
}
@keyframes ringRotate { to { transform: rotate(360deg); } }
.hero-yoga-svg { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
.hero-yoga-svg svg { width: 280px; height: 280px; }

.hero-float-tag {
  position: absolute; background: white; border-radius: 12px;
  padding: 12px 18px; box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  font-size: 12px; font-weight: 500; display: flex; align-items: center; gap: 8px;
  animation: tagFloat 3s ease-in-out infinite;
}
.hero-float-tag.t1 { top: 80px; right: -20px; }
.hero-float-tag.t2 { bottom: 100px; left: -30px; animation-delay: 1.5s; }
.hero-float-tag .dot { width: 8px; height: 8px; border-radius: 50%; }
.hero-float-tag .dot.green { background: var(--sage); }
.hero-float-tag .dot.gold { background: var(--gold); }
@keyframes tagFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }

@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

.scroll-hint {
  position: absolute; bottom: 30px; left: 60px;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  opacity: 0; animation: fadeUp 1s ease 1.5s forwards;
}
.scroll-line {
  width: 1px; height: 50px; background: linear-gradient(to bottom, var(--sage), transparent);
  animation: scrollLine 2s ease-in-out infinite;
}
@keyframes scrollLine { 0% { transform: scaleY(0) translateY(-100%); opacity: 0; } 50% { opacity: 1; } 100% { transform: scaleY(1) translateY(0); opacity: 0; } }
.scroll-text { font-size: 9px; letter-spacing: 3px; color: var(--text-soft); text-transform: uppercase; writing-mode: vertical-rl; }

/* ── SECTION BASE ── */
section { position: relative; overflow: hidden; }
.section-inner { max-width: 1280px; margin: 0 auto; padding: 0 60px; }
.section-label {
  font-size: 10px; letter-spacing: 5px; color: var(--sage);
  text-transform: uppercase; margin-bottom: 16px; display: block;
}
.section-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 300; line-height: 1.1; color: var(--text-dark);
}
.section-title em { font-style: italic; color: var(--sage-dark); }

/* ── FEATURES ── */
#features { padding: 120px 0; background: var(--cream); }
.features-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 2px; margin-top: 64px;
  border: 1px solid rgba(0,0,0,0.06);
}
.feature-card {
  padding: 48px 40px; background: white;
  transition: all 0.4s ease; cursor: default;
  position: relative; overflow: hidden;
}
.feature-card::before {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0;
  height: 2px; background: linear-gradient(90deg, var(--sage), var(--gold));
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.4s ease;
}
.feature-card:hover::before { transform: scaleX(1); }
.feature-card:hover { transform: translateY(-4px); box-shadow: 0 20px 60px rgba(0,0,0,0.06); z-index: 1; }
.feature-icon {
  width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(135deg, rgba(124,154,109,0.12), rgba(201,168,76,0.08));
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; margin-bottom: 24px;
  transition: transform 0.3s ease;
}
.feature-card:hover .feature-icon { transform: scale(1.1) rotate(5deg); }
.feature-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 22px; font-weight: 500; margin-bottom: 12px; color: var(--text-dark);
}
.feature-desc { font-size: 13px; line-height: 1.8; color: var(--text-soft); font-weight: 300; }
.feature-num {
  position: absolute; top: 32px; right: 32px;
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 48px; font-weight: 300; color: rgba(0,0,0,0.04); line-height: 1;
}

/* ── HOW IT WORKS ── */
#how { padding: 120px 0; background: var(--deep); overflow: hidden; }
#how .section-label { color: var(--gold); }
#how .section-title { color: white; }
.how-bg-text {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(80px, 15vw, 180px); font-weight: 300;
  color: rgba(255,255,255,0.02); white-space: nowrap;
  pointer-events: none; user-select: none; letter-spacing: 8px;
}
.how-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; margin-top: 64px; }
.how-steps { display: flex; flex-direction: column; gap: 0; }
.how-step {
  display: flex; gap: 24px; padding: 32px 0;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  transition: all 0.3s ease; cursor: default; opacity: 0.5;
}
.how-step.active, .how-step:hover { opacity: 1; }
.step-num { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 13px; color: var(--gold); font-weight: 400; letter-spacing: 1px; padding-top: 4px; min-width: 30px; }
.step-title { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 24px; font-weight: 400; color: white; margin-bottom: 8px; }
.step-desc { font-size: 13px; line-height: 1.8; color: rgba(255,255,255,0.45); font-weight: 300; }
.how-visual { position: relative; display: flex; align-items: center; justify-content: center; }
.how-phone {
  width: 260px; height: 520px; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 36px;
  overflow: hidden; position: relative;
  box-shadow: 0 40px 80px rgba(0,0,0,0.4);
}
.phone-notch { width: 100px; height: 28px; background: rgba(0,0,0,0.5); border-radius: 0 0 16px 16px; margin: 0 auto; }
.phone-screen { padding: 20px 16px; }
.phone-card {
  background: rgba(255,255,255,0.06); border-radius: 12px;
  padding: 14px; margin-bottom: 10px;
  border: 1px solid rgba(255,255,255,0.06);
  animation: phoneCard 3s ease-in-out infinite;
}
.phone-card:nth-child(2) { animation-delay: 0.5s; }
.phone-card:nth-child(3) { animation-delay: 1s; }
@keyframes phoneCard { 0%,100% { transform: translateX(0); opacity: 0.8; } 50% { transform: translateX(-3px); opacity: 1; } }
.phone-card-label { font-size: 9px; letter-spacing: 2px; color: var(--gold); text-transform: uppercase; margin-bottom: 6px; }
.phone-card-text { font-size: 12px; color: rgba(255,255,255,0.6); }
.phone-otp { display: flex; gap: 6px; justify-content: center; margin-top: 16px; }
.otp-box {
  width: 36px; height: 44px; border-radius: 6px;
  background: rgba(124,154,109,0.15); border: 1px solid rgba(124,154,109,0.3);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Cormorant Garamond', Georgia, serif; font-size: 20px; color: #9aab8a;
  animation: otpPop 2s ease-in-out infinite;
}
.otp-box:nth-child(1) { animation-delay: 0s; }
.otp-box:nth-child(2) { animation-delay: 0.15s; }
.otp-box:nth-child(3) { animation-delay: 0.3s; }
.otp-box:nth-child(4) { animation-delay: 0.45s; }
.otp-box:nth-child(5) { animation-delay: 0.6s; }
.otp-box:nth-child(6) { animation-delay: 0.75s; }
@keyframes otpPop { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }

/* ── TRAINERS ── */
#trainers { padding: 120px 0; background: var(--beige-warm, #EDE8D5); }
.trainers-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  margin-bottom: 64px;
}
.trainers-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.trainer-card {
  background: white; border-radius: 4px; overflow: hidden;
  transition: all 0.4s ease; cursor: default;
}
.trainer-card:hover { transform: translateY(-8px); box-shadow: 0 24px 60px rgba(0,0,0,0.1); }
.trainer-img {
  height: 220px; position: relative;
  display: flex; align-items: center; justify-content: center;
}
.trainer-img-inner { font-size: 64px; }
.trainer-badge {
  position: absolute; top: 16px; right: 16px;
  background: var(--gold); color: white;
  font-size: 9px; letter-spacing: 2px; text-transform: uppercase;
  padding: 4px 10px; border-radius: 2px;
}
.trainer-info { padding: 24px; }
.trainer-name { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 20px; font-weight: 500; color: var(--text-dark); margin-bottom: 4px; }
.trainer-spec { font-size: 12px; color: var(--sage); letter-spacing: 1px; margin-bottom: 20px; }
.trainer-stats { display: flex; gap: 20px; }
.trainer-stat-num { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 22px; font-weight: 400; color: var(--text-dark); }
.trainer-stat-label { font-size: 10px; color: var(--text-soft); letter-spacing: 1px; }

/* ── PRICING ── */
#pricing { padding: 120px 0; background: var(--cream); }
.pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 64px; align-items: start; }
.pricing-card {
  border: 1px solid rgba(0,0,0,0.08); border-radius: 4px; padding: 48px 40px;
  background: white; transition: all 0.4s ease; position: relative;
}
.pricing-card:hover { box-shadow: 0 20px 60px rgba(0,0,0,0.08); transform: translateY(-4px); }
.pricing-card.featured { background: var(--deep); border-color: transparent; transform: scale(1.04); }
.pricing-card.featured:hover { transform: scale(1.04) translateY(-4px); }
.pricing-tag {
  display: inline-block; background: var(--gold); color: white;
  font-size: 9px; letter-spacing: 2px; text-transform: uppercase;
  padding: 4px 12px; border-radius: 2px; margin-bottom: 20px;
}
.pricing-plan { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--sage); display: block; margin-bottom: 16px; }
.pricing-card.featured .pricing-plan { color: rgba(255,255,255,0.5); }
.pricing-price {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 52px; font-weight: 300; color: var(--text-dark); line-height: 1; margin-bottom: 8px;
}
.pricing-period { font-size: 12px; color: var(--text-soft); margin-bottom: 32px; }
.pricing-card.featured .pricing-period { color: rgba(255,255,255,0.35); }
.pricing-features { list-style: none; margin-bottom: 40px; }
.pricing-features li {
  font-size: 13px; color: var(--text-mid); padding: 10px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05); font-weight: 300;
}
.pricing-card.featured .pricing-features li { color: rgba(255,255,255,0.55); border-bottom-color: rgba(255,255,255,0.06); }
.pricing-features li::before { content: '✦ '; color: var(--sage); font-size: 8px; }
.pricing-card.featured .pricing-features li::before { color: var(--gold); }
.pricing-btn {
  display: block; text-align: center; padding: 14px;
  border: 1px solid var(--sage); color: var(--sage);
  text-decoration: none; font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  border-radius: 2px; transition: all 0.3s ease;
}
.pricing-btn:hover { background: var(--sage); color: white; }
.pricing-card.featured .pricing-btn { background: var(--gold); border-color: var(--gold); color: white; }
.pricing-card.featured .pricing-btn:hover { background: #b8960f; }

/* ── REVIEWS ── */
#reviews { padding: 120px 0; background: var(--beige-warm, #EDE8D5); overflow: hidden; }
.reviews-track-wrap { overflow: hidden; margin-top: 64px; }
.reviews-track {
  display: flex; gap: 24px;
  animation: reviewsScroll 30s linear infinite;
  width: max-content;
}
.reviews-track:hover { animation-play-state: paused; }
@keyframes reviewsScroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.review-card {
  width: 340px; flex-shrink: 0;
  background: white; border-radius: 4px; padding: 36px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.04);
}
.review-stars { color: var(--gold); font-size: 14px; margin-bottom: 16px; letter-spacing: 2px; }
.review-text {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 17px; font-weight: 300; line-height: 1.7;
  color: var(--text-dark); margin-bottom: 24px; font-style: italic;
}
.review-author { display: flex; align-items: center; gap: 12px; }
.review-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--sage), var(--deep));
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 16px;
  font-family: 'Cormorant Garamond', Georgia, serif;
}
.review-name { font-size: 13px; font-weight: 500; }
.review-role { font-size: 11px; color: var(--text-soft); }

/* ── CTA ── */
#cta {
  padding: 140px 0;
  background: linear-gradient(135deg, var(--sage-dark) 0%, var(--deep) 100%);
  position: relative; overflow: hidden;
}
.cta-bg-lotus {
  position: absolute; right: -100px; top: -100px;
  width: 600px; height: 600px; opacity: 0.04;
  animation: ctaRotate 30s linear infinite;
}
@keyframes ctaRotate { to { transform: rotate(360deg); } }
.cta-content { text-align: center; position: relative; z-index: 1; }
.cta-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(40px, 6vw, 72px);
  font-weight: 300; color: white; margin-bottom: 20px; line-height: 1.1;
}
.cta-title em { color: var(--gold); font-style: italic; }
.cta-sub { font-size: 14px; color: rgba(255,255,255,0.5); margin-bottom: 48px; font-weight: 300; line-height: 1.8; }
.cta-actions { display: flex; align-items: center; justify-content: center; gap: 24px; flex-wrap: wrap; }
.btn-gold {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--gold); color: white;
  padding: 18px 44px; border-radius: 2px;
  font-size: 12px; letter-spacing: 2.5px; text-transform: uppercase;
  text-decoration: none; font-weight: 500;
  transition: all 0.4s ease;
}
.btn-gold:hover { background: var(--gold-light, #e5b029); transform: translateY(-2px); box-shadow: 0 12px 40px rgba(201,168,76,0.4); }
.btn-outline-white {
  display: inline-flex; align-items: center; gap: 10px;
  border: 1px solid rgba(255,255,255,0.3); color: white;
  padding: 17px 36px; border-radius: 2px;
  font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  text-decoration: none; font-weight: 400;
  transition: all 0.3s ease;
}
.btn-outline-white:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.6); }
.cta-trust {
  margin-top: 48px; display: flex; align-items: center;
  justify-content: center; gap: 32px; flex-wrap: wrap;
}
.cta-trust-item { display: flex; align-items: center; gap: 8px; color: rgba(255,255,255,0.4); font-size: 12px; letter-spacing: 1px; }
.cta-check { color: var(--gold); }

/* ── REVEAL ANIMATIONS ── */
.reveal { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease, transform 0.8s ease; }
.reveal.visible { opacity: 1; transform: translateY(0); }
.reveal-left { opacity: 0; transform: translateX(-40px); transition: opacity 0.8s ease, transform 0.8s ease; }
.reveal-left.visible { opacity: 1; transform: translateX(0); }
.reveal-right { opacity: 0; transform: translateX(40px); transition: opacity 0.8s ease, transform 0.8s ease; }
.reveal-right.visible { opacity: 1; transform: translateX(0); }

/* ── STAGGER DELAYS ── */
.stagger-1 { transition-delay: 0.1s; }
.stagger-2 { transition-delay: 0.2s; }
.stagger-3 { transition-delay: 0.3s; }
.stagger-4 { transition-delay: 0.4s; }
.stagger-5 { transition-delay: 0.5s; }
.stagger-6 { transition-delay: 0.6s; }

/* ── RESPONSIVE ── */
@media (max-width: 1100px) {
  .hero-visual { display: none; }
  .trainers-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 860px) {
  .hero-content { padding: 120px 24px 60px; }
  .section-inner { padding: 0 24px; }
  .features-grid { grid-template-columns: 1fr; }
  .pricing-grid { grid-template-columns: 1fr; }
  .pricing-card.featured { transform: none; }
  .how-grid { grid-template-columns: 1fr; }
  .trainers-grid { grid-template-columns: 1fr 1fr; }
  .hero-stats { position: static; flex-direction: row; padding: 24px; gap: 40px; }
  .stat-item { text-align: left; }
  .trainers-header { flex-direction: column; align-items: flex-start; gap: 16px; }
}
@media (max-width: 540px) {
  .trainers-grid { grid-template-columns: 1fr; }
  .scroll-hint { display: none; }
}
</style>