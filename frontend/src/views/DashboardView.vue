<<template>
  <div class="app-layout">
    <!-- Боковая панель (такая же как на главной) -->
    <aside class="sidebar">
      <div class="logo">
        <img src="/favicon.ico" class="logo-icon"  />
        <span>Живые Страницы</span>
      </div>

      <nav>
        <RouterLink to="/">Главная страница</RouterLink>
        <RouterLink to="/dash">Все персоны</RouterLink>
        <a href="#" @click.prevent="openFormsDrawer">Формы индексации</a>
      </nav>

      <div class="docs-list">
        <div class="doc-item">Метрические книги</div>
        <div class="doc-item">Ревизиские сказки</div>
        <div class="doc-item">Переписи населения</div>
        <div class="doc-item">Похозяйственные книги</div>
        <div class="doc-item">Иные документы</div>
      </div>

      <div class="bottom-links">
        <RouterLink to="/register">Регистрация</RouterLink>
        <RouterLink to="/login">Авторизация</RouterLink>
      </div>
    </aside>

    <!-- Основной контент -->
    <main class="main-content">
      <div class="welcome-header">
        <h1>Все персоны</h1>
      </div>

      <!-- Фильтры -->
      <div class="filters">
        <input type="text" placeholder="ФИО" class="filter-input" />
        <input type="text" placeholder="Дата рождения" class="filter-input" />
        <input type="text" placeholder="Статус" class="filter-input" />
        <button class="filter-btn">Поиск</button>
      </div>

      <!-- Таблица -->
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Дата рождения</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Иванов Василий Александрович</td>
              <td>01.12.1905</td>
              <td><span class="status published">Опубликовано</span></td>
            </tr>
            <tr>
              <td>Петрова Анна Ивановна</td>
              <td>15.03.1910</td>
              <td><span class="status draft">Черновик</span></td>
            </tr>
            <tr>
              <td>Сидоров Петр Николаевич</td>
              <td>23.07.1898</td>
              <td><span class="status published">Опубликовано</span></td>
            </tr>
            <tr>
              <td>Кузнецова Елена Дмитриевна</td>
              <td>08.11.1915</td>
              <td><span class="status processing">В обработке</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Шторка для форм индексации -->
    <Transition name="drawer">
      <div v-if="isDrawerOpen" class="drawer-overlay" @click.self="closeDrawer">
        <div class="drawer">
          <div class="drawer-header">
            <h2>Формы индексации</h2>
            <button class="drawer-close" @click="closeDrawer">&times;</button>
          </div>
          <div class="drawer-body">
            <div class="drawer-item" @click="navigateTo('/birth')">
              <span class="item-icon">📖</span>
              <div class="item-content">
                <div class="item-title">Рождение</div>
                <div class="item-desc">Индексация записей о рождении</div>
              </div>
              <span class="item-arrow">→</span>
            </div>
            <div class="drawer-item" @click="navigateTo('/marriage')">
              <span class="item-icon">💍</span>
              <div class="item-content">
                <div class="item-title">Бракосочетание</div>
                <div class="item-desc">Индексация записей о бракосочетании</div>
              </div>
              <span class="item-arrow">→</span>
            </div>
            <div class="drawer-item" @click="navigateTo('/death')">
              <span class="item-icon">🕊️</span>
              <div class="item-content">
                <div class="item-title">Смерть</div>
                <div class="item-desc">Индексация записей о смерти</div>
              </div>
              <span class="item-arrow">→</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
//import favicon from 'favicon.ico'

const router = useRouter()
const isDrawerOpen = ref(false)

const openFormsDrawer = () => {
  isDrawerOpen.value = true
}

const closeDrawer = () => {
  isDrawerOpen.value = false
}

const navigateTo = (path) => {
  closeDrawer()
  router.push(path)
}
</script>

<style scoped>
/* ---------- Общая структура (как на главной) ---------- */
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: #ffffff;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}

/* ---------- Сайдбар ---------- */
.sidebar {
  width: 260px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  padding: 28px 20px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.logo {
  font-size: 22px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 32px;
  letter-spacing: -0.3px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 28px;
}

nav a, nav a:visited {
  color: #495057;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.2s;
  cursor: pointer;
}

nav a:hover {
  color: #0d6efd;
}

.docs-list {
  margin-top: 8px;
  margin-bottom: 32px;
}

.doc-item {
  padding: 8px 0 8px 12px;
  color: #6c757d;
  font-size: 14px;
  border-left: 2px solid transparent;
  transition: all 0.2s;
  cursor: default;
}

.doc-item:hover {
  color: #212529;
  border-left-color: #0d6efd;
  background-color: #f1f3f5;
}

.bottom-links {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #dee2e6;
}

.bottom-links a {
  color: #6c757d;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.bottom-links a:hover {
  color: #0d6efd;
}

/* ---------- Основной контент ---------- */
.main-content {
  flex: 1;
  padding: 40px 48px;
  background-color: #ffffff;
}

.welcome-header h1 {
  font-size: 28px;
  font-weight: 500;
  color: #212529;
  margin-bottom: 32px;
}

/* ---------- Фильтры (улучшенная версия) ---------- */
.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-input {
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid #dee2e6;
  font-size: 14px;
  min-width: 160px;
  transition: all 0.2s;
  background-color: #ffffff;
}

.filter-input:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.filter-input::placeholder {
  color: #adb5bd;
}

.filter-btn {
  padding: 10px 24px;
  border-radius: 12px;
  border: none;
  background-color: #0d6efd;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #0b5ed7;
  transform: translateY(-1px);
}

/* ---------- Таблица ---------- */
.table-wrapper {
  background: white;
  border-radius: 16px;
  border: 1px solid #e9ecef;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 16px 20px;
  background-color: #f8f9fa;
  font-weight: 600;
  font-size: 14px;
  color: #495057;
  border-bottom: 1px solid #e9ecef;
}

td {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f3f5;
  font-size: 14px;
  color: #212529;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background-color: #f8f9fa;
}

/* Статусы */
.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 500;
}

.status.published {
  background-color: #d1f4e0;
  color: #0a6e3d;
}

.status.draft {
  background-color: #e9ecef;
  color: #495057;
}

.status.processing {
  background-color: #fff3cd;
  color: #856404;
}

/* ---------- Шторка (Drawer) ---------- */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 380px;
  height: 100%;
  background-color: white;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px 24px;
  border-bottom: 1px solid #e9ecef;
}

.drawer-header h2 {
  font-size: 22px;
  font-weight: 600;
  color: #212529;
  margin: 0;
}

.drawer-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #adb5bd;
  transition: color 0.2s;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.drawer-close:hover {
  color: #dc3545;
  background-color: #fff5f5;
}

.drawer-body {
  flex: 1;
  padding: 16px 12px;
}

.drawer-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  margin-bottom: 8px;
  background-color: #ffffff;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e9ecef;
}

.drawer-item:hover {
  background-color: #f8f9fa;
  border-color: #0d6efd;
  transform: translateX(-4px);
}

.item-icon {
  font-size: 28px;
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: 17px;
  font-weight: 600;
  color: #212529;
  margin-bottom: 4px;
}

.item-desc {
  font-size: 13px;
  color: #6c757d;
}

.item-arrow {
  font-size: 18px;
  color: #adb5bd;
  transition: transform 0.2s;
}

.drawer-item:hover .item-arrow {
  transform: translateX(4px);
  color: #0d6efd;
}

/* Анимация шторки */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.25s ease;
}

.drawer-enter-active .drawer,
.drawer-leave-active .drawer {
  transition: transform 0.25s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from .drawer,
.drawer-leave-to .drawer {
  transform: translateX(100%);
}

.drawer-enter-to .drawer,
.drawer-leave-from .drawer {
  transform: translateX(0);
}

/* Адаптивность */
@media (max-width: 768px) {
  .main-content {
    padding: 24px 20px;
  }
  
  .sidebar {
    width: 220px;
    padding: 20px 16px;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-input {
    width: 100%;
  }
  
  .drawer {
    width: 100%;
    max-width: 320px;
  }
}
</style>