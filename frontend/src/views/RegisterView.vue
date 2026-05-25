<template>
  <div class="wrapper">
    <div class="card">
      <h1>Создайте аккаунт</h1>

      <label>Имя Фамилия</label>
      <input type="text" v-model="name" />

      <label>Адрес почты</label>
      <input type="email" v-model="email" />

      <label>Пароль</label>
      <input type="password" v-model="password" />

      <label>Повторите пароль</label>
      <input type="password" v-model="repeatPassword" />

      <button @click="register">Зарегистрироваться</button>

      <div class="bottom">
      
        <router-link to="/home">Войти как гость</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const API = 'http://localhost:8000'

const name = ref('')
const email = ref('')
const password = ref('')
const repeatPassword = ref('')

const register = async () => {
  if (password.value !== repeatPassword.value) {
    alert('Пароли не совпадают')
    return
  }

  try {
    const response = await fetch(`${API}/api/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        full_name: name.value,
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      console.log('Пользователь создан:', data)
      alert('Регистрация успешна')

      // очистка формы
      name.value = ''
      email.value = ''
      password.value = ''
      repeatPassword.value = ''
    } else {
      console.log('Ошибка:', data)
      alert('Ошибка регистрации')
    }

  } catch (error) {
    console.error(error)
    alert('Ошибка сервера (backend недоступен)')
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

button {
  margin-top: 20px;
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