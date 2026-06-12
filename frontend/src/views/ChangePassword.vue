<template>
  <div class="app-layout">
    <AppSidebar />
    <main class="main-content">
      <header class="main-header">
        <button class="btn-back" @click="$router.back()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M19 12H5M12 5l-7 7 7 7"/>
          </svg>
          Назад
        </button>
        <h1 class="page-title">Смена пароля</h1>
      </header>

      <div class="change-password-container">
        <div class="info-card">
          <h2 class="card-title">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            Изменение пароля
          </h2>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">✓ Пароль успешно изменён!</div>

          <form @submit.prevent="changePassword" class="password-form">
            <div class="form-group">
              <label>Текущий пароль</label>
              <div class="password-input-wrapper">
                <input 
                  :type="showCurrentPassword ? 'text' : 'password'"
                  v-model="formData.current_password"
                  placeholder="Введите текущий пароль"
                  class="form-input"
                />
                <button type="button" class="toggle-password" @click="showCurrentPassword = !showCurrentPassword">
                  {{ showCurrentPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>

            <div class="form-group">
              <label>Новый пароль</label>
              <div class="password-input-wrapper">
                <input 
                  :type="showNewPassword ? 'text' : 'password'"
                  v-model="formData.new_password"
                  placeholder="Введите новый пароль"
                  class="form-input"
                />
                <button type="button" class="toggle-password" @click="showNewPassword = !showNewPassword">
                  {{ showNewPassword ? '🙈' : '👁️' }}
                </button>
              </div>
              <div class="password-hint">
                Пароль должен содержать не менее 8 символов
              </div>
            </div>

            <div class="form-group">
              <label>Подтверждение нового пароля</label>
              <div class="password-input-wrapper">
                <input 
                  :type="showConfirmPassword ? 'text' : 'password'"
                  v-model="formData.confirm_password"
                  placeholder="Подтвердите новый пароль"
                  class="form-input"
                />
                <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword">
                  {{ showConfirmPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-submit" :disabled="loading">
                {{ loading ? 'Сохранение...' : 'Изменить пароль' }}
              </button>
              <button type="button" class="btn-cancel" @click="$router.back()">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import AppSidebar from '@/components/AppSidebar.vue'
import { authHeaders } from '@/utils/api.js'

const API_BASE = import.meta?.env?.VITE_API_BASE ?? 'http://localhost:8000'

export default {
  name: 'ChangePassword',
  components: { AppSidebar },

  data() {
    return {
      loading: false,
      error: null,
      success: false,
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      formData: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
  },

  methods: {
    async changePassword() {
      this.error = null
      this.success = false

      // Валидация
      if (!this.formData.current_password) {
        this.error = 'Введите текущий пароль'
        return
      }
      if (!this.formData.new_password) {
        this.error = 'Введите новый пароль'
        return
      }
      if (this.formData.new_password.length < 8) {
        this.error = 'Новый пароль должен содержать не менее 8 символов'
        return
      }
      if (this.formData.new_password !== this.formData.confirm_password) {
        this.error = 'Новый пароль и подтверждение не совпадают'
        return
      }

      this.loading = true

      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.error = 'Необходима авторизация'
          this.loading = false
          return
        }

        const response = await fetch(`${API_BASE}/api/auth/change-password/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            current_password: this.formData.current_password,
            new_password: this.formData.new_password
          })
        })

        const data = await response.json()

        if (response.ok) {
          this.success = true
          this.formData = {
            current_password: '',
            new_password: '',
            confirm_password: ''
          }
          // Через 2 секунды возвращаемся на главную
          setTimeout(() => {
            this.$router.push('/')
          }, 2000)
        } else {
          this.error = data.error || data.detail || 'Ошибка при смене пароля'
        }
      } catch (err) {
        console.error('Ошибка:', err)
        this.error = 'Ошибка соединения с сервером'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  font-family: 'PT Sans', 'Helvetica Neue', Arial, sans-serif;
  background: #f0efee;
  color: #1a1a1a;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 32px 40px;
  min-width: 0;
}

.main-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  padding: 4px 0;
  transition: color .15s;
}

.btn-back svg {
  width: 18px;
  height: 18px;
}

.btn-back:hover {
  color: #1a1a1a;
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -.3px;
  margin: 0;
}

.change-password-container {
  max-width: 500px;
  margin: 0 auto;
  width: 100%;
}

.info-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0efee;
}

.card-icon {
  width: 22px;
  height: 22px;
  color: #888780;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #444;
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  flex: 1;
  padding: 10px 40px 10px 12px;
  border: 1px solid #c8c5c0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color .15s;
}

.form-input:focus {
  outline: none;
  border-color: #888780;
  box-shadow: 0 0 0 3px rgba(136,135,128,0.12);
}

.toggle-password {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
}

.password-hint {
  font-size: 11px;
  color: #888;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.btn-submit {
  flex: 1;
  padding: 10px 20px;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background .15s;
}

.btn-submit:hover:not(:disabled) {
  background: #333;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-cancel {
  padding: 10px 24px;
  background: #f0efee;
  border: 1px solid #c8c5c0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
}

.btn-cancel:hover {
  background: #e9e7e3;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 20px;
}

.success-message {
  background: #e8f4ea;
  border: 1px solid #b6ddb9;
  color: #2e7d42;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 20px;
}
</style>