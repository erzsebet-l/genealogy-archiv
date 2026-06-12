<template>
  <div class="app-layout">
    <AppSidebar :isAdmin="isAdmin" />

    <main class="main-content">
      <AppHeader :user-name="userName" :isAdmin="isAdmin" />

      <section class="records-section">
        <!-- Заголовок + счётчики -->
        <div class="section-top">
          <h2 class="section-label">Мои записи</h2>
          <div v-if="!loading && !error" class="counts-row">
            <template v-if="statusFilter === 'published'">
              <span
                v-for="(badge, key) in badgeConfig"
                :key="key"
                :class="['count-badge', `badge-${key}`, { active: activeFilter === key }]"
                @click="toggleFilter(key)"
              >
                {{ badge.label }}: {{ publishedCounts[key] ?? 0 }}
              </span>
              <span
                :class="['count-badge', 'badge-all', { active: activeFilter === null }]"
                @click="toggleFilter(null)"
              >
                Все: {{ totalPublishedCount }}
              </span>
            </template>
            
            <template v-else>
              <span
                v-for="(badge, key) in badgeConfig"
                :key="key"
                :class="['count-badge', `badge-${key}`, { active: activeFilter === key }]"
                @click="toggleFilter(key)"
              >
                {{ badge.label }}: {{ draftCounts[key] ?? 0 }}
              </span>
              <span
                :class="['count-badge', 'badge-all', { active: activeFilter === null }]"
                @click="toggleFilter(null)"
              >
                Все: {{ totalDraftCount }}
              </span>
            </template>
          </div>
        </div>

        <div class="toolbar-row">
          <div class="search-bar">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск по записям"
              class="search-input"
            />
          </div>

          <div class="status-filter">
            <button
              :class="['sf-btn', { active: statusFilter === 'published' }]"
              @click="switchToPublished"
            >
              <span class="sf-dot pub"></span> Опубликованные
              <span v-if="totalPublishedCount > 0" class="sf-count">{{ totalPublishedCount }}</span>
            </button>
            <button
              :class="['sf-btn', { active: statusFilter === 'draft' }]"
              @click="switchToDrafts"
            >
              <span class="sf-dot draft"></span> Черновики
              <span v-if="totalDraftCount > 0" class="sf-count draft-count">{{ totalDraftCount }}</span>
            </button>
          </div>
        </div>

        <div v-if="loading" class="state-box">
          <span class="spinner"></span>
          <span>Загрузка данных…</span>
        </div>

        <div v-else-if="error" class="state-box error-box">
          <span>{{ error }}</span>
          <button class="retry-btn" @click="fetchRecords">Повторить</button>
        </div>

        <!-- Таблица опубликованных -->
        <div v-else-if="statusFilter === 'published'" class="table-wrapper">
          <table class="records-table">
            <thead>
              <tr>
                <th>Тип</th>
                <th>Описание</th>
                <th>Дата</th>
                <th>Архив</th>
                <th>Лист / Запись</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in filteredRecords" :key="`${rec.type}-${rec.id}`" class="table-row">
                <td><span :class="['type-pill', `pill-${rec.type}`]">{{ rec.type_label }}</span></td>
                <td class="col-desc">{{ rec.description }}</td>
                <td class="col-date">{{ formatDate(rec.date) }}</td>
                <td class="col-archive">{{ rec.archive }}</td>
                <td class="col-page">{{ rec.page }} / {{ rec.number_record }}</td>
                <td class="col-actions">
                  <div class="record-actions">
                    <button class="action-btn edit-btn" @click="editPublishedRecord(rec)" title="Редактировать">✏ Редактировать</button>
                    <button class="action-btn del-btn" @click="openRecordDeleteConfirm(rec)" title="Удалить">✕ Удалить</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredRecords.length === 0">
                <td colspan="6" class="no-results">Записи не найдены</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Таблица черновиков -->
        <div v-else class="table-wrapper">
          <table class="records-table">
            <thead>
              <tr>
                <th>Тип</th>
                <th>Описание</th>
                <th>Изменён</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="draft in filteredDrafts" :key="draft.draft_id" class="table-row">
                <td><span :class="['type-pill', `pill-${draft.record_type}`]">{{ typeLabels[draft.record_type] || draft.record_type }}</span></td>
                <td class="col-desc">{{ draft.description }}</td>
                <td class="col-date">{{ formatDateTime(draft.updated_at) }}</td>
                <td class="col-actions">
                  <div class="draft-actions">
                    <button class="action-btn edit-btn" @click="editDraft(draft)" title="Редактировать">✏ Редактировать</button>
                    <button class="action-btn del-btn" @click="openDraftDeleteConfirm(draft)" title="Удалить">✕</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredDrafts.length === 0">
                <td colspan="4" class="no-results">Черновиков нет</td>
              </tr>
            </tbody>
          </table>
        </div>

      </section>
    </main>

    <!-- Диалог подтверждения удаления публикации -->
    <div v-if="showRecordDeleteConfirm" class="modal-overlay" @click.self="showRecordDeleteConfirm = false">
      <div class="modal confirm-modal">
        <div class="confirm-icon">🗑️</div>
        <h4>Удалить запись?</h4>
        <p class="confirm-text">
          Запись будет удалена из базы данных без возможности восстановления.
          Убедитесь, что вы хотите выполнить это действие.
        </p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="showRecordDeleteConfirm = false">Отмена</button>
          <button type="button" class="btn-confirm-publish" @click="confirmRecordDelete" :disabled="loading">
            {{ loading ? 'Удаление...' : 'Да, удалить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Диалог подтверждения удаления черновика -->
    <div v-if="showDraftDeleteConfirm" class="modal-overlay" @click.self="showDraftDeleteConfirm = false">
      <div class="modal confirm-modal">
        <div class="confirm-icon">🗑️</div>
        <h4>Удалить черновик?</h4>
        <p class="confirm-text">
          Черновик будет удален без возможности восстановления. Убедитесь, что вы хотите выполнить это действие.
        </p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="showDraftDeleteConfirm = false">Отмена</button>
          <button type="button" class="btn-confirm-publish" @click="confirmDraftDelete" :disabled="loading">
            {{ loading ? 'Удаление...' : 'Да, удалить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Диалог успешного удаления -->
    <div v-if="showDeleteSuccess" class="modal-overlay">
      <div class="modal success-modal">
        <div class="success-icon">✅</div>
        <h4>{{ deleteSuccessMessage }}</h4>
        <p class="success-text">{{ deleteSuccessText }}</p>
        <button type="button" class="btn-ok" @click="closeDeleteSuccess">OK</button>
      </div>
    </div>

  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import { api, authHeaders } from '@/utils/api.js'

export default {
  name: 'HomeView',
  components: { AppHeader, AppSidebar },

  data() {
    return {
      userName: '',
      isAdmin: false,
      allRecords: [],
      drafts: [],
      publishedCounts: { birth: 0, marriage: 0, death: 0 },
      draftCounts: { birth: 0, marriage: 0, death: 0 },
      loading: false,
      error: null,
      searchQuery: '',
      activeFilter: null,
      statusFilter: 'published',

      showRecordDeleteConfirm: false,
      showDraftDeleteConfirm: false,
      showDeleteSuccess: false,
      deleteSuccessMessage: '',
      deleteSuccessText: '',
      recordToDelete: null,
      draftToDelete: null,

      badgeConfig: {
        birth:    { label: 'Рождения' },
        marriage: { label: 'Браки'    },
        death:    { label: 'Смерти'   },
      },

      typeLabels: {
        birth:    'Рождение',
        marriage: 'Брак',
        death:    'Смерть',
      },
    }
  },

  computed: {
    totalPublishedCount() {
      return (this.publishedCounts.birth ?? 0) + (this.publishedCounts.marriage ?? 0) + (this.publishedCounts.death ?? 0)
    },

    totalDraftCount() {
      return (this.draftCounts.birth ?? 0) + (this.draftCounts.marriage ?? 0) + (this.draftCounts.death ?? 0)
    },

    filteredRecords() {
      let list = this.allRecords
      if (this.activeFilter) list = list.filter(r => r.type === this.activeFilter)
      const q = this.searchQuery.trim().toLowerCase()
      if (q) {
        list = list.filter(r =>
          (r.description || '').toLowerCase().includes(q) ||
          (r.archive || '').toLowerCase().includes(q) ||
          (r.date || '').includes(q)
        )
      }
      return list
    },

    filteredDrafts() {
      let list = this.drafts
      if (this.activeFilter) list = list.filter(d => d.record_type === this.activeFilter)
      const q = this.searchQuery.trim().toLowerCase()
      if (q) {
        list = list.filter(d =>
          (d.description || '').toLowerCase().includes(q) ||
          (d.record_type || '').includes(q)
        )
      }
      return list
    },
  },

  async created() {
    await this.fetchRecords()
  },

  methods: {
    async fetchRecords() {
      this.loading = true
      this.error = null

      try {
        const headers = authHeaders()

        const [data, draftsData] = await Promise.all([
          api('/api/home/', { headers }),
          api('/api/drafts/', { headers }).catch(() => null),
        ])

        this.userName = data.user || 'пользователь'
        this.isAdmin = data.user_role === 'admin'

        this.allRecords = (data.records ?? []).map(r => {
          let personId = null

          if (r.person_id) {
            personId = r.person_id
          } else if (r.person && r.person.person_id) {
            personId = r.person.person_id
          } else if (r.person && typeof r.person === 'number') {
            personId = r.person
          }

          return {
            ...r,
            id: r.birth_id ?? r.marriage_id ?? r.death_id ?? r.id,
            person_id: personId,
          }
        })

        this.publishedCounts = data.counts ?? { birth: 0, marriage: 0, death: 0 }

        if (draftsData) {
          const rawDrafts = Array.isArray(draftsData) ? draftsData : (draftsData.results ?? [])

          this.drafts = rawDrafts.map(d => ({
            ...d,
            description: this._draftDescription(d),
          }))

          this.draftCounts = {
            birth: this.drafts.filter(d => d.record_type === 'birth').length,
            marriage: this.drafts.filter(d => d.record_type === 'marriage').length,
            death: this.drafts.filter(d => d.record_type === 'death').length,
          }
        }
      } catch (err) {
        console.error('Error in fetchRecords:', err)
        this.error = err.message || 'Не удалось загрузить данные.'
      } finally {
        this.loading = false
      }
    },

    _draftDescription(draft) {
      const fd = draft.payload?.formData ?? {}
      const name = fd.name || ''
      const surname = fd.father_surname || fd.child_surname || ''
      if (name || surname) return `${surname} ${name}`.trim()
      return `Черновик #${draft.draft_id}`
    },

    switchToPublished() {
      this.statusFilter = 'published'
      this.activeFilter = null
      this.searchQuery = ''
    },

    switchToDrafts() {
      this.statusFilter = 'draft'
      this.activeFilter = null
      this.searchQuery = ''
    },

    toggleFilter(type) {
      this.activeFilter = this.activeFilter === type ? null : type
    },

    formatDate(isoDate) {
      if (!isoDate) return '—'
      const [y, m, d] = isoDate.split('-')
      return `${d}.${m}.${y}`
    },

    formatDateTime(iso) {
      if (!iso) return '—'
      const d = new Date(iso)
      return d.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },

    // Редактирование опубликованной записи
    editPublishedRecord(record) {
      localStorage.setItem('edit_record', JSON.stringify({
        recordId: record.id,
        recordType: record.type,
        personId: record.person_id,
        isEditing: true,
        savedAt: new Date().toISOString(),
      }))

      const routeMap = { birth: '/birth', marriage: '/marriage', death: '/death' }
      this.$router.push(routeMap[record.type] || '/birth')
    },

    editDraft(draft) {
      const payload = {
        ...draft.payload,
        _draftId: draft.draft_id,
        _isEditingDraft: true,
        savedAt: new Date().toISOString(),
      }

      const draftKeyMap = {
        birth: 'birth_draft',
        marriage: 'marriage_draft',
        death: 'death_draft'
      }
      const key = draftKeyMap[draft.record_type] || 'birth_draft'

      localStorage.setItem(key, JSON.stringify(payload))

      const routeMap = { birth: '/birth', marriage: '/marriage', death: '/death' }
      this.$router.push(routeMap[draft.record_type] || '/birth')
    },

    openRecordDeleteConfirm(record) {
      this.recordToDelete = record
      this.showRecordDeleteConfirm = true
    },

    openDraftDeleteConfirm(draft) {
      this.draftToDelete = draft
      this.showDraftDeleteConfirm = true
    },

    async confirmRecordDelete() {
      if (!this.recordToDelete) return

      this.loading = true
      try {
        const typeMap = {
          birth: 'birth-records',
          marriage: 'marriage-records',
          death: 'death-records'
        }
        const endpoint = typeMap[this.recordToDelete.type]

        if (!endpoint) {
          throw new Error('Неизвестный тип записи')
        }

        await api(`/api/${endpoint}/${this.recordToDelete.id}/`, {
          method: 'DELETE',
          headers: authHeaders(),
        })

        this.allRecords = this.allRecords.filter(r => r.id !== this.recordToDelete.id)

        if (this.recordToDelete.type === 'birth') this.publishedCounts.birth--
        if (this.recordToDelete.type === 'marriage') this.publishedCounts.marriage--
        if (this.recordToDelete.type === 'death') this.publishedCounts.death--

        this.showRecordDeleteConfirm = false
        this.deleteSuccessMessage = 'Запись удалена'
        this.deleteSuccessText = `Запись успешно удалена из базы данных.`
        this.showDeleteSuccess = true
        this.recordToDelete = null
      } catch (err) {
        console.error('Ошибка удаления:', err)
        this.error = 'Ошибка удаления: ' + err.message
        setTimeout(() => {
          this.error = null
        }, 3000)
        this.showRecordDeleteConfirm = false
        this.recordToDelete = null
      } finally {
        this.loading = false
      }
    },

    async confirmDraftDelete() {
      if (!this.draftToDelete) return

      this.loading = true
      try {
        await api(`/api/drafts/${this.draftToDelete.draft_id}/`, {
          method: 'DELETE',
          headers: authHeaders(),
        })

        this.drafts = this.drafts.filter(d => d.draft_id !== this.draftToDelete.draft_id)

        if (this.draftToDelete.record_type === 'birth') this.draftCounts.birth--
        if (this.draftToDelete.record_type === 'marriage') this.draftCounts.marriage--
        if (this.draftToDelete.record_type === 'death') this.draftCounts.death--

        this.showDraftDeleteConfirm = false
        this.deleteSuccessMessage = 'Черновик удалён'
        this.deleteSuccessText = 'Черновик успешно удалён.'
        this.showDeleteSuccess = true
        this.draftToDelete = null
      } catch (err) {
        console.error('Ошибка удаления:', err)
        this.error = 'Ошибка удаления: ' + err.message
        setTimeout(() => {
          this.error = null
        }, 3000)
        this.showDraftDeleteConfirm = false
        this.draftToDelete = null
      } finally {
        this.loading = false
      }
    },

    closeDeleteSuccess() {
      this.showDeleteSuccess = false
      this.deleteSuccessMessage = ''
      this.deleteSuccessText = ''
    },

    logout() {
      api('/api/auth/logout/', { method: 'POST' })
        .catch(() => {})
        .finally(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$router.push('/login')
        })
    },
  },
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.app-layout {
  display: flex;
  min-height: 100vh;
  font-family: 'PT Sans', 'Helvetica Neue', Arial, sans-serif;
  background: #f0efee;
  color: #1a1a1a;
}

.main-content { 
  flex: 1; 
  display: flex; 
  flex-direction: column; 
  padding: 32px 40px; 
  min-width: 0; 
}

.section-top { 
  display: flex; 
  align-items: center; 
  gap: 20px; 
  flex-wrap: wrap; 
  margin-bottom: 14px; 
}

.section-label { 
  font-size: 15px; 
  font-weight: 400; 
  color: #444; 
  white-space: nowrap; 
}

.counts-row { 
  display: flex; 
  gap: 8px; 
  flex-wrap: wrap; 
}

.count-badge { 
  padding: 3px 12px; 
  border-radius: 20px; 
  font-size: 12px; 
  font-weight: 600; 
  cursor: pointer; 
  border: 1.5px solid transparent; 
  transition: all .15s; 
  user-select: none; 
}

.badge-birth    { background: #e8f4ea; color: #2e7d42; border-color: #b6ddb9; }
.badge-marriage { background: #e8eef8; color: #2a55a0; border-color: #b3c6e8; }
.badge-death    { background: #faeaea; color: #9b2c2c; border-color: #e8b3b3; }
.badge-all      { background: #f0efee; color: #444;    border-color: #c8c5c0; }

.count-badge.active, 
.count-badge:hover { 
  filter: brightness(0.93); 
  border-color: currentColor; 
}

.toolbar-row { 
  display: flex; 
  align-items: center; 
  gap: 16px; 
  margin-bottom: 18px; 
  flex-wrap: wrap; 
}

.search-bar { 
  position: relative; 
  max-width: 280px; 
  flex-shrink: 0; 
}

.search-icon { 
  position: absolute; 
  left: 10px; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 15px; 
  height: 15px; 
  color: #999; 
  pointer-events: none; 
}

.search-input { 
  width: 100%; 
  padding: 8px 14px 8px 34px; 
  border: 1px solid #ccc; 
  border-radius: 6px; 
  background: #fff; 
  font-size: 13px; 
  color: #333; 
  outline: none; 
  transition: border-color .15s; 
}

.search-input::placeholder { color: #aaa; }
.search-input:focus { border-color: #888; }

.status-filter { 
  display: flex; 
  gap: 0; 
  background: #f0efee; 
  border: 1px solid #d5d3cf; 
  border-radius: 8px; 
  padding: 3px; 
}

.sf-btn { 
  display: flex; 
  align-items: center; 
  gap: 6px; 
  padding: 5px 14px; 
  border: none; 
  border-radius: 6px; 
  font-size: 12px; 
  font-weight: 500; 
  font-family: inherit; 
  cursor: pointer; 
  background: transparent; 
  color: #777; 
  transition: all .15s; 
  white-space: nowrap; 
}

.sf-btn.active { 
  background: #fff; 
  color: #1a1a1a; 
  box-shadow: 0 1px 3px rgba(0,0,0,0.10); 
}

.sf-dot { 
  width: 7px; 
  height: 7px; 
  border-radius: 50%; 
  flex-shrink: 0; 
}

.sf-dot.pub   { background: #22c55e; }
.sf-dot.draft { background: #f59e0b; }

.sf-count { 
  background: #1a1a1a; 
  color: #fff; 
  border-radius: 10px; 
  padding: 1px 6px; 
  font-size: 11px; 
}

.sf-count.draft-count { background: #f59e0b; }

.table-wrapper { 
  border-top: 2px solid #b0ada8; 
  overflow-x: auto; 
}

.records-table { 
  width: 100%; 
  border-collapse: collapse; 
  font-size: 14px; 
}

.records-table thead tr { border-bottom: 1px solid #c5c2bc; }

.records-table th { 
  text-align: left; 
  padding: 10px 14px; 
  font-weight: 600; 
  font-size: 13px; 
  color: #444; 
  white-space: nowrap; 
}

.records-table th:first-child { padding-left: 0; }

.table-row { 
  border-bottom: 1px solid #dddad5; 
  transition: background .12s; 
}

.table-row:hover { background: #e9e7e3; }

.records-table td { 
  padding: 10px 14px; 
  vertical-align: middle; 
}

.records-table td:first-child { padding-left: 0; }

.type-pill { 
  display: inline-block; 
  padding: 2px 10px; 
  border-radius: 12px; 
  font-size: 12px; 
  font-weight: 600; 
  white-space: nowrap; 
}

.pill-birth    { background: #e8f4ea; color: #2e7d42; }
.pill-marriage { background: #e8eef8; color: #2a55a0; }
.pill-death    { background: #faeaea; color: #9b2c2c; }

.col-desc    { font-weight: 500; }
.col-date    { color: #444; white-space: nowrap; }
.col-archive { color: #555; font-size: 13px; }
.col-page    { color: #777; font-size: 13px; white-space: nowrap; }
.col-actions { white-space: nowrap; }

.record-actions, .draft-actions { 
  display: flex; 
  gap: 6px; 
  flex-wrap: wrap; 
}

.action-btn { 
  padding: 4px 10px; 
  border-radius: 5px; 
  font-size: 12px; 
  font-family: inherit; 
  cursor: pointer; 
  border: 1px solid transparent; 
  transition: all .15s; 
  white-space: nowrap; 
}

.edit-btn { 
  background: #f0efee; 
  border-color: #c8c5c0; 
  color: #444; 
}

.edit-btn:hover { background: #e9e7e3; }

.del-btn { 
  background: #fef2f2; 
  border-color: #fecaca; 
  color: #991b1b; 
}

.del-btn:hover { background: #fee2e2; }

.state-box { 
  display: flex; 
  align-items: center; 
  gap: 12px; 
  padding: 24px 0; 
  font-size: 14px; 
  color: #666; 
}

.error-box { 
  color: #a00; 
  flex-wrap: wrap; 
}

.retry-btn { 
  padding: 5px 14px; 
  border: 1px solid #a00; 
  border-radius: 4px; 
  background: transparent; 
  color: #a00; 
  font-size: 13px; 
  cursor: pointer; 
  transition: background .15s; 
}

.retry-btn:hover { background: #fff0f0; }

.spinner { 
  width: 20px; 
  height: 20px; 
  border: 2px solid #ccc; 
  border-top-color: #666; 
  border-radius: 50%; 
  animation: spin .7s linear infinite; 
  flex-shrink: 0; 
}

@keyframes spin { 
  to { transform: rotate(360deg); } 
}

.no-results { 
  text-align: center; 
  color: #999; 
  padding: 24px 0; 
  font-size: 14px; 
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
  backdrop-filter: blur(3px);
}

.modal {
  background: #fff;
  border-radius: 20px;
  max-width: 460px;
  width: 90%;
  padding: 24px 28px;
  text-align: center;
  box-shadow: 0 20px 35px -12px rgba(0,0,0,0.25);
  animation: fadeSlideIn 0.2s ease-out;
}

.confirm-icon, .success-icon {
  font-size: 52px;
  margin-bottom: 12px;
}

.modal h4 {
  font-size: 1.7rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #222;
}

.confirm-text, .success-text {
  font-size: 1rem;
  line-height: 1.4;
  color: #4b5563;
  margin-bottom: 28px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel, .btn-confirm-publish, .btn-ok {
  border: none;
  padding: 8px 22px;
  border-radius: 40px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: #f1f5f9;
  color: #1e293b;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

.btn-confirm-publish {
  background: #dc2626;
  color: white;
  box-shadow: 0 2px 6px rgba(220,38,38,0.2);
}

.btn-confirm-publish:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-1px);
}

.btn-confirm-publish:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-ok {
  background: #10b981;
  color: white;
  padding: 8px 28px;
  box-shadow: 0 2px 6px rgba(16,185,129,0.2);
}

.btn-ok:hover {
  background: #059669;
  transform: translateY(-1px);
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>