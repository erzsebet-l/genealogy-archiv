<template>
  <div class="app-layout">
    <AppSidebar />
    <main class="main-content">
      <header class="main-header">
        <div class="header-left">
          <button class="btn-back" @click="$router.back()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M19 12H5M12 5l-7 7 7 7"/>
            </svg>
            Назад
          </button>
          <h1 class="page-title">{{ person.full_name || 'Загрузка...' }}</h1>
        </div>
        <div class="header-right">
          <span :class="['gender-badge', person.sex === 'М' ? 'gender-male' : 'gender-female']">
            {{ person.sex === 'М' ? '♂ Мужской' : '♀ Женский' }}
          </span>
        </div>
      </header>

      <div v-if="loading" class="state-box">
        <span class="spinner"></span>
        <span>Загрузка данных...</span>
      </div>

      <div v-else-if="error" class="state-box error-box">
        <span>{{ error }}</span>
        <button class="retry-btn" @click="fetchPersonData">Повторить</button>
      </div>

      <div v-else class="person-content">
        <!-- Основная информация -->
        <div class="info-card">
          <h2 class="card-title">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Основные сведения
          </h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Фамилия</span>
              <span class="info-value">{{ person.surname || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Имя</span>
              <span class="info-value">{{ person.name || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Отчество</span>
              <span class="info-value">{{ person.patronymic || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Дата рождения</span>
              <span class="info-value">{{ formatDate(person.date) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Дата крещения</span>
              <span class="info-value">{{ birthRecordAsChild ? formatDate(birthRecordAsChild.date_of_baptism) : '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Сословие</span>
              <span class="info-value">{{ person.estate_name || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Вероисповедание</span>
              <span class="info-value">{{ person.creed_name || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Губерния</span>
              <span class="info-value">{{ getLocationName('province', person.province) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Уезд</span>
              <span class="info-value">{{ getLocationName('yezd', person.yezd) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Волость</span>
              <span class="info-value">{{ getLocationName('volost', person.volost) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Населенный пункт</span>
              <span class="info-value">{{ getLocationName('village', person.village) }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">Комментарий</span>
              <span class="info-value">{{ person.comment || '—' }}</span>
            </div>
          </div>
        </div>

        <!-- Запись о рождении (где персона - ребенок) -->
        <div v-if="birthRecordAsChild" class="info-card">
          <h2 class="card-title">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            Запись о рождении
          </h2>
          
          <!-- Отец -->
          <div v-if="birthRecordAsChild.father_name" class="sub-section">
            <h3 class="sub-title">Отец</h3>
            <div class="simple-info-block">
              <div class="simple-icon">👨</div>
              <div class="simple-info">
                <div class="simple-name">{{ birthRecordAsChild.father_surname }} {{ birthRecordAsChild.father_name }} {{ birthRecordAsChild.father_patronymic || '' }}</div>
                <div class="simple-details">
                  <span>Сословие: {{ birthRecordAsChild.father_estate_name || '—' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Мать -->
          <div v-if="birthRecordAsChild.mother_name" class="sub-section">
            <h3 class="sub-title">Мать</h3>
            <div class="simple-info-block">
              <div class="simple-icon">👩</div>
              <div class="simple-info">
                <div class="simple-name">{{ birthRecordAsChild.mother_surname }} {{ birthRecordAsChild.mother_name }} {{ birthRecordAsChild.mother_patronymic || '' }}</div>
                <div class="simple-details">
                  <span>Статус: {{ birthRecordAsChild.mother_status || '—' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Документ о рождении -->
          <div class="sub-section">
            <h3 class="sub-title">Документ</h3>
            <div class="info-grid small">
              <div class="info-item">
                <span class="info-label">Архив</span>
                <span class="info-value">{{ birthRecordAsChild.archive_name || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер дела</span>
                <span class="info-value">{{ birthRecordAsChild.number_case || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Лист</span>
                <span class="info-value">{{ birthRecordAsChild.page || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер записи</span>
                <span class="info-value">{{ birthRecordAsChild.number_record || '—' }}</span>
              </div>
            </div>
            <div v-if="birthRecordAsChild.scan_url" class="scan-section">
              <a :href="birthRecordAsChild.scan_url" target="_blank" class="scan-link">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                  <polyline points="13 2 13 9 20 9"/>
                </svg>
                Открыть скан документа
              </a>
            </div>
          </div>

          <!-- Восприемники (мужчины) -->
          <div v-if="birthRecordAsChild.godmen && birthRecordAsChild.godmen.length" class="sub-section">
            <h3 class="sub-title">Восприемники (мужчины)</h3>
            <div class="compact-list">
              <div v-for="godman in birthRecordAsChild.godmen" :key="godman.godmen_id" class="compact-item">
                <div class="compact-icon">👨</div>
                <div class="compact-info">
                  <div class="compact-name">{{ godman.surname }} {{ godman.name }} {{ godman.patronymic || '' }}</div>
                  <div class="compact-meta">{{ godman.estate_name || '' }} {{ godman.creed_name || '' }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Восприемницы (женщины) -->
          <div v-if="birthRecordAsChild.godmothers && birthRecordAsChild.godmothers.length" class="sub-section">
            <h3 class="sub-title">Восприемницы (женщины)</h3>
            <div class="compact-list">
              <div v-for="godmother in birthRecordAsChild.godmothers" :key="godmother.godmother_id" class="compact-item">
                <div class="compact-icon">👩</div>
                <div class="compact-info">
                  <div class="compact-name">{{ godmother.surname }} {{ godmother.name }} {{ godmother.patronymic || '' }}</div>
                  <div class="compact-meta">{{ godmother.status_name || '' }} {{ godmother.estate_name || '' }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Священнослужители при рождении -->
          <div v-if="birthRecordAsChild.priests && birthRecordAsChild.priests.length" class="sub-section">
            <h3 class="sub-title">Священнослужители</h3>
            <div class="compact-list">
              <div v-for="priest in birthRecordAsChild.priests" :key="priest.id" class="compact-item">
                <div class="compact-icon">⛪</div>
                <div class="compact-info">
                  <div class="compact-name">{{ priest.surname }} {{ priest.name }}</div>
                  <div class="compact-meta">{{ priest.clergy_name || 'священнослужитель' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Запись о браке -->
        <div v-if="marriageRecord" class="info-card">
          <h2 class="card-title">
            <span class="card-icon">💍</span>
            Запись о браке
          </h2>
          
          <!-- Супруг/супруга -->
          <div v-if="marriageRecord.spouse" class="sub-section">
            <h3 class="sub-title">{{ marriageRecord.spouse.sex === 'М' ? 'Муж' : 'Жена' }}</h3>
            <div class="simple-info-block">
              <div class="simple-icon">{{ marriageRecord.spouse.sex === 'М' ? '👨' : '👰' }}</div>
              <div class="simple-info">
                <div class="simple-name">{{ marriageRecord.spouse.full_name }}</div>
                <div class="simple-details">
                  <span>Возраст: {{ marriageRecord.spouse_age || '—' }}</span>
                  <span>Брак №{{ marriageRecord.number_marriage || '1' }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="sub-section">
            <h3 class="sub-title">Документ</h3>
            <div class="info-grid small">
              <div class="info-item">
                <span class="info-label">Дата брака</span>
                <span class="info-value">{{ formatDate(marriageRecord.date) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Архив</span>
                <span class="info-value">{{ marriageRecord.archive_name || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер дела</span>
                <span class="info-value">{{ marriageRecord.number_case || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Лист</span>
                <span class="info-value">{{ marriageRecord.page || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер записи</span>
                <span class="info-value">{{ marriageRecord.number_record || '—' }}</span>
              </div>
            </div>
          </div>

          <!-- Поручители (мужчины) -->
          <div v-if="marriageRecord.male_guarantors && marriageRecord.male_guarantors.length" class="sub-section">
            <h3 class="sub-title">Поручители (мужчины)</h3>
            <div class="compact-list">
              <div v-for="guarantor in marriageRecord.male_guarantors" :key="guarantor.guarantors_id" class="compact-item">
                <div class="compact-icon">👨</div>
                <div class="compact-info">
                  <div class="compact-name">{{ guarantor.person_surname }} {{ guarantor.person_name }} {{ guarantor.person_patronymic || '' }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Поручительницы (женщины) -->
          <div v-if="marriageRecord.female_guarantors && marriageRecord.female_guarantors.length" class="sub-section">
            <h3 class="sub-title">Поручительницы (женщины)</h3>
            <div class="compact-list">
              <div v-for="guarantor in marriageRecord.female_guarantors" :key="guarantor.guarantors_id" class="compact-item">
                <div class="compact-icon">👩</div>
                <div class="compact-info">
                  <div class="compact-name">{{ guarantor.person_surname }} {{ guarantor.person_name }} {{ guarantor.person_patronymic || '' }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Священники при браке -->
          <div v-if="marriageRecord.priests && marriageRecord.priests.length" class="sub-section">
            <h3 class="sub-title">Священнослужители</h3>
            <div class="compact-list">
              <div v-for="priest in marriageRecord.priests" :key="priest.id" class="compact-item">
                <div class="compact-icon">⛪</div>
                <div class="compact-info">
                  <div class="compact-name">{{ priest.surname }} {{ priest.name }}</div>
                  <div class="compact-meta">{{ priest.clergy_name || 'священнослужитель' }}</div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="marriageRecord.scan_url" class="sub-section">
            <a :href="marriageRecord.scan_url" target="_blank" class="scan-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                <polyline points="13 2 13 9 20 9"/>
              </svg>
              Открыть скан документа
            </a>
          </div>
        </div>

        <!-- Запись о смерти -->
        <div v-if="deathRecord" class="info-card">
          <h2 class="card-title">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 8v4M12 16h.01"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
            Запись о смерти
          </h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Дата смерти</span>
              <span class="info-value">{{ formatDate(deathRecord.date) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Возраст</span>
              <span class="info-value">{{ deathRecord.age || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Причина смерти</span>
              <span class="info-value">{{ deathRecord.cause_of_death || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Место погребения</span>
              <span class="info-value">{{ deathRecord.burial_place || '—' }}</span>
            </div>
          </div>
          
          <div class="sub-section">
            <h3 class="sub-title">Документ</h3>
            <div class="info-grid small">
              <div class="info-item">
                <span class="info-label">Архив</span>
                <span class="info-value">{{ deathRecord.archive_name || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер дела</span>
                <span class="info-value">{{ deathRecord.number_case || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Лист</span>
                <span class="info-value">{{ deathRecord.page || '—' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Номер записи</span>
                <span class="info-value">{{ deathRecord.number_record || '—' }}</span>
              </div>
            </div>
          </div>

          <div v-if="deathRecord.scan_url" class="sub-section">
            <a :href="deathRecord.scan_url" target="_blank" class="scan-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                <polyline points="13 2 13 9 20 9"/>
              </svg>
              Открыть скан документа
            </a>
          </div>

          <!-- Священники при смерти -->
          <div v-if="deathRecord.priests && deathRecord.priests.length" class="sub-section">
            <h3 class="sub-title">Священнослужители</h3>
            <div class="compact-list">
              <div v-for="priest in deathRecord.priests" :key="priest.id" class="compact-item">
                <div class="compact-icon">⛪</div>
                <div class="compact-info">
                  <div class="compact-name">{{ priest.surname }} {{ priest.name }}</div>
                  <div class="compact-meta">{{ priest.clergy_name || 'священнослужитель' }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Родственники умершего -->
          <div v-if="deathRecord.relatives && deathRecord.relatives.length" class="sub-section">
            <h3 class="sub-title">Родственники</h3>
            <div class="compact-list">
              <div v-for="rel in deathRecord.relatives" :key="rel.id" class="compact-item">
                <div class="compact-icon">👤</div>
                <div class="compact-info">
                  <div class="compact-name">{{ rel.surname }} {{ rel.name }} {{ rel.patronymic || '' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Родственные связи (обратные и прямые) -->
        <div v-if="allRelationships.length > 0" class="info-card">
          <h2 class="card-title">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            Родственные связи
          </h2>
          <div class="compact-list">
            <div v-for="rel in allRelationships" :key="rel.id" class="compact-item">
              <div class="compact-icon">👤</div>
              <div class="compact-info">
                <div class="compact-name">{{ rel.related_person_name }}</div>
                <div class="compact-meta">{{ rel.relation_type }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import AppSidebar from '@/components/AppSidebar.vue'
import { api, authHeaders } from '@/utils/api.js'

export default {
  name: 'InfoPerson',
  components: { AppSidebar },

  data() {
    return {
      loading: false,
      error: null,
      personId: null,
      
      person: {
        full_name: '',
        surname: '',
        name: '',
        patronymic: '',
        sex: '',
        date: null,
        estate_name: '',
        creed_name: '',
        province: null,
        yezd: null,
        volost: null,
        village: null,
        comment: ''
      },
      
      birthRecordAsChild: null,
      deathRecord: null,
      marriageRecord: null,
      allRelationships: [],
      
      provincesList: [],
      yezdsList: [],
      volostsList: [],
      villagesList: []
    }
  },

  async created() {
    this.personId = parseInt(this.$route.params.id)
    await this.loadReferenceData()
    await this.fetchPersonData()
  },

  methods: {
    formatDate(isoDate) {
      if (!isoDate) return '—'
      const [y, m, d] = isoDate.split('-')
      return `${d}.${m}.${y}`
    },

    getLocationName(type, id) {
      if (!id) return '—'
      let list = []
      if (type === 'province') list = this.provincesList
      else if (type === 'yezd') list = this.yezdsList
      else if (type === 'volost') list = this.volostsList
      else if (type === 'village') list = this.villagesList
      
      const found = list.find(item => {
        if (type === 'province') return item.province_id === id
        if (type === 'yezd') return item.yezd_id === id
        if (type === 'volost') return item.volost_id === id
        if (type === 'village') return item.village_id === id
        return false
      })
      return found ? found.name : '—'
    },

    getFatherLocation(birth) {
      const parts = []
      if (birth.father_province_name) parts.push(birth.father_province_name)
      if (birth.father_yezd_name) parts.push(birth.father_yezd_name)
      if (birth.father_volost_name) parts.push(birth.father_volost_name)
      if (birth.father_village_name) parts.push(birth.father_village_name)
      return parts.join(', ') || '—'
    },

    getReverseKinship(kinshipName, currentPersonSex) {
      // Нормализуем название родства (приводим к нижнему регистру и убираем окончания)
      let normalized = (kinshipName || '').toLowerCase().trim()
      
      // Карта обратного родства
      const reverseMap = {
        'отец': currentPersonSex === 'М' ? 'сын' : 'дочь',
        'мать': currentPersonSex === 'М' ? 'сын' : 'дочь',
        'сын': 'отец',
        'дочь': 'отец',
        'брат': 'брат',
        'сестра': 'сестра',
        'муж': 'жена',
        'жена': 'муж',
        'дед': currentPersonSex === 'М' ? 'внук' : 'внучка',
        'бабка': currentPersonSex === 'М' ? 'внук' : 'внучка',
        'дедушка': currentPersonSex === 'М' ? 'внук' : 'внучка',
        'бабушка': currentPersonSex === 'М' ? 'внук' : 'внучка',
        'внук': 'дед',
        'внучка': 'дед',
        'дядя': 'племянник',
        'тетя': 'племянница',
        'племянник': 'дядя',
        'племянница': 'тетя'
      }
      
      return reverseMap[normalized] || kinshipName
    },

    async loadReferenceData() {
      try {
        const headers = authHeaders()
        const [provinces, yezds, volosts, villages] = await Promise.all([
          api('/api/provinces/', { headers }).catch(() => []),
          api('/api/yezds/', { headers }).catch(() => []),
          api('/api/volosts/', { headers }).catch(() => []),
          api('/api/villages/', { headers }).catch(() => [])
        ])
        
        this.provincesList = Array.isArray(provinces) ? provinces : (provinces.results || [])
        this.yezdsList = Array.isArray(yezds) ? yezds : (yezds.results || [])
        this.volostsList = Array.isArray(volosts) ? volosts : (volosts.results || [])
        this.villagesList = Array.isArray(villages) ? villages : (villages.results || [])
      } catch (err) {
        console.error('Ошибка загрузки справочников:', err)
      }
    },

    async fetchPersonData() {
      this.loading = true
      this.error = null
      
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.error = 'Необходима авторизация'
          this.loading = false
          return
        }

        const headers = authHeaders()

        // 1. Загружаем данные персоны
        const personData = await api(`/api/persons/${this.personId}/`, { headers })
        this.person = {
          ...personData,
          full_name: `${personData.surname || ''} ${personData.name || ''} ${personData.patronymic || ''}`.trim(),
          estate_name: personData.estate_name,
          creed_name: personData.creed_name,
          province: personData.province,
          yezd: personData.yezd,
          volost: personData.volost,
          village: personData.village
        }

        // 2. Загружаем запись о рождении
        const allBirths = await api('/api/birth-records/', { headers })
        const births = Array.isArray(allBirths) ? allBirths : (allBirths.results || [])
        
        for (const birth of births) {
          const birthPersonId = birth.person ? parseInt(birth.person) : (birth.person_data?.person_id ? parseInt(birth.person_data.person_id) : null)
          
          if (birthPersonId === this.personId) {
            let numberCase = null
            if (birth.archive) {
              try {
                const archiveData = await api(`/api/archives/${birth.archive}/`, { headers })
                numberCase = archiveData.number_case
              } catch (e) {}
            }
            
            this.birthRecordAsChild = {
              ...birth,
              number_case: numberCase || birth.number_case
            }
            break
          }
        }

        // 3. Загружаем запись о смерти
        const allDeaths = await api('/api/death-records/', { headers })
        const deaths = Array.isArray(allDeaths) ? allDeaths : (allDeaths.results || [])
        
        for (const death of deaths) {
          const deathPersonId = death.person ? parseInt(death.person) : (death.person_data?.person_id ? parseInt(death.person_data.person_id) : null)
          
          if (deathPersonId === this.personId) {
            let numberCase = null
            if (death.archive) {
              try {
                const archiveData = await api(`/api/archives/${death.archive}/`, { headers })
                numberCase = archiveData.number_case
              } catch (e) {}
            }
            
            this.deathRecord = {
              ...death,
              number_case: numberCase || death.number_case
            }
            break
          }
        }

        // 4. Загружаем брак
        let husbandsData = await api(`/api/husbands/?person=${this.personId}`, { headers })
        let husbands = Array.isArray(husbandsData) ? husbandsData : (husbandsData.results || [])
        
        if (husbands.length > 0) {
          const h = husbands[0]
          const marriageData = await api(`/api/marriage-records/${h.marriage}/`, { headers })
          
          let numberCase = null
          if (marriageData.archive) {
            try {
              const archiveData = await api(`/api/archives/${marriageData.archive}/`, { headers })
              numberCase = archiveData.number_case
            } catch (e) {}
          }
          
          const wivesData = await api(`/api/wives/?marriage=${h.marriage}`, { headers })
          const wives = Array.isArray(wivesData) ? wivesData : (wivesData.results || [])
          let spouse = null
          if (wives.length > 0) {
            const wife = wives[0]
            if (wife.person) {
              const wifePerson = await api(`/api/persons/${wife.person}/`, { headers })
              spouse = {
                person_id: wifePerson.person_id,
                full_name: `${wifePerson.surname || ''} ${wifePerson.name || ''} ${wifePerson.patronymic || ''}`.trim(),
                sex: 'Ж'
              }
            } else {
              spouse = {
                person_id: null,
                full_name: `${wife.person_surname || ''} ${wife.person_name || ''}`.trim(),
                sex: 'Ж'
              }
            }
          }
          
          const maleGuarantorsData = await api(`/api/male-guarantors/?marriage=${h.marriage}`, { headers })
          const maleGuarantors = Array.isArray(maleGuarantorsData) ? maleGuarantorsData : (maleGuarantorsData.results || [])
          
          const femaleGuarantorsData = await api(`/api/female-guarantors/?marriage=${h.marriage}`, { headers })
          const femaleGuarantors = Array.isArray(femaleGuarantorsData) ? femaleGuarantorsData : (femaleGuarantorsData.results || [])
          
          this.marriageRecord = {
            marriage_id: h.marriage,
            spouse: spouse,
            spouse_age: wives[0]?.age,
            number_marriage: h.number_marriage,
            date: marriageData.date,
            archive_name: marriageData.archive_name,
            number_case: numberCase,
            page: marriageData.page,
            number_record: marriageData.number_record,
            male_guarantors: maleGuarantors,
            female_guarantors: femaleGuarantors,
            priests: marriageData.priests || [],
            scan_url: null
          }
        } else {
          const wivesData = await api(`/api/wives/?person=${this.personId}`, { headers })
          const wives = Array.isArray(wivesData) ? wivesData : (wivesData.results || [])
          
          if (wives.length > 0) {
            const w = wives[0]
            const marriageData = await api(`/api/marriage-records/${w.marriage}/`, { headers })
            
            let numberCase = null
            if (marriageData.archive) {
              try {
                const archiveData = await api(`/api/archives/${marriageData.archive}/`, { headers })
                numberCase = archiveData.number_case
              } catch (e) {}
            }
            
            const husbandsData2 = await api(`/api/husbands/?marriage=${w.marriage}`, { headers })
            const husbands2 = Array.isArray(husbandsData2) ? husbandsData2 : (husbandsData2.results || [])
            let spouse = null
            if (husbands2.length > 0) {
              const husband = husbands2[0]
              if (husband.person) {
                const husbandPerson = await api(`/api/persons/${husband.person}/`, { headers })
                spouse = {
                  person_id: husbandPerson.person_id,
                  full_name: `${husbandPerson.surname || ''} ${husbandPerson.name || ''} ${husbandPerson.patronymic || ''}`.trim(),
                  sex: 'М'
                }
              } else {
                spouse = {
                  person_id: null,
                  full_name: `${husband.person_surname || ''} ${husband.person_name || ''}`.trim(),
                  sex: 'М'
                }
              }
            }
            
            const maleGuarantorsData = await api(`/api/male-guarantors/?marriage=${w.marriage}`, { headers })
            const maleGuarantors = Array.isArray(maleGuarantorsData) ? maleGuarantorsData : (maleGuarantorsData.results || [])
            
            const femaleGuarantorsData = await api(`/api/female-guarantors/?marriage=${w.marriage}`, { headers })
            const femaleGuarantors = Array.isArray(femaleGuarantorsData) ? femaleGuarantorsData : (femaleGuarantorsData.results || [])
            
            this.marriageRecord = {
              marriage_id: w.marriage,
              spouse: spouse,
              spouse_age: husbands2[0]?.age,
              number_marriage: w.number_marriage,
              date: marriageData.date,
              archive_name: marriageData.archive_name,
              number_case: numberCase,
              page: marriageData.page,
              number_record: marriageData.number_record,
              male_guarantors: maleGuarantors,
              female_guarantors: femaleGuarantors,
              priests: marriageData.priests || [],
              scan_url: null
            }
          }
        }

        // 5. Загружаем родственные связи
        this.allRelationships = []
        
        // 5.1. Прямые связи - персона является whom (кому) - это родственники персоны
        const relationsWhomData = await api(`/api/relationships/?whom=${this.personId}`, { headers })
        const relationsWhom = relationsWhomData.results || relationsWhomData || []
        
        for (const r of relationsWhom) {
          let whoId = null
          let whoName = ''
          let kinshipName = ''
          
          if (r.who) {
            if (typeof r.who === 'object') {
              whoId = r.who.person_id
              whoName = `${r.who.surname || ''} ${r.who.name || ''}`.trim()
              kinshipName = r.kinship_name || (r.kinship?.name) || 'родственник'
            } else {
              whoId = r.who
              whoName = r.who_name || `ID:${r.who}`
              kinshipName = r.kinship_name || 'родственник'
            }
            
            this.allRelationships.push({
              id: `whom_${r.relationship_id}`,
              related_person_name: whoName || 'Неизвестно',
              relation_type: kinshipName,
              related_person_id: whoId
            })
          }
        }
        
        // 5.2. Обратные связи - персона является who (кто) - это те, для кого персона является родственником
        const relationsWhoData = await api(`/api/relationships/?who=${this.personId}`, { headers })
        const relationsWho = relationsWhoData.results || relationsWhoData || []
        
        for (const r of relationsWho) {
          let whomId = null
          let whomName = ''
          let kinshipName = ''
          
          if (r.whom) {
            if (typeof r.whom === 'object') {
              whomId = r.whom.person_id
              whomName = `${r.whom.surname || ''} ${r.whom.name || ''}`.trim()
              kinshipName = r.kinship_name || (r.kinship?.name) || 'родственник'
            } else {
              whomId = r.whom
              whomName = r.whom_name || `ID:${r.whom}`
              kinshipName = r.kinship_name || 'родственник'
            }
            
            // Для обратной связи меняем название родства
            let reverseKinship = this.getReverseKinship(kinshipName, this.person.sex)
            
            // Отображаем связь в правильном порядке: "Отец: Иван" (если персона сын)
            this.allRelationships.push({
              id: `who_${r.relationship_id}`,
              related_person_name: whomName || 'Неизвестно',
              relation_type: reverseKinship,
              related_person_id: whomId
            })
          }
        }

        // Удаляем дубликаты (если есть одинаковые связи)
        const uniqueRelationships = []
        const seen = new Set()
        for (const rel of this.allRelationships) {
          const key = `${rel.related_person_id}_${rel.relation_type}`
          if (!seen.has(key) && rel.related_person_id && rel.related_person_id !== this.personId) {
            seen.add(key)
            uniqueRelationships.push(rel)
          }
        }
        this.allRelationships = uniqueRelationships

      } catch (err) {
        console.error('Ошибка загрузки данных:', err)
        this.error = err.message || 'Не удалось загрузить данные.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Стили остаются без изменений */
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
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  padding: 4px 0;
  transition: color .15s;
}

.btn-back svg {
  width: 18px;
  height: 18px;
}

.btn-back:hover {
  color: #1a1a1a;
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -.3px;
  margin: 0;
}

.gender-badge {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.gender-male {
  background: #e8eef8;
  color: #2a55a0;
}

.gender-female {
  background: #fce8f4;
  color: #9b2c7a;
}

.person-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  background: #fff;
  border-radius: 20px;
  padding: 20px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0efee;
}

.card-icon {
  width: 20px;
  height: 20px;
  color: #888780;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.info-grid.small {
  grid-template-columns: repeat(3, 1fr);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item.full-width {
  grid-column: span 4;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #888;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  word-break: break-word;
}

.sub-section {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #efeeec;
}

.sub-title {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 12px;
}

.simple-info-block {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: #faf9f8;
  border-radius: 14px;
}

.simple-icon {
  font-size: 32px;
}

.simple-info {
  flex: 1;
}

.simple-name {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.simple-details {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #888;
  flex-wrap: wrap;
}

.compact-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: #faf9f8;
  border-radius: 12px;
}

.compact-icon {
  font-size: 22px;
}

.compact-info {
  flex: 1;
}

.compact-name {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.compact-meta {
  font-size: 11px;
  color: #888;
}

.scan-section {
  margin-top: 12px;
}

.scan-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f0efee;
  border-radius: 8px;
  color: #1a1a1a;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.2s;
}

.scan-link svg {
  width: 16px;
  height: 16px;
}

.scan-link:hover {
  background: #e9e7e3;
}

.state-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px 0;
  font-size: 14px;
  color: #666;
}

.error-box {
  color: #a00;
  flex-direction: column;
}

.retry-btn {
  padding: 6px 16px;
  background: transparent;
  border: 1px solid #a00;
  border-radius: 6px;
  color: #a00;
  cursor: pointer;
  font-size: 13px;
}

.retry-btn:hover {
  background: #fee;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ccc;
  border-top-color: #666;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 900px) {
  .main-content {
    padding: 20px;
  }
  
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .info-item.full-width {
    grid-column: span 2;
  }
  
  .info-grid.small {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .simple-details {
    flex-direction: column;
    gap: 4px;
  }
}

@media (max-width: 500px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item.full-width {
    grid-column: span 1;
  }
}
</style>