<template>
  <div class="register-layout">
    <div class="register-card">
      <div class="register-header">
        <h1 class="register-title">Создание аккаунта</h1>
        <p class="register-subtitle">Заполните форму ниже</p>
      </div>

      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Имя и фамилия
          </label>
          <input 
            type="text" 
            v-model="fullName" 
            placeholder="Иван Иванов"
            class="form-input"
            :class="{ 'input-error': validationErrors.fullName }"
            @input="clearError('fullName')"
          />
          <div v-if="validationErrors.fullName" class="field-error">{{ validationErrors.fullName }}</div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            Электронная почта
          </label>
          <input 
            type="email" 
            v-model="email" 
            placeholder="example@mail.ru"
            class="form-input"
            :class="{ 'input-error': validationErrors.email }"
            @input="clearError('email')"
          />
          <div v-if="validationErrors.email" class="field-error">{{ validationErrors.email }}</div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            Пароль
          </label>
          <div class="password-wrapper">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="password" 
              placeholder="••••••••"
              class="form-input"
              :class="{ 'input-error': validationErrors.password }"
              @input="clearError('password')"
            />
            <button 
              type="button" 
              class="password-toggle" 
              @click="showPassword = !showPassword"
              tabindex="-1"
            >
              <svg v-if="!showPassword" class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
          <div v-if="validationErrors.password" class="field-error">{{ validationErrors.password }}</div>
          <div class="password-hint">Пароль должен содержать минимум 6 символов</div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              <line x1="12" y1="15" x2="12" y2="15" stroke-width="2"/>
            </svg>
            Повторите пароль
          </label>
          <div class="password-wrapper">
            <input 
              :type="showRepeatPassword ? 'text' : 'password'" 
              v-model="repeatPassword" 
              placeholder="••••••••"
              class="form-input"
              :class="{ 'input-error': validationErrors.repeatPassword }"
              @input="clearError('repeatPassword')"
            />
            <button 
              type="button" 
              class="password-toggle" 
              @click="showRepeatPassword = !showRepeatPassword"
              tabindex="-1"
            >
              <svg v-if="!showRepeatPassword" class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
          <div v-if="validationErrors.repeatPassword" class="field-error">{{ validationErrors.repeatPassword }}</div>
        </div>

        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <div v-if="error" class="error-message">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <circle cx="12" cy="16" r="0.5" fill="currentColor" stroke="none"/>
          </svg>
          {{ error }}
        </div>

        <div class="register-footer">
          <span class="footer-text">Уже есть аккаунт?</span>
          <router-link to="/login" class="login-link">Войти</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = import.meta?.env?.VITE_API_BASE ?? 'http://localhost:8000'
const router = useRouter()

const fullName = ref('')
const email = ref('')
const password = ref('')
const repeatPassword = ref('')
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const showRepeatPassword = ref(false)

const validationErrors = ref({
  fullName: '',
  email: '',
  password: '',
  repeatPassword: ''
})

const validateForm = () => {
  let isValid = true
  
  // Проверка имени
  if (!fullName.value.trim()) {
    validationErrors.value.fullName = 'Укажите имя и фамилию'
    isValid = false
  } else if (fullName.value.trim().length < 3) {
    validationErrors.value.fullName = 'Имя должно содержать минимум 3 символа'
    isValid = false
  } else {
    validationErrors.value.fullName = ''
  }
  
  // Проверка email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value.trim()) {
    validationErrors.value.email = 'Укажите адрес электронной почты'
    isValid = false
  } else if (!emailRegex.test(email.value)) {
    validationErrors.value.email = 'Введите корректный email адрес'
    isValid = false
  } else {
    validationErrors.value.email = ''
  }
  
  // Проверка пароля
  if (!password.value) {
    validationErrors.value.password = 'Введите пароль'
    isValid = false
  } else if (password.value.length < 6) {
    validationErrors.value.password = 'Пароль должен содержать минимум 6 символов'
    isValid = false
  } else {
    validationErrors.value.password = ''
  }
  
  // Проверка повторения пароля
  if (!repeatPassword.value) {
    validationErrors.value.repeatPassword = 'Повторите пароль'
    isValid = false
  } else if (password.value !== repeatPassword.value) {
    validationErrors.value.repeatPassword = 'Пароли не совпадают'
    isValid = false
  } else {
    validationErrors.value.repeatPassword = ''
  }
  
  return isValid
}

const clearError = (field) => {
  validationErrors.value[field] = ''
  error.value = ''
}

const register = async () => {
  error.value = ''
  
  if (!validateForm()) {
    return
  }
  
  loading.value = true

  try {
    const response = await fetch(`${API_BASE}/api/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        full_name: fullName.value.trim(),
        email: email.value.trim(),
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      // Автоматический вход после регистрации
      const loginResponse = await fetch(`${API_BASE}/api/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.value.trim(),
          password: password.value
        })
      })
      
      const loginData = await loginResponse.json()
      
      if (loginResponse.ok) {
        localStorage.setItem('access_token', loginData.access)
        localStorage.setItem('refresh_token', loginData.refresh)
        router.push('/home')
      } else {
        // Если автоматический вход не удался, перенаправляем на страницу входа
        router.push('/login')
      }
    } else {
      error.value = data.detail || data.email?.[0] || 'Ошибка регистрации. Попробуйте другой email.'
    }
  } catch (err) {
    console.error(err)
    error.value = 'Ошибка соединения с сервером'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.register-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0efee;
  font-family: 'PT Sans', 'Helvetica Neue', Arial, sans-serif;
  padding: 20px;
}

.register-card {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 480px;
  padding: 40px 36px;
  transition: transform 0.2s ease;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.3px;
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: 14px;
  color: #888780;
  font-weight: 400;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #444;
  letter-spacing: 0.3px;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #888780;
}

.password-wrapper {
  position: relative;
  width: 100%;
}

.form-input {
  padding: 11px 14px;
  border: 1.5px solid #e0dedb;
  border-radius: 12px;
  font-size: 14px;
  font-family: inherit;
  color: #1a1a1a;
  background: #fff;
  transition: all 0.2s ease;
  width: 100%;
  outline: none;
}

.password-wrapper .form-input {
  padding-right: 45px;
}

.form-input:focus {
  border-color: #b0ada8;
  box-shadow: 0 0 0 3px rgba(136, 135, 128, 0.12);
}

.form-input.input-error {
  border-color: #dc2626;
  background-color: #fef2f2;
}

.form-input.input-error:focus {
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  transition: color 0.15s;
}

.password-toggle:hover {
  color: #666;
}

.toggle-icon {
  width: 20px;
  height: 20px;
}

.field-error {
  font-size: 11px;
  color: #dc2626;
  margin-top: 2px;
  font-weight: 500;
}

.password-hint {
  font-size: 11px;
  color: #aaa;
  margin-top: 2px;
}

.btn-submit {
  padding: 12px 20px;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 40px;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-submit:hover:not(:disabled) {
  background: #333;
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #991b1b;
  font-size: 13px;
}

.error-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.register-footer {
  text-align: center;
  padding-top: 12px;
  font-size: 13px;
  color: #888780;
  display: flex;
  justify-content: center;
  gap: 6px;
}

.footer-text {
  color: #888780;
}

.login-link {
  color: #1a1a1a;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.15s;
}

.login-link:hover {
  color: #555;
  text-decoration: none;
}

@media (max-width: 500px) {
  .register-card {
    padding: 32px 24px;
  }
  
  .register-title {
    font-size: 24px;
  }
}
</style>