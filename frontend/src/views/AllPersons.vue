<template>
  <div class="app-layout">
    <AppSidebar :isAdmin="isAdmin" />
    <main class="main-content">
      <header class="main-header">
        <h1 class="welcome-title">Все персоны</h1>
      </header>

      <section class="records-section">
        <div class="section-top">
          <div v-if="!loading && !error" class="counts-row">
            <span
              :class="['count-badge', 'badge-male', { active: activeFilter === 'male' }]"
              @click="toggleFilter('male')"
            >
              Мужчины: {{ counts.male ?? 0 }}
            </span>
            <span
              :class="['count-badge', 'badge-female', { active: activeFilter === 'female' }]"
              @click="toggleFilter('female')"
            >
              Женщины: {{ counts.female ?? 0 }}
            </span>
            <span
              :class="['count-badge', 'badge-all', { active: activeFilter === null }]"
              @click="toggleFilter(null)"
            >
              Все: {{ totalCount }}
            </span>

            <button class="filter-toggle-btn" @click="showFilters = !showFilters">
              <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <polygon points="22 3 2 3 10 13 10 21 14 18 14 13 22 3"/>
              </svg>
              Фильтры
              <span v-if="hasActiveFilters" class="filter-dot"></span>
            </button>
          </div>
        </div>

        <div v-show="showFilters" class="filters-dropdown">
          <div class="filters-grid">
            <div class="filter-chip filter-chip-estate">
              <span class="chip-label">Сословие</span>
              <select v-model="filters.estate_name" class="chip-select" @change="applyFilters">
                <option value="">Все</option>
                <option v-for="e in estatesList" :key="e.name" :value="e.name">
                  {{ e.name }}
                </option>
              </select>
            </div>

            <div class="filter-chip filter-chip-province">
              <span class="chip-label">Губерния</span>
              <select v-model="filters.province_name" class="chip-select" @change="applyFilters">
                <option value="">Все</option>
                <option v-for="p in provincesList" :key="p.name" :value="p.name">
                  {{ p.name }}
                </option>
              </select>
            </div>

            <div class="filter-chip filter-chip-yezd">
              <span class="chip-label">Уезд</span>
              <select v-model="filters.yezd_name" class="chip-select" @change="applyFilters">
                <option value="">Все</option>
                <option v-for="y in yezdsList" :key="y.name" :value="y.name">
                  {{ y.name }}
                </option>
              </select>
            </div>

            <div class="filter-chip filter-chip-volost">
              <span class="chip-label">Волость</span>
              <select v-model="filters.volost_name" class="chip-select" @change="applyFilters">
                <option value="">Все</option>
                <option v-for="v in volostsList" :key="v.name" :value="v.name">
                  {{ v.name }}
                </option>
              </select>
            </div>

            <div class="filter-chip filter-chip-village">
              <span class="chip-label">Населенный пункт</span>
              <select v-model="filters.village_name" class="chip-select" @change="applyFilters">
                <option value="">Все</option>
                <option v-for="v in villagesList" :key="v.name" :value="v.name">
                  {{ v.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="filters-actions">
            <button class="clear-filters-btn" @click="clearFilters">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
              Сбросить все
            </button>
          </div>
        </div>

        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск по ФИО"
            class="search-input"
            @input="onSearchInput"
          />
        </div>

        <div v-if="loading" class="state-box">
          <span class="spinner"></span>
          <span>Загрузка данных…</span>
        </div>

        <div v-else-if="error" class="state-box error-box">
          <span>{{ error }}</span>
          <button class="retry-btn" @click="fetchAllPeople">Повторить</button>
        </div>

        <div v-else class="table-wrapper">
          <table class="records-table">
            <thead>
              <tr>
                <th>ФИО</th>
                <th>Пол</th>
                <th>Дата</th>
                <th>Сословие</th>
                <th>Архив</th>
                <th>Страница / Запись</th>
                <th>Тип</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="person in filteredPeople"
                :key="person.id"
                class="table-row"
                @click="viewPerson(person)"
              >
                <td class="col-name">{{ person.full_name }}</td>
                <td class="col-gender">
                  <span :class="['sex-pill', person.sex === 'М' ? 'pill-male' : 'pill-female']">
                    {{ person.sex === 'М' ? 'Муж.' : 'Жен.' }}
                  </span>
                </td>
                <td class="col-date">{{ person.date_display || '—' }}</td>
                <td class="col-secondary">{{ person.estate_name || '—' }}</td>
                <td class="col-archive">{{ person.archive_name || '—' }}</td>
                <td class="col-page">{{ person.page_record || '—' }}</td>
                <td class="col-type">
                  <span :class="['type-pill', `pill-${person.role_type}`]">
                    {{ person.role_label }}
                  </span>
                </td>
              </tr>
              <tr v-if="filteredPeople.length === 0">
                <td colspan="7" class="no-results">Записи не найдены</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Сообщение "Записи не найдены" по центру -->
        <div v-if="!loading && filteredPeople.length === 0" class="no-results-container">
          <div class="no-results-message">
            <svg class="no-results-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <p>Записи не найдены</p>
            <p class="no-results-hint">Попробуйте изменить параметры поиска или сбросить фильтры</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import AppSidebar from '@/components/AppSidebar.vue'
import { api, authHeaders } from '@/utils/api.js'

export default {
  name: 'AllPersons',
  components: { AppSidebar },

  data() {
    return {
      isAdmin: false,
      allPeople: [],
      counts: { male: 0, female: 0 },
      loading: false,
      error: null,
      searchQuery: '',
      activeFilter: null,
      showFilters: false,
      _searchTimer: null,

      estatesList: [],
      provincesList: [],
      yezdsList: [],
      volostsList: [],
      villagesList: [],

      filters: {
        estate_name: '',
        province_name: '',
        yezd_name: '',
        volost_name: '',
        village_name: ''
      },
    }
  },

  computed: {
    totalCount() {
      return this.allPeople.length
    },

    hasActiveFilters() {
      return Object.values(this.filters).some(v => v !== '' && v !== null)
    },

    filteredPeople() {
      let list = [...this.allPeople]

      if (this.activeFilter === 'male') {
        list = list.filter(p => p.sex === 'М')
      }
      if (this.activeFilter === 'female') {
        list = list.filter(p => p.sex === 'Ж')
      }

      if (this.filters.estate_name && this.filters.estate_name !== '') {
        list = list.filter(p => p.estate_name === this.filters.estate_name)
      }

      if (this.filters.province_name && this.filters.province_name !== '') {
        list = list.filter(p => p.province_name === this.filters.province_name)
      }

      if (this.filters.yezd_name && this.filters.yezd_name !== '') {
        list = list.filter(p => p.yezd_name === this.filters.yezd_name)
      }

      if (this.filters.volost_name && this.filters.volost_name !== '') {
        list = list.filter(p => p.volost_name === this.filters.volost_name)
      }

      if (this.filters.village_name && this.filters.village_name !== '') {
        list = list.filter(p => p.village_name === this.filters.village_name)
      }

      const q = this.searchQuery.trim().toLowerCase()
      if (q) {
        list = list.filter(p => (p.full_name || '').toLowerCase().includes(q))
      }

      return list
    },
  },

  watch: {
    filters: {
      deep: true,
      handler() {
        this.applyFilters()
      }
    },
    activeFilter() {
      this.applyFilters()
    }
  },

  async created() {
    await this.checkUserRole()
    await this.loadReferenceData()
    await this.fetchAllPeople()
  },

  methods: {
    formatDateForDisplay(isoDate) {
      if (!isoDate) return null
      const [y, m, d] = isoDate.split('-')
      return `${d}.${m}.${y}`
    },

    applyFilters() {
      this.$forceUpdate()
    },

    onSearchInput() {
      clearTimeout(this._searchTimer)
      this._searchTimer = setTimeout(() => {
        this.applyFilters()
      }, 300)
    },

    async checkUserRole() {
      try {
        const headers = authHeaders()
        const data = await api('/api/home/', { headers })
        this.isAdmin = data.user_role === 'admin'
      } catch (err) {
        console.error('Ошибка получения роли пользователя:', err)
        this.isAdmin = false
      }
    },

    async loadReferenceData() {
      try {
        const headers = authHeaders()
        
        const [estates, provinces, yezds, volosts, villages] = await Promise.all([
          api('/api/estates/', { headers }).catch(() => []),
          api('/api/provinces/', { headers }).catch(() => []),
          api('/api/yezds/', { headers }).catch(() => []),
          api('/api/volosts/', { headers }).catch(() => []),
          api('/api/villages/', { headers }).catch(() => [])
        ])

        this.estatesList = Array.isArray(estates) ? estates : (estates.results || [])
        this.provincesList = Array.isArray(provinces) ? provinces : (provinces.results || [])
        this.yezdsList = Array.isArray(yezds) ? yezds : (yezds.results || [])
        this.volostsList = Array.isArray(volosts) ? volosts : (volosts.results || [])
        this.villagesList = Array.isArray(villages) ? villages : (villages.results || [])
        
        console.log('Загружено справочников:', {
          estates: this.estatesList.length,
          provinces: this.provincesList.length,
          yezds: this.yezdsList.length,
          volosts: this.volostsList.length,
          villages: this.villagesList.length
        })
      } catch (err) {
        console.error('Ошибка загрузки справочников:', err)
      }
    },

    async fetchPersonEstate(personId) {
      if (!personId) return null
      try {
        const headers = authHeaders()
        const personData = await api(`/api/persons/${personId}/`, { headers })
        return personData.estate_name || null
      } catch (err) {
        console.error(`Ошибка загрузки сословия для person ${personId}:`, err)
        return null
      }
    },

    async fetchAllPeople() {
      this.loading = true
      this.error = null
      this.allPeople = []

      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.error = 'Необходима авторизация'
          this.loading = false
          return
        }

        const headers = authHeaders()
        const result = []
        
        // Кэш для сословий персон
        const estateCache = new Map()

        // ────────────────────────────────────────────────────────────
        // 1. Записи о рождениях
        // ────────────────────────────────────────────────────────────
        let birthRecords = []
        try {
          const birthRes = await api('/api/birth-records/', { headers })
          birthRecords = Array.isArray(birthRes) ? birthRes : (birthRes.results ?? [])
          console.log(`Загружено записей о рождениях: ${birthRecords.length}`)
        } catch (err) {
          console.error('Ошибка загрузки записей о рождениях:', err)
        }

        for (const record of birthRecords) {
          const pd = record.person_data
          const archiveDisplay = record.archive_name || (record.archive?.name)

          // 1.1 Родившийся
          result.push({
            id: `birth_person_${record.birth_id}`,
            full_name: pd ? `${pd.surname || ''} ${pd.name || ''} ${pd.patronymic || ''}`.trim() : '—',
            sex: record.sex,
            date_display: this.formatDateForDisplay(record.date_of_baptism),
            estate_name: pd?.estate_name || record.estate_name || null,
            province_name: record.father_province?.name || null,
            yezd_name: record.father_yezd?.name || null,
            volost_name: record.father_volost?.name || null,
            village_name: record.father_village?.name || null,
            archive_name: archiveDisplay,
            page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
            role_type: 'born',
            role_label: 'Родившийся',
            source_type: 'person',
            source_id: pd?.person_id,
          })

          // 1.2 Отец
          if (record.father_surname || record.father_name) {
            result.push({
              id: `birth_father_${record.birth_id}`,
              full_name: `${record.father_surname || ''} ${record.father_name || ''} ${record.father_patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: record.father_estate_name || null,
              province_name: record.father_province?.name || null,
              yezd_name: record.father_yezd?.name || null,
              volost_name: record.father_volost?.name || null,
              village_name: record.father_village?.name || null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'father',
              role_label: 'Отец',
              source_type: 'person',
              source_id: record.father,
            })
          }

          // 1.3 Мать
          if (record.mother_surname || record.mother_name) {
            result.push({
              id: `birth_mother_${record.birth_id}`,
              full_name: `${record.mother_surname || ''} ${record.mother_name || ''} ${record.mother_patronymic || ''}`.trim(),
              sex: 'Ж',
              date_display: null,
              estate_name: null,
              province_name: record.father_province?.name || null,
              yezd_name: record.father_yezd?.name || null,
              volost_name: record.father_volost?.name || null,
              village_name: record.father_village?.name || null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'mother',
              role_label: 'Мать',
              source_type: 'person',
              source_id: record.mother,
            })
          }

          // 1.4 Восприемники
          for (const godman of (record.godmen || [])) {
            result.push({
              id: `birth_godman_${record.birth_id}_${godman.godmen_id}`,
              full_name: `${godman.surname || ''} ${godman.name || ''} ${godman.patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: godman.estate_name || null,
              province_name: godman.province_name || null,
              yezd_name: godman.yezd_name || null,
              volost_name: godman.volost_name || null,
              village_name: godman.village_name || null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'godparent',
              role_label: 'Восприемник',
              source_type: 'person',
              source_id: godman.person,
            })
          }

          // 1.5 Восприемницы
          for (const godmother of (record.godmothers || [])) {
            result.push({
              id: `birth_godmother_${record.birth_id}_${godmother.godmother_id}`,
              full_name: `${godmother.surname || ''} ${godmother.name || ''} ${godmother.patronymic || ''}`.trim(),
              sex: 'Ж',
              date_display: null,
              estate_name: godmother.estate_name || null,
              province_name: godmother.province_name || null,
              yezd_name: godmother.yezd_name || null,
              volost_name: godmother.volost_name || null,
              village_name: godmother.village_name || null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'godparent',
              role_label: 'Восприемница',
              source_type: 'person',
              source_id: godmother.person,
            })
          }

          // 1.6 Священнослужители
          for (const priest of (record.priests || [])) {
            result.push({
              id: `birth_priest_${record.birth_id}_${priest.id}`,
              full_name: `${priest.surname || ''} ${priest.name || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: priest.clergy_name || null,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'priest',
              role_label: 'Священнослужитель',
              source_type: 'priest',
              source_id: priest.church_worker ?? priest.id,
            })
          }
        }

        // ────────────────────────────────────────────────────────────
        // 2. Записи о смертях
        // ────────────────────────────────────────────────────────────
        let deathRecords = []
        try {
          const deathRes = await api('/api/death-records/', { headers })
          deathRecords = Array.isArray(deathRes) ? deathRes : (deathRes.results ?? [])
          console.log(`Загружено записей о смертях: ${deathRecords.length}`)
        } catch (err) {
          console.error('Ошибка загрузки записей о смертях:', err)
        }

        for (const record of deathRecords) {
          const pd = record.person_data
          const archiveDisplay = record.archive_name || (record.archive?.name)

          // 2.1 Умерший
          let deceasedEstate = record.estate_name || pd?.estate_name || null
          
          result.push({
            id: `death_person_${record.death_id}`,
            full_name: pd ? `${pd.surname || ''} ${pd.name || ''} ${pd.patronymic || ''}`.trim() : '—',
            sex: record.sex,
            date_display: null,
            estate_name: deceasedEstate,
            province_name: record.province_name || null,
            yezd_name: record.yezd_name || null,
            volost_name: record.volost_name || null,
            village_name: record.village_name || null,
            archive_name: archiveDisplay,
            page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
            role_type: 'deceased',
            role_label: 'Умерший',
            source_type: 'person',
            source_id: pd?.person_id,
          })

          // 2.2 Родственники умершего
          for (const rel of (record.relatives || [])) {
            result.push({
              id: `death_relative_${record.death_id}_${Date.now()}_${Math.random()}`,
              full_name: `${rel.surname || ''} ${rel.name || ''} ${rel.patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: null,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'relative',
              role_label: 'Родственник умершего',
              source_type: null,
              source_id: null,
            })
          }

          // 2.3 Священнослужители
          for (const priest of (record.priests || [])) {
            result.push({
              id: `death_priest_${record.death_id}_${priest.id}`,
              full_name: `${priest.surname || ''} ${priest.name || ''} ${priest.patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: priest.clergy_name || null,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'priest',
              role_label: 'Священнослужитель',
              source_type: 'priest',
              source_id: priest.church_worker ?? priest.id,
            })
          }
        }

        // ────────────────────────────────────────────────────────────
        // 3. Записи о браках
        // ────────────────────────────────────────────────────────────
        let marriageRecords = []
        try {
          const marriageRes = await api('/api/marriage-records/', { headers })
          marriageRecords = Array.isArray(marriageRes) ? marriageRes : (marriageRes.results ?? [])
          console.log(`Загружено записей о браках: ${marriageRecords.length}`)
        } catch (err) {
          console.error('Ошибка загрузки записей о браках:', err)
        }

        for (const record of marriageRecords) {
          const archiveDisplay = record.archive_name || (record.archive?.name)

          // 3.1 Жених
          let husbands = []
          try {
            const hRes = await api(`/api/husbands/?marriage=${record.marriage_id}`, { headers })
            husbands = Array.isArray(hRes) ? hRes : (hRes.results ?? [])
          } catch (err) {
            console.error('Ошибка загрузки женихов:', err)
          }
          
          for (const h of husbands) {
            let estateName = null
            if (h.person) {
              if (estateCache.has(h.person)) {
                estateName = estateCache.get(h.person)
              } else {
                estateName = await this.fetchPersonEstate(h.person)
                estateCache.set(h.person, estateName)
              }
            }
            
            result.push({
              id: `marriage_husband_${h.man_id}`,
              full_name: `${h.person_surname || ''} ${h.person_name || ''} ${h.person_patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: estateName,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'husband',
              role_label: 'Муж',
              source_type: 'person',
              source_id: h.person,
            })
          }

          // 3.2 Невеста
          let wives = []
          try {
            const wRes = await api(`/api/wives/?marriage=${record.marriage_id}`, { headers })
            wives = Array.isArray(wRes) ? wRes : (wRes.results ?? [])
          } catch (err) {
            console.error('Ошибка загрузки невест:', err)
          }
          
          for (const w of wives) {
            let estateName = null
            if (w.person) {
              if (estateCache.has(w.person)) {
                estateName = estateCache.get(w.person)
              } else {
                estateName = await this.fetchPersonEstate(w.person)
                estateCache.set(w.person, estateName)
              }
            }
            
            result.push({
              id: `marriage_wife_${w.wife_id}`,
              full_name: `${w.person_surname || ''} ${w.person_name || ''} ${w.person_patronymic || ''}`.trim(),
              sex: 'Ж',
              date_display: null,
              estate_name: estateName,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'wife',
              role_label: 'Жена',
              source_type: 'person',
              source_id: w.person,
            })
          }

          // 3.3 Поручители (мужчины)
          let maleGuarantors = []
          try {
            const mgRes = await api(`/api/male-guarantors/?marriage=${record.marriage_id}`, { headers })
            maleGuarantors = Array.isArray(mgRes) ? mgRes : (mgRes.results ?? [])
          } catch (err) {
            console.error('Ошибка загрузки поручителей (м):', err)
          }
          
          for (const g of maleGuarantors) {
            let estateName = null
            if (g.person) {
              if (estateCache.has(g.person)) {
                estateName = estateCache.get(g.person)
              } else {
                estateName = await this.fetchPersonEstate(g.person)
                estateCache.set(g.person, estateName)
              }
            }
            
            result.push({
              id: `marriage_male_guarantor_${g.guarantors_id}`,
              full_name: `${g.person_surname || ''} ${g.person_name || ''} ${g.person_patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: estateName,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'guarantor',
              role_label: 'Поручитель',
              source_type: 'person',
              source_id: g.person,
            })
          }

          // 3.4 Поручительницы (женщины)
          let femaleGuarantors = []
          try {
            const fgRes = await api(`/api/female-guarantors/?marriage=${record.marriage_id}`, { headers })
            femaleGuarantors = Array.isArray(fgRes) ? fgRes : (fgRes.results ?? [])
          } catch (err) {
            console.error('Ошибка загрузки поручителей (ж):', err)
          }
          
          for (const g of femaleGuarantors) {
            let estateName = null
            if (g.person) {
              if (estateCache.has(g.person)) {
                estateName = estateCache.get(g.person)
              } else {
                estateName = await this.fetchPersonEstate(g.person)
                estateCache.set(g.person, estateName)
              }
            }
            
            result.push({
              id: `marriage_female_guarantor_${g.guarantors_id}`,
              full_name: `${g.person_surname || ''} ${g.person_name || ''} ${g.person_patronymic || ''}`.trim(),
              sex: 'Ж',
              date_display: null,
              estate_name: estateName,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'guarantor',
              role_label: 'Поручительница',
              source_type: 'person',
              source_id: g.person,
            })
          }

          // 3.5 Священнослужители
          for (const priest of (record.priests || [])) {
            result.push({
              id: `marriage_priest_${record.marriage_id}_${priest.id}`,
              full_name: `${priest.surname || ''} ${priest.name || ''} ${priest.patronymic || ''}`.trim(),
              sex: 'М',
              date_display: null,
              estate_name: priest.clergy_name || null,
              province_name: null,
              yezd_name: null,
              volost_name: null,
              village_name: null,
              archive_name: archiveDisplay,
              page_record: record.page ? `${record.page} / ${record.number_record || '—'}` : '—',
              role_type: 'priest',
              role_label: 'Священнослужитель',
              source_type: 'priest',
              source_id: priest.church_worker ?? priest.id,
            })
          }
        }

        // НЕ ДОБАВЛЯЕМ базовые персоны из Persons
        this.allPeople = result

        // Подсчет статистики
        this.counts = {
          male: this.allPeople.filter(p => p.sex === 'М').length,
          female: this.allPeople.filter(p => p.sex === 'Ж').length,
        }

        console.log('Всего персон:', this.allPeople.length)
        console.log('Примеры персон с сословием:')
        this.allPeople.slice(0, 10).forEach(p => {
          console.log(`- ${p.full_name}: сословие="${p.estate_name}", тип=${p.role_label}`)
        })

      } catch (err) {
        console.error('Ошибка загрузки:', err)
        this.error = err.message || 'Не удалось загрузить данные.'
      } finally {
        this.loading = false
      }
    },

    toggleFilter(type) {
      this.activeFilter = this.activeFilter === type ? null : type
    },

    clearFilters() {
      this.filters = {
        estate_name: '',
        province_name: '',
        yezd_name: '',
        volost_name: '',
        village_name: ''
      }
      this.searchQuery = ''
      this.activeFilter = null
      this.showFilters = false
      this.applyFilters()
    },

    viewPerson(person) {
      if (person.role_type === 'priest' && person.source_id) {
        this.$router.push(`/clergy/view/${person.source_id}`)
        return
      }
      if (person.source_type === 'person' && person.source_id) {
        this.$router.push(`/person/view/${person.source_id}/birth`)
      }
    },
  },
}
</script>

<style scoped>
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

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.welcome-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -.3px;
}

.section-top {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.counts-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
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

.badge-male   { background: #e8eef8; color: #2a55a0; border-color: #b3c6e8; }
.badge-female { background: #fce8f4; color: #9b2c7a; border-color: #e8b3d8; }
.badge-all    { background: #f0efee; color: #444; border-color: #c8c5c0; }

.count-badge.active,
.count-badge:hover { filter: brightness(0.93); border-color: currentColor; }

.filter-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 12px;
  background: #fff;
  border: 1px solid #e0dedb;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
  position: relative;
}

.filter-toggle-btn:hover {
  background: #f0efee;
  border-color: #c8c5c0;
}

.filter-icon {
  width: 14px;
  height: 14px;
}

.filter-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 8px;
  height: 8px;
  background: #2a55a0;
  border-radius: 50%;
  border: 1px solid #fff;
}

.filters-dropdown {
  background: #fff;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 18px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.filters-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 24px;
  transition: all 0.2s;
}

.chip-label {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.filter-chip-estate  { background: #e8f4ea; }
.filter-chip-estate .chip-label  { color: #2e7d42; }
.filter-chip-province { background: #fef3c7; }
.filter-chip-province .chip-label { color: #92400e; }
.filter-chip-yezd    { background: #e0e7ff; }
.filter-chip-yezd .chip-label    { color: #3730a3; }
.filter-chip-volost  { background: #d1fae5; }
.filter-chip-volost .chip-label  { color: #065f46; }
.filter-chip-village { background: #fed7aa; }
.filter-chip-village .chip-label { color: #9a3412; }

.chip-select {
  padding: 3px 18px 3px 8px;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 20px;
  font-size: 11px;
  font-family: inherit;
  font-weight: 500;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 6px center;
  color: #333;
  max-width: 130px;
}
.chip-select:hover    { background: #fff; }
.chip-select:disabled { opacity: 0.5; cursor: not-allowed; }

.filters-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 8px;
  border-top: 1px solid #efeeec;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: transparent;
  border: none;
  border-radius: 20px;
  font-size: 11px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
  color: #888;
}
.clear-filters-btn svg { width: 12px; height: 12px; }
.clear-filters-btn:hover { background: #fef2f2; color: #dc2626; }

.search-bar {
  position: relative;
  max-width: 280px;
  margin-bottom: 18px;
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
.search-input:focus { border-color: #888; }

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

.table-row { border-bottom: 1px solid #dddad5; transition: background .12s; cursor: pointer; }
.table-row:hover { background: #e9e7e3; }
.records-table td { padding: 10px 14px; vertical-align: middle; }
.records-table td:first-child { padding-left: 0; }

.type-pill {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}
.pill-born      { background: #e8f4ea; color: #2e7d42; }
.pill-father    { background: #e8eef8; color: #2a55a0; }
.pill-mother    { background: #fce8f4; color: #9b2c7a; }
.pill-deceased  { background: #faeaea; color: #9b2c2c; }
.pill-priest    { background: #fef3c7; color: #92400e; }
.pill-godparent { background: #e0e7ff; color: #3730a3; }
.pill-guarantor { background: #fed7aa; color: #9a3412; }
.pill-husband   { background: #e8eef8; color: #1a3a6b; }
.pill-wife      { background: #fce8f4; color: #6b1a4a; }
.pill-relative  { background: #f0e8fc; color: #5b1a8b; }

.sex-pill {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}
.pill-male   { background: #e8eef8; color: #2a55a0; }
.pill-female { background: #fce8f4; color: #9b2c7a; }

.col-name      { font-weight: 500; }
.col-date      { color: #444; white-space: nowrap; }
.col-secondary { color: #555; font-size: 13px; }
.col-archive   { color: #555; font-size: 13px; }
.col-page      { color: #777; font-size: 13px; white-space: nowrap; }

.state-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 0;
  font-size: 14px;
  color: #666;
}

.error-box { color: #a00; flex-wrap: wrap; }

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
@keyframes spin { to { transform: rotate(360deg); } }

/* Сообщение "Записи не найдены" по центру */
.no-results-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
}

.no-results-message {
  color: #999;
}

.no-results-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  color: #ccc;
}

.no-results-message p {
  font-size: 16px;
  margin: 8px 0;
}

.no-results-hint {
  font-size: 13px;
  color: #bbb;
}
</style>