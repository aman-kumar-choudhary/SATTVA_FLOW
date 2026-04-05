<template>
  <div id="app">

    <!-- ── NAVBAR ── (hidden on dashboard routes) -->
    <nav v-if="!isDashboardRoute" class="navbar" :class="{ scrolled: isScrolled }">
      <div class="nav-container">
        <div class="nav-logo" @click="$router.push('/')">
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

        <div class="nav-links">
          <a href="#" @click.prevent="scrollTo('features')">Platform</a>
          <a href="#" @click.prevent="scrollTo('how')">How It Works</a>
          <a href="#" @click.prevent="scrollTo('trainers')">Trainers</a>
          <a href="#" @click.prevent="scrollTo('pricing')">Pricing</a>
          <a href="#" @click.prevent="scrollTo('reviews')">Reviews</a>
          <div class="nav-divider"></div>
          <template v-if="!isAuthenticated">
            <a href="#" class="nav-text-link" @click.prevent="$router.push('/login')">Login</a>
            <a href="#" class="nav-cta" @click.prevent="$router.push('/signup')">
              <span>Join Free</span>
              <span class="nav-cta-arrow">→</span>
            </a>
          </template>
          <template v-else>
            <span class="nav-user-name">{{ userName }}</span>
            <a href="#" class="nav-cta" @click.prevent="goToDashboard">Dashboard</a>
            <a href="#" class="nav-logout" @click.prevent="logout">Logout</a>
          </template>
        </div>

        <div class="hamburger" :class="{ open: mobileMenuOpen }" @click="toggleMenu">
          <span></span><span></span><span></span>
        </div>
      </div>
    </nav>

    <!-- ── MOBILE MENU ── (hidden on dashboard routes) -->
    <div v-if="!isDashboardRoute" class="mobile-menu" :class="{ open: mobileMenuOpen }">
      <div class="mobile-menu-inner">
        <div class="mobile-menu-links">
          <a href="#" @click.prevent="scrollTo('features'); closeMenu()">Platform</a>
          <a href="#" @click.prevent="scrollTo('how'); closeMenu()">How It Works</a>
          <a href="#" @click.prevent="scrollTo('trainers'); closeMenu()">Trainers</a>
          <a href="#" @click.prevent="scrollTo('pricing'); closeMenu()">Pricing</a>
          <a href="#" @click.prevent="scrollTo('reviews'); closeMenu()">Reviews</a>
        </div>
        <div class="mobile-menu-actions">
          <template v-if="!isAuthenticated">
            <a href="#" @click.prevent="$router.push('/login'); closeMenu()" class="mm-login">Login</a>
            <a href="#" @click.prevent="$router.push('/signup'); closeMenu()" class="mm-join">Join Free →</a>
          </template>
          <template v-else>
            <a href="#" @click.prevent="goToDashboard(); closeMenu()" class="mm-join">Dashboard</a>
            <a href="#" @click.prevent="logout" class="mm-login">Logout</a>
          </template>
        </div>
      </div>
    </div>

    <!-- ── PAGE CONTENT ── -->
    <router-view />

    <!-- ── FOOTER ── (hidden on dashboard routes) -->
    <footer v-if="!isDashboardRoute" class="site-footer">
      <div class="footer-inner">
        <div class="footer-grid">
          <!-- Brand -->
          <div class="footer-brand">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 100" fill="none" height="52">
              <defs>
                <linearGradient id="fG2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#aac4a2"/><stop offset="100%" style="stop-color:#7c9a6e"/>
                </linearGradient>
              </defs>
              <circle cx="50" cy="50" r="44" fill="url(#fG2)"/>
              <path d="M50 68 Q42 73 38 80 Q44 75 50 73 Q56 75 62 80 Q58 73 50 68Z" fill="#e5b029" opacity="0.85"/>
              <path d="M50 68 Q35 72 30 78 Q38 73 50 71Z" fill="#e5b029" opacity="0.45"/>
              <path d="M50 68 Q65 72 70 78 Q62 73 50 71Z" fill="#e5b029" opacity="0.45"/>
              <circle cx="50" cy="28" r="7" fill="rgba(255,255,255,0.95)"/>
              <line x1="50" y1="35" x2="50" y2="56" stroke="rgba(255,255,255,0.95)" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M50 42 Q40 40 36 44" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M50 42 Q60 40 64 44" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <text x="108" y="42" font-family="Georgia, serif" font-size="26" font-weight="500" fill="#ffffff" letter-spacing="0.5">SattvaFlow</text>
              <text x="110" y="62" font-family="Georgia, serif" font-size="14" font-weight="300" fill="#e5c46a" letter-spacing="5">YOGA</text>
              <text x="110" y="80" font-family="Arial, sans-serif" font-size="9" fill="rgba(255,255,255,0.3)" letter-spacing="3">FIND YOUR FLOW</text>
            </svg>
            <p class="footer-brand-desc">A premium yoga management platform connecting expert trainers with dedicated clients. OTP-secured, admin-controlled, privacy-first.</p>
            <div class="footer-socials">
              <a href="#" class="footer-social" title="Twitter">𝕏</a>
              <a href="#" class="footer-social" title="LinkedIn">in</a>
              <a href="#" class="footer-social" title="Instagram">ig</a>
              <a href="#" class="footer-social" title="YouTube">yt</a>
            </div>
          </div>

          <!-- Platform -->
          <div class="footer-col">
            <div class="footer-col-title">Platform</div>
            <ul class="footer-links">
              <li><a href="#" @click.prevent="scrollTo('features')">Features</a></li>
              <li><a href="#" @click.prevent="scrollTo('how')">How It Works</a></li>
              <li><a href="#" @click.prevent="scrollTo('trainers')">Our Trainers</a></li>
              <li><a href="#" @click.prevent="scrollTo('pricing')">Pricing</a></li>
              <li><a href="#" @click.prevent="$router.push('/login')">Dashboard Login</a></li>
            </ul>
          </div>

          <!-- Company -->
          <div class="footer-col">
            <div class="footer-col-title">Company</div>
            <ul class="footer-links">
              <li><a href="#">About Us</a></li>
              <li><a href="#">Contact</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Careers</a></li>
              <li><a href="#">Press Kit</a></li>
            </ul>
          </div>

          <!-- Legal -->
          <div class="footer-col">
            <div class="footer-col-title">Legal</div>
            <ul class="footer-links">
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Use</a></li>
              <li><a href="#">Cookie Policy</a></li>
              <li><a href="#">Data Security</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <div>© 2025 SattvaFlow. All rights reserved. Built with 🌿 in India.</div>
          <div class="footer-bottom-links">
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">Contact</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- WhatsApp Float (hidden on dashboard routes) -->
    <a v-if="!isDashboardRoute" href="https://wa.me/" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">💬</a>

  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isScrolled: false,
      mobileMenuOpen: false
    }
  },
  computed: {
    isDashboardRoute() {
      const dashboardPaths = ['/admin', '/trainer', '/client']
      return dashboardPaths.some(p => this.$route.path.startsWith(p))
    },
    isAuthenticated() {
      return !!localStorage.getItem('token')
    },
    userName() {
      return localStorage.getItem('userName') || ''
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 60
    },
    toggleMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
      document.body.style.overflow = this.mobileMenuOpen ? 'hidden' : ''
    },
    closeMenu() {
      this.mobileMenuOpen = false
      document.body.style.overflow = ''
    },
    scrollTo(sectionId) {
      this.closeMenu()
      if (this.$route.path !== '/') {
        this.$router.push('/').then(() => {
          setTimeout(() => {
            const el = document.getElementById(sectionId)
            if (el) el.scrollIntoView({ behavior: 'smooth' })
          }, 150)
        })
      } else {
        const el = document.getElementById(sectionId)
        if (el) el.scrollIntoView({ behavior: 'smooth' })
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
      localStorage.removeItem('userName')
      localStorage.removeItem('userId')
      this.$router.push('/')
      this.closeMenu()
    },
    goToDashboard() {
      const role = localStorage.getItem('userRole')
      if (role === 'admin') this.$router.push('/admin')
      else if (role === 'trainer') this.$router.push('/trainer')
      else this.$router.push('/client')
      this.closeMenu()
    }
  }
}
</script>

<style>
/* ── GOOGLE FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=DM+Sans:wght@200;300;400;500&family=Cinzel:wght@400;500&display=swap');

/* ── RESET ── */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }

/* ── CSS VARIABLES ── */
:root {
  --sage: #7C9A6D;
  --sage-light: #9aab8a;
  --sage-dark: #4a6640;
  --deep: #2F4F4F;
  --beige: #F5F5DC;
  --beige-warm: #EDE8D5;
  --gold: #c9a84c;
  --gold-light: #e5b029;
  --cream: #FAFAF5;
  --text-dark: #1a2e1a;
  --text-mid: #4a5c4a;
  --text-soft: #7a8c7a;
}

body {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--cream);
  color: var(--text-dark);
  overflow-x: hidden;
}

/* ── NAVBAR ── */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 0 48px; height: 80px;
  display: flex; align-items: center;
  transition: all 0.4s ease;
  background: transparent;
}
.navbar.scrolled {
  background: rgba(250, 250, 245, 0.94);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 1px 0 rgba(0,0,0,0.06);
  height: 68px;
}
.nav-container {
  width: 100%; max-width: 1280px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
}
.nav-logo {
  cursor: pointer; transition: opacity 0.3s;
  display: flex; align-items: center;
}
.nav-logo:hover { opacity: 0.85; }
.nav-logo svg { height: 52px; transition: height 0.4s ease; }
.navbar.scrolled .nav-logo svg { height: 44px; }

.nav-links {
  display: flex; align-items: center; gap: 28px;
}
.nav-links a {
  text-decoration: none; color: var(--text-dark);
  font-size: 12px; font-weight: 400; letter-spacing: 1.5px;
  text-transform: uppercase; position: relative; padding-bottom: 2px;
  transition: color 0.3s;
}
.nav-links a::after {
  content: ''; position: absolute; bottom: 0; left: 0;
  width: 0; height: 1px; background: var(--sage);
  transition: width 0.3s ease;
}
.nav-links a:hover::after { width: 100%; }
.nav-links a:hover { color: var(--sage-dark); }

.nav-divider { width: 1px; height: 20px; background: rgba(0,0,0,0.12); }

.nav-text-link { letter-spacing: 1.5px !important; }
.nav-user-name {
  font-size: 12px; color: var(--text-mid); letter-spacing: 0.5px;
  max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.nav-cta {
  display: inline-flex !important; align-items: center; gap: 6px;
  background: var(--deep) !important; color: white !important;
  padding: 9px 20px !important; border-radius: 2px;
  letter-spacing: 1.5px !important; transition: all 0.3s !important;
}
.nav-cta::after { display: none !important; }
.nav-cta:hover { background: var(--sage-dark) !important; transform: translateY(-1px); }
.nav-cta-arrow { opacity: 0.7; }
.nav-logout {
  font-size: 11px !important; color: var(--text-soft) !important; letter-spacing: 1px !important;
}

/* ── HAMBURGER ── */
.hamburger {
  display: none; flex-direction: column; gap: 6px; cursor: pointer;
  padding: 4px; z-index: 1100;
}
.hamburger span {
  display: block; width: 22px; height: 1.5px;
  background: var(--text-dark); transition: all 0.35s ease;
  transform-origin: center;
}
.hamburger.open span:nth-child(1) { transform: translateY(7.5px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger.open span:nth-child(3) { transform: translateY(-7.5px) rotate(-45deg); }

/* ── MOBILE MENU ── */
.mobile-menu {
  position: fixed; inset: 0; z-index: 999;
  background: var(--cream);
  display: flex; align-items: center; justify-content: center;
  transform: translateX(100%);
  transition: transform 0.5s cubic-bezier(0.77, 0, 0.175, 1);
}
.mobile-menu.open { transform: translateX(0); }
.mobile-menu-inner {
  display: flex; flex-direction: column; align-items: center; gap: 48px;
}
.mobile-menu-links {
  display: flex; flex-direction: column; align-items: center; gap: 28px;
}
.mobile-menu-links a {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 36px; font-weight: 300; color: var(--text-dark);
  text-decoration: none; transition: color 0.3s; letter-spacing: 1px;
}
.mobile-menu-links a:hover { color: var(--sage); }
.mobile-menu-actions {
  display: flex; flex-direction: column; align-items: center; gap: 16px;
}
.mm-join {
  background: var(--deep); color: white !important;
  padding: 14px 40px !important; border-radius: 2px;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important; letter-spacing: 2px;
  text-transform: uppercase; text-decoration: none !important;
}
.mm-login {
  font-size: 13px !important; color: var(--text-soft) !important;
  text-decoration: none; letter-spacing: 1px; text-transform: uppercase;
}

/* ── FOOTER ── */
.site-footer {
  background: var(--text-dark);
  padding: 80px 0 40px;
  margin-top: 0;
}
.footer-inner { max-width: 1280px; margin: 0 auto; padding: 0 60px; }
.footer-grid {
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 60px; margin-bottom: 60px;
  align-items: start;
}
.footer-brand svg { display: block; }
.footer-brand-desc {
  font-size: 13px; line-height: 1.8; margin-top: 20px;
  color: rgba(255,255,255,0.3); max-width: 280px; font-weight: 300;
}
.footer-socials { display: flex; gap: 10px; margin-top: 24px; }
.footer-social {
  width: 36px; height: 36px; border: 1px solid rgba(255,255,255,0.1);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.4); text-decoration: none; font-size: 13px;
  transition: all 0.3s ease;
}
.footer-social:hover { border-color: var(--gold); color: var(--gold); transform: translateY(-2px); }
.footer-col-title {
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: white; margin-bottom: 20px; font-weight: 400;
}
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 10px; }
.footer-links a {
  text-decoration: none; color: rgba(255,255,255,0.35);
  font-size: 13px; transition: color 0.3s; font-weight: 300;
}
.footer-links a:hover { color: var(--gold); }
.footer-bottom {
  display: flex; align-items: center; justify-content: space-between;
  padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 12px; color: rgba(255,255,255,0.25);
}
.footer-bottom-links { display: flex; gap: 24px; }
.footer-bottom-links a { color: rgba(255,255,255,0.25); text-decoration: none; font-size: 12px; transition: color 0.3s; }
.footer-bottom-links a:hover { color: var(--gold); }

/* ── WHATSAPP FLOAT ── */
.whatsapp-float {
  position: fixed; bottom: 32px; right: 32px;
  width: 56px; height: 56px; background: #25D366;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  text-decoration: none; font-size: 26px;
  box-shadow: 0 8px 24px rgba(37,211,102,0.4);
  z-index: 500; transition: transform 0.3s, box-shadow 0.3s;
  animation: waPulse 3s ease-in-out infinite;
}
.whatsapp-float:hover { transform: scale(1.1); box-shadow: 0 12px 40px rgba(37,211,102,0.55); }
@keyframes waPulse { 0%,100% { box-shadow: 0 8px 24px rgba(37,211,102,0.4); } 50% { box-shadow: 0 8px 40px rgba(37,211,102,0.65); } }

/* ── RESPONSIVE ── */
@media (max-width: 1024px) {
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 40px; }
}
@media (max-width: 768px) {
  .navbar { padding: 0 20px; }
  .nav-links { display: none; }
  .hamburger { display: flex; }
  .footer-inner { padding: 0 24px; }
  .footer-grid { grid-template-columns: 1fr; gap: 32px; }
  .footer-bottom { flex-direction: column; gap: 16px; text-align: center; }
  .footer-bottom-links { justify-content: center; }
  .whatsapp-float { bottom: 20px; right: 20px; width: 48px; height: 48px; font-size: 22px; }
}
</style>