<template>
  <div class="death-layout">
    <!-- Левая панель — форма -->
    <div class="form-panel">
      <h2>Заполнение данных</h2>

      <div class="form-grid">
        <div class="field">
          <label>Архив</label>
          <input type="text" placeholder="Введите архив" />
        </div>
        <div class="field">
          <label>Номер дела</label>
          <input type="text" placeholder="Номер дела" />
        </div>
        <div class="field">
          <label>Год индексации</label>
          <input type="text" placeholder="Год" />
        </div>
        <div class="field">
          <label>Номер листа</label>
          <input type="text" placeholder="Лист" />
        </div>

        <h3 class="full-width">Об умершем</h3>

        <div class="field">
          <label>Пол</label>
          <select>
            <option>Мужской</option>
            <option>Женский</option>
          </select>
        </div>
        <div class="field">
          <label>Номер записи</label>
          <input type="text" />
        </div>

        <div class="field">
          <label>Месяц смерти</label>
          <input type="text" placeholder="Месяц" />
        </div>
        <div class="field">
          <label>Число смерти</label>
          <input type="number" />
        </div>
        <div class="field">
          <label>Число погребения</label>
          <input type="number" />
        </div>

        <div class="field">
          <label>Населенный пункт</label>
          <input type="text" />
        </div>
        <div class="field">
          <label>Сословие</label>
          <input type="text" />
        </div>

        <div class="field">
          <label>Имя</label>
          <input type="text" />
        </div>
        <div class="field">
          <label>Отчество</label>
          <input type="text" />
        </div>
        <div class="field">
          <label>Фамилия</label>
          <input type="text" />
        </div>

        <div class="field age-field">
          <label>Возраст</label>
          <div class="age-controls">
            <input type="number" value="0" />
            <button>+</button>
            <button>-</button>
          </div>
        </div>
      </div>  <!-- ← закрывающий .form-grid -->

      <div class="footer-bar">
        <div class="actions">
          <button class="draft">Сохранить в черновики</button>
          <button class="continue">Продолжить</button>
        </div>
      </div>
    </div>  <!-- ← закрывающий .form-panel -->

    <!-- Правая панель — изображение -->
    <div class="scan-panel">
      <div class="scan-placeholder">
        <img src="/image.png" alt="Скан документа" />
        <div class="scan-controls">
          <button>−</button>
          <span>Zoom</span>
          <button>+</button>
        </div>
      </div>
    </div>
  </div>  <!-- ← закрывающий .death-layout -->
</template>

<style scoped>
.death-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.form-panel {
  width: 33.333%;
  overflow-y: auto;
  padding: 20px;
  background: #fff;
  border-right: 1px solid #ddd;
  box-sizing: border-box;
}

.scan-panel {
  width: 66.666%;
  background: #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.scan-placeholder {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scan-placeholder img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.scan-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(0,0,0,0.6);
  padding: 8px 12px;
  border-radius: 8px;
  color: white;
  display: flex;
  gap: 12px;
}

.scan-controls button {
  background: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
}

.full-width {
  grid-column: span 2;
}

label {
  font-weight: bold;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

input, select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.age-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.age-controls button {
  width: 32px;
  background: #eee;
  border: none;
  cursor: pointer;
  border-radius: 6px;
}

.footer-bar {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #eee;
  padding-top: 16px;
}

.actions {
  display: flex;
  gap: 12px;
}

.draft {
  background: #f0f0f0;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.continue {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
}
</style>