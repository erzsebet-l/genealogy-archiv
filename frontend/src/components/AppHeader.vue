<template>
  <header class="main-header">
    <h1 class="welcome-title">
      Добро пожаловать, <em>{{ userName }}</em>
    </h1>
    <button class="user-btn" aria-label="Профиль">
      <svg class="icon-lg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
        <circle cx="12" cy="8" r="4"/>
        <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
      </svg>
    </button>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
    userName: {
      type: String,
      default: 'пользователь'
    }
  }
}
</script>

<style scoped>
.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.welcome-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -.3px;
}

.welcome-title em {
  font-style: italic;
}

.user-btn {
  width: 38px;
  height: 38px;
  border: none;
  background: transparent;
  border-radius: 50%;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .15s;
}

.user-btn:hover {
  background: #ddd;
}

.icon-lg {
  width: 26px;
  height: 26px;
}
</style>