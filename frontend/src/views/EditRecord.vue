<template>
  <div class="birth-layout">

    <!-- ══════════════ ЛЕВАЯ ПАНЕЛЬ — ФОРМА ══════════════ -->
    <div class="form-panel">
      <div class="form-header">
        <div class="header-top">
          <button type="button" class="btn-back" @click="$router.push('/home')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="18" height="18">
              <path d="M19 12H5M12 5l-7 7 7 7"/>
            </svg>
            Назад
          </button>
          <div class="edit-badge">
            <span class="edit-dot"></span>
            Редактирование
          </div>
        </div>

        <h2 class="page-title">Запись о <em>{{ typeLabel }}</em></h2>

        <div v-if="pageLoading" class="info-banner">⏳ Загрузка данных записи…</div>
        <div v-if="error"       class="error-banner">{{ error }}</div>
        <div v-if="successMsg"  class="success-banner">{{ successMsg }}</div>
      </div>

      <div v-if="pageLoading" class="state-box">
        <span class="spinner"></span>
        <span>Загрузка…</span>
      </div>

      <form v-else @submit.prevent="handleSave" class="form-body">

        <!-- ══ АРХИВ ══ -->
        <section class="block">
          <h3 class="block-title">Архив</h3>
          <div class="field full">
            <label>Название архива</label>
            <div class="combobox-wrap">
              <input
                type="text" v-model="archiveSearch"
                @input="archiveDropOpen = true; formData.archive_id = null"
                @focus="archiveDropOpen = true"
                @blur="closeArchiveDrop"
                placeholder="Начните вводить…" autocomplete="off"
                :class="['combo-input', { auto: autoFields.archive }]"
              />
              <ul v-show="archiveDropOpen && archiveDropItems.length" class="drop-list">
                <li v-for="a in archiveDropItems" :key="a.archive_id"
                  @mousedown.prevent="selectArchive(a)" class="drop-item">
                  <span class="drop-main">{{ a.name }}</span>
                  <span class="drop-sub">{{ a.number_case }} · {{ a.year }}</span>
                </li>
              </ul>
            </div>
            <span v-if="autoFields.archive" class="auto-hint">⚡ Загружено из записи</span>
          </div>
          <div class="row three">
            <div class="field">
              <label>Номер дела</label>
              <input type="text" v-model="formData.number_case" :class="{ auto: autoFields.archive }" placeholder="Ф.160 Оп.1" />
            </div>
            <div class="field">
              <label>Год индексации</label>
              <input type="number" v-model.number="formData.year" :class="{ auto: autoFields.archive }" placeholder="1850" />
            </div>
            <div class="field">
              <label>Номер листа</label>
              <input type="number" v-model.number="formData.page" :class="{ auto: autoFields.page }" required placeholder="1" />
              <span v-if="autoFields.page" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
          <div class="row two">
            <div class="field">
              <label>Номер записи</label>
              <input type="number" v-model.number="formData.number_record" :class="{ auto: autoFields.number_record }" required placeholder="1" />
              <span v-if="autoFields.number_record" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field checkbox-field">
              <label>&nbsp;</label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.page_turn" />
                Оборот листа
              </label>
            </div>
          </div>
        </section>

        <!-- ══ BIRTH: ДАТА ══ -->
        <section v-if="recordType === 'birth'" class="block">
          <h3 class="block-title">Дата</h3>
          <div class="row three">
            <div class="field">
              <label>Месяц рождения</label>
              <select v-model.number="formData.birth_month" :class="{ auto: autoFields.birth_month }" required>
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
              <span v-if="autoFields.birth_month" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Число рождения</label>
              <input type="number" min="1" max="31" v-model.number="formData.birth_day" :class="{ auto: autoFields.birth_day }" required placeholder="1" />
              <span v-if="autoFields.birth_day" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Число крещения</label>
              <input type="number" min="1" max="31" v-model.number="formData.baptism_day" :class="{ auto: autoFields.baptism_day }" required placeholder="3" />
              <span v-if="autoFields.baptism_day" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
        </section>

        <!-- ══ MARRIAGE: ДАТА ══ -->
        <section v-if="recordType === 'marriage'" class="block">
          <h3 class="block-title">Дата венчания</h3>
          <div class="row three">
            <div class="field">
              <label>Месяц</label>
              <select v-model.number="formData.marriage_month" :class="{ auto: autoFields.marriage_month }" required>
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
            </div>
            <div class="field">
              <label>Число</label>
              <input type="number" min="1" max="31" v-model.number="formData.marriage_day" :class="{ auto: autoFields.marriage_day }" required placeholder="1" />
            </div>
            <div class="field">
              <label>Год</label>
              <input type="number" v-model.number="formData.marriage_year" :class="{ auto: autoFields.marriage_year }" required placeholder="1850" />
            </div>
          </div>
        </section>

        <!-- ══ DEATH: ДАТА ══ -->
        <section v-if="recordType === 'death'" class="block">
          <h3 class="block-title">Дата смерти</h3>
          <div class="row three">
            <div class="field">
              <label>Месяц</label>
              <select v-model.number="formData.death_month" :class="{ auto: autoFields.death_month }" required>
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
            </div>
            <div class="field">
              <label>Число смерти</label>
              <input type="number" min="1" max="31" v-model.number="formData.death_day" :class="{ auto: autoFields.death_day }" required placeholder="1" />
            </div>
            <div class="field">
              <label>Число погребения</label>
              <input type="number" min="1" max="31" v-model.number="formData.burial_day" :class="{ auto: autoFields.burial_day }" placeholder="3" />
            </div>
          </div>
        </section>

        <!-- ══ BIRTH: РОДИВШИЙСЯ ══ -->
        <section v-if="recordType === 'birth'" class="block">
          <h3 class="block-title">О родившемся</h3>
          <div class="row two">
            <div class="field">
              <label>Пол <span class="req">*</span></label>
              <select v-model="formData.sex" :class="{ auto: autoFields.sex }" required>
                <option value="">Выберите</option>
                <option value="М">Мужской</option>
                <option value="Ж">Женский</option>
              </select>
              <span v-if="autoFields.sex" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.name" :class="{ auto: autoFields.name }" required placeholder="Иван" />
              <span v-if="autoFields.name" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
          <div class="row two">
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.child_patronymic" :class="{ auto: autoFields.child_patronymic }" placeholder="Петрович" />
              <span v-if="autoFields.child_patronymic" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input type="text" v-model="formData.child_surname" :class="{ auto: autoFields.child_surname }" placeholder="Смирнов" />
              <span v-if="autoFields.child_surname" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
        </section>

        <!-- ══ BIRTH: ОТЕЦ ══ -->
        <section v-if="recordType === 'birth'" class="block">
          <h3 class="block-title">Отец</h3>

          <div class="location-block">
            <div class="location-header">
              <span class="location-label">Место жительства</span>
            </div>
            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="provinceSearch"
                    @input="provinceDropOpen = true; formData.father_province_id = ''"
                    @focus="provinceDropOpen = true"
                    @blur="closeLocationDrop('province')"
                    autocomplete="off" :class="['combo-input', { auto: autoFields.father_province_id }]"
                    placeholder="Начните вводить…" />
                  <ul v-show="provinceDropOpen && filteredProvinces.length" class="drop-list">
                    <li v-for="p in filteredProvinces" :key="p.province_id"
                      @mousedown.prevent="selectLocation('province', p)" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                  </ul>
                </div>
                <span v-if="autoFields.father_province_id" class="auto-hint">⚡ Загружено</span>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="yezdSearch"
                    @input="yezdDropOpen = true; formData.father_yezd_id = ''"
                    @focus="yezdDropOpen = true"
                    @blur="closeLocationDrop('yezd')"
                    autocomplete="off" :class="['combo-input', { auto: autoFields.father_yezd_id }]"
                    placeholder="Начните вводить…" />
                  <ul v-show="yezdDropOpen && filteredYezds.length" class="drop-list">
                    <li v-for="y in filteredYezds" :key="y.yezd_id"
                      @mousedown.prevent="selectLocation('yezd', y)" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                  </ul>
                </div>
                <span v-if="autoFields.father_yezd_id" class="auto-hint">⚡ Загружено</span>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="volostSearch"
                    @input="volostDropOpen = true; formData.father_volost_id = ''"
                    @focus="volostDropOpen = true"
                    @blur="closeLocationDrop('volost')"
                    autocomplete="off" :class="['combo-input', { auto: autoFields.father_volost_id }]"
                    placeholder="Начните вводить…" />
                  <ul v-show="volostDropOpen && filteredVolosts.length" class="drop-list">
                    <li v-for="v in filteredVolosts" :key="v.volost_id"
                      @mousedown.prevent="selectLocation('volost', v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
                <span v-if="autoFields.father_volost_id" class="auto-hint">⚡ Загружено</span>
              </div>
              <div class="field">
                <label>Село / Населённый пункт</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="villageSearch"
                    @input="villageDropOpen = true; formData.father_village_id = ''"
                    @focus="villageDropOpen = true"
                    @blur="closeLocationDrop('village')"
                    autocomplete="off" :class="['combo-input', { auto: autoFields.father_village_id }]"
                    placeholder="Начните вводить…" />
                  <ul v-show="villageDropOpen && filteredVillages.length" class="drop-list">
                    <li v-for="v in filteredVillages" :key="v.village_id"
                      @mousedown.prevent="selectLocation('village', v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
                <span v-if="autoFields.father_village_id" class="auto-hint">⚡ Загружено</span>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field">
              <label>Сословие <span class="req">*</span></label>
              <select v-model="formData.father_estate_id" :class="{ auto: autoFields.father_estate_id }" required>
                <option value="">Выберите</option>
                <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
              </select>
              <span v-if="autoFields.father_estate_id" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Вероисповедание <span class="req">*</span></label>
              <select v-model="formData.creed_id" :class="{ auto: autoFields.creed_id }" required>
                <option value="">Выберите</option>
                <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
              </select>
              <span v-if="autoFields.creed_id" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
          <div class="row three">
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.father_name" :class="{ auto: autoFields.father_name }" required placeholder="Пётр" />
              <span v-if="autoFields.father_name" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.father_patronymic" :class="{ auto: autoFields.father_patronymic }" placeholder="Иванович" />
            </div>
            <div class="field">
              <label>Фамилия <span class="req">*</span></label>
              <input type="text" v-model="formData.father_surname" :class="{ auto: autoFields.father_surname }" required placeholder="Смирнов" />
              <span v-if="autoFields.father_surname" class="auto-hint">⚡ Загружено</span>
            </div>
          </div>
        </section>

        <!-- ══ BIRTH: МАТЬ ══ -->
        <section v-if="recordType === 'birth'" class="block">
          <h3 class="block-title">Мать</h3>
          <div class="row two">
            <div class="field">
              <label>Статус <span class="req">*</span></label>
              <select v-model="formData.mother_status" :class="{ auto: autoFields.mother_status }" required>
                <option value="">Выберите</option>
                <option v-for="s in motherStatuses" :key="s.status_choice_id" :value="s.name">{{ s.name }}</option>
              </select>
              <span v-if="autoFields.mother_status" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Сословие</label>
              <input type="text" :value="fatherEstateName" readonly class="readonly-input" placeholder="Берётся от отца" />
            </div>
          </div>
          <div class="row three">
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.mother_name" :class="{ auto: autoFields.mother_name }" required placeholder="Мария" />
              <span v-if="autoFields.mother_name" class="auto-hint">⚡ Загружено</span>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.mother_patronymic" :class="{ auto: autoFields.mother_patronymic }" placeholder="Петровна" />
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input type="text" v-model="formData.mother_surname" :class="{ auto: autoFields.mother_surname }" placeholder="Смирнова" />
            </div>
          </div>
        </section>

        <!-- ══ BIRTH: ВОСПРИЕМНИКИ ══ -->
        <section v-if="recordType === 'birth'" class="block">
          <div class="block-title-row">
            <h3 class="block-title">Восприемники (мужчины)</h3>
            <button type="button" class="btn-add-block" @click="addGodman">＋ добавить</button>
          </div>
          <div v-for="(g, i) in godmen" :key="'gm'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Восприемник #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="godmen.splice(i,1)" v-if="godmen.length > 1">✕</button>
            </div>
            <div class="row two">
              <div class="field">
                <label>Имя</label>
                <input type="text" v-model="g.name" placeholder="Имя" />
              </div>
              <div class="field">
                <label>Фамилия</label>
                <input type="text" v-model="g.surname" placeholder="Фамилия" />
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Отчество</label>
                <input type="text" v-model="g.patronymic" placeholder="Отчество" />
              </div>
              <div class="field">
                <label>Сословие</label>
                <select v-model="g.estate_id">
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
              </div>
            </div>
          </div>
        </section>

        <section v-if="recordType === 'birth'" class="block">
          <div class="block-title-row">
            <h3 class="block-title">Восприемницы (женщины)</h3>
            <button type="button" class="btn-add-block" @click="addGodmother">＋ добавить</button>
          </div>
          <div v-for="(g, i) in godmothers" :key="'gw'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Восприемница #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="godmothers.splice(i,1)" v-if="godmothers.length > 1">✕</button>
            </div>
            <div class="row three">
              <div class="field">
                <label>Имя</label>
                <input type="text" v-model="g.name" placeholder="Имя" />
              </div>
              <div class="field">
                <label>Отчество</label>
                <input type="text" v-model="g.patronymic" placeholder="Отчество" />
              </div>
              <div class="field">
                <label>Фамилия</label>
                <input type="text" v-model="g.surname" placeholder="Фамилия" />
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Сословие</label>
                <select v-model="g.estate_id">
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
              </div>
              <div class="field">
                <label>Статус</label>
                <select v-model="g.status">
                  <option value="">Выберите</option>
                  <option value="жена">Жена</option>
                  <option value="вдова">Вдова</option>
                  <option value="девица">Девица</option>
                </select>
              </div>
            </div>
          </div>
        </section>

        <!-- ══ MARRIAGE: ЖЕНИХ / НЕВЕСТА ══ -->
        <section v-if="recordType === 'marriage'" class="block">
          <h3 class="block-title">Жених</h3>
          <div class="row three">
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.groom_name" :class="{ auto: autoFields.groom_name }" required placeholder="Иван" />
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.groom_patronymic" :class="{ auto: autoFields.groom_patronymic }" placeholder="Петрович" />
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input type="text" v-model="formData.groom_surname" :class="{ auto: autoFields.groom_surname }" placeholder="Смирнов" />
            </div>
          </div>
          <div class="row two">
            <div class="field">
              <label>Сословие</label>
              <select v-model="formData.groom_estate_id" :class="{ auto: autoFields.groom_estate_id }">
                <option value="">Выберите</option>
                <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
              </select>
            </div>
            <div class="field">
              <label>Вероисповедание</label>
              <select v-model="formData.creed_id" :class="{ auto: autoFields.creed_id }">
                <option value="">Выберите</option>
                <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
              </select>
            </div>
          </div>
        </section>

        <section v-if="recordType === 'marriage'" class="block">
          <h3 class="block-title">Невеста</h3>
          <div class="row three">
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.bride_name" :class="{ auto: autoFields.bride_name }" required placeholder="Мария" />
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.bride_patronymic" :class="{ auto: autoFields.bride_patronymic }" placeholder="Ивановна" />
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input type="text" v-model="formData.bride_surname" :class="{ auto: autoFields.bride_surname }" placeholder="Петрова" />
            </div>
          </div>
          <div class="field">
            <label>Сословие</label>
            <select v-model="formData.bride_estate_id" :class="{ auto: autoFields.bride_estate_id }">
              <option value="">Выберите</option>
              <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
            </select>
          </div>
        </section>

        <!-- ══ DEATH: УМЕРШИЙ ══ -->
        <section v-if="recordType === 'death'" class="block">
          <h3 class="block-title">Об умершем</h3>
          <div class="row two">
            <div class="field">
              <label>Пол <span class="req">*</span></label>
              <select v-model="formData.sex" :class="{ auto: autoFields.sex }" required>
                <option value="">Выберите</option>
                <option value="М">Мужской</option>
                <option value="Ж">Женский</option>
              </select>
            </div>
            <div class="field">
              <label>Возраст</label>
              <input type="number" v-model.number="formData.age" :class="{ auto: autoFields.age }" placeholder="65" />
            </div>
          </div>
          <div class="row three">
            <div class="field">
              <label>Имя <span class="req">*</span></label>
              <input type="text" v-model="formData.name" :class="{ auto: autoFields.name }" required placeholder="Иван" />
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.patronymic" :class="{ auto: autoFields.patronymic }" placeholder="Петрович" />
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input type="text" v-model="formData.surname" :class="{ auto: autoFields.surname }" placeholder="Смирнов" />
            </div>
          </div>
          <div class="row two">
            <div class="field">
              <label>Сословие</label>
              <select v-model="formData.estate_id" :class="{ auto: autoFields.estate_id }">
                <option value="">Выберите</option>
                <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
              </select>
            </div>
            <div class="field">
              <label>Причина смерти</label>
              <input type="text" v-model="formData.death_cause" :class="{ auto: autoFields.death_cause }" placeholder="Горячка" />
            </div>
          </div>
        </section>

        <!-- ══ ПРИМЕЧАНИЕ ══ -->
        <section class="block">
          <h3 class="block-title">Примечание</h3>
          <div class="field full">
            <textarea v-model="formData.comment" :class="{ auto: autoFields.comment }" rows="3" placeholder="Дополнительные сведения…"></textarea>
          </div>
        </section>

        <div class="form-footer">
          <button type="submit" class="btn-submit" :disabled="saving || deleting">
            {{ saving ? 'Сохранение…' : '✓ Сохранить изменения' }}
          </button>
        </div>
      </form>
    </div>

    <!-- ══════════════ ПРАВАЯ ПАНЕЛЬ — СКАН ══════════════ -->
    <div class="scan-panel">
      <div
        class="scan-viewport"
        @mousedown="startDrag" @wheel.prevent="onWheel"
        :class="{ grabbing: isDragging }"
      >
        <div v-if="scanLoading" class="scan-empty">
          <span class="spinner scan-spinner"></span>
          <p style="margin-top:12px">Загрузка скана…</p>
        </div>
        <div v-else-if="scanSrc" class="scan-inner" :style="scanTransformStyle">
          <img :src="scanSrc" alt="Скан документа" draggable="false" />
        </div>
        <div v-else class="scan-empty">
          <div class="scan-empty-icon">📄</div>
          <p>Скан не найден</p>
          <p class="scan-empty-hint">Загрузите скан документа</p>
        </div>
      </div>
      <div class="scan-toolbar">
        <button @click="zoomOut" :disabled="zoom <= 0.2" class="scan-btn">−</button>
        <span class="zoom-display">{{ Math.round(zoom * 100) }}%</span>
        <button @click="zoomIn"  :disabled="zoom >= 8"   class="scan-btn">+</button>
        <button @click="resetScan" class="scan-btn">⟳</button>
        <label class="scan-upload-btn">
          📁 Загрузить скан
          <input type="file" accept="image/*" @change="loadScan" style="display:none" />
        </label>
        <span v-if="scanFile" class="scan-new-badge">● новый</span>
      </div>
    </div>

    <!-- ══════════════ ДИАЛОГ УДАЛЕНИЯ ══════════════ -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal">
        <div class="modal-icon">⚠️</div>
        <h4>Удалить запись?</h4>
        <p class="modal-desc">
          Будет удалена запись о {{ typeLabel }} и связанная персона. Это действие нельзя отменить.
        </p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="showDeleteModal = false">Отмена</button>
          <button type="button" class="btn-confirm-delete" @click="confirmDelete" :disabled="deleting">
            {{ deleting ? 'Удаление…' : 'Да, удалить' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { api, authHeaders, API_BASE } from '@/utils/api.js'

const TYPE_CONFIG = {
  birth:    { label: 'рождении',  endpoint: id => `/api/birth-records/${id}/`,    personEndpoint: id => `/api/persons/${id}/` },
  marriage: { label: 'браке',     endpoint: id => `/api/marriage-records/${id}/`, personEndpoint: id => `/api/persons/${id}/` },
  death:    { label: 'смерти',    endpoint: id => `/api/death-records/${id}/`,    personEndpoint: id => `/api/persons/${id}/` },
}

// Вытащить числовой ID из поля, которое может быть числом или объектом
function resolveId(val, idKey) {
  if (!val && val !== 0) return ''
  if (typeof val === 'object') return val[idKey] ?? ''
  return val
}

// Вытащить имя из поля или из списка по id
function resolveName(val, list, idKey) {
  if (!val && val !== 0) return ''
  if (typeof val === 'object' && val !== null) return val.name ?? ''
  const found = list.find(i => i[idKey] === val)
  return found ? found.name : ''
}

export default {
  name: 'EditRecord',

  data() {
    return {
      pageLoading: true,
      saving:  false,
      deleting: false,
      error:    null,
      successMsg: null,
      showDeleteModal: false,

      recordType: '',
      recordId:   null,
      personId:   null,

      // Флаги жёлтой подсветки — true для каждого поля, которое заполнено из API
      autoFields: {},

      allArchives:   [],
      estates:       [],
      religions:     [],
      provinces:     [],
      yezds:         [],
      volosts:       [],
      villages:      [],
      motherStatuses: [],

      archiveSearch:   '',
      archiveDropOpen: false,
      provinceSearch:  '',
      provinceDropOpen: false,
      yezdSearch:      '',
      yezdDropOpen:    false,
      volostSearch:    '',
      volostDropOpen:  false,
      villageSearch:   '',
      villageDropOpen: false,

      formData: {
        archive_id: null, number_case: '', year: '', page: '', page_turn: false, number_record: '', comment: '',
        // birth
        birth_month: '', birth_day: '', baptism_day: '',
        sex: '', name: '', child_patronymic: '', child_surname: '',
        father_province_id: '', father_yezd_id: '', father_volost_id: '', father_village_id: '',
        father_name: '', father_patronymic: '', father_surname: '',
        father_estate_id: '', creed_id: '',
        mother_name: '', mother_patronymic: '', mother_surname: '', mother_status: '',
        // marriage
        marriage_month: '', marriage_day: '', marriage_year: '',
        groom_name: '', groom_patronymic: '', groom_surname: '', groom_estate_id: '',
        bride_name: '', bride_patronymic: '', bride_surname: '', bride_estate_id: '',
        // death
        death_month: '', death_day: '', burial_day: '',
        age: '', patronymic: '', surname: '', estate_id: '', death_cause: '',
      },

      godmen:     [],
      godmothers: [],

      // скан
      scanSrc:     null,
      scanFile:    null,
      scanLoading: false,
      zoom: 1, panX: 0, panY: 0,
      isDragging: false,
      _dragStartX: 0, _dragStartY: 0,

      months: ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
    }
  },

  computed: {
    typeLabel() { return TYPE_CONFIG[this.recordType]?.label || '' },

    archiveDropItems() {
      const q = this.archiveSearch.toLowerCase().trim()
      if (!q) return this.allArchives
      return this.allArchives.filter(a => a.name.toLowerCase().includes(q) || (a.number_case||'').toLowerCase().includes(q))
    },

    filteredProvinces() { return this.filterList(this.provinces, this.provinceSearch) },
    filteredYezds()     { return this.filterList(this.yezds,     this.yezdSearch) },
    filteredVolosts()   { return this.filterList(this.volosts,   this.volostSearch) },
    filteredVillages()  { return this.filterList(this.villages,  this.villageSearch) },

    fatherEstateName() {
      const e = this.estates.find(e => e.estate_id === this.formData.father_estate_id)
      return e ? e.name : ''
    },

    scanTransformStyle() {
      return {
        position: 'absolute',
        transformOrigin: 'center center',
        transform: `translate(${this.panX}px,${this.panY}px) scale(${this.zoom})`,
        transition: this.isDragging ? 'none' : 'transform 0.08s ease',
      }
    },
  },

  async mounted() {
    this.recordType = this.$route.params.type
    this.recordId   = this.$route.params.id

    // Сначала загружаем справочники, потом запись —
    // чтобы при заполнении уже были списки для resolveName
    await this.loadReferenceData()
    await this.loadRecord()
    this.pageLoading = false
  },

  beforeUnmount() {
    document.removeEventListener('mousemove', this._onMouseMove)
    document.removeEventListener('mouseup',   this._onMouseUp)
  },

  methods: {
    filterList(list, search) {
      const q = (search || '').toLowerCase().trim()
      return q ? list.filter(i => i.name.toLowerCase().includes(q)) : list
    },

    // ── Справочники ────────────────────────────────────────────────────────
    async loadReferenceData() {
      try {
        const h = authHeaders()
        const [archives, estates, religions, provinces, yezds, volosts, villages, motherStatuses] =
          await Promise.all([
            api('/api/archives/',       { headers: h }),
            api('/api/estates/',        { headers: h }),
            api('/api/religions/',      { headers: h }),
            api('/api/provinces/',      { headers: h }),
            api('/api/yezds/',          { headers: h }),
            api('/api/volosts/',        { headers: h }),
            api('/api/villages/',       { headers: h }),
            api('/api/status-choices/', { headers: h }),
          ])
        this.allArchives    = archives       || []
        this.estates        = estates        || []
        this.religions      = religions      || []
        this.provinces      = provinces      || []
        this.yezds          = yezds          || []
        this.volosts        = volosts        || []
        this.villages       = villages       || []
        this.motherStatuses = motherStatuses || []
      } catch (err) {
        this.error = 'Ошибка загрузки справочников: ' + err.message
      }
    },

    // ── Загрузка записи ────────────────────────────────────────────────────
    async loadRecord() {
      try {
        const cfg    = TYPE_CONFIG[this.recordType]
        if (!cfg) throw new Error('Неизвестный тип: ' + this.recordType)

        const record = await api(cfg.endpoint(this.recordId), { headers: authHeaders() })

        // Персона (id или объект)
        const pField  = record[record.person !== undefined ? 'person' : 'person_id']
        this.personId = typeof pField === 'object' ? pField?.person_id : pField

        this.fillCommon(record)

        if      (this.recordType === 'birth')    this.fillBirth(record)
        else if (this.recordType === 'marriage') this.fillMarriage(record)
        else if (this.recordType === 'death')    this.fillDeath(record)

        // Загрузка скана по имени {id}.jpg
        await this.loadScanFromServer()
      } catch (err) {
        this.error = 'Ошибка загрузки записи: ' + err.message
      }
    },

    // ── Общие поля (архив, лист, номер) ────────────────────────────────────
    fillCommon(r) {
      // Архив может прийти объектом или id
      const archObj = typeof r.archive === 'object' ? r.archive : this.allArchives.find(a => a.archive_id === r.archive)
      if (archObj) {
        this.formData.archive_id  = archObj.archive_id
        this.archiveSearch        = archObj.name       || ''
        this.formData.number_case = archObj.number_case || ''
        this.formData.year        = archObj.year        || ''
        this.setAuto('archive', true)
      }

      if (r.page)          { this.formData.page          = r.page;          this.setAuto('page', true) }
      if (r.page_turn !== undefined) this.formData.page_turn = r.page_turn
      if (r.number_record) { this.formData.number_record = r.number_record; this.setAuto('number_record', true) }
      if (r.comment)         this.formData.comment = r.comment
    },

    // ── Заполнение birth ───────────────────────────────────────────────────
    fillBirth(r) {
      // Дата
      this.setField('birth_month',  r.birth_month  ? Number(r.birth_month) : '')
      this.setField('birth_day',    r.birth_day    || '')
      this.setField('birth_day',    r.birth_day    || '')
      this.setField('baptism_day',  r.baptism_day  || '')
      this.setField('sex',          r.sex          || '')

      // Отец
      this.setField('father_name',       r.father_name       || '')
      this.setField('father_patronymic', r.father_patronymic || '')
      this.setField('father_surname',    r.father_surname    || '')

      // Сословие — поле может называться father_estate или father_estate_id
      const estateVal = r.father_estate ?? r.father_estate_id
      const estateId  = resolveId(estateVal, 'estate_id')
      if (estateId) { this.formData.father_estate_id = estateId; this.setAuto('father_estate_id', true) }

      // Вероисповедание
      const creedVal = r.creed ?? r.creed_id
      const creedId  = resolveId(creedVal, 'creed_id')
      if (creedId) { this.formData.creed_id = creedId; this.setAuto('creed_id', true) }

      // Местоположение отца — пробуем все возможные варианты названий полей
      this.fillLocation(r, 'father_province', 'province_id', 'provinceSearch', this.provinces)
      this.fillLocation(r, 'father_yezd',     'yezd_id',     'yezdSearch',     this.yezds)
      this.fillLocation(r, 'father_volost',   'volost_id',   'volostSearch',   this.volosts)
      this.fillLocation(r, 'father_village',  'village_id',  'villageSearch',  this.villages)

      // Мать
      this.setField('mother_name',       r.mother_name       || '')
      this.setField('mother_patronymic', r.mother_patronymic || '')
      this.setField('mother_surname',    r.mother_surname    || '')
      this.setField('mother_status',     r.mother_status     || '')

      // Персона-ребёнок: данные могут быть в r.person (объект) или в полях записи
      const person = r.person
      if (person && typeof person === 'object') {
        this.setField('name',             person.name       || '')
        this.setField('child_patronymic', person.patronymic || '')
        this.setField('child_surname',    person.surname    || '')
      } else {
        // Если person — просто id, ищем данные в самой записи
        // (некоторые API дублируют поля child_name / child_surname)
        this.setField('name',             r.child_name       || r.name       || '')
        this.setField('child_patronymic', r.child_patronymic || r.patronymic || '')
        this.setField('child_surname',    r.child_surname    || r.surname    || '')
      }

      // Восприемники
      this.godmen     = (r.godmen     || []).map(g => ({
        godman_id:   g.godman_id || g.id || null,
        name:        g.name        || '',
        patronymic:  g.patronymic  || '',
        surname:     g.surname     || '',
        estate_id:   resolveId(g.estate, 'estate_id'),
        province_id: resolveId(g.province, 'province_id'),
        yezd_id:     resolveId(g.yezd,    'yezd_id'),
        volost_id:   resolveId(g.volost,  'volost_id'),
        village_id:  resolveId(g.village, 'village_id'),
      }))
      this.godmothers = (r.godmothers || []).map(g => ({
        godmother_id: g.godmother_id || g.id || null,
        name:         g.name       || '',
        patronymic:   g.patronymic || '',
        surname:      g.surname    || '',
        estate_id:    resolveId(g.estate, 'estate_id'),
        status:       g.status     || '',
      }))
      if (!this.godmen.length)     this.godmen     = [this.emptyGodman()]
      if (!this.godmothers.length) this.godmothers = [this.emptyGodmother()]
    },

    // ── Заполнение поля местоположения (province/yezd/volost/village) ──────
    // API может вернуть father_province как объект {province_id, name}
    // или как число (id), или поля с суффиксом _id
    fillLocation(r, fieldBase, idKey, searchProp, list) {
      // Пробуем разные варианты: r.father_province, r.father_province_id
      const raw = r[fieldBase] ?? r[`${fieldBase}_id`]
      if (!raw && raw !== 0) return

      const id   = resolveId(raw, idKey)
      const name = resolveName(raw, list, idKey)

      const formKey = `father_${idKey}`   // father_province_id, father_yezd_id …
      if (id) {
        this.formData[formKey] = id
        this[searchProp]       = name || resolveName(id, list, idKey)
        this.setAuto(formKey, true)
      }
    },

    fillMarriage(r) {
      this.setField('marriage_month',   r.marriage_month ? Number(r.marriage_month) : '')
      this.setField('marriage_day',     r.marriage_day   || '')
      this.setField('marriage_year',    r.marriage_year  || '')
      this.setField('groom_name',       r.groom_name       || '')
      this.setField('groom_patronymic', r.groom_patronymic || '')
      this.setField('groom_surname',    r.groom_surname    || '')
      this.setField('bride_name',       r.bride_name       || '')
      this.setField('bride_patronymic', r.bride_patronymic || '')
      this.setField('bride_surname',    r.bride_surname    || '')
      const gEstId = resolveId(r.groom_estate ?? r.groom_estate_id, 'estate_id')
      if (gEstId) { this.formData.groom_estate_id = gEstId; this.setAuto('groom_estate_id', true) }
      const bEstId = resolveId(r.bride_estate ?? r.bride_estate_id, 'estate_id')
      if (bEstId) { this.formData.bride_estate_id = bEstId; this.setAuto('bride_estate_id', true) }
      const creedId = resolveId(r.creed ?? r.creed_id, 'creed_id')
      if (creedId) { this.formData.creed_id = creedId; this.setAuto('creed_id', true) }
    },

    fillDeath(r) {
      this.setField('death_month', r.death_month ? Number(r.death_month) : '')
      this.setField('death_day',   r.death_day   || '')
      this.setField('burial_day',  r.burial_day  || '')
      this.setField('sex',         r.sex         || '')
      this.setField('age',         r.age         || '')
      this.setField('death_cause', r.death_cause || '')
      const estId = resolveId(r.estate ?? r.estate_id, 'estate_id')
      if (estId) { this.formData.estate_id = estId; this.setAuto('estate_id', true) }

      const person = r.person
      if (person && typeof person === 'object') {
        this.setField('name',       person.name       || '')
        this.setField('patronymic', person.patronymic || '')
        this.setField('surname',    person.surname    || '')
      } else {
        this.setField('name',       r.name       || '')
        this.setField('patronymic', r.patronymic || '')
        this.setField('surname',    r.surname    || '')
      }
    },

    // Установить поле formData + отметить как авто (жёлтое) если значение есть
    setField(key, value) {
      this.formData[key] = value
      if (value !== '' && value !== null && value !== undefined) {
        this.setAuto(key, true)
      }
    },

    setAuto(key, val) {
      this.autoFields = { ...this.autoFields, [key]: val }
    },

    // ── Загрузка скана с сервера ────────────────────────────────────────────
    async loadScanFromServer() {
      // Скан хранится как /media/scans/birth/{id}.jpg (или .png — пробуем оба)
      const typeFolder = this.recordType  // birth / marriage / death
      const exts = ['jpg', 'jpeg', 'png', 'tiff']
      this.scanLoading = true
      for (const ext of exts) {
        const url = `${API_BASE}/media/scans/${typeFolder}/${this.recordId}.${ext}`
        try {
          const res = await fetch(url, { method: 'HEAD', headers: authHeaders() })
          if (res.ok) {
            // добавляем timestamp чтобы не брать из кеша после замены
            this.scanSrc = url + '?t=' + Date.now()
            this.scanLoading = false
            return
          }
        } catch (_) { /* продолжаем */ }
      }
      this.scanLoading = false
      // Скана нет — оставляем scanSrc = null
    },

    // ── Архив combobox ──────────────────────────────────────────────────────
    selectArchive(a) {
      this.formData.archive_id  = a.archive_id
      this.archiveSearch        = a.name
      this.formData.number_case = a.number_case
      this.formData.year        = a.year
      this.archiveDropOpen      = false
      this.setAuto('archive', false)   // пользователь выбрал сам — снимаем авто
    },
    closeArchiveDrop() { setTimeout(() => { this.archiveDropOpen = false }, 200) },

    // ── Местоположение combobox ─────────────────────────────────────────────
    selectLocation(type, item) {
      const map = {
        province: ['father_province_id', 'provinceSearch', 'provinceDropOpen'],
        yezd:     ['father_yezd_id',     'yezdSearch',     'yezdDropOpen'],
        volost:   ['father_volost_id',   'volostSearch',   'volostDropOpen'],
        village:  ['father_village_id',  'villageSearch',  'villageDropOpen'],
      }
      const [fKey, sKey, dKey] = map[type]
      this.formData[fKey] = item[Object.keys(item).find(k => k.endsWith('_id') && k !== 'archive_id')]
      this[sKey]          = item.name
      this[dKey]          = false
      this.setAuto(fKey, false)
    },
    closeLocationDrop(type) {
      const keys = { province: 'provinceDropOpen', yezd: 'yezdDropOpen', volost: 'volostDropOpen', village: 'villageDropOpen' }
      setTimeout(() => { this[keys[type]] = false }, 200)
    },

    emptyGodman()    { return { name:'', patronymic:'', surname:'', estate_id:'' } },
    emptyGodmother() { return { name:'', patronymic:'', surname:'', estate_id:'', status:'' } },
    addGodman()      { this.godmen.push(this.emptyGodman()) },
    addGodmother()   { this.godmothers.push(this.emptyGodmother()) },

    // ── Сохранение ─────────────────────────────────────────────────────────
    async handleSave() {
      this.error = null
      this.saving = true
      try {
        const H   = authHeaders(true)
        const cfg = TYPE_CONFIG[this.recordType]

        await api(cfg.endpoint(this.recordId), {
          method:  'PATCH',
          headers: H,
          body:    JSON.stringify(this.buildPatchBody()),
        })

        if (this.personId) await this.patchPerson(H)
        if (this.recordType === 'birth') { await this.saveGodmen(H); await this.saveGodmothers(H) }

        // Загрузка нового скана
        if (this.scanFile) await this.uploadScan()

        this.successMsg = '✅ Изменения сохранены'
        setTimeout(() => this.$router.push('/home'), 1000)
      } catch (err) {
        this.error = 'Ошибка при сохранении: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.saving = false
      }
    },

    buildPatchBody() {
      const f = this.formData
      const base = {
        archive:       f.archive_id    || undefined,
        page:          f.page          || undefined,
        page_turn:     f.page_turn,
        number_record: f.number_record || undefined,
        comment:       f.comment       || undefined,
      }
      if (this.recordType === 'birth') return {
        ...base,
        birth_month:       f.birth_month || undefined,
        birth_day:         f.birth_day   || undefined,
        baptism_day:       f.baptism_day || undefined,
        sex:               f.sex         || undefined,
        father_name:       f.father_name       || undefined,
        father_patronymic: f.father_patronymic || undefined,
        father_surname:    f.father_surname    || undefined,
        father_estate:     f.father_estate_id  || null,
        father_province:   f.father_province_id || null,
        father_yezd:       f.father_yezd_id     || null,
        father_volost:     f.father_volost_id   || null,
        father_village:    f.father_village_id  || null,
        creed:             f.creed_id           || null,
        mother_name:       f.mother_name        || undefined,
        mother_patronymic: f.mother_patronymic  || undefined,
        mother_surname:    f.mother_surname      || undefined,
        mother_status:     f.mother_status       || undefined,
      }
      if (this.recordType === 'marriage') return {
        ...base,
        marriage_month:   f.marriage_month   || undefined,
        marriage_day:     f.marriage_day     || undefined,
        marriage_year:    f.marriage_year    || undefined,
        groom_name:       f.groom_name       || undefined,
        groom_patronymic: f.groom_patronymic || undefined,
        groom_surname:    f.groom_surname    || undefined,
        groom_estate:     f.groom_estate_id  || null,
        bride_name:       f.bride_name       || undefined,
        bride_patronymic: f.bride_patronymic || undefined,
        bride_surname:    f.bride_surname    || undefined,
        bride_estate:     f.bride_estate_id  || null,
        creed:            f.creed_id         || null,
      }
      if (this.recordType === 'death') return {
        ...base,
        death_month: f.death_month || undefined,
        death_day:   f.death_day   || undefined,
        burial_day:  f.burial_day  || undefined,
        sex:         f.sex         || undefined,
        age:         f.age         || undefined,
        death_cause: f.death_cause || undefined,
        estate:      f.estate_id   || null,
      }
      return base
    },

    async patchPerson(H) {
      const f = this.formData
      let body = {}
      if (this.recordType === 'birth')    body = { name: f.name, patronymic: f.child_patronymic, surname: f.child_surname, sex: f.sex }
      if (this.recordType === 'death')    body = { name: f.name, patronymic: f.patronymic,        surname: f.surname,       sex: f.sex }
      if (this.recordType === 'marriage') body = { name: f.groom_name, patronymic: f.groom_patronymic, surname: f.groom_surname }
      await api(TYPE_CONFIG[this.recordType].personEndpoint(this.personId), {
        method: 'PATCH', headers: H, body: JSON.stringify(body),
      })
    },

    async saveGodmen(H) {
      try {
        await api(`/api/birth-records/${this.recordId}/godmen/`, {
          method: 'PUT', headers: H,
          body: JSON.stringify(this.godmen.filter(g => g.name?.trim()).map(g => ({
            name: g.name, patronymic: g.patronymic||null, surname: g.surname||null,
            estate: g.estate_id||null, province: g.province_id||null,
            yezd: g.yezd_id||null, volost: g.volost_id||null, village: g.village_id||null,
          }))),
        })
      } catch (_) { /* bulk-endpoint optional */ }
    },

    async saveGodmothers(H) {
      try {
        await api(`/api/birth-records/${this.recordId}/godmothers/`, {
          method: 'PUT', headers: H,
          body: JSON.stringify(this.godmothers.filter(g => g.name?.trim()).map(g => ({
            name: g.name, patronymic: g.patronymic||null, surname: g.surname||null,
            estate: g.estate_id||null, status: g.status||null,
          }))),
        })
      } catch (_) { /* bulk-endpoint optional */ }
    },

    // ── Загрузка скана на сервер ────────────────────────────────────────────
    async uploadScan() {
      const fd = new FormData()
      fd.append('scan', this.scanFile)
      // Передаём имя файла явно: {id}.ext — Django-вьюха переименует
      await fetch(`${API_BASE}/api/${this.recordType}-records/${this.recordId}/upload-scan/`, {
        method:  'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        body:    fd,
      })
    },

    // ── Удаление ─────────────────────────────────────────────────────────────
    async confirmDelete() {
      this.deleting = true
      const cfg = TYPE_CONFIG[this.recordType]
      try {
        await api(cfg.endpoint(this.recordId),     { method: 'DELETE', headers: authHeaders() })
        if (this.personId)
          await api(cfg.personEndpoint(this.personId), { method: 'DELETE', headers: authHeaders() })
        this.$router.push('/home')
      } catch (err) {
        this.error = 'Ошибка при удалении: ' + err.message
        this.showDeleteModal = false
      } finally {
        this.deleting = false
      }
    },

    // ── Скан (локальный выбор файла) ────────────────────────────────────────
    loadScan(e) {
      const file = e.target.files[0]
      if (!file) return
      this.scanFile = file
      const reader  = new FileReader()
      reader.onload = ev => { this.scanSrc = ev.target.result; this.resetScan() }
      reader.readAsDataURL(file)
    },

    startDrag(e) {
      if (!this.scanSrc) return
      e.preventDefault()
      this.isDragging = true
      this._dragStartX = e.clientX - this.panX
      this._dragStartY = e.clientY - this.panY
      this._onMouseMove = ev => { this.panX = ev.clientX - this._dragStartX; this.panY = ev.clientY - this._dragStartY }
      this._onMouseUp   = () => {
        this.isDragging = false
        document.removeEventListener('mousemove', this._onMouseMove)
        document.removeEventListener('mouseup',   this._onMouseUp)
      }
      document.addEventListener('mousemove', this._onMouseMove)
      document.addEventListener('mouseup',   this._onMouseUp)
    },
    onWheel(e) {
      if (!this.scanSrc) return
      const d = e.deltaY < 0 ? 0.15 : -0.15
      this.zoom = Math.min(8, Math.max(0.2, Math.round((this.zoom + d) * 100) / 100))
    },
    zoomIn()    { this.zoom = Math.min(8,   Math.round((this.zoom + 0.25) * 100) / 100) },
    zoomOut()   { this.zoom = Math.max(0.2, Math.round((this.zoom - 0.25) * 100) / 100) },
    resetScan() { this.zoom = 1; this.panX = 0; this.panY = 0 },
  },
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.birth-layout {
  display: flex; height: 100vh; width: 100%; overflow: hidden;
  font-family: 'PT Sans', 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px; color: #1a1a1a; background: #f0efee;
}

/* ── ЛЕВАЯ ПАНЕЛЬ ── */
.form-panel {
  width: 42%; min-width: 400px; max-width: 600px;
  display: flex; flex-direction: column; overflow: hidden;
  background: #fff; border-right: 1px solid #d5d3cf;
}
.form-header {
  padding: 20px 24px 14px; border-bottom: 1px solid #d5d3cf;
  background: #fff; position: sticky; top: 0; z-index: 10; flex-shrink: 0;
}
.header-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; gap: 12px; }
.btn-back { display: flex; align-items: center; gap: 6px; background: none; border: none; font-family: inherit; font-size: 13px; color: #555; cursor: pointer; padding: 4px 0; transition: color .15s; }
.btn-back:hover { color: #1a1a1a; }

.edit-badge { display: flex; align-items: center; gap: 6px; padding: 4px 12px; background: #f0f4ff; border: 1px solid #c7d4f5; border-radius: 20px; font-size: 12px; font-weight: 600; color: #2a55a0; }
.edit-dot { width: 7px; height: 7px; border-radius: 50%; background: #2a55a0; }

.page-title { font-size: 26px; font-weight: 700; letter-spacing: -.3px; color: #1a1a1a; margin-bottom: 2px; }
.page-title em { font-style: italic; }

.info-banner    { background: #f0f9ff; border: 1px solid #bae6fd; color: #075985; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 8px; }
.error-banner   { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 6px; }
.success-banner { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 6px; }

.form-body { flex: 1; overflow-y: auto; padding: 16px 24px; }
.form-body::-webkit-scrollbar { width: 6px; }
.form-body::-webkit-scrollbar-track { background: #f0efee; }
.form-body::-webkit-scrollbar-thumb { background: #c8c5c0; border-radius: 3px; }

/* Блоки */
.block { margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid #e9e7e3; }
.block:last-of-type { border-bottom: none; }
.block-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #888780; margin: 0 0 12px; }
.block-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.block-title-row .block-title { margin-bottom: 0; }

/* Местоположение */
.location-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px; }
.location-header { margin-bottom: 10px; }
.location-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #5f5e5a; }

/* Поля */
.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #444; }
.req { color: #a00; }
.field input, .field select, .field textarea {
  padding: 7px 10px; border: 1px solid #c8c5c0; border-radius: 6px;
  font-size: 13px; font-family: inherit; color: #1a1a1a; background: #fff;
  transition: border-color .15s, box-shadow .15s; width: 100%;
}
.field input:focus, .field select:focus, .field textarea:focus {
  outline: none; border-color: #888780; box-shadow: 0 0 0 3px rgba(136,135,128,0.12);
}
/* Жёлтая подсветка автозаполненных полей */
.field input.auto, .field select.auto, .field textarea.auto { background: #fffbeb; border-color: #fde68a; }
.combo-input.auto { background: #fffbeb !important; border-color: #fde68a !important; }
.auto-hint { font-size: 11px; color: #b45309; margin-top: 1px; }
.readonly-input { background: #f0efee !important; color: #888 !important; cursor: default; }
.field textarea { resize: vertical; min-height: 60px; }

.row { display: grid; gap: 10px; margin-bottom: 10px; }
.row.two   { grid-template-columns: 1fr 1fr; }
.row.three { grid-template-columns: 1fr 1fr 1fr; }
.full { margin-bottom: 10px; }

.checkbox-field { justify-content: flex-end; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #444; cursor: pointer; font-weight: 400 !important; padding: 7px 0; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; }

/* Combobox */
.combobox-wrap { position: relative; }
.combo-input { width: 100%; padding: 7px 10px; border: 1px solid #c8c5c0; border-radius: 6px; font-size: 13px; font-family: inherit; color: #1a1a1a; background: #fff; transition: border-color .15s; }
.combo-input:focus { outline: none; border-color: #888780; box-shadow: 0 0 0 3px rgba(136,135,128,0.12); }
.drop-list { position: absolute; top: calc(100% + 4px); left: 0; right: 0; background: #fff; border: 1px solid #c8c5c0; border-radius: 6px; z-index: 100; max-height: 200px; overflow-y: auto; list-style: none; padding: 4px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.drop-item { padding: 8px 12px; cursor: pointer; display: flex; flex-direction: column; gap: 2px; border-bottom: 1px solid #e9e7e3; }
.drop-item:last-child { border-bottom: none; }
.drop-item:hover { background: #f0efee; }
.drop-main { font-size: 13px; color: #1a1a1a; }
.drop-sub  { font-size: 11px; color: #aaa; }

/* Суб-блоки */
.sub-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; }
.sub-block-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.sub-block-header span { font-size: 12px; font-weight: 600; color: #888780; }
.btn-remove { background: none; border: none; cursor: pointer; font-size: 16px; color: #aaa; padding: 0 4px; transition: color .15s; }
.btn-remove:hover { color: #a00; }
.btn-add-block { font-size: 12px; padding: 4px 10px; background: #fff; border: 1px solid #c8c5c0; border-radius: 6px; cursor: pointer; color: #5f5e5a; font-weight: 500; font-family: inherit; transition: all .15s; }
.btn-add-block:hover { background: #e9e7e3; }

/* Подвал */
.form-footer {
  display: flex;
  gap: 10px;
  padding: 14px 24px;
  border-top: 1px solid #d5d3cf;
  background: #fff;
  flex-shrink: 0;
}
.btn-delete { padding: 9px 16px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; font-size: 13px; font-family: inherit; cursor: pointer; color: #991b1b; font-weight: 500; transition: background .15s; white-space: nowrap; }
.btn-delete:hover:not(:disabled) { background: #fee2e2; }
.btn-delete:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-submit { flex: 1; padding: 9px 20px; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; font-family: inherit; cursor: pointer; transition: background .15s; }
.btn-submit:not(:disabled) { background: #1a1a1a; color: #fff; }
.btn-submit:hover:not(:disabled) { background: #333; }
.btn-submit:disabled { background: #ccc; color: #888; cursor: not-allowed; }

/* Загрузка */
.state-box { display: flex; align-items: center; gap: 12px; padding: 40px 24px; font-size: 14px; color: #666; }
.spinner { width: 20px; height: 20px; border: 2px solid #ccc; border-top-color: #666; border-radius: 50%; animation: spin .7s linear infinite; flex-shrink: 0; }
.scan-spinner { width: 28px; height: 28px; border-width: 2.5px; border-top-color: #aaa; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── ПРАВАЯ ПАНЕЛЬ — СКАН ── */
.scan-panel { flex: 1; display: flex; flex-direction: column; background: #2c2c2a; overflow: hidden; }
.scan-viewport { flex: 1; position: relative; overflow: hidden; cursor: grab; display: flex; align-items: center; justify-content: center; user-select: none; }
.scan-viewport.grabbing { cursor: grabbing; }
.scan-inner { will-change: transform; }
.scan-inner img { display: block; max-width: none; pointer-events: none; }
.scan-empty { text-align: center; color: #888780; display: flex; flex-direction: column; align-items: center; }
.scan-empty-icon { font-size: 48px; margin-bottom: 12px; opacity: 0.4; }
.scan-empty p { font-size: 14px; margin: 0 0 4px; }
.scan-empty-hint { font-size: 12px; color: #5f5e5a; }
.scan-toolbar { display: flex; align-items: center; gap: 10px; padding: 10px 16px; background: rgba(0,0,0,0.5); }
.scan-btn { width: 30px; height: 30px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.18); border-radius: 6px; color: #fff; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background .15s; }
.scan-btn:hover:not(:disabled) { background: rgba(255,255,255,0.2); }
.scan-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.zoom-display { color: #aaa; font-size: 12px; min-width: 46px; text-align: center; }
.scan-upload-btn { margin-left: auto; padding: 6px 14px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.18); border-radius: 6px; color: #fff; font-size: 12px; cursor: pointer; transition: background .15s; font-family: inherit; }
.scan-upload-btn:hover { background: rgba(255,255,255,0.2); }
.scan-new-badge { font-size: 11px; color: #f59e0b; font-weight: 600; white-space: nowrap; }

/* Модалка удаления */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.35); z-index: 999; display: flex; align-items: center; justify-content: center; }
.modal { background: #fff; border-radius: 12px; padding: 28px 24px; width: 360px; border: 1px solid #d5d3cf; box-shadow: 0 8px 32px rgba(0,0,0,0.14); text-align: center; }
.modal-icon { font-size: 36px; margin-bottom: 12px; }
.modal h4 { font-size: 18px; font-weight: 700; margin: 0 0 8px; }
.modal-desc { font-size: 13px; color: #666; line-height: 1.5; }
.modal-footer { display: flex; gap: 10px; margin-top: 20px; justify-content: center; }
.btn-cancel { padding: 9px 20px; background: #f0efee; border: 1px solid #c8c5c0; border-radius: 6px; font-size: 13px; font-family: inherit; cursor: pointer; color: #444; }
.btn-cancel:hover { background: #e9e7e3; }
.btn-confirm-delete { padding: 9px 20px; background: #991b1b; color: #fff; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; font-family: inherit; cursor: pointer; }
.btn-confirm-delete:hover:not(:disabled) { background: #7f1d1d; }
.btn-confirm-delete:disabled { opacity: 0.5; cursor: not-allowed; }

/* Адаптив */
@media (max-width: 900px) {
  .birth-layout { flex-direction: column; }
  .form-panel { width: 100%; max-width: 100%; height: 55vh; }
  .scan-panel { height: 45vh; }
  .row.three { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .row.two, .row.three { grid-template-columns: 1fr; }
  .header-top { flex-wrap: wrap; }
}
</style>