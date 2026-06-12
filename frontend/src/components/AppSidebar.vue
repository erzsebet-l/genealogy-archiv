<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="logo-box">
        <img v-if="logoImage" :src="logoImage" alt="Логотип" class="logo-img" />
        <span v-else>Лого</span>
      </div>
      <div class="logo-title">
        <span class="logo-main">Живые</span>
        <span class="logo-sub">Страницы</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <ul>
        <li v-for="item in navItems" :key="item.label" class="nav-item">
          <router-link :to="item.path" class="nav-link" active-class="nav-link-active">
            {{ item.label }}
          </router-link>
        </li>

        <!-- Ссылка на Django Admin только для администратора -->
        <li v-if="isAdmin" class="nav-item">
          <a href="http://localhost:8000/admin" target="_blank" class="nav-link admin-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            Админ панель
          </a>
        </li>

        <li class="nav-item nav-item-dropdown">
          <span class="nav-toggle" @click="toggleForms">
            <span class="nav-arrow" :class="{ rotated: showForms }">▶</span>
            Формы индексации
          </span>
          <div class="dropdown-list" :class="{ show: showForms }">
            <router-link to="/birth"    class="dropdown-item">Раздел о рождении</router-link>
            <router-link to="/marriage" class="dropdown-item">Раздел о браке</router-link>
            <router-link to="/death"    class="dropdown-item">Раздел о смерти</router-link>
          </div>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/change-password" class="footer-item">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
        </svg>
        <span>Настройки</span>
      </router-link>
      <div class="footer-item" @click="logout">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>Выйти</span>
      </div>
    </div>
  </aside>
</template>

<script>
// Пытаемся импортировать логотип, если файл существует
let logoImage = null
try {
  logoImage = new URL('@/assets/logo.jpg', import.meta.url).href
} catch (e) {
  console.log('Логотип не найден, используется текстовая версия')
}

export default {
  name: 'AppSidebar',

  props: {
    isAdmin: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      showForms: false,
      logoImage: logoImage,

      navItems: [
        { label: 'Главная страница', path: '/' },
        { label: 'Все персоны', path: '/allpersons' },
      ],
    }
  },

  methods: {
    toggleForms() {
      this.showForms = !this.showForms
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
.sidebar {
  width: 220px;
  min-height: 100vh;
  background: #e4e2df;
  border-right: 1px solid #d5d3cf;
  display: flex;
  flex-direction: column;
  padding: 24px 0 20px;
  flex-shrink: 0;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px 28px;
}

.logo-box {
  width: 44px;
  height: 44px;
  background: #ccc9c4;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  font-size: 11px;
  color: #555;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-title {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-main {
  font-size: 15px;
  font-weight: 700;
}

.logo-sub {
  font-size: 13px;
  color: #666;
}

.sidebar-nav {
  flex: 1;
}

.sidebar-nav ul {
  list-style: none;
}

.nav-item {
  list-style: none;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  font-size: 14px;
  color: #1a1a1a;
  text-decoration: none;
  transition: background .15s;
}

.nav-link:hover {
  background: #d8d5d0;
}

.nav-link-active {
  background: #ccc9c4;
  font-weight: 600;
}

.admin-link {
  color: #2a55a0;
  border-left: 3px solid transparent;
}

.admin-link:hover {
  color: #1a3a6b;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.nav-item-dropdown {
  position: relative;
}

.nav-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  user-select: none;
  transition: background .15s;
}

.nav-toggle:hover {
  background: #d8d5d0;
}

.nav-arrow {
  font-size: 8px;
  color: #999;
  transition: transform .2s;
}

.nav-arrow.rotated {
  transform: rotate(90deg);
  color: #333;
}

.dropdown-list {
  display: none;
  position: absolute;
  left: 100%;
  top: 0;
  margin-left: 5px;
  background: white;
  min-width: 180px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-list.show {
  display: block;
}

.dropdown-item {
  display: block;
  padding: 10px 16px;
  color: #333;
  text-decoration: none;
  font-size: 13px;
  transition: background 0.15s;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: #f0efee;
  color: #000;
}

.sidebar-footer {
  padding: 12px 20px 0;
  border-top: 1px solid #d0cdc8;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  padding: 4px 0;
  transition: color .15s;
  text-decoration: none;
}

.footer-item:hover {
  color: #1a1a1a;
}

.icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}
</style>