<template>
  <DashboardLayout>
    <div class="page">
      <div class="left-column">
        <h1>Заполнение данных</h1>

        <div class="form-grid">
          <input placeholder="Имя" />
          <input placeholder="Фамилия" />
          <input placeholder="Дата рождения" />
          <input placeholder="Место рождения" />
        </div>

        <RelativeBlock title="О родителях" />

        <RelativeBlock title="Жених" />

        <div class="actions">
          <button class="secondary">Сохранить в черновик</button>
          <button class="primary">Продолжить</button>
        </div>
      </div>

      <div class="right-column">
        <ScanViewer />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/views/DashboardLayout.vue'
import RelativeBlock from '@/views/RelativeBlock.vue'
import ScanViewer from '@/views/ScanViewer.vue'
</script>

<style scoped>
.page {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 24px 0;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
}

.primary {
  background: #8b7b7b;
  color: white;
}

.secondary {
  background: white;
}

button {
  padding: 12px 18px;
  border-radius: 10px;
  border: 1px solid #ccc;
  cursor: pointer;
}
</style>