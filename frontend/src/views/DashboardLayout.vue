<template>
  <div class="layout">
    <Sidebar />

    <main class="content">
      <slot />
    </main>
  </div>
</template>

<script setup>
import Sidebar from '@/views/HomeView.vue'
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 32px;
  background: #fafafa;
}
</style>