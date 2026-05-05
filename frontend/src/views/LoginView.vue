<template>
  <div class="wrapper">
    <div class="card">
      <h1>С возвращением!</h1>

      <label>Адрес почты</label>
      <input type="email" v-model="email" />

      <label>Пароль</label>
      <input type="password" v-model="password" />

      <div class="forgot">Забыли пароль?</div>

      <button @click="login">Войти</button>

      <div class="bottom">
        Нет аккаунта?
        <router-link to="/register">Зарегистрироваться</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

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

      // сюда обычно кладут токен
      localStorage.setItem('token', data.access)

      alert('Вход выполнен')
    } else {
      const error = await response.json()
      console.log('LOGIN ERROR:', error)
      alert('Ошибка входа')
    }

  } catch (err) {
    console.error(err)
    alert('Ошибка сервера')
  }
}
</script>

<style scoped>
.wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #e5e5e5;
}

.card {
  background: #f3f3f3;
  padding: 40px;
  border-radius: 16px;
  width: 350px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
}

label {
  display: block;
  text-align: left;
  margin: 10px 0 5px;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: none;
  background: #ddd;
}

.forgot {
  text-align: right;
  font-size: 12px;
  margin: 5px 0 20px;
  color: gray;
}

button {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: #cfcfcf;
  cursor: pointer;
}

.bottom {
  margin-top: 15px;
  font-size: 12px;
}
</style>