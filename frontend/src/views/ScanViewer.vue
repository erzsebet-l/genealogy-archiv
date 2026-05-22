<template>
  <div class="viewer">
    <div class="toolbar">
      <span>Просмотр скана</span>

      <div class="actions">
        <button>🔍</button>
        <button>➕</button>
      </div>
    </div>

    <div class="canvas">
      <img v-if="image" :src="image" alt="scan" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  image: String
})
</script>

<style scoped>
.viewer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.canvas {
  background: #e5e5e5;
  border-radius: 10px;
  min-height: 500px;
  overflow: hidden;
}

.canvas img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>