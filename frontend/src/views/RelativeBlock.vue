<template>
  <div class="relative-block">
    <h3>{{ title }}</h3>

    <div class="grid">
      <input placeholder="Имя" />
      <input placeholder="Фамилия" />
      <input placeholder="Возраст" />
      <input placeholder="Статус" />
    </div>

    <button class="add-btn">+ Добавить родственника</button>
  </div>
</template>

<script setup>
defineProps({
  title: String
})
</script>

<style scoped>
.relative-block {
  margin-bottom: 32px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 12px;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d6d6d6;
}

.add-btn {
  margin-top: 12px;
  border: none;
  background: transparent;
  cursor: pointer;
}
</style>
