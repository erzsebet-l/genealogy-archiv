<template>
  <aside class="sidebar">
    <div class="logo">Vite app</div>

    <nav>
      <RouterLink to="/">Главная</RouterLink>
      <RouterLink to="/dash">Все персоны</RouterLink>
      <RouterLink to="/forms">Формы индексации</RouterLink>
    </nav>

    <div class="bottom-links">
      <a href="#">Настройки</a>
      <a href="#">Выход</a>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 220px;
  min-height: 100vh;
  background: #f5f5f5;
  border-right: 1px solid #ddd;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 40px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

nav a {
  color: #444;
  text-decoration: none;
}

.bottom-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>