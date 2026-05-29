<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <img src="/favicon.ico" alt="Лого" class="auth-logo" />
        <h1>С возвращением!</h1>
        <p>Войдите в свой аккаунт</p>
      </div>

      <form @submit.prevent="login">
        <div class="form-group">
          <label>Электронная почта</label>
          <input 
            type="email" 
            v-model="email" 
            placeholder="example@mail.ru"
            class="auth-input"
          />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input 
            type="password" 
            v-model="password" 
            placeholder="••••••••"
            class="auth-input"
          />
        </div>

        <div class="forgot-link">
          <a href="#">Забыли пароль?</a>
        </div>

        <button type="submit" class="auth-btn">Войти</button>

        <div class="auth-footer">
          Нет аккаунта?
          <router-link to="/register">Зарегистрироваться</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const login = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    if (response.ok) {
      const data = await response.json()
      console.log('LOGIN SUCCESS:', data)

      localStorage.setItem('token', data.access)
      alert('Вход выполнен')
      
      // Перенаправление на главную после входа
      router.push('/')
    } else {
      const error = await response.json()
      console.log('LOGIN ERROR:', error)
      alert('Неверный email или пароль')
    }

  } catch (err) {
    console.error(err)
    alert('Ошибка подключения к серверу')
  }
}
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 28px;
  padding: 48px 40px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-logo {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
}

.auth-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #212529;
  margin: 0 0 8px 0;
}

.auth-header p {
  font-size: 14px;
  color: #6c757d;
  margin: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #343a40;
}

.auth-input {
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid #e9ecef;
  border-radius: 14px;
  font-size: 15px;
  transition: all 0.2s;
  background: white;
  box-sizing: border-box;
}

.auth-input:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.auth-input::placeholder {
  color: #adb5bd;
}

.forgot-link {
  text-align: right;
  margin-bottom: 24px;
}

.forgot-link a {
  font-size: 13px;
  color: #6c757d;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link a:hover {
  color: #0d6efd;
}

.auth-btn {
  width: 100%;
  padding: 12px 24px;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 24px;
}

.auth-btn:hover {
  background: #0b5ed7;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.auth-btn:active {
  transform: translateY(0);
}

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #6c757d;
  padding-top: 16px;
  border-top: 1px solid #e9ecef;
}

.auth-footer a {
  color: #0d6efd;
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
  transition: color 0.2s;
}

.auth-footer a:hover {
  color: #0b5ed7;
  text-decoration: underline;
}
</style>