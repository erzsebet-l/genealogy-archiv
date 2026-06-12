<!-- components/PersonSearch.vue -->
<template>
  <div class="person-search">
    <div class="combobox-wrap">
      <input
        type="text"
        v-model="searchText"
        @input="onSearchInput"
        @focus="dropOpen = true"
        @blur="closeDrop"
        :placeholder="placeholder"
        autocomplete="off"
        class="combo-input"
        :class="{ 'has-value': selectedPerson }"
      />
      <ul v-show="dropOpen && searchResults.length > 0" class="drop-list">
        <li
          v-for="person in searchResults"
          :key="person.person_id"
          @mousedown.prevent="selectPerson(person)"
          class="drop-item"
        >
          <div class="drop-main">{{ getFullName(person) }}</div>
          <div class="drop-sub">
            <span v-if="person.date">📅 {{ formatDate(person.date) }}</span>
            <span v-if="person.estate_name"> | {{ person.estate_name }}</span>
            <span v-if="person.village_name"> | {{ person.village_name }}</span>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- Модальное окно для подтверждения дубликата -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click.self="showDuplicateModal = false">
      <div class="modal duplicate-modal">
        <div class="warning-icon">⚠️</div>
        <h4>Найдена похожая персона</h4>
        <div class="duplicate-info">
          <p><strong>{{ getFullName(duplicateCandidate) }}</strong></p>
          <div class="person-details">
            <div><strong>Дата рождения:</strong> {{ formatDate(duplicateCandidate.date) || '—' }}</div>
            <div><strong>Сословие:</strong> {{ duplicateCandidate.estate_name || '—' }}</div>
            <div><strong>Населенный пункт:</strong> {{ duplicateCandidate.village_name || '—' }}</div>
          </div>
          <div class="related-records">
            <strong>Участвует в записях:</strong>
            <ul>
              <li v-for="record in duplicateCandidate.related_records" :key="record.id">
                {{ record.type_label }} от {{ formatDate(record.date) }}
              </li>
              <li v-if="!duplicateCandidate.related_records?.length">Нет связанных записей</li>
            </ul>
          </div>
        </div>
        <p class="confirm-text">Это та же персона?</p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="rejectDuplicate">Нет, создать новую</button>
          <button type="button" class="btn-confirm" @click="acceptDuplicate">Да, использовать существующую</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = import.meta?.env?.VITE_API_BASE ?? 'http://localhost:8000'


export default {
  name: 'PersonSearch',
  props: {
    value: {
      type: Object,
      default: null
    },
    placeholder: {
      type: String,
      default: 'Начните вводить ФИО...'
    },
    sex: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      searchText: '',
      searchResults: [],
      dropOpen: false,
      selectedPerson: null,
      showDuplicateModal: false,
      duplicateCandidate: null,
      pendingNewPersonData: null,
      searchTimer: null
    }
  },
  watch: {
    value: {
      handler(val) {
        if (val) {
          this.selectedPerson = val
          this.searchText = this.getFullName(val)
        }
      },
      immediate: true
    }
  },
  methods: {
    getFullName(person) {
      const parts = []
      if (person.surname) parts.push(person.surname)
      if (person.name) parts.push(person.name)
      if (person.patronymic) parts.push(person.patronymic)
      return parts.length ? parts.join(' ') : '—'
    },
    formatDate(isoDate) {
      if (!isoDate) return ''
      const [y, m, d] = isoDate.split('-')
      return `${d}.${m}.${y}`
    },
    async onSearchInput() {
      clearTimeout(this.searchTimer)
      const q = this.searchText.trim()
      if (q.length < 2) {
        this.searchResults = []
        return
      }
      
      this.searchTimer = setTimeout(async () => {
        try {
          const headers = { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          let url = `${API_BASE}/api/persons-search/?q=${encodeURIComponent(q)}`
          if (this.sex) {
            url += `&sex=${this.sex}`
          }
          const response = await fetch(url, { headers })
          if (response.ok) {
            const data = await response.json()
            this.searchResults = data.results || data.persons || []
          }
        } catch (err) {
          console.error('Search error:', err)
        }
      }, 300)
    },
    closeDrop() {
      setTimeout(() => { this.dropOpen = false }, 200)
    },
    selectPerson(person) {
      this.selectedPerson = person
      this.searchText = this.getFullName(person)
      this.dropOpen = false
      this.$emit('input', person)
      this.$emit('select', person)
    },
    async checkForDuplicate(personData) {
      // Проверяем, есть ли уже такая персона в БД
      try {
        const headers = { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        const query = new URLSearchParams({
          surname: personData.surname || '',
          name: personData.name || '',
          patronymic: personData.patronymic || '',
          sex: personData.sex || ''
        }).toString()
        
        const response = await fetch(`${API_BASE}/api/persons/find-duplicate/?${query}`, { headers })
        if (response.ok) {
          const result = await response.json()
          if (result.found && result.person) {
            this.duplicateCandidate = result.person
            this.pendingNewPersonData = personData
            this.showDuplicateModal = true
            return true
          }
        }
        return false
      } catch (err) {
        console.error('Duplicate check error:', err)
        return false
      }
    },
    acceptDuplicate() {
      this.selectPerson(this.duplicateCandidate)
      this.showDuplicateModal = false
      this.$emit('duplicate-resolved', { action: 'use-existing', person: this.duplicateCandidate })
    },
    rejectDuplicate() {
      this.showDuplicateModal = false
      // Создаем новую персону с увеличенным дубликатом
      const newPersonData = { ...this.pendingNewPersonData }
      newPersonData.duplicate = (this.duplicateCandidate?.duplicate || 0) + 1
      this.$emit('duplicate-resolved', { action: 'create-new', personData: newPersonData })
      this.pendingNewPersonData = null
    },
    clear() {
      this.selectedPerson = null
      this.searchText = ''
      this.$emit('input', null)
    }
  }
}
</script>

<style scoped>
.person-search {
  width: 100%;
}

.combobox-wrap {
  position: relative;
}

.combo-input {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
}

.combo-input.has-value {
  background: #f0fdf4;
  border-color: #86efac;
}

.drop-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  z-index: 100;
  max-height: 250px;
  overflow-y: auto;
  list-style: none;
  padding: 4px 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.drop-item {
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid #e9e7e3;
}

.drop-item:hover {
  background: #f0efee;
}

.drop-main {
  font-size: 13px;
  font-weight: 500;
  color: #1a1a1a;
}

.drop-sub {
  font-size: 11px;
  color: #888;
  margin-top: 2px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.duplicate-modal {
  max-width: 500px;
  width: 90%;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
}

.warning-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.duplicate-info {
  text-align: left;
  background: #f8f7f5;
  border-radius: 8px;
  padding: 12px;
  margin: 12px 0;
}

.person-details {
  margin: 12px 0;
  padding: 8px;
  background: #fff;
  border-radius: 6px;
}

.person-details div {
  margin: 4px 0;
  font-size: 13px;
}

.related-records {
  margin-top: 12px;
  padding: 8px;
  background: #fff;
  border-radius: 6px;
  font-size: 12px;
}

.related-records ul {
  margin: 8px 0 0 20px;
}

.btn-confirm {
  background: #10b981;
  color: white;
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-confirm:hover {
  background: #059669;
}
</style>