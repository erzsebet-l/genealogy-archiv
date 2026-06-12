<template>
  <div class="birth-layout">

    <!-- ══════════════ ЛЕВАЯ ПАНЕЛЬ — ФОРМА ══════════════ -->
    <div class="form-panel">
      <div class="form-header">
        <div class="header-top">
          <button type="button" class="btn-back" @click="$router.back()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="18" height="18">
              <path d="M19 12H5M12 5l-7 7 7 7"/>
            </svg>
            Назад
          </button>

          <!-- ───── ПЕРЕКЛЮЧАТЕЛЬ ЧЕРНОВИК / ПУБЛИКАЦИЯ (скрыт в режиме редактирования) ───── -->
          <div class="status-toggle" v-if="!isEditMode">
            <button
              type="button"
              :class="['toggle-btn', { active: formStatus === 'draft' }]"
              @click="switchToDraft"
            >
              <span class="toggle-dot draft-dot"></span>
              Черновик
            </button>
            <button
              type="button"
              :class="['toggle-btn', { active: formStatus === 'published' }]"
              @click="switchToPublish"
            >
              <span class="toggle-dot pub-dot"></span>
              Опубликовать
            </button>
          </div>

          <!-- ───── БЕЙДЖ РЕЖИМА РЕДАКТИРОВАНИЯ ───── -->
          <div v-if="isEditMode" class="edit-mode-badge">
            ✏️ Редактирование записи
          </div>
        </div>

        <h2 class="page-title">Запись о <em>рождении</em></h2>

        <div v-if="isEditMode" class="edit-mode-banner">
          ✏️ Режим редактирования — изменения обновят существующую запись и данные персон
        </div>
        <div v-else-if="formStatus === 'draft'" class="draft-banner">
          📝 Режим черновика — все поля необязательны, данные будут сохранены на сервере
        </div>
        <div v-else-if="formStatus === 'published'" class="publish-banner">
          📢 Режим публикации — поля, отмеченные <span class="red-star">*</span>, обязательны для заполнения
        </div>

        <div v-if="error" class="error-banner">{{ error }}</div>
      </div>

      <form @submit.prevent="handleSubmit" class="form-body">

        <!-- ───────────── БЛОК: АРХИВ ───────────── -->
        <section class="block">
          <h3 class="block-title">Архив</h3>

          <div class="field full">
            <label>Название архива</label>
            <div class="combobox-wrap" ref="archiveCombo">
              <input
                type="text"
                v-model="archiveSearch"
                @input="onArchiveInput"
                @focus="archiveDropOpen = true"
                @blur="closeArchiveDrop"
                placeholder="Начните вводить название архива..."
                autocomplete="off"
                class="combo-input"
                :class="{ auto: autoFilledFields.archive }"
              />
              <ul v-show="archiveDropOpen && archiveDropItems.length > 0" class="drop-list">
                <li
                  v-for="a in archiveDropItems"
                  :key="a.archive_id"
                  @mousedown.prevent="selectArchive(a)"
                  class="drop-item"
                >
                  <span class="drop-main">{{ a.name }}</span>
                  <span class="drop-sub">{{ a.number_case }} · {{ a.year }}</span>
                </li>
                <li
                  v-if="archiveSearch.trim() && !archiveExactMatch"
                  @mousedown.prevent="prepareNewArchive"
                  class="drop-item drop-new"
                >
                  ＋ Создать «{{ archiveSearch.trim() }}»
                </li>
              </ul>
            </div>
            <div v-if="autoFilledFields.archive" class="auto-hint">⚡ Автозаполнено</div>
          </div>

          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('number_case') }">
              <label>Номер дела <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.number_case"
                placeholder="Ф.160 Оп.1"
                :class="{ 'error-input': showFieldError('number_case'), auto: autoFilledFields.number_case }"
              />
              <div v-if="autoFilledFields.number_case" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('number_case')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('year') }">
              <label>Год <span class="req-star">*</span></label>
              <input
                type="number"
                v-model.number="formData.year"
                placeholder="1850"
                min="1000"
                max="2000"
                :class="{ auto: autoFilledFields.year }"
              />
              <div v-if="autoFilledFields.year" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('year')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('page') }">
              <label>Номер листа <span class="req-star">*</span></label>
              <input
                type="number"
                v-model.number="formData.page"
                :class="{ auto: autoFilledFields.page, 'error-input': showFieldError('page') }"
                placeholder="1"
              />
              <div v-if="autoFilledFields.page" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('page')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>

          <div class="row two">
            <div class="field checkbox-field">
              <label>&nbsp;</label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.page_turn" />
                Оборот листа
              </label>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ДАТА ───────────── -->
        <section class="block">
          <h3 class="block-title">Дата</h3>
          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('birth_month') }">
              <label>Месяц рождения <span class="req-star">*</span></label>
              <select
                v-model.number="formData.birth_month"
                :class="{ auto: autoFilledFields.birth_month, 'error-input': showFieldError('birth_month') }"
              >
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
              <div v-if="autoFilledFields.birth_month" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('birth_month')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('birth_day') }">
              <label>Число рождения <span class="req-star">*</span></label>
              <input
                type="number"
                min="1"
                max="31"
                v-model.number="formData.birth_day"
                @input="autoBaptDay"
                placeholder="1"
                :class="{ 'error-input': showFieldError('birth_day') }"
              />
              <div v-if="showFieldError('birth_day')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('baptism_day') }">
              <label>Число крещения <span class="req-star">*</span></label>
              <input
                type="number"
                min="1"
                max="31"
                v-model.number="formData.baptism_day"
                :class="{ auto: baptismAuto, 'error-input': showFieldError('baptism_day') }"
                placeholder="3"
              />
              <div v-if="baptismAuto" class="auto-hint">⚡ День рождения +2</div>
              <div v-if="showFieldError('baptism_day')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: РОДИВШИЙСЯ ───────────── -->
        <section ref="childBlock" class="block">
          <h3 class="block-title">О родившемся</h3>
          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('sex') }">
              <label>Пол <span class="req-star">*</span></label>
              <select
                v-model="formData.sex"
                @change="onSexChange"
                :class="{ 'error-input': showFieldError('sex') }"
              >
                <option value="">Выберите</option>
                <option value="М">Мужской</option>
                <option value="Ж">Женский</option>
              </select>
              <div v-if="showFieldError('sex')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('number_record') }">
              <label>Номер записи <span class="req-star">*</span></label>
              <div class="record-number-wrapper">
                <span class="record-gender-badge">{{ currentGenderLabel }}</span>
                <input
                  type="number"
                  v-model.number="currentNumberRecord"
                  @change="updateNumberRecord"
                  :class="{ auto: autoFilledFields.number_record, 'error-input': showFieldError('number_record') }"
                  placeholder="1"
                />
              </div>
              <div v-if="autoFilledFields.number_record" class="auto-hint">⚡ +1 от предыдущей записи ({{ currentGenderLabel }})</div>
              <div v-if="showFieldError('number_record')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>
          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.name"
                placeholder="Иван"
                :class="{ 'error-input': showFieldError('name') }"
              />
              <div v-if="showFieldError('name')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input
                type="text"
                v-model="formData.child_patronymic"
                placeholder="Иванович"
              />
              <div v-if="showPatronymicSuggestion" class="suggestion-below">
                <span class="suggestion-below-text">
                  💡 Предложено отчество от имени отца <strong>{{ formData.father_name || '?' }}</strong>:
                </span>
                <span class="suggestion-below-value">{{ suggestedPatronymic }}</span>
                <button type="button" class="suggestion-below-button" @click="acceptPatronymicSuggestion">
                  Применить
                </button>
              </div>
              <div v-else-if="formData.father_name && formData.sex && formData.child_patronymic" class="auto-hint">
                💡 От отца: {{ formData.father_name }} → {{ suggestedPatronymic }}
              </div>
            </div>
          </div>
          <div class="row two">
            <div class="field">
              <label>Фамилия</label>
              <input
                type="text"
                v-model="formData.child_surname"
                placeholder="Смирнов"
              />
              <div v-if="showSurnameSuggestion" class="suggestion-below">
                <span class="suggestion-below-text">
                  💡 Предложена фамилия от фамилии отца <strong>{{ formData.father_surname || '?' }}</strong>:
                </span>
                <span class="suggestion-below-value">{{ suggestedSurname }}</span>
                <button type="button" class="suggestion-below-button" @click="acceptSurnameSuggestion">
                  Применить
                </button>
              </div>
              <div v-else-if="formData.father_surname && formData.sex && formData.child_surname" class="auto-hint">
                💡 От отца: {{ formData.father_surname }} → {{ suggestedSurname }}
              </div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ОТЕЦ ───────────── -->
        <section class="block">
          <h3 class="block-title">Отец</h3>

          <div class="location-block">
            <div class="location-header">
              <span class="location-label">Место жительства</span>
              <span class="location-hint" :class="{ 'hint-error': showFieldError('location') }">
                {{ showFieldError('location') ? '⚠ Заполните хотя бы одно поле' : 'Заполните хотя бы одно поле' }}
              </span>
            </div>
            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input
                    type="text"
                    v-model="provinceSearch"
                    @input="onProvinceInput"
                    @focus="provinceDropOpen = true"
                    @blur="onProvinceBlur"
                    :placeholder="getLocationName('province')"
                    autocomplete="off"
                    class="combo-input"
                  />
                  <ul v-show="provinceDropOpen && filteredProvinces.length" class="drop-list">
                    <li v-for="p in filteredProvinces" :key="p.province_id"
                      @mousedown.prevent="selectLocation('province', p)" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                    <li v-if="provinceSearch.trim() && !provinceExactMatch"
                      @mousedown.prevent="createNewProvince" class="drop-item drop-new">
                      ＋ Создать губернию «{{ provinceSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input
                    type="text"
                    v-model="yezdSearch"
                    @input="onYezdInput"
                    @focus="yezdDropOpen = true"
                    @blur="onYezdBlur"
                    :placeholder="getLocationName('yezd')"
                    autocomplete="off"
                    class="combo-input"
                  />
                  <ul v-show="yezdDropOpen && filteredYezds.length" class="drop-list">
                    <li v-for="y in filteredYezds" :key="y.yezd_id"
                      @mousedown.prevent="selectLocation('yezd', y)" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                    <li v-if="yezdSearch.trim() && !yezdExactMatch"
                      @mousedown.prevent="createNewYezd" class="drop-item drop-new">
                      ＋ Создать уезд «{{ yezdSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input
                    type="text"
                    v-model="volostSearch"
                    @input="onVolostInput"
                    @focus="volostDropOpen = true"
                    @blur="onVolostBlur"
                    :placeholder="getLocationName('volost')"
                    autocomplete="off"
                    class="combo-input"
                  />
                  <ul v-show="volostDropOpen && filteredVolosts.length" class="drop-list">
                    <li v-for="v in filteredVolosts" :key="v.volost_id"
                      @mousedown.prevent="selectLocation('volost', v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="volostSearch.trim() && !volostExactMatch"
                      @mousedown.prevent="createNewVolost" class="drop-item drop-new">
                      ＋ Создать волость «{{ volostSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Село / Населённый пункт</label>
                <div class="combobox-wrap">
                  <input
                    type="text"
                    v-model="villageSearch"
                    @input="onVillageInput"
                    @focus="villageDropOpen = true"
                    @blur="onVillageBlur"
                    :placeholder="getLocationName('village')"
                    autocomplete="off"
                    class="combo-input"
                  />
                  <ul v-show="villageDropOpen && filteredVillages.length" class="drop-list">
                    <li v-for="v in filteredVillages" :key="v.village_id"
                      @mousedown.prevent="selectLocation('village', v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="villageSearch.trim() && !villageExactMatch"
                      @mousedown.prevent="createNewVillage" class="drop-item drop-new">
                      ＋ Создать село «{{ villageSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('father_estate_id') }">
              <label>Сословие <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select
                  v-model="formData.father_estate_id"
                  @change="syncMotherEstate"
                  :class="{ 'error-input': showFieldError('father_estate_id') }"
                >
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('estate')" title="Добавить новое сословие">＋</button>
              </div>
              <div v-if="showFieldError('father_estate_id')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('creed_id') }">
              <label>Вероисповедание <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select
                  v-model="formData.creed_id"
                  :class="{ 'error-input': showFieldError('creed_id') }"
                >
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('religion')" title="Добавить новое вероисповедание">＋</button>
              </div>
              <div v-if="showFieldError('creed_id')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>

          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('father_name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.father_name"
                placeholder="Пётр"
                :class="{ 'error-input': showFieldError('father_name') }"
              />
              <div v-if="showFieldError('father_name')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.father_patronymic" placeholder="Иванович" />
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('father_surname') }">
              <label>Фамилия <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.father_surname"
                placeholder="Смирнов"
                :class="{ 'error-input': showFieldError('father_surname') }"
              />
              <div v-if="showFieldError('father_surname')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: МАТЬ ───────────── -->
        <section class="block">
          <h3 class="block-title">Мать</h3>
          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('mother_status') }">
              <label>Статус <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select
                  v-model="formData.mother_status"
                  :class="{ 'error-input': showFieldError('mother_status') }"
                >
                  <option value="">Выберите</option>
                  <option v-for="s in motherStatuses" :key="s.status_choice_id" :value="s.name">{{ s.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('mother_status')" title="Добавить новый статус">＋</button>
              </div>
              <div v-if="showFieldError('mother_status')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Сословие</label>
              <input type="text" :value="fatherEstateName" readonly class="readonly-input" placeholder="Берётся от отца" />
            </div>
          </div>
          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('mother_name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.mother_name"
                placeholder="Мария"
                :class="{ 'error-input': showFieldError('mother_name') }"
              />
              <div v-if="showFieldError('mother_name')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.mother_patronymic" placeholder="Петровна" />
            </div>
            <div class="field">
              <label>Фамилия</label>
              <input
                type="text"
                v-model="formData.mother_surname"
                placeholder="Смирнова"
              />
              <div v-if="showMotherSurnameSuggestion && isMotherLawful" class="suggestion-below">
                <span class="suggestion-below-text">
                  💡 Предложена фамилия от мужа <strong>{{ formData.father_surname || '?' }}</strong>:
                </span>
                <span class="suggestion-below-value">{{ suggestedMotherSurname }}</span>
                <button type="button" class="suggestion-below-button" @click="acceptMotherSurnameSuggestion">
                  Применить
                </button>
              </div>
              <div v-else-if="isMotherLawful && formData.father_surname && formData.mother_surname" class="auto-hint">
                💡 От мужа: {{ formData.father_surname }} → {{ suggestedMotherSurname }}
              </div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ВОСПРИЕМНИКИ (МУЖЧИНЫ) ───────────── -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Восприемники (мужчины)</h3>
            <button type="button" class="btn-add-block" @click="addGodman">＋ добавить</button>
          </div>

          <div v-for="(g, i) in godmen" :key="'gm'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Восприемник #{{ i + 1 }}</span>
              <div class="header-actions">
                <button
                  type="button"
                  class="btn-auto-fill"
                  @click="autoFillGodparentLocation(g)"
                  :disabled="!formData.father_province_id && !formData.father_yezd_id && !formData.father_volost_id && !formData.father_village_id"
                  title="Заполнить как у отца"
                >
                  ⚡ Авто
                </button>
                <button type="button" class="btn-remove" @click="godmen.splice(i, 1)" v-if="godmen.length > 1">✕</button>
              </div>
            </div>

            <div class="row two">
              <div class="field">
                <div class="field-with-auto">
                  <label>Губерния</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.provinceSearch"
                      @input="g.provinceDropOpen = true; g.province_id = ''; g.provinceAuto = false"
                      @focus="g.provinceDropOpen = true"
                      @blur="closeGodDrop(g, 'provinceDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.provinceAuto }" />
                    <ul v-show="g.provinceDropOpen && filterItems(provinces, g.provinceSearch, 'province_id').length" class="drop-list">
                      <li v-for="p in filterItems(provinces, g.provinceSearch, 'province_id')" :key="p.province_id"
                        @mousedown.prevent="g.province_id = p.province_id; g.provinceSearch = p.name; g.provinceDropOpen = false; g.provinceAuto = false" class="drop-item">
                        <span class="drop-main">{{ p.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.provinceAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
              <div class="field">
                <div class="field-with-auto">
                  <label>Уезд</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.yezdSearch"
                      @input="g.yezdDropOpen = true; g.yezd_id = ''; g.yezdAuto = false"
                      @focus="g.yezdDropOpen = true"
                      @blur="closeGodDrop(g, 'yezdDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.yezdAuto }" />
                    <ul v-show="g.yezdDropOpen && filterItems(yezds, g.yezdSearch, 'yezd_id').length" class="drop-list">
                      <li v-for="y in filterItems(yezds, g.yezdSearch, 'yezd_id')" :key="y.yezd_id"
                        @mousedown.prevent="g.yezd_id = y.yezd_id; g.yezdSearch = y.name; g.yezdDropOpen = false; g.yezdAuto = false" class="drop-item">
                        <span class="drop-main">{{ y.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.yezdAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <div class="field-with-auto">
                  <label>Волость</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.volostSearch"
                      @input="g.volostDropOpen = true; g.volost_id = ''; g.volostAuto = false"
                      @focus="g.volostDropOpen = true"
                      @blur="closeGodDrop(g, 'volostDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.volostAuto }" />
                    <ul v-show="g.volostDropOpen && filterItems(volosts, g.volostSearch, 'volost_id').length" class="drop-list">
                      <li v-for="v in filterItems(volosts, g.volostSearch, 'volost_id')" :key="v.volost_id"
                        @mousedown.prevent="g.volost_id = v.volost_id; g.volostSearch = v.name; g.volostDropOpen = false; g.volostAuto = false" class="drop-item">
                        <span class="drop-main">{{ v.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.volostAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
              <div class="field">
                <div class="field-with-auto">
                  <label>Село</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.villageSearch"
                      @input="g.villageDropOpen = true; g.village_id = ''; g.villageAuto = false"
                      @focus="g.villageDropOpen = true"
                      @blur="closeGodDrop(g, 'villageDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.villageAuto }" />
                    <ul v-show="g.villageDropOpen && filterItems(villages, g.villageSearch, 'village_id').length" class="drop-list">
                      <li v-for="v in filterItems(villages, g.villageSearch, 'village_id')" :key="v.village_id"
                        @mousedown.prevent="g.village_id = v.village_id; g.villageSearch = v.name; g.villageDropOpen = false; g.villageAuto = false" class="drop-item">
                        <span class="drop-main">{{ v.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.villageAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
            </div>

            <div class="row two">
              <div class="field">
                <label>Сословие</label>
                <div class="field-with-add">
                  <select v-model="g.estate_id" :class="{ auto: g.estateAuto }" @change="g.estateAuto = false">
                    <option value="">Выберите</option>
                    <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                  </select>
                  <button type="button" class="btn-add-ref" @click="openModal('estate')" title="Добавить сословие">＋</button>
                </div>
                <div v-if="g.estateAuto" class="auto-hint">⚡ Как у отца</div>
              </div>
              <div class="field">
                <label>Вероисповедание</label>
                <select v-model="g.creed_id" :class="{ auto: g.creedAuto }" @change="g.creedAuto = false">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
                <div v-if="g.creedAuto" class="auto-hint">⚡ Как у отца</div>
              </div>
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
          </div>
        </section>

        <!-- ───────────── БЛОК: ВОСПРИЕМНИЦЫ (ЖЕНЩИНЫ) ───────────── -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Восприемницы (женщины)</h3>
            <button type="button" class="btn-add-block" @click="addGodmother">＋ добавить</button>
          </div>

          <div v-for="(g, i) in godmothers" :key="'gw'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Восприемница #{{ i + 1 }}</span>
              <div class="header-actions">
                <button
                  type="button"
                  class="btn-auto-fill"
                  @click="autoFillGodparentLocation(g)"
                  :disabled="!formData.father_province_id && !formData.father_yezd_id && !formData.father_volost_id && !formData.father_village_id"
                  title="Заполнить как у отца"
                >
                  ⚡ Авто
                </button>
                <button type="button" class="btn-remove" @click="godmothers.splice(i, 1)" v-if="godmothers.length > 1">✕</button>
              </div>
            </div>

            <div class="row two">
              <div class="field">
                <div class="field-with-auto">
                  <label>Губерния</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.provinceSearch"
                      @input="g.provinceDropOpen = true; g.province_id = ''; g.provinceAuto = false"
                      @focus="g.provinceDropOpen = true"
                      @blur="closeGodDrop(g, 'provinceDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.provinceAuto }" />
                    <ul v-show="g.provinceDropOpen && filterItems(provinces, g.provinceSearch, 'province_id').length" class="drop-list">
                      <li v-for="p in filterItems(provinces, g.provinceSearch, 'province_id')" :key="p.province_id"
                        @mousedown.prevent="g.province_id = p.province_id; g.provinceSearch = p.name; g.provinceDropOpen = false; g.provinceAuto = false" class="drop-item">
                        <span class="drop-main">{{ p.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.provinceAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
              <div class="field">
                <div class="field-with-auto">
                  <label>Уезд</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.yezdSearch"
                      @input="g.yezdDropOpen = true; g.yezd_id = ''; g.yezdAuto = false"
                      @focus="g.yezdDropOpen = true"
                      @blur="closeGodDrop(g, 'yezdDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.yezdAuto }" />
                    <ul v-show="g.yezdDropOpen && filterItems(yezds, g.yezdSearch, 'yezd_id').length" class="drop-list">
                      <li v-for="y in filterItems(yezds, g.yezdSearch, 'yezd_id')" :key="y.yezd_id"
                        @mousedown.prevent="g.yezd_id = y.yezd_id; g.yezdSearch = y.name; g.yezdDropOpen = false; g.yezdAuto = false" class="drop-item">
                        <span class="drop-main">{{ y.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.yezdAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <div class="field-with-auto">
                  <label>Волость</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.volostSearch"
                      @input="g.volostDropOpen = true; g.volost_id = ''; g.volostAuto = false"
                      @focus="g.volostDropOpen = true"
                      @blur="closeGodDrop(g, 'volostDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.volostAuto }" />
                    <ul v-show="g.volostDropOpen && filterItems(volosts, g.volostSearch, 'volost_id').length" class="drop-list">
                      <li v-for="v in filterItems(volosts, g.volostSearch, 'volost_id')" :key="v.volost_id"
                        @mousedown.prevent="g.volost_id = v.volost_id; g.volostSearch = v.name; g.volostDropOpen = false; g.volostAuto = false" class="drop-item">
                        <span class="drop-main">{{ v.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.volostAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
              <div class="field">
                <div class="field-with-auto">
                  <label>Село</label>
                  <div class="combobox-wrap">
                    <input type="text" v-model="g.villageSearch"
                      @input="g.villageDropOpen = true; g.village_id = ''; g.villageAuto = false"
                      @focus="g.villageDropOpen = true"
                      @blur="closeGodDrop(g, 'villageDropOpen')"
                      autocomplete="off" class="combo-input" :class="{ auto: g.villageAuto }" />
                    <ul v-show="g.villageDropOpen && filterItems(villages, g.villageSearch, 'village_id').length" class="drop-list">
                      <li v-for="v in filterItems(villages, g.villageSearch, 'village_id')" :key="v.village_id"
                        @mousedown.prevent="g.village_id = v.village_id; g.villageSearch = v.name; g.villageDropOpen = false; g.villageAuto = false" class="drop-item">
                        <span class="drop-main">{{ v.name }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="g.villageAuto" class="auto-hint">⚡ Как у отца</div>
                </div>
              </div>
            </div>

            <div class="row two">
              <div class="field">
                <label>Сословие</label>
                <div class="field-with-add">
                  <select v-model="g.estate_id" :class="{ auto: g.estateAuto }" @change="g.estateAuto = false">
                    <option value="">Выберите</option>
                    <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                  </select>
                  <button type="button" class="btn-add-ref" @click="openModal('estate')">＋</button>
                </div>
                <div v-if="g.estateAuto" class="auto-hint">⚡ Как у отца</div>
              </div>
              <div class="field">
                <label>Вероисповедание</label>
                <select v-model="g.creed_id" :class="{ auto: g.creedAuto }" @change="g.creedAuto = false">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
                <div v-if="g.creedAuto" class="auto-hint">⚡ Как у отца</div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Статус</label>
                <div class="field-with-add">
                  <select v-model="g.status_id">
                    <option value="">Выберите</option>
                    <option v-for="s in motherStatuses" :key="s.status_choice_id" :value="s.status_choice_id">
                      {{ s.name }}
                    </option>
                  </select>
                  <button type="button" class="btn-add-ref" @click="openModal('mother_status')" title="Добавить новый статус">＋</button>
                </div>
              </div>
              <div class="field">
                <label>Имя</label>
                <input type="text" v-model="g.name" placeholder="Имя" />
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Отчество</label>
                <input type="text" v-model="g.patronymic" placeholder="Отчество" />
              </div>
              <div class="field">
                <label>Фамилия</label>
                <input type="text" v-model="g.surname" placeholder="Фамилия" :class="{ auto: g.surnameAuto }" />
                <div v-if="g.surnameAuto" class="auto-hint">⚡ От мужа-восприемника</div>
              </div>
            </div>

            <div v-if="g.linked_husband_index !== null && godmen[g.linked_husband_index]" class="linked-husband-badge">
              <span class="badge-icon">💍</span>
              Супруга восприемника: {{ godmen[g.linked_husband_index].name }} {{ godmen[g.linked_husband_index].surname }}
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: СВЯЩЕННОСЛУЖИТЕЛИ ───────────── -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Священнослужители</h3>
            <button type="button" class="btn-add-block" @click="addPriest">＋ добавить</button>
          </div>

          <div v-for="(p, i) in priests" :key="'pr'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Священнослужитель #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="priests.splice(i, 1)" v-if="priests.length > 1">✕</button>
            </div>

            <div class="field full" style="margin-bottom:10px">
              <label>Поиск по базе</label>
              <div class="combobox-wrap">
                <input
                  type="text" v-model="p.searchText"
                  @input="onPriestSearch(i)"
                  @focus="p.dropOpen = true"
                  @blur="closePriestDrop(i)"
                  placeholder="Фамилия или имя — начните вводить..."
                  autocomplete="off" class="combo-input"
                  :class="{ 'input-linked': p.church_worker_id }"
                />
                <ul v-show="p.dropOpen && p.dropItems.length > 0" class="drop-list">
                  <li v-for="cw in p.dropItems" :key="cw.pries_id"
                    @mousedown.prevent="selectChurchWorker(i, cw)" class="drop-item">
                    <span class="drop-main">{{ cw.surname }} {{ cw.name }} {{ cw.patronymic || '' }}</span>
                    <span class="drop-sub">{{ cw.clergy_name || cw.clergy }}</span>
                  </li>
                </ul>
              </div>
              <div v-if="p.church_worker_id" class="priest-linked-badge">
                <span class="badge-icon">✓</span>
                Привязан к записи в базе
                <button type="button" class="badge-unlink" @click="unlinkChurchWorker(i)">✕ отвязать</button>
              </div>
            </div>

            <div class="row two">
              <div class="field">
                <label>Имя</label>
                <input type="text" v-model="p.name" placeholder="Имя"
                  :readonly="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }" />
              </div>
              <div class="field">
                <label>Фамилия</label>
                <input type="text" v-model="p.surname" placeholder="Фамилия"
                  :readonly="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }" />
              </div>
            </div>

            <div class="field full">
              <label>Степень духовенства</label>
              <div class="field-with-add">
                <select v-model="p.clergy_id"
                  :disabled="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }">
                  <option value="">Выберите</option>
                  <option v-for="c in clergyList" :key="c.clergy_id" :value="c.clergy_id">{{ c.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('clergy')" :disabled="!!p.church_worker_id">＋</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ПРИМЕЧАНИЕ ───────────── -->
        <section class="block">
          <h3 class="block-title">Примечание</h3>
          <div class="field full">
            <textarea v-model="formData.comment" rows="3" placeholder="Дополнительные сведения..."></textarea>
          </div>
        </section>

        <!-- ───────────── ПОДВАЛ ФОРМЫ ───────────── -->
        <div class="form-footer">
          <button
            type="submit"
            class="btn-submit"
            :disabled="loading"
            :class="formStatus === 'draft' ? 'draft-submit' : (isEditMode ? 'edit-submit' : 'publish-submit')"
          >
            {{ submitButtonLabel }}
          </button>
        </div>

      </form>
    </div>

    <!-- ══════════════ ПРАВАЯ ПАНЕЛЬ — СКАН ══════════════ -->
    <div class="scan-panel">
      <div
        class="scan-viewport" ref="scanViewport"
        @mousedown="startDrag" @wheel.prevent="onWheel"
        :class="{ grabbing: isDragging }"
      >
        <div v-if="scanSrc" class="scan-inner" ref="scanInner" :style="scanTransformStyle">
          <img :src="scanSrc" alt="Скан документа" draggable="false" ref="scanImg" />
        </div>
        <div v-else class="scan-empty">
          <div class="scan-empty-icon">📄</div>
          <p>Загрузите скан документа</p>
          <p class="scan-empty-hint">Поддерживаются JPG, PNG, TIFF</p>
        </div>
      </div>

      <div class="scan-toolbar">
        <button @click="zoomOut" :disabled="zoom <= 0.2" class="scan-btn" title="Уменьшить">−</button>
        <span class="zoom-display">{{ Math.round(zoom * 100) }}%</span>
        <button @click="zoomIn" :disabled="zoom >= 8" class="scan-btn" title="Увеличить">+</button>
        <button @click="resetScan" class="scan-btn" title="Сбросить">⟳</button>
        <label class="scan-upload-btn">
          📁 {{ scanFile ? 'Заменить скан' : (scanSrc ? 'Заменить скан' : 'Загрузить скан') }}
          <input type="file" accept="image/*" @change="loadScan" ref="fileInput" style="display: none" />
        </label>
        <div v-if="scanSrc" class="scan-status">
          <span class="scan-status-icon">📄</span>
          <span class="scan-status-text">Скан загружен</span>
        </div>
      </div>
    </div>

    <!-- ══════════════ МОДАЛЬНЫЕ ОКНА СПРАВОЧНИКОВ ══════════════ -->
    <div v-if="modal.type === 'estate'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить сословие</h4>
        <div class="field">
          <label>Название</label>
          <input type="text" v-model="modal.value" placeholder="Например: Дворянин" @keyup.enter="saveRef" autofocus />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="closeModal">Отмена</button>
          <button type="button" class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>

    <div v-if="modal.type === 'religion'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить вероисповедание</h4>
        <div class="field">
          <label>Название</label>
          <input type="text" v-model="modal.value" placeholder="Например: Православное" @keyup.enter="saveRef" autofocus />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="closeModal">Отмена</button>
          <button type="button" class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>

    <div v-if="modal.type === 'mother_status'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить статус</h4>
        <div class="field">
          <label>Название</label>
          <input type="text" v-model="modal.value" placeholder="Например: законная жена" @keyup.enter="saveRef" autofocus />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="closeModal">Отмена</button>
          <button type="button" class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>

    <div v-if="modal.type === 'clergy'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить степень духовенства</h4>
        <div class="field">
          <label>Название</label>
          <input type="text" v-model="modal.value" placeholder="Например: Диакон" @keyup.enter="saveRef" autofocus />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="closeModal">Отмена</button>
          <button type="button" class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- ══════════════ ПОДТВЕРЖДЕНИЕ ПУБЛИКАЦИИ (только для новых записей) ══════════════ -->
    <div v-if="showPublishConfirm" class="modal-overlay" @click.self="showPublishConfirm = false">
      <div class="modal modal-confirm">
        <div class="modal-icon">📢</div>
        <h4>Опубликовать запись?</h4>
        <p class="modal-text">
          Запись будет сохранена в основную базу данных и станет доступна для всех пользователей.
          Убедитесь, что все данные проверены.
        </p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="showPublishConfirm = false">Отмена</button>
          <button type="button" class="btn-action" @click="confirmPublish" :disabled="loading">
            {{ loading ? 'Публикация...' : 'Да, опубликовать' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ══════════════ УСПЕХ: ЧЕРНОВИК ══════════════ -->
    <div v-if="showDraftSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Черновик сохранён</h4>
        <p class="modal-text">Черновик успешно сохранён.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="closeDraftSuccess">OK</button>
        </div>
      </div>
    </div>

    <!-- ══════════════ УСПЕХ: ПУБЛИКАЦИЯ ══════════════ -->
    <div v-if="showPublishSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Запись опубликована</h4>
        <p class="modal-text">Запись о рождении успешно опубликована и добавлена в основную базу данных.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="closePublishSuccess">OK</button>
        </div>
      </div>
    </div>

    <!-- ══════════════ УСПЕХ: РЕДАКТИРОВАНИЕ ══════════════ -->
    <div v-if="showEditSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Изменения сохранены</h4>
        <p class="modal-text">Запись о рождении и данные персон успешно обновлены.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="closeEditSuccess">OK</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { api, authHeaders, API_BASE } from '@/utils/api.js'

export default {
  name: 'Birth',

  data() {
    return {
      loading: false,
      error: null,
      autoFilled: false,
      baptismAuto: false,
      showPublishConfirm: false,
      showDraftSuccess: false,
      showPublishSuccess: false,
      showEditSuccess: false,
      missingFieldsList: [],
      showPublishAttempt: false,
      currentDraftId: null,
      editingRecordId: null,

      // ID персон, созданных при первой публикации — используются при редактировании
      existingPersonIds: {
        child: null,
        father: null,
        mother: null,
      },

      autoFilledFields: {
        archive: false,
        number_case: false,
        year: false,
        page: false,
        number_record: false,
        birth_month: false,
      },

      formStatus: 'published',

      archiveSearch: '',
      archiveDropOpen: false,
      allArchives: [],

      provinceSearch: '',
      provinceDropOpen: false,
      yezdSearch: '',
      yezdDropOpen: false,
      volostSearch: '',
      volostDropOpen: false,
      villageSearch: '',
      villageDropOpen: false,

      allChurchWorkers: [],
      estates: [],
      religions: [],
      villages: [],
      provinces: [],
      yezds: [],
      volosts: [],
      motherStatuses: [],
      clergyList: [],

      modal: { type: null, value: '' },

      scanSrc: null,
      scanFile: null,
      zoom: 1,
      panX: 0,
      panY: 0,
      isDragging: false,
      _dragStartX: 0,
      _dragStartY: 0,

      numberRecordMale: '',
      numberRecordFemale: '',

      formData: {
        archive_id: null,
        number_case: '',
        year: '',
        page: '',
        page_turn: false,
        number_record: '',
        birth_month: '',
        birth_day: '',
        baptism_day: '',
        sex: '',
        name: '',
        child_patronymic: '',
        child_surname: '',
        father_province_id: '',
        father_yezd_id: '',
        father_volost_id: '',
        father_village_id: '',
        father_name: '',
        father_patronymic: '',
        father_surname: '',
        father_estate_id: '',
        creed_id: '',
        mother_name: '',
        mother_patronymic: '',
        mother_surname: '',
        mother_status: '',
        comment: ''
      },

      godmen: [],
      godmothers: [],
      priests: [],

      months: [
        'Январь','Февраль','Март','Апрель','Май','Июнь',
        'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'
      ]
    }
  },

  computed: {
    // ── Режим редактирования ──────────────────────────────────────
    isEditMode() {
      return !!this.editingRecordId
    },

    submitButtonLabel() {
      if (this.loading) return 'Сохранение...'
      if (this.formStatus === 'draft') return 'Сохранить черновик'
      if (this.isEditMode) return 'Сохранить изменения'
      return 'Опубликовать запись'
    },

    // ── Архив ─────────────────────────────────────────────────────
    archiveDropItems() {
      const q = this.archiveSearch.toLowerCase().trim()
      if (!q) return this.allArchives
      return this.allArchives.filter(a =>
        a.name.toLowerCase().includes(q) ||
        (a.number_case || '').toLowerCase().includes(q)
      )
    },

    archiveExactMatch() {
      return this.allArchives.some(
        a => a.name.toLowerCase() === this.archiveSearch.toLowerCase().trim()
      )
    },

    provinceExactMatch() {
      return this.provinces.some(
        p => p.name.toLowerCase() === this.provinceSearch.toLowerCase().trim()
      )
    },

    yezdExactMatch() {
      return this.yezds.some(
        y => y.name.toLowerCase() === this.yezdSearch.toLowerCase().trim()
      )
    },

    volostExactMatch() {
      return this.volosts.some(
        v => v.name.toLowerCase() === this.volostSearch.toLowerCase().trim()
      )
    },

    villageExactMatch() {
      return this.villages.some(
        v => v.name.toLowerCase() === this.villageSearch.toLowerCase().trim()
      )
    },

    filteredProvinces() { return this.filterItems(this.provinces, this.provinceSearch, 'province_id') },
    filteredYezds()     { return this.filterItems(this.yezds,     this.yezdSearch,     'yezd_id') },
    filteredVolosts()   { return this.filterItems(this.volosts,   this.volostSearch,   'volost_id') },
    filteredVillages()  { return this.filterItems(this.villages,  this.villageSearch,  'village_id') },

    fatherEstateName() {
      const e = this.estates.find(e => e.estate_id === this.formData.father_estate_id)
      return e ? e.name : ''
    },

    scanTransformStyle() {
      return {
        position: 'absolute',
        transformOrigin: 'center center',
        transform: `translate(${this.panX}px, ${this.panY}px) scale(${this.zoom})`,
        transition: this.isDragging ? 'none' : 'transform 0.08s ease'
      }
    },

    currentGenderLabel() {
      if (this.formData.sex === 'М') return '♂ Мужской'
      if (this.formData.sex === 'Ж') return '♀ Женский'
      return 'Выберите пол'
    },

    currentNumberRecord: {
      get() {
        if (this.formData.sex === 'М') return this.numberRecordMale
        if (this.formData.sex === 'Ж') return this.numberRecordFemale
        return ''
      },
      set(value) {
        if (this.formData.sex === 'М') {
          this.numberRecordMale = value
          this.formData.number_record = value
        } else if (this.formData.sex === 'Ж') {
          this.numberRecordFemale = value
          this.formData.number_record = value
        }
      }
    },

    suggestedPatronymic() {
      if (!this.formData.father_name || !this.formData.sex) return ''
      return this.formPatronymic(this.formData.father_name, this.formData.sex)
    },

    showPatronymicSuggestion() {
      return this.suggestedPatronymic &&
             this.formData.child_patronymic !== this.suggestedPatronymic &&
             !this.formData.child_patronymic
    },

    suggestedSurname() {
      if (!this.formData.father_surname || !this.formData.sex) return ''
      return this.formSurname(this.formData.father_surname, this.formData.sex)
    },

    showSurnameSuggestion() {
      return this.suggestedSurname &&
             this.formData.child_surname !== this.suggestedSurname &&
             !this.formData.child_surname
    },

    isMotherLawful() {
      const status = (this.formData.mother_status || '').toLowerCase().trim()
      return status === 'законная жена' || status === 'законная'
    },

    suggestedMotherSurname() {
      if (!this.formData.father_surname) return ''
      return this.formSurname(this.formData.father_surname, 'Ж')
    },

    showMotherSurnameSuggestion() {
      return this.isMotherLawful &&
             this.suggestedMotherSurname &&
             this.formData.mother_surname !== this.suggestedMotherSurname &&
             !this.formData.mother_surname
    },

    isLawfulWife() {
      return (statusId) => {
        if (!statusId) return false
        const status = this.motherStatuses.find(s => s.status_choice_id === statusId)
        if (!status) return false
        const statusName = status.name.toLowerCase()
        return statusName === 'законная жена' || statusName === 'законная'
      }
    }
  },

  watch: {
    'formData.father_name': {
      handler(newVal, oldVal) {
        this.suggestChildFromFather()
        if (newVal && newVal !== oldVal && !oldVal) {
          setTimeout(() => this.scrollToChildFields(), 100)
        }
      }
    },
    'formData.father_surname': {
      handler(newVal, oldVal) {
        this.suggestChildFromFather()
        this.suggestMotherSurname()
        if (newVal && newVal !== oldVal && !oldVal) {
          setTimeout(() => this.scrollToChildFields(), 100)
        }
      }
    },
    'formData.sex': {
      handler(newVal) {
        this.suggestChildFromFather()
        if (newVal) {
          setTimeout(() => this.scrollToChildFields(), 100)
        }
      }
    },
    'formData.mother_status': {
      handler() {
        this.suggestMotherSurname()
      }
    },

    godmothers: {
      deep: true,
      handler(newVal, oldVal) {
        newVal.forEach((godmother, index) => {
          const oldStatus = oldVal?.[index]?.status_id
          const newStatus = godmother.status_id
          if (newStatus !== oldStatus && this.isLawfulWife(newStatus) && !godmother.surname) {
            this.autoFillGodmotherFromHusband(index)
          }
        })
      }
    },

    godmen: {
      deep: true,
      handler(newVal, oldVal) {
        if (newVal.length > (oldVal?.length || 0)) {
          this.godmothers.forEach((godmother, index) => {
            if (this.isLawfulWife(godmother.status_id) && !godmother.surname) {
              this.autoFillGodmotherFromHusband(index)
            }
          })
        }
      }
    }
  },

  async mounted() {
    this.godmen     = [this.emptyGodman()]
    this.godmothers = [this.emptyGodmother()]
    this.priests    = [this.emptyPriest()]

    await this.loadReferenceData()

    const editRecordData = localStorage.getItem('edit_record')
    if (editRecordData) {
      try {
        const editData = JSON.parse(editRecordData)
        if (editData.isEditing && editData.recordId && editData.recordType) {
          await this.loadRecordForEditing(editData.recordId, editData.recordType)
          localStorage.removeItem('edit_record')
        }
      } catch (e) {
        console.error('Ошибка загрузки данных для редактирования:', e)
      }
    }

    const raw = localStorage.getItem('birth_draft')
    if (raw) {
      try {
        const draftData = JSON.parse(raw)
        if (draftData._draftId || draftData._isEditingDraft) {
          this.loadDraftData(draftData)
          this.currentDraftId = draftData._draftId
          if (draftData._missingFields && draftData._missingFields.length > 0) {
            this.missingFieldsList = draftData._missingFields
            this.showPublishAttempt = true
            this.formStatus = 'published'
          }
        }
        localStorage.removeItem('birth_draft')
      } catch (e) {
        console.error('Ошибка загрузки черновика:', e)
      }
    }
  },

  beforeUnmount() {
    document.removeEventListener('mousemove', this._onMouseMove)
    document.removeEventListener('mouseup',  this._onMouseUp)
  },

  methods: {
    emptyGodman() {
      return {
        name: '', patronymic: '', surname: '',
        estate_id: '', creed_id: '',
        village_id: '', province_id: '', yezd_id: '', volost_id: '',
        provinceSearch: '', yezdSearch: '', volostSearch: '', villageSearch: '',
        provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false,
        provinceAuto: false, yezdAuto: false, volostAuto: false, villageAuto: false,
        estateAuto: false, creedAuto: false,
        // ID для редактирования (если восприемник уже существует в БД)
        godman_id: null,
      }
    },

    emptyGodmother() {
      return {
        name: '', patronymic: '', surname: '',
        estate_id: '', creed_id: '', status_id: '',
        village_id: '', province_id: '', yezd_id: '', volost_id: '',
        provinceSearch: '', yezdSearch: '', volostSearch: '', villageSearch: '',
        provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false,
        provinceAuto: false, yezdAuto: false, volostAuto: false, villageAuto: false,
        estateAuto: false, creedAuto: false,
        surnameAuto: false,
        linked_husband_index: null,
        // ID для редактирования
        godmother_id: null,
      }
    },

    emptyPriest() {
      return {
        searchText: '', dropOpen: false, dropItems: [],
        church_worker_id: null, name: '', surname: '', clergy_id: '',
        // ID для редактирования
        priest_record_id: null,
      }
    },

    filterItems(list, search, idKey) {
      const q = (search || '').toLowerCase().trim()
      if (!q) return list
      return list.filter(item => item.name.toLowerCase().includes(q))
    },

    getLocationName(type) {
      const map = {
        province: { list: this.provinces, id: this.formData.father_province_id, key: 'province_id' },
        yezd:     { list: this.yezds,     id: this.formData.father_yezd_id,     key: 'yezd_id' },
        volost:   { list: this.volosts,   id: this.formData.father_volost_id,   key: 'volost_id' },
        village:  { list: this.villages,  id: this.formData.father_village_id,  key: 'village_id' }
      }
      const m = map[type]
      if (!m || !m.id) return 'Начните вводить...'
      const found = m.list.find(i => i[m.key] === m.id)
      if (found) return found.name
      if (type === 'province' && this.provinceSearch) return this.provinceSearch
      if (type === 'yezd' && this.yezdSearch) return this.yezdSearch
      if (type === 'volost' && this.volostSearch) return this.volostSearch
      if (type === 'village' && this.villageSearch) return this.villageSearch
      return 'Начните вводить...'
    },

    selectLocation(type, item) {
      if (type === 'province') {
        this.formData.father_province_id = item.province_id
        this.provinceSearch = item.name
        this.provinceDropOpen = false
        this.clearLocationError()
      } else if (type === 'yezd') {
        this.formData.father_yezd_id = item.yezd_id
        this.yezdSearch = item.name
        this.yezdDropOpen = false
        this.clearLocationError()
      } else if (type === 'volost') {
        this.formData.father_volost_id = item.volost_id
        this.volostSearch = item.name
        this.volostDropOpen = false
        this.clearLocationError()
      } else if (type === 'village') {
        this.formData.father_village_id = item.village_id
        this.villageSearch = item.name
        this.villageDropOpen = false
        this.clearLocationError()
      }

      if (this.showPublishAttempt && this.checkLocation()) {
        const index = this.missingFieldsList.indexOf('location')
        if (index !== -1) this.missingFieldsList.splice(index, 1)
        if (this.missingFieldsList.length === 0) this.error = null
      }
    },

    onProvinceInput() {
      this.formData.father_province_id = null
      this.clearLocationError()
      this.provinceDropOpen = true
    },

    async onProvinceBlur() {
      setTimeout(async () => {
        if (this.provinceDropOpen) this.provinceDropOpen = false
        const name = this.provinceSearch.trim()
        if (name && !this.formData.father_province_id) {
          const existing = this.provinces.find(p => p.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.father_province_id = existing.province_id
            this.provinceSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/provinces/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.provinces.push(newItem)
              this.formData.father_province_id = newItem.province_id
              this.provinceSearch = newItem.name
            } catch (err) { console.error('Ошибка создания губернии:', err) }
          }
          this.clearLocationError()
        }
      }, 200)
    },

    async createNewProvince() {
      const name = this.provinceSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/provinces/', {
          method: 'POST', headers: authHeaders(true),
          body: JSON.stringify({ name })
        })
        this.provinces.push(newItem)
        this.formData.father_province_id = newItem.province_id
        this.provinceSearch = newItem.name
        this.provinceDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания губернии:', err) }
    },

    onYezdInput() {
      this.formData.father_yezd_id = null
      this.clearLocationError()
      this.yezdDropOpen = true
    },

    async onYezdBlur() {
      setTimeout(async () => {
        if (this.yezdDropOpen) this.yezdDropOpen = false
        const name = this.yezdSearch.trim()
        if (name && !this.formData.father_yezd_id) {
          const existing = this.yezds.find(y => y.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.father_yezd_id = existing.yezd_id
            this.yezdSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/yezds/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.yezds.push(newItem)
              this.formData.father_yezd_id = newItem.yezd_id
              this.yezdSearch = newItem.name
            } catch (err) { console.error('Ошибка создания уезда:', err) }
          }
          this.clearLocationError()
        }
      }, 200)
    },

    async createNewYezd() {
      const name = this.yezdSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/yezds/', {
          method: 'POST', headers: authHeaders(true),
          body: JSON.stringify({ name })
        })
        this.yezds.push(newItem)
        this.formData.father_yezd_id = newItem.yezd_id
        this.yezdSearch = newItem.name
        this.yezdDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания уезда:', err) }
    },

    onVolostInput() {
      this.formData.father_volost_id = null
      this.clearLocationError()
      this.volostDropOpen = true
    },

    async onVolostBlur() {
      setTimeout(async () => {
        if (this.volostDropOpen) this.volostDropOpen = false
        const name = this.volostSearch.trim()
        if (name && !this.formData.father_volost_id) {
          const existing = this.volosts.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.father_volost_id = existing.volost_id
            this.volostSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/volosts/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.volosts.push(newItem)
              this.formData.father_volost_id = newItem.volost_id
              this.volostSearch = newItem.name
            } catch (err) { console.error('Ошибка создания волости:', err) }
          }
          this.clearLocationError()
        }
      }, 200)
    },

    async createNewVolost() {
      const name = this.volostSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/volosts/', {
          method: 'POST', headers: authHeaders(true),
          body: JSON.stringify({ name })
        })
        this.volosts.push(newItem)
        this.formData.father_volost_id = newItem.volost_id
        this.volostSearch = newItem.name
        this.volostDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания волости:', err) }
    },

    onVillageInput() {
      this.formData.father_village_id = null
      this.clearLocationError()
      this.villageDropOpen = true
    },

    async onVillageBlur() {
      setTimeout(async () => {
        if (this.villageDropOpen) this.villageDropOpen = false
        const name = this.villageSearch.trim()
        if (name && !this.formData.father_village_id) {
          const existing = this.villages.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.father_village_id = existing.village_id
            this.villageSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/villages/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.villages.push(newItem)
              this.formData.father_village_id = newItem.village_id
              this.villageSearch = newItem.name
            } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
          }
          this.clearLocationError()
        }
      }, 200)
    },

    async createNewVillage() {
      const name = this.villageSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/villages/', {
          method: 'POST', headers: authHeaders(true),
          body: JSON.stringify({ name })
        })
        this.villages.push(newItem)
        this.formData.father_village_id = newItem.village_id
        this.villageSearch = newItem.name
        this.villageDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
    },

    clearLocationError() {
      if (this.missingFieldsList.includes('location')) {
        const index = this.missingFieldsList.indexOf('location')
        this.missingFieldsList.splice(index, 1)
      }
      if (this.missingFieldsList.length === 0 && this.error && this.error.includes('местоположения')) {
        this.error = null
      }
    },

    async loadReferenceData() {
      this.loading = true
      try {
        const h = authHeaders()
        const [
          archives, estates, religions, villages,
          provinces, yezds, volosts, churchWorkers,
          motherStatuses, clergyList
        ] = await Promise.all([
          api('/api/archives/',        { headers: h }),
          api('/api/estates/',         { headers: h }),
          api('/api/religions/',       { headers: h }),
          api('/api/villages/',        { headers: h }),
          api('/api/provinces/',       { headers: h }),
          api('/api/yezds/',           { headers: h }),
          api('/api/volosts/',         { headers: h }),
          api('/api/church-workers/',  { headers: h }),
          api('/api/status-choices/',  { headers: h }),
          api('/api/clergy/',          { headers: h }),
        ])

        this.allArchives      = archives       || []
        this.estates          = estates        || []
        this.religions        = religions      || []
        this.villages         = villages       || []
        this.provinces        = provinces      || []
        this.yezds            = yezds          || []
        this.volosts          = volosts        || []
        this.allChurchWorkers = churchWorkers  || []
        this.motherStatuses   = motherStatuses || []
        this.clergyList       = clergyList     || []
      } catch (err) {
        this.error = 'Ошибка загрузки справочников: ' + err.message
      } finally {
        this.loading = false
      }
    },

    scrollToChildFields() {
      this.$nextTick(() => {
        if (this.$refs.childBlock) {
          this.$refs.childBlock.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' })
        }
      })
    },

    onArchiveInput() {
      this.archiveDropOpen = true
      this.formData.archive_id = null
      this.formData.number_case = ''
      this.formData.year = ''
      this.formData.page = ''
      this.formData.number_record = ''
      this.formData.birth_month = ''
      this.autoFilled = false
      this.numberRecordMale = ''
      this.numberRecordFemale = ''
      this.autoFilledFields = {
        archive: false, number_case: false, year: false,
        page: false, number_record: false, birth_month: false,
      }
    },

    closeArchiveDrop() {
      setTimeout(() => { this.archiveDropOpen = false }, 200)
    },

    async selectArchive(archive) {
      this.formData.archive_id  = archive.archive_id
      this.archiveSearch        = archive.name
      this.formData.number_case = archive.number_case
      this.formData.year        = archive.year
      this.autoFilledFields.number_case = true
      this.autoFilledFields.year = true
      this.autoFilledFields.archive = true
      this.archiveDropOpen      = false
      await this.fetchLastRecords(archive.archive_id)

      try {
        const lastRecord = await api(`/api/birth-records/last/?archive_id=${archive.archive_id}`, { headers: authHeaders() }).catch(() => null)
        if (lastRecord && lastRecord.birth_month) {
          this.formData.birth_month = lastRecord.birth_month
          this.autoFilledFields.birth_month = true
        }
      } catch (_) { }
    },

    prepareNewArchive() {
      this.formData.archive_id = null
      this.archiveDropOpen     = false
      this.autoFilled          = false
      this.formData.number_case = ''
      this.formData.year = ''
      this.numberRecordMale = ''
      this.numberRecordFemale = ''
      this.autoFilledFields.number_case = false
      this.autoFilledFields.year = false
      this.autoFilledFields.archive = false
    },

    async fetchLastRecords(archiveId) {
      if (!archiveId) return
      try {
        const [lastMale, lastFemale] = await Promise.all([
          api(`/api/birth-records/last/?archive_id=${archiveId}&sex=М`, { headers: authHeaders() }).catch(() => null),
          api(`/api/birth-records/last/?archive_id=${archiveId}&sex=Ж`, { headers: authHeaders() }).catch(() => null)
        ])
        if (lastMale && lastMale.number_record) {
          this.numberRecordMale = lastMale.number_record + 1
          this.autoFilledFields.number_record = true
        }
        if (lastFemale && lastFemale.number_record) {
          this.numberRecordFemale = lastFemale.number_record + 1
          this.autoFilledFields.number_record = true
        }
        this.autoFilled = true
      } catch (_) { }
    },

    onPriestSearch(i) {
      const p = this.priests[i]
      const q = (p.searchText || '').toLowerCase().trim()
      if (p.church_worker_id) this.unlinkChurchWorker(i)
      if (!q) { p.dropItems = []; p.dropOpen = false; return }
      p.dropItems = this.allChurchWorkers.filter(cw =>
        (cw.surname || '').toLowerCase().includes(q) ||
        (cw.name    || '').toLowerCase().includes(q)
      ).slice(0, 10)
      p.dropOpen = true
    },

    closePriestDrop(i) {
      setTimeout(() => { this.priests[i].dropOpen = false }, 200)
    },

    selectChurchWorker(i, cw) {
      const p            = this.priests[i]
      p.church_worker_id = cw.pries_id
      p.name             = cw.name
      p.surname          = cw.surname
      p.clergy_id        = cw.clergy_id ?? cw.clergy?.clergy_id ?? ''
      p.searchText       = `${cw.surname} ${cw.name}${cw.patronymic ? ' ' + cw.patronymic : ''}`
      p.dropOpen         = false
      p.dropItems        = []
    },

    unlinkChurchWorker(i) {
      const p            = this.priests[i]
      p.church_worker_id = null
      p.name             = ''
      p.surname          = ''
      p.clergy_id        = ''
    },

    autoBaptDay() {
      const d = parseInt(this.formData.birth_day)
      if (!isNaN(d) && d >= 1 && d <= 31) {
        this.formData.baptism_day = Math.min(d + 2, 31)
        this.baptismAuto = true
      }
    },

    onSexChange() {
      if (this.formData.sex === 'М') {
        this.formData.number_record = this.numberRecordMale
      } else if (this.formData.sex === 'Ж') {
        this.formData.number_record = this.numberRecordFemale
      }
    },

    updateNumberRecord() {
      if (this.formData.sex === 'М') {
        this.numberRecordMale = this.formData.number_record
      } else if (this.formData.sex === 'Ж') {
        this.numberRecordFemale = this.formData.number_record
      }
    },

    syncMotherEstate() { },

    formPatronymic(fatherName, sex) {
      if (!fatherName) return ''
      const specialCases = {
        'Пётр': { male: 'Петрович', female: 'Петровна' },
        'Илья': { male: 'Ильич', female: 'Ильинична' },
        'Лука': { male: 'Лукич', female: 'Лукинична' },
        'Фома': { male: 'Фомич', female: 'Фоминична' },
        'Кузьма': { male: 'Кузьмич', female: 'Кузьминична' },
        'Никита': { male: 'Никитич', female: 'Никитична' },
        'Савва': { male: 'Саввич', female: 'Саввична' }
      }
      if (specialCases[fatherName]) {
        return sex === 'М' ? specialCases[fatherName].male : specialCases[fatherName].female
      }
      let base = fatherName
      const lastChar = fatherName.slice(-1)
      const lastTwoChars = fatherName.slice(-2)
      if (lastTwoChars === 'ий' || lastTwoChars === 'ый' || lastTwoChars === 'ой') {
        base = fatherName.slice(0, -2)
      } else if (lastChar === 'й' || lastChar === 'ь') {
        base = fatherName.slice(0, -1)
      } else if (lastChar === 'а' || lastChar === 'я') {
        base = fatherName.slice(0, -1)
      }
      const softConsonants = ['ч', 'щ', 'ж', 'ш']
      if (softConsonants.includes(base.slice(-1))) {
        return sex === 'М' ? base + 'евич' : base + 'евна'
      }
      return base + (sex === 'М' ? 'ович' : 'овна')
    },

    formSurname(fatherSurname, sex) {
      if (!fatherSurname) return ''
      const immutable = ['Черных', 'Хохол', 'Дурень', 'Корень', 'Бездетко', 'Нетудыхата']
      if (immutable.includes(fatherSurname)) return fatherSurname
      if (fatherSurname.match(/(ов|ев|ин|ын)$/i)) {
        return sex === 'Ж' ? fatherSurname + 'а' : fatherSurname
      }
      if (fatherSurname.match(/(ский|цкий)$/i)) {
        return sex === 'Ж' ? fatherSurname.replace(/ий$/, 'ая') : fatherSurname
      }
      if (fatherSurname.match(/ой$/i)) {
        return sex === 'Ж' ? fatherSurname.replace(/ой$/, 'ая') : fatherSurname
      }
      const vowels = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']
      const lastChar = fatherSurname.slice(-1)
      if (!vowels.includes(lastChar)) {
        return sex === 'Ж' ? fatherSurname + 'а' : fatherSurname
      }
      return fatherSurname
    },

    suggestChildFromFather() { this.$forceUpdate() },
    suggestMotherSurname()   { this.$forceUpdate() },

    acceptPatronymicSuggestion()    { this.formData.child_patronymic = this.suggestedPatronymic },
    acceptSurnameSuggestion()       { this.formData.child_surname    = this.suggestedSurname },
    acceptMotherSurnameSuggestion() { this.formData.mother_surname   = this.suggestedMotherSurname },

    checkLocation() {
      return !!(
        this.formData.father_province_id ||
        this.formData.father_yezd_id ||
        this.formData.father_volost_id ||
        this.formData.father_village_id ||
        (this.provinceSearch && this.provinceSearch.trim() !== '') ||
        (this.yezdSearch && this.yezdSearch.trim() !== '') ||
        (this.volostSearch && this.volostSearch.trim() !== '') ||
        (this.villageSearch && this.villageSearch.trim() !== '')
      )
    },

    autoFillGodparentLocation(godparent) {
      if (this.formData.father_province_id && this.formData.father_province_id !== '') {
        godparent.province_id = Number(this.formData.father_province_id)
        const province = this.provinces.find(p => p.province_id === this.formData.father_province_id)
        godparent.provinceSearch = province ? province.name : ''
        godparent.provinceAuto = true
      } else { godparent.province_id = null; godparent.provinceSearch = ''; godparent.provinceAuto = false }

      if (this.formData.father_yezd_id && this.formData.father_yezd_id !== '') {
        godparent.yezd_id = Number(this.formData.father_yezd_id)
        const yezd = this.yezds.find(y => y.yezd_id === this.formData.father_yezd_id)
        godparent.yezdSearch = yezd ? yezd.name : ''
        godparent.yezdAuto = true
      } else { godparent.yezd_id = null; godparent.yezdSearch = ''; godparent.yezdAuto = false }

      if (this.formData.father_volost_id && this.formData.father_volost_id !== '') {
        godparent.volost_id = Number(this.formData.father_volost_id)
        const volost = this.volosts.find(v => v.volost_id === this.formData.father_volost_id)
        godparent.volostSearch = volost ? volost.name : ''
        godparent.volostAuto = true
      } else { godparent.volost_id = null; godparent.volostSearch = ''; godparent.volostAuto = false }

      if (this.formData.father_village_id && this.formData.father_village_id !== '') {
        godparent.village_id = Number(this.formData.father_village_id)
        const village = this.villages.find(v => v.village_id === this.formData.father_village_id)
        godparent.villageSearch = village ? village.name : ''
        godparent.villageAuto = true
      } else { godparent.village_id = null; godparent.villageSearch = ''; godparent.villageAuto = false }

      if (this.formData.father_estate_id && this.formData.father_estate_id !== '') {
        godparent.estate_id = Number(this.formData.father_estate_id)
        godparent.estateAuto = true
      } else { godparent.estate_id = null; godparent.estateAuto = false }

      if (this.formData.creed_id && this.formData.creed_id !== '') {
        godparent.creed_id = Number(this.formData.creed_id)
        godparent.creedAuto = true
      } else { godparent.creed_id = null; godparent.creedAuto = false }

      this.$forceUpdate()
    },

    autoFillGodmotherFromHusband(godmotherIndex) {
      const godmother = this.godmothers[godmotherIndex]
      if (!godmother) return
      if (!this.isLawfulWife(godmother.status_id)) return
      const lastGodman = this.godmen[this.godmen.length - 1]
      if (!lastGodman || !lastGodman.name) return
      godmother.linked_husband_index = this.godmen.length - 1
      if (lastGodman.surname && !godmother.surname) {
        godmother.surname = this.formSurname(lastGodman.surname, 'Ж')
        godmother.surnameAuto = true
      }
      if (lastGodman.patronymic && !godmother.patronymic) godmother.patronymic = lastGodman.patronymic
      if (lastGodman.province_id && !godmother.province_id) { godmother.province_id = lastGodman.province_id; godmother.provinceSearch = lastGodman.provinceSearch; godmother.provinceAuto = true }
      if (lastGodman.yezd_id && !godmother.yezd_id) { godmother.yezd_id = lastGodman.yezd_id; godmother.yezdSearch = lastGodman.yezdSearch; godmother.yezdAuto = true }
      if (lastGodman.volost_id && !godmother.volost_id) { godmother.volost_id = lastGodman.volost_id; godmother.volostSearch = lastGodman.volostSearch; godmother.volostAuto = true }
      if (lastGodman.village_id && !godmother.village_id) { godmother.village_id = lastGodman.village_id; godmother.villageSearch = lastGodman.villageSearch; godmother.villageAuto = true }
      if (lastGodman.estate_id && !godmother.estate_id) { godmother.estate_id = lastGodman.estate_id; godmother.estateAuto = true }
      if (lastGodman.creed_id && !godmother.creed_id) { godmother.creed_id = lastGodman.creed_id; godmother.creedAuto = true }
      this.$forceUpdate()
    },

    addGodman() {
      const locationSearch = this._fatherLocationSearch()
      this.godmen.push({
        ...this.emptyGodman(),
        province_id: this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
        yezd_id:     this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
        volost_id:   this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
        village_id:  this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
        estate_id:   this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
        creed_id:    this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
        ...locationSearch,
        provinceAuto: !!this.formData.father_province_id,
        yezdAuto:     !!this.formData.father_yezd_id,
        volostAuto:   !!this.formData.father_volost_id,
        villageAuto:  !!this.formData.father_village_id,
        estateAuto:   !!this.formData.father_estate_id,
        creedAuto:    !!this.formData.creed_id,
      })
    },

    addGodmother() {
      const locationSearch = this._fatherLocationSearch()
      const newGodmother = {
        ...this.emptyGodmother(),
        province_id: this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
        yezd_id:     this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
        volost_id:   this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
        village_id:  this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
        estate_id:   this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
        creed_id:    this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
        status_id: null,
        ...locationSearch,
        provinceAuto: !!this.formData.father_province_id,
        yezdAuto:     !!this.formData.father_yezd_id,
        volostAuto:   !!this.formData.father_volost_id,
        villageAuto:  !!this.formData.father_village_id,
        estateAuto:   !!this.formData.father_estate_id,
        creedAuto:    !!this.formData.creed_id,
        linked_husband_index: null,
      }
      this.godmothers.push(newGodmother)
      if (this.isLawfulWife(newGodmother.status_id)) {
        this.autoFillGodmotherFromHusband(this.godmothers.length - 1)
      }
    },

    _fatherLocationSearch() {
      const findName = (list, id, key) => {
        if (!id) return ''
        const found = list.find(i => i[key] === id)
        return found ? found.name : ''
      }
      return {
        provinceSearch: this.provinceSearch || findName(this.provinces, this.formData.father_province_id, 'province_id'),
        yezdSearch:     this.yezdSearch     || findName(this.yezds,     this.formData.father_yezd_id,     'yezd_id'),
        volostSearch:   this.volostSearch   || findName(this.volosts,   this.formData.father_volost_id,   'volost_id'),
        villageSearch:  this.villageSearch  || findName(this.villages,  this.formData.father_village_id,  'village_id'),
      }
    },

    addPriest() {
      this.priests.push(this.emptyPriest())
    },

    closeGodDrop(g, field) {
      window.setTimeout(() => { g[field] = false }, 200)
    },

    openModal(type) { this.modal = { type, value: '' } },
    closeModal()    { this.modal = { type: null, value: '' } },

    async saveRef() {
      if (!this.modal.value.trim()) return
      const type = this.modal.type
      try {
        let result
        if (type === 'estate') {
          result = await api('/api/estates/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.estates.push(result)
          this.formData.father_estate_id = result.estate_id
        }
        if (type === 'religion') {
          result = await api('/api/religions/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.religions.push(result)
          this.formData.creed_id = result.creed_id
        }
        if (type === 'mother_status') {
          result = await api('/api/status-choices/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.motherStatuses.push(result)
        }
        if (type === 'clergy') {
          result = await api('/api/clergy/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.clergyList.push(result)
          const editable = [...this.priests].reverse().find(p => !p.church_worker_id)
          if (editable) editable.clergy_id = result.clergy_id
        }
        this.closeModal()
      } catch (err) {
        alert('Ошибка сохранения: ' + err.message)
      }
    },

    loadScan(e) {
      const file = e.target.files[0]
      if (!file) return
      this.scanFile = file
      const reader = new FileReader()
      reader.onload = ev => { this.scanSrc = ev.target.result; this.resetScan() }
      reader.readAsDataURL(file)
    },

    startDrag(e) {
      if (!this.scanSrc) return
      e.preventDefault()
      this.isDragging = true
      this._dragStartX = e.clientX - this.panX
      this._dragStartY = e.clientY - this.panY
      this._onMouseMove = (ev) => {
        this.panX = ev.clientX - this._dragStartX
        this.panY = ev.clientY - this._dragStartY
      }
      this._onMouseUp = () => {
        this.isDragging = false
        document.removeEventListener('mousemove', this._onMouseMove)
        document.removeEventListener('mouseup',  this._onMouseUp)
      }
      document.addEventListener('mousemove', this._onMouseMove)
      document.addEventListener('mouseup',   this._onMouseUp)
    },

    onWheel(e) {
      if (!this.scanSrc) return
      const delta = e.deltaY < 0 ? 0.15 : -0.15
      this.zoom = Math.min(8, Math.max(0.2, Math.round((this.zoom + delta) * 100) / 100))
    },

    zoomIn()    { this.zoom = Math.min(8,   Math.round((this.zoom + 0.25) * 100) / 100) },
    zoomOut()   { this.zoom = Math.max(0.2, Math.round((this.zoom - 0.25) * 100) / 100) },
    resetScan() { this.zoom = 1; this.panX = 0; this.panY = 0 },

    formatDateForApi(year, month, day) {
      if (!year || !month || !day) return null
      return `${String(year).trim()}-${String(month).padStart(2,'0')}-${String(day).padStart(2,'0')}`
    },

    // ══════════════════════════════════════════════════════════════
    // ЗАГРУЗКА ЗАПИСИ ДЛЯ РЕДАКТИРОВАНИЯ
    // ══════════════════════════════════════════════════════════════
    async loadRecordForEditing(recordId, recordType) {
      this.loading = true
      try {
        const headers = authHeaders()
        const endpoint = recordType === 'birth' ? 'birth-records' :
                         recordType === 'marriage' ? 'marriage-records' : 'death-records'

        const record = await api(`/api/${endpoint}/${recordId}/`, { headers })
        if (!record) throw new Error('Запись не найдена')

        const resolveId = (val, idField = null) => {
          if (val === null || val === undefined || val === '') return null
          if (typeof val === 'object') {
            if (idField && val[idField] !== undefined) return Number(val[idField])
            const key = Object.keys(val).find(k => k.endsWith('_id'))
            return key ? Number(val[key]) : null
          }
          const n = Number(val)
          return isNaN(n) ? null : n
        }

        this.editingRecordId = recordId

        // ── Сохраняем ID персон для последующего PATCH ────────────
        const personData = record.person_data || record.person || {}
        this.existingPersonIds.child  = resolveId(record.person, 'person_id') ?? null
        this.existingPersonIds.father = null
        this.existingPersonIds.mother = null

        // Ищем отца по ФИО
        if (record.father_surname && record.father_name) {
          try {
            const res = await api(
              `/api/persons/?surname=${encodeURIComponent(record.father_surname)}&name=${encodeURIComponent(record.father_name)}&sex=М`,
              { headers: authHeaders() }
            )
            const list = Array.isArray(res) ? res : (res.results ?? res.persons ?? [])
            // Берём первого с совпадающим отчеством (если есть), иначе просто первого
            const found = record.father_patronymic
              ? list.find(p => p.patronymic === record.father_patronymic) ?? list[0]
              : list[0]
            if (found) this.existingPersonIds.father = found.person_id
          } catch (err) { console.warn('Поиск отца не удался:', err) }
        }

        // Ищем мать по ФИО
        if (record.mother_surname && record.mother_name) {
          try {
            const res = await api(
              `/api/persons/?surname=${encodeURIComponent(record.mother_surname)}&name=${encodeURIComponent(record.mother_name)}&sex=Ж`,
              { headers: authHeaders() }
            )
            const list = Array.isArray(res) ? res : (res.results ?? res.persons ?? [])
            const found = record.mother_patronymic
              ? list.find(p => p.patronymic === record.mother_patronymic) ?? list[0]
              : list[0]
            if (found) this.existingPersonIds.mother = found.person_id
          } catch (err) { console.warn('Поиск матери не удался:', err) }
        }

        // ── Архив ─────────────────────────────────────────────────
        let archiveId = resolveId(record.archive, 'archive_id')
        if (archiveId) {
          this.formData.archive_id = archiveId
          let foundArchive = this.allArchives.find(a => a.archive_id === archiveId)
          if (foundArchive) {
            this.archiveSearch        = foundArchive.name
            this.formData.number_case = foundArchive.number_case || ''
            this.formData.year        = foundArchive.year || ''
          } else {
            try {
              const archiveData = await api(`/api/archives/${archiveId}/`, { headers })
              this.archiveSearch        = archiveData.name || ''
              this.formData.number_case = archiveData.number_case || ''
              this.formData.year        = archiveData.year || ''
              this.allArchives.push(archiveData)
            } catch {
              this.archiveSearch = record.archive_name || ''
            }
          }
        } else {
          this.archiveSearch = record.archive_name || ''
        }

        // ── Основные поля ─────────────────────────────────────────
        this.formData.page          = record.page          || ''
        this.formData.page_turn     = record.page_turn     || false
        this.formData.number_record = record.number_record || ''
        this.formData.birth_month   = record.birth_month   || ''
        this.formData.birth_day     = record.birth_day     || ''
        this.formData.baptism_day   = record.baptism_day   || ''
        this.formData.sex           = record.sex           || ''
        this.formData.comment       = record.comment       || ''

        // ── Ребёнок ───────────────────────────────────────────────
        const pd = record.person_data || {}
        this.formData.name             = pd.name       || ''
        this.formData.child_patronymic = pd.patronymic || ''
        this.formData.child_surname    = pd.surname    || ''

        this.formData.creed_id =
          resolveId(pd.creed,      'creed_id') ||
          resolveId(record.creed,  'creed_id') ||
          resolveId(record.creed_id) ||
          null

        // ── Отец ──────────────────────────────────────────────────
        this.formData.father_name       = record.father_name       || ''
        this.formData.father_patronymic = record.father_patronymic || ''
        this.formData.father_surname    = record.father_surname    || ''
        this.formData.father_estate_id  = resolveId(record.father_estate, 'estate_id')

        this.formData.father_province_id = resolveId(record.father_province, 'province_id')
        if (this.formData.father_province_id) {
          const found = this.provinces.find(p => p.province_id === this.formData.father_province_id)
          if (found) this.provinceSearch = found.name
        }

        this.formData.father_yezd_id = resolveId(record.father_yezd, 'yezd_id')
        if (this.formData.father_yezd_id) {
          const found = this.yezds.find(y => y.yezd_id === this.formData.father_yezd_id)
          if (found) this.yezdSearch = found.name
        }

        this.formData.father_volost_id = resolveId(record.father_volost, 'volost_id')
        if (this.formData.father_volost_id) {
          const found = this.volosts.find(v => v.volost_id === this.formData.father_volost_id)
          if (found) this.volostSearch = found.name
        }

        this.formData.father_village_id = resolveId(record.father_village, 'village_id')
        if (this.formData.father_village_id) {
          const found = this.villages.find(v => v.village_id === this.formData.father_village_id)
          if (found) this.villageSearch = found.name
        }

        // ── Мать ──────────────────────────────────────────────────
        this.formData.mother_name       = record.mother_name       || ''
        this.formData.mother_patronymic = record.mother_patronymic || ''
        this.formData.mother_surname    = record.mother_surname    || ''
        this.formData.mother_status     = record.mother_status     || ''

        if (record.number_record) {
          this.formData.number_record = record.number_record
          if (record.sex === 'М') this.numberRecordMale   = record.number_record
          else if (record.sex === 'Ж') this.numberRecordFemale = record.number_record
        }

        // ── Вспомогательная функция для поиска имени ──────────────
        const findName = (list, id, key) => {
          if (!id) return ''
          const found = list.find(i => i[key] === id)
          return found ? found.name : ''
        }

        // ── Восприемники (мужчины) ────────────────────────────────
        if (record.godmen && record.godmen.length) {
          this.godmen = record.godmen.map(g => {
            const provinceId = resolveId(g.province, 'province_id')
            const yezdId     = resolveId(g.yezd,     'yezd_id')
            const volostId   = resolveId(g.volost,   'volost_id')
            const villageId  = resolveId(g.village,  'village_id')
            const estateId   = resolveId(g.estate,   'estate_id')
            const creedId    = resolveId(g.creed,    'creed_id')
            return {
              ...this.emptyGodman(),
              godman_id:    g.godman_id ?? g.id ?? null,
              name:         g.name       || '',
              patronymic:   g.patronymic || '',
              surname:      g.surname    || '',
              province_id:  provinceId,
              yezd_id:      yezdId,
              volost_id:    volostId,
              village_id:   villageId,
              estate_id:    estateId,
              creed_id:     creedId,
              provinceSearch: findName(this.provinces, provinceId, 'province_id'),
              yezdSearch:     findName(this.yezds,     yezdId,     'yezd_id'),
              volostSearch:   findName(this.volosts,   volostId,   'volost_id'),
              villageSearch:  g.village_name || findName(this.villages, villageId, 'village_id'),
              provinceAuto: false, yezdAuto: false, volostAuto: false,
              villageAuto:  false, estateAuto: false, creedAuto: false,
            }
          })
        } else {
          this.godmen = [this.emptyGodman()]
        }

        // ── Восприемницы (женщины) ────────────────────────────────
        if (record.godmothers && record.godmothers.length) {
          this.godmothers = record.godmothers.map(g => {
            const provinceId = resolveId(g.province, 'province_id')
            const yezdId     = resolveId(g.yezd,     'yezd_id')
            const volostId   = resolveId(g.volost,   'volost_id')
            const villageId  = resolveId(g.village,  'village_id')
            const estateId   = resolveId(g.estate,   'estate_id')
            const creedId    = resolveId(g.creed,    'creed_id')
            const statusId   = resolveId(g.status,   'status_choice_id')
            return {
              ...this.emptyGodmother(),
              godmother_id: g.godmother_id ?? g.id ?? null,
              name:         g.name       || '',
              patronymic:   g.patronymic || '',
              surname:      g.surname    || '',
              province_id:  provinceId,
              yezd_id:      yezdId,
              volost_id:    volostId,
              village_id:   villageId,
              estate_id:    estateId,
              creed_id:     creedId,
              status_id:    statusId,
              provinceSearch: findName(this.provinces, provinceId, 'province_id'),
              yezdSearch:     findName(this.yezds,     yezdId,     'yezd_id'),
              volostSearch:   findName(this.volosts,   volostId,   'volost_id'),
              villageSearch:  g.village_name || findName(this.villages, villageId, 'village_id'),
              provinceAuto: false, yezdAuto: false, volostAuto: false,
              villageAuto:  false, estateAuto: false, creedAuto: false,
              surnameAuto: false, linked_husband_index: null,
            }
          })
        } else {
          this.godmothers = [this.emptyGodmother()]
        }

        // ── Священнослужители ─────────────────────────────────────
        if (record.priests && record.priests.length) {
          this.priests = record.priests.map(p => {
            let clergyId = resolveId(p.clergy, 'clergy_id') || resolveId(p.clergy_id)
            if (!clergyId && p.clergy_name) {
              const found = this.clergyList.find(c => c.name === p.clergy_name)
              if (found) clergyId = found.clergy_id
            }
            const churchWorkerId = resolveId(p.church_worker, 'pries_id')
            return {
              ...this.emptyPriest(),
              priest_record_id: p.id ?? p.priest_record_id ?? null,
              name:             p.name    || '',
              surname:          p.surname || '',
              clergy_id:        clergyId,
              church_worker_id: churchWorkerId,
              searchText:       p.searchText || `${p.surname || ''} ${p.name || ''}`.trim(),
            }
          })
        } else {
          this.priests = [this.emptyPriest()]
        }

        // ── Скан ──────────────────────────────────────────────────
        this.scanSrc = null
        if (this.editingRecordId) {
          const possibleExts = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
          for (const ext of possibleExts) {
            const scanUrl = `${API_BASE}/media/scans/birth/${this.editingRecordId}${ext}`
            try {
              const response = await fetch(scanUrl, { method: 'HEAD' })
              if (response.ok) { this.scanSrc = scanUrl; break }
            } catch { /* продолжаем */ }
          }
        }

        this.formStatus         = 'published'
        this.showPublishAttempt = false
        this.missingFieldsList  = []
        this.error              = null
        this.$forceUpdate()

      } catch (err) {
        console.error('Ошибка загрузки записи для редактирования:', err)
        this.error = 'Не удалось загрузить данные для редактирования: ' + err.message
      } finally {
        this.loading = false
      }
    },

    loadDraftData(draftData) {
      if (draftData.formData) {
        Object.assign(this.formData, draftData.formData)
        ;['birth_month','birth_day','baptism_day','year','page','number_record'].forEach(k => {
          if (this.formData[k]) this.formData[k] = Number(this.formData[k])
        })
      }
      if (draftData.numberRecordMale)   this.numberRecordMale   = draftData.numberRecordMale
      if (draftData.numberRecordFemale) this.numberRecordFemale = draftData.numberRecordFemale
      if (draftData.archiveSearch)  this.archiveSearch  = draftData.archiveSearch
      if (draftData.provinceSearch !== undefined) this.provinceSearch = draftData.provinceSearch || ''
      if (draftData.yezdSearch     !== undefined) this.yezdSearch     = draftData.yezdSearch     || ''
      if (draftData.volostSearch   !== undefined) this.volostSearch   = draftData.volostSearch   || ''
      if (draftData.villageSearch  !== undefined) this.villageSearch  = draftData.villageSearch  || ''
      if (draftData.scanSrc) this.scanSrc = draftData.scanSrc
      if (draftData.godmen?.length) {
        this.godmen = draftData.godmen.map(g => ({
          ...this.emptyGodman(), ...g,
          provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false,
          provinceSearch: g.provinceSearch || '', yezdSearch: g.yezdSearch || '',
          volostSearch: g.volostSearch || '', villageSearch: g.villageSearch || '',
        }))
      }
      if (draftData.godmothers?.length) {
        this.godmothers = draftData.godmothers.map(g => ({
          ...this.emptyGodmother(), ...g,
          provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false,
          provinceSearch: g.provinceSearch || '', yezdSearch: g.yezdSearch || '',
          volostSearch: g.volostSearch || '', villageSearch: g.villageSearch || '',
        }))
      }
      if (draftData.priests?.length) {
        this.priests = draftData.priests.map(p => ({
          ...this.emptyPriest(), ...p,
          dropOpen: false, dropItems: [], searchText: p.searchText || '',
        }))
      }
    },

    showFieldError(fieldName) {
      if (this.formStatus !== 'published') return false
      if (!this.showPublishAttempt) return false
      if (fieldName === 'location') return this.missingFieldsList.includes('location')
      return this.missingFieldsList.includes(fieldName)
    },

    isFieldMissing(fieldName) {
      const value = this.formData[fieldName]
      const isEmpty = value === null || value === undefined || value === '' || value === 0
      const requiredFields = [
        'number_case', 'year', 'page', 'number_record',
        'birth_month', 'birth_day', 'baptism_day',
        'sex', 'name',
        'father_estate_id', 'creed_id', 'father_name', 'father_surname',
        'mother_name', 'mother_status'
      ]
      if (fieldName === 'location') return !this.checkLocation()
      if (!requiredFields.includes(fieldName)) return false
      if (fieldName === 'number_case' && this.formData.archive_id && this.archiveSearch.trim()) return false
      if (fieldName === 'year'        && this.formData.archive_id && this.archiveSearch.trim()) return false
      return isEmpty
    },

    switchToDraft() {
      this.formStatus = 'draft'
      this.showPublishAttempt = false
      this.missingFieldsList = []
      this.error = null
    },

    switchToPublish() {
      this.formStatus = 'published'
    },

    validateAllFields() {
      const requiredFields = [
        'number_case', 'year', 'page', 'number_record',
        'birth_month', 'birth_day', 'baptism_day',
        'sex', 'name',
        'father_estate_id', 'creed_id', 'father_name', 'father_surname',
        'mother_name', 'mother_status', 'location'
      ]
      const missing = []
      for (const field of requiredFields) {
        if (this.isFieldMissing(field)) missing.push(field)
      }
      this.missingFieldsList = missing
      this.showPublishAttempt = true
      if (missing.length > 0) {
        this.error = `Необходимо заполнить ${missing.length} обязательное(ых) поле(й)`
        setTimeout(() => { this.scrollToFirstError() }, 100)
      } else {
        this.error = null
      }
      return missing.length === 0
    },

    scrollToFirstError() {
      const firstError = document.querySelector('.field-error')
      if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
    },

    // ══════════════════════════════════════════════════════════════
    // ОБРАБОТЧИК SUBMIT — направляет в нужный метод
    // ══════════════════════════════════════════════════════════════
    async handleSubmit() {
      if (this.formStatus === 'draft') {
        await this.saveServerDraft()
        return
      }

      const isValid = this.validateAllFields()
      if (!isValid) return

      if (this.isEditMode) {
        // В режиме редактирования — сразу сохраняем без диалога
        await this.saveEditedRecord()
      } else {
        this.showPublishConfirm = true
      }
    },

    async confirmPublish() {
      this.showPublishConfirm = false
      await this.saveBirthRecord()
    },

    // ══════════════════════════════════════════════════════════════
    // СОХРАНЕНИЕ ИЗМЕНЕНИЙ (режим редактирования)
    // ══════════════════════════════════════════════════════════════
    async saveEditedRecord() {
      this.error = null
      ;['year', 'birth_month', 'birth_day', 'baptism_day'].forEach(k => {
        this.formData[k] = Number(this.formData[k])
      })
      await this.ensureLocationObjects()
      this.loading = true

      try {
        const H = authHeaders(true)
        const { year, birth_month: month, birth_day: birthDay, baptism_day: baptDay } = this.formData
        const birthDate     = this.formatDateForApi(year, month, birthDay)
        const dateOfBaptism = this.formatDateForApi(year, month, baptDay)

        // ── 1. Обновляем персону ребёнка ──────────────────────────
        if (this.existingPersonIds.child) {
          await api(`/api/persons/${this.existingPersonIds.child}/`, {
            method: 'PATCH', headers: H,
            body: JSON.stringify({
              name:       this.formData.name,
              surname:    this.formData.child_surname    || this.formData.father_surname || '',
              patronymic: this.formData.child_patronymic || '',
              sex:        this.formData.sex,
              date:       birthDate,
              estate:     this.formData.father_estate_id    ? Number(this.formData.father_estate_id)    : null,
              creed:      this.formData.creed_id            ? Number(this.formData.creed_id)            : null,
              province:   this.formData.father_province_id  ? Number(this.formData.father_province_id)  : null,
              yezd:       this.formData.father_yezd_id      ? Number(this.formData.father_yezd_id)      : null,
              volost:     this.formData.father_volost_id    ? Number(this.formData.father_volost_id)    : null,
              village:    this.formData.father_village_id   ? Number(this.formData.father_village_id)   : null,
              comment:    this.formData.comment || '',
            })
          })
        }

        // ── 2. Обновляем или создаём персону отца ─────────────────
        if (this.existingPersonIds.father && this.formData.father_name) {
          await api(`/api/persons/${this.existingPersonIds.father}/`, {
            method: 'PATCH', headers: H,
            body: JSON.stringify({
              name:       this.formData.father_name,
              surname:    this.formData.father_surname    || '',
              patronymic: this.formData.father_patronymic || '',
              sex:        'М',
              estate:     this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
              creed:      this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
              province:   this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
              yezd:       this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
              volost:     this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
              village:    this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
            })
          })
        } else if (!this.existingPersonIds.father && this.formData.father_name && this.formData.father_surname) {
          const newFather = await api('/api/persons/', {
            method: 'POST', headers: H,
            body: JSON.stringify({
              name: this.formData.father_name, surname: this.formData.father_surname,
              patronymic: this.formData.father_patronymic || '', sex: 'М',
              estate:   this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
              creed:    this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
              province: this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
              yezd:     this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
              volost:   this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
              village:  this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
              duplicate: 0,
              comment: `Отец из записи о рождении #${this.formData.number_record}`,
            })
          })
          this.existingPersonIds.father = newFather.person_id
        }

        // ── 3. Обновляем или создаём персону матери ───────────────
        if (this.existingPersonIds.mother && this.formData.mother_name) {
          await api(`/api/persons/${this.existingPersonIds.mother}/`, {
            method: 'PATCH', headers: H,
            body: JSON.stringify({
              name:       this.formData.mother_name,
              surname:    this.formData.mother_surname    || '',
              patronymic: this.formData.mother_patronymic || '',
              sex:        'Ж',
              estate:     this.formData.father_estate_id ? Number(this.formData.father_estate_id) : null,
              creed:      this.formData.creed_id         ? Number(this.formData.creed_id)         : null,
            })
          })
        } else if (!this.existingPersonIds.mother && this.formData.mother_name && this.formData.mother_surname) {
          const newMother = await api('/api/persons/', {
            method: 'POST', headers: H,
            body: JSON.stringify({
              name: this.formData.mother_name, surname: this.formData.mother_surname,
              patronymic: this.formData.mother_patronymic || '', sex: 'Ж',
              estate:    this.formData.father_estate_id ? Number(this.formData.father_estate_id) : null,
              creed:     this.formData.creed_id         ? Number(this.formData.creed_id)         : null,
              duplicate: 0,
              comment: `Мать из записи о рождении #${this.formData.number_record}`,
            })
          })
          this.existingPersonIds.mother = newMother.person_id
        }

        // ── 4. Обновляем саму запись о рождении ───────────────────
        await api(`/api/birth-records/${this.editingRecordId}/`, {
          method: 'PATCH', headers: H,
          body: JSON.stringify({
            page:           this.formData.page         ? String(this.formData.page)          : '',
            page_turn:      this.formData.page_turn    || false,
            number_record:  this.formData.number_record ? String(this.formData.number_record) : '',
            sex:            this.formData.sex          || '',
            birth_month:    this.formData.birth_month  ? Number(this.formData.birth_month)   : null,
            birth_day:      this.formData.birth_day    ? Number(this.formData.birth_day)     : null,
            baptism_day:    this.formData.baptism_day  ? Number(this.formData.baptism_day)   : null,
            date_of_baptism: dateOfBaptism,
            father_name:       this.formData.father_name       || '',
            father_patronymic: this.formData.father_patronymic || '',
            father_surname:    this.formData.father_surname    || '',
            father_estate:   this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
            father_province: this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
            father_yezd:     this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
            father_volost:   this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
            father_village:  this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
            mother_name:       this.formData.mother_name       || '',
            mother_patronymic: this.formData.mother_patronymic || '',
            mother_surname:    this.formData.mother_surname    || '',
            mother_status:   this.formData.mother_status || '',
            comment:         this.formData.comment      || '',
            status:          'published',
          })
        })

        // ── 5. Скан (только если выбрали новый файл) ──────────────
        if (this.scanFile) {
          try {
            await this._uploadScan('birth', this.editingRecordId, this.scanFile)
          } catch (scanErr) {
            console.error('Ошибка загрузки скана:', scanErr)
          }
        }

        // ── 6. Синхронизация восприемников (мужчины) ──────────────
        // Удаляем старых, которых нет в текущем списке, затем создаём/обновляем
        const existingGodmenIds = this.godmen.filter(g => g.godman_id).map(g => Number(g.godman_id))

        // Получаем актуальный список из БД чтобы найти удалённых
        try {
          const currentRecord = await api(`/api/birth-records/${this.editingRecordId}/`, { headers: authHeaders() })
          const dbGodmenIds = (currentRecord.godmen || []).map(g => g.godmen_id ?? g.godman_id ?? g.id)
          for (const dbId of dbGodmenIds) {
            if (!existingGodmenIds.includes(dbId)) {
              await api(`/api/godmen/${dbId}/`, { method: 'DELETE', headers: H }).catch(() => {})
            }
          }
        } catch (_) { }

        for (const g of this.godmen) {
          if (!g.name || !g.name.trim()) continue
          const godmanPayload = {
            birth:     this.editingRecordId,
            name:      g.name       || '',
            patronymic: g.patronymic || '',
            surname:   g.surname    || '',
            estate:    g.estate_id  && g.estate_id  !== '' ? Number(g.estate_id)  : null,
            creed:     g.creed_id   && g.creed_id   !== '' ? Number(g.creed_id)   : null,
            province:  g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
            yezd:      g.yezd_id    && g.yezd_id    !== '' ? Number(g.yezd_id)    : null,
            volost:    g.volost_id  && g.volost_id  !== '' ? Number(g.volost_id)  : null,
            village:   g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
          }
          if (g.godman_id) {
            await api(`/api/godmen/${g.godman_id}/`, {
              method: 'PATCH', headers: H,
              body: JSON.stringify(godmanPayload)
            }).catch(err => console.error('Ошибка обновления восприемника:', err))
          } else {
            const created = await api('/api/godmen/', {
              method: 'POST', headers: H,
              body: JSON.stringify(godmanPayload)
            }).catch(err => console.error('Ошибка создания восприемника:', err))
            if (created) g.godman_id = created.godman_id ?? created.id
          }
        }

        // ── 7. Синхронизация восприемниц (женщины) ────────────────
        const existingGodmotherIds = this.godmothers
          .filter(g => g.godmother_id)
          .map(g => g.godmother_id)

        try {
          const currentRecord = await api(`/api/birth-records/${this.editingRecordId}/`, { headers: authHeaders() })
          const dbGodmotherIds = (currentRecord.godmothers || []).map(g => g.godmother_id ?? g.id)
          for (const dbId of dbGodmotherIds) {
            if (!existingGodmotherIds.includes(dbId)) {
              await api(`/api/godmothers/${dbId}/`, { method: 'DELETE', headers: H }).catch(() => {})
            }
          }
        } catch (_) { }

        for (const g of this.godmothers) {
          if (!g.name || !g.name.trim()) continue
          const godmotherPayload = {
            birth:      this.editingRecordId,
            name:       g.name       || '',
            patronymic: g.patronymic || '',
            surname:    g.surname    || '',
            estate:     g.estate_id  && g.estate_id  !== '' ? Number(g.estate_id)  : null,
            creed:      g.creed_id   && g.creed_id   !== '' ? Number(g.creed_id)   : null,
            province:   g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
            yezd:       g.yezd_id    && g.yezd_id    !== '' ? Number(g.yezd_id)    : null,
            volost:     g.volost_id  && g.volost_id  !== '' ? Number(g.volost_id)  : null,
            village:    g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
            status:     g.status_id  && g.status_id  !== '' ? Number(g.status_id)  : null,
          }
          if (g.godmother_id) {
            await api(`/api/godmothers/${g.godmother_id}/`, {
              method: 'PATCH', headers: H,
              body: JSON.stringify(godmotherPayload)
            }).catch(err => console.error('Ошибка обновления восприемницы:', err))
          } else {
            const created = await api('/api/godmothers/', {
              method: 'POST', headers: H,
              body: JSON.stringify(godmotherPayload)
            }).catch(err => console.error('Ошибка создания восприемницы:', err))
            if (created) g.godmother_id = created.godmother_id ?? created.id
          }
        }

        // ── 8. Синхронизация священнослужителей ───────────────────
        const existingPriestRecordIds = this.priests
          .filter(p => p.priest_record_id)
          .map(p => p.priest_record_id)

        try {
          const currentRecord = await api(`/api/birth-records/${this.editingRecordId}/`, { headers: authHeaders() })
          const dbPriestIds = (currentRecord.priests || []).map(p => p.id ?? p.priest_record_id)
          for (const dbId of dbPriestIds) {
            if (!existingPriestRecordIds.includes(dbId)) {
              await api(`/api/birth-record-priests/${dbId}/`, { method: 'DELETE', headers: H }).catch(() => {})
            }
          }
        } catch (_) { }

        for (const p of this.priests) {
          if (!p.name || !p.name.trim()) continue
          const priestPayload = {
            birth:   this.editingRecordId,
            name:    p.name    || '',
            surname: p.surname || '',
            clergy:  p.clergy_id       && p.clergy_id       !== '' ? Number(p.clergy_id)       : null,
            church_worker: p.church_worker_id && p.church_worker_id !== '' ? Number(p.church_worker_id) : null,
          }
          if (p.priest_record_id) {
            await api(`/api/birth-record-priests/${p.priest_record_id}/`, {
              method: 'PATCH', headers: H,
              body: JSON.stringify(priestPayload)
            }).catch(err => console.error('Ошибка обновления священнослужителя:', err))
          } else {
            const created = await api('/api/birth-record-priests/', {
              method: 'POST', headers: H,
              body: JSON.stringify(priestPayload)
            }).catch(err => console.error('Ошибка создания священнослужителя:', err))
            if (created) p.priest_record_id = created.priest_record_id ?? created.id
          }
        }

        this.showEditSuccess = true

      } catch (err) {
        console.error('Ошибка при сохранении изменений:', err)
        this.error = 'Ошибка при сохранении изменений: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.loading = false
      }
    },

    closeEditSuccess() {
      this.showEditSuccess = false
      this.$router.push('/home')
    },

    // ══════════════════════════════════════════════════════════════
    // ЧЕРНОВИК
    // ══════════════════════════════════════════════════════════════
    async saveServerDraft() {
      this.error = null
      this.loading = true
      try {
        const payload = this.buildFullPayload()
        if (this.scanSrc) payload.scanSrc = this.scanSrc
        let url = '/api/drafts/'
        let method = 'POST'
        if (this.currentDraftId) {
          url = `/api/drafts/${this.currentDraftId}/`
          method = 'PUT'
        }
        await api(url, {
          method, headers: authHeaders(true),
          body: JSON.stringify({ record_type: 'birth', payload })
        })
        this.showDraftSuccess = true
      } catch (err) {
        this.error = 'Ошибка сохранения черновика: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.loading = false
      }
    },

    closeDraftSuccess()   { this.showDraftSuccess   = false; this.$router.push('/home') },
    closePublishSuccess() { this.showPublishSuccess = false; this.$router.push('/home') },

    buildFullPayload() {
      return {
        formData: {
          ...this.formData,
          father_province_id: this.formData.father_province_id || null,
          father_yezd_id:     this.formData.father_yezd_id     || null,
          father_volost_id:   this.formData.father_volost_id   || null,
          father_village_id:  this.formData.father_village_id  || null,
        },
        numberRecordMale:   this.numberRecordMale,
        numberRecordFemale: this.numberRecordFemale,
        archiveSearch:  this.archiveSearch  || '',
        provinceSearch: this.provinceSearch || '',
        yezdSearch:     this.yezdSearch     || '',
        volostSearch:   this.volostSearch   || '',
        villageSearch:  this.villageSearch  || '',
        scanSrc: this.scanSrc || null,
        godmen:     this.godmen.map(g => ({ ...g, provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false })),
        godmothers: this.godmothers.map(g => ({ ...g, provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false })),
        priests:    this.priests.map(p => ({ ...p, dropOpen: false, dropItems: [] })),
      }
    },

    _uploadScan(recordType, recordId, file) {
      const fd = new FormData()
      fd.append('scan', file)
      return fetch(`${API_BASE}/api/${recordType}-records/${recordId}/upload_scan/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        body: fd,
      })
    },

    // ══════════════════════════════════════════════════════════════
    // ПУБЛИКАЦИЯ НОВОЙ ЗАПИСИ
    // ══════════════════════════════════════════════════════════════
    async saveBirthRecord() {
      this.error = null
      ;['year','birth_month','birth_day','baptism_day'].forEach(k => {
        this.formData[k] = Number(this.formData[k])
      })
      await this.ensureLocationObjects()

      const { year, birth_month: month, birth_day: birthDay, baptism_day: baptDay } = this.formData
      if (!year || !month || !birthDay) {
        this.error = 'Заполните год, месяц и число рождения'
        window.scrollTo({ top: 0, behavior: 'smooth' })
        return
      }

      this.loading = true
      try {
        const H = authHeaders(true)

        let archiveId = this.formData.archive_id
        if (!archiveId && this.archiveSearch.trim()) {
          const newArchive = await api('/api/archives/', {
            method: 'POST', headers: H,
            body: JSON.stringify({
              name: this.archiveSearch.trim(),
              number_case: this.formData.number_case,
              year: this.formData.year
            })
          })
          archiveId = newArchive.archive_id
        } else if (!archiveId) {
          throw new Error('Необходимо указать архив')
        }

        const birthDate     = this.formatDateForApi(year, month, birthDay)
        const dateOfBaptism = this.formatDateForApi(year, month, baptDay)

        // ── 1. Создаём отца ───────────────────────────────────────
        let fatherPersonId = null
        if (this.formData.father_name && this.formData.father_surname) {
          try {
            const fatherPerson = await api('/api/persons/', {
              method: 'POST', headers: H,
              body: JSON.stringify({
                name:       this.formData.father_name,
                surname:    this.formData.father_surname,
                patronymic: this.formData.father_patronymic || '',
                sex:        'М',
                date:       null,
                estate:     this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
                creed:      this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
                province:   this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
                yezd:       this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
                volost:     this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
                village:    this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
                duplicate:  0,
                comment:    `Отец из записи о рождении #${this.formData.number_record}`,
              })
            })
            fatherPersonId = fatherPerson.person_id
          } catch (err) { console.error('Ошибка создания отца:', err) }
        }

        // ── 2. Создаём мать ───────────────────────────────────────
        let motherPersonId = null
        if (this.formData.mother_name && this.formData.mother_surname) {
          try {
            const motherPerson = await api('/api/persons/', {
              method: 'POST', headers: H,
              body: JSON.stringify({
                name:       this.formData.mother_name,
                surname:    this.formData.mother_surname,
                patronymic: this.formData.mother_patronymic || '',
                sex:        'Ж',
                date:       null,
                estate:     this.formData.father_estate_id ? Number(this.formData.father_estate_id) : null,
                creed:      this.formData.creed_id         ? Number(this.formData.creed_id)         : null,
                province:   null, yezd: null, volost: null, village: null,
                duplicate:  0,
                comment:    `Мать из записи о рождении #${this.formData.number_record}, статус: ${this.formData.mother_status}`,
              })
            })
            motherPersonId = motherPerson.person_id
          } catch (err) { console.error('Ошибка создания матери:', err) }
        }

        // ── 3. Создаём ребёнка ────────────────────────────────────
        const childPerson = await api('/api/persons/', {
          method: 'POST', headers: H,
          body: JSON.stringify({
            name:       this.formData.name,
            surname:    this.formData.child_surname || this.formData.father_surname || '',
            patronymic: this.formData.child_patronymic || '',
            sex:        this.formData.sex || '',
            date:       birthDate,
            estate:     this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
            creed:      this.formData.creed_id           ? Number(this.formData.creed_id)           : null,
            province:   this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
            yezd:       this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
            volost:     this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
            village:    this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
            duplicate:  0,
            comment:    this.formData.comment || '',
          })
        })

        // ── 4. Создаём запись о рождении ─────────────────────────
        const birth = await api('/api/birth-records/', {
          method: 'POST', headers: H,
          body: JSON.stringify({
            archive:        Number(archiveId),
            person:         childPerson.person_id,
            page:           this.formData.page         ? String(this.formData.page)          : '',
            page_turn:      this.formData.page_turn    || false,
            number_record:  this.formData.number_record ? String(this.formData.number_record) : '',
            sex:            this.formData.sex          || '',
            birth_month:    this.formData.birth_month  ? Number(this.formData.birth_month)   : null,
            birth_day:      this.formData.birth_day    ? Number(this.formData.birth_day)     : null,
            baptism_day:    this.formData.baptism_day  ? Number(this.formData.baptism_day)   : null,
            date_of_baptism: dateOfBaptism,
            father_name:       this.formData.father_name       || '',
            father_patronymic: this.formData.father_patronymic || '',
            father_surname:    this.formData.father_surname    || '',
            father_estate:   this.formData.father_estate_id   ? Number(this.formData.father_estate_id)   : null,
            father_province: this.formData.father_province_id ? Number(this.formData.father_province_id) : null,
            father_yezd:     this.formData.father_yezd_id     ? Number(this.formData.father_yezd_id)     : null,
            father_volost:   this.formData.father_volost_id   ? Number(this.formData.father_volost_id)   : null,
            father_village:  this.formData.father_village_id  ? Number(this.formData.father_village_id)  : null,
            mother_name:       this.formData.mother_name       || '',
            mother_patronymic: this.formData.mother_patronymic || '',
            mother_surname:    this.formData.mother_surname    || '',
            mother_status:   this.formData.mother_status || '',
            comment:         this.formData.comment      || '',
            status:          'published',
          })
        })

        // ── 5. Скан ───────────────────────────────────────────────
        if (this.scanFile) {
          try {
            await this._uploadScan('birth', birth.birth_id, this.scanFile)
          } catch (scanErr) { console.error('Ошибка загрузки скана:', scanErr) }
        }

        // ── 6. Восприемники (мужчины) ─────────────────────────────
        for (const g of this.godmen) {
          if (!g.name || !g.name.trim()) continue
          const godmanData = {
            birth:      birth.birth_id,
            name:       g.name       || '',
            patronymic: g.patronymic || '',
            surname:    g.surname    || '',
          }
          if (g.estate_id  && g.estate_id  !== '') godmanData.estate   = Number(g.estate_id)
          if (g.creed_id   && g.creed_id   !== '') godmanData.creed    = Number(g.creed_id)
          if (g.province_id && g.province_id !== '') godmanData.province = Number(g.province_id)
          if (g.yezd_id    && g.yezd_id    !== '') godmanData.yezd     = Number(g.yezd_id)
          if (g.volost_id  && g.volost_id  !== '') godmanData.volost   = Number(g.volost_id)
          if (g.village_id && g.village_id !== '') godmanData.village  = Number(g.village_id)
          await api('/api/godmen/', { method: 'POST', headers: H, body: JSON.stringify(godmanData) })
        }

        // ── 7. Восприемницы (женщины) ─────────────────────────────
        for (const g of this.godmothers) {
          if (!g.name || !g.name.trim()) continue
          const godmotherData = {
            birth:      birth.birth_id,
            name:       g.name       || '',
            patronymic: g.patronymic || '',
            surname:    g.surname    || '',
          }
          if (g.estate_id  && g.estate_id  !== '') godmotherData.estate   = Number(g.estate_id)
          if (g.creed_id   && g.creed_id   !== '') godmotherData.creed    = Number(g.creed_id)
          if (g.province_id && g.province_id !== '') godmotherData.province = Number(g.province_id)
          if (g.yezd_id    && g.yezd_id    !== '') godmotherData.yezd     = Number(g.yezd_id)
          if (g.volost_id  && g.volost_id  !== '') godmotherData.volost   = Number(g.volost_id)
          if (g.village_id && g.village_id !== '') godmotherData.village  = Number(g.village_id)
          if (g.status_id  && g.status_id  !== '') godmotherData.status   = Number(g.status_id)
          await api('/api/godmothers/', { method: 'POST', headers: H, body: JSON.stringify(godmotherData) })
        }

        // ── 8. Священнослужители ──────────────────────────────────
        for (const p of this.priests) {
          if (!p.name || !p.name.trim()) continue
          const priestData = {
            birth:   birth.birth_id,
            name:    p.name    || '',
            surname: p.surname || '',
          }
          if (p.clergy_id       && p.clergy_id       !== '') priestData.clergy        = Number(p.clergy_id)
          if (p.church_worker_id && p.church_worker_id !== '') priestData.church_worker = Number(p.church_worker_id)
          await api('/api/birth-record-priests/', { method: 'POST', headers: H, body: JSON.stringify(priestData) })
        }

        // ── 9. Удаляем черновик (если был) ────────────────────────
        if (this.currentDraftId) {
          try {
            await fetch(`${API_BASE}/api/drafts/${this.currentDraftId}/`, {
              method: 'DELETE',
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            })
          } catch (e) { console.error('Ошибка удаления черновика:', e) }
        }

        this.showPublishSuccess = true

      } catch (err) {
        console.error('Ошибка при сохранении:', err)
        this.error = 'Ошибка при сохранении: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.loading = false
      }
    },

    async ensureLocationObjects() {
      const ensure = async (search, idField, list, endpoint, idKey) => {
        if (search && search.trim() && !this.formData[idField]) {
          const existing = list.find(i => i.name.toLowerCase() === search.trim().toLowerCase())
          if (existing) {
            this.formData[idField] = existing[idKey]
          } else {
            try {
              const newItem = await api(endpoint, {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name: search.trim() })
              })
              list.push(newItem)
              this.formData[idField] = newItem[idKey]
            } catch (err) { console.error(`Ошибка создания ${endpoint}:`, err) }
          }
        }
      }
      await ensure(this.provinceSearch, 'father_province_id', this.provinces, '/api/provinces/', 'province_id')
      await ensure(this.yezdSearch,     'father_yezd_id',     this.yezds,     '/api/yezds/',     'yezd_id')
      await ensure(this.volostSearch,   'father_volost_id',   this.volosts,   '/api/volosts/',   'volost_id')
      await ensure(this.villageSearch,  'father_village_id',  this.villages,  '/api/villages/',  'village_id')
    },
  }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.birth-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  font-family: 'PT Sans', 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  color: #1a1a1a;
  background: #f0efee;
}

.form-panel {
  width: 42%;
  min-width: 400px;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #fff;
  border-right: 1px solid #d5d3cf;
}

.form-header {
  padding: 20px 24px 14px;
  border-bottom: 1px solid #d5d3cf;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
  flex-shrink: 0;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  gap: 12px;
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
  flex-shrink: 0;
}
.btn-back:hover { color: #1a1a1a; }

.status-toggle {
  display: flex;
  background: #f0efee;
  border: 1px solid #d5d3cf;
  border-radius: 8px;
  padding: 3px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
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
.toggle-btn.active { background: #fff; color: #1a1a1a; box-shadow: 0 1px 3px rgba(0,0,0,0.10); }

.toggle-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.draft-dot { background: #f59e0b; }
.pub-dot   { background: #22c55e; }

/* ── Бейдж и баннер режима редактирования ── */
.edit-mode-badge {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  background: #e0f2fe;
  border: 1px solid #7dd3fc;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #0369a1;
  white-space: nowrap;
}

.edit-mode-banner {
  background: #e0f2fe;
  border: 1px solid #7dd3fc;
  color: #0369a1;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  margin-top: 8px;
}

.page-title { font-size: 26px; font-weight: 700; letter-spacing: -.3px; color: #1a1a1a; margin-bottom: 2px; }
.page-title em { font-style: italic; }

.draft-banner { background: #fffbeb; border: 1px solid #fde68a; color: #92400e; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 8px; }
.publish-banner { background: #e8f4ea; border: 1px solid #b6ddb9; color: #2e7d42; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 8px; }
.red-star { color: #dc2626; font-size: 14px; }
.error-banner { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 6px; }

.form-body { flex: 1; overflow-y: auto; padding: 16px 24px; }
.form-body::-webkit-scrollbar { width: 6px; }
.form-body::-webkit-scrollbar-track { background: #f0efee; }
.form-body::-webkit-scrollbar-thumb { background: #c8c5c0; border-radius: 3px; }

.block { margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid #e9e7e3; }
.block:last-of-type { border-bottom: none; }
.block-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #888780; margin: 0 0 12px; }
.block-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.block-title-row .block-title { margin-bottom: 0; }

.location-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px; }
.location-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.location-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #5f5e5a; }
.location-hint { font-size: 11px; color: #aaa; transition: color .2s; }
.location-hint.hint-error { color: #a00; font-weight: 600; }

.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #444; }
.req-star { color: #dc2626; font-size: 12px; margin-left: 2px; }
.field-error { position: relative; }
.error-input { border-color: #dc2626 !important; background-color: #fef2f2 !important; }
.error-input:focus { border-color: #dc2626 !important; box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important; }
.error-message { font-size: 11px; color: #dc2626; margin-top: 2px; font-weight: 500; }

.field input, .field select, .field textarea {
  padding: 7px 10px; border: 1px solid #c8c5c0; border-radius: 6px;
  font-size: 13px; font-family: inherit; color: #1a1a1a; background: #fff;
  transition: border-color .15s, box-shadow .15s; width: 100%;
}
.field input:focus, .field select:focus, .field textarea:focus {
  outline: none; border-color: #888780; box-shadow: 0 0 0 3px rgba(136,135,128,0.12);
}
.field input.auto, .field select.auto, .combo-input.auto { background: #fffbeb !important; border-color: #fde68a !important; }
.field input.input-linked { background: #f2faf4; border-color: #b6ddb9; }
.readonly-input { background: #f0efee !important; color: #888 !important; cursor: default; }
.auto-hint { font-size: 11px; color: #b45309; margin-top: 1px; }
.field textarea { resize: vertical; min-height: 60px; }

.row { display: grid; gap: 10px; margin-bottom: 10px; }
.row.two   { grid-template-columns: 1fr 1fr; }
.row.three { grid-template-columns: 1fr 1fr 1fr; }
.full { margin-bottom: 10px; }

.checkbox-field { justify-content: flex-end; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #444; cursor: pointer; font-weight: 400 !important; padding: 7px 0; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; }

.record-number-wrapper { display: flex; align-items: center; gap: 8px; }
.record-gender-badge { display: inline-block; padding: 4px 10px; background: #f0efee; border: 1px solid #d5d3cf; border-radius: 6px; font-size: 12px; font-weight: 600; color: #5f5e5a; white-space: nowrap; min-width: 90px; text-align: center; }
.record-number-wrapper input { flex: 1; min-width: 0; }

.combobox-wrap { position: relative; }
.combo-input { width: 100%; }
.drop-list { position: absolute; top: calc(100% + 4px); left: 0; right: 0; background: #fff; border: 1px solid #c8c5c0; border-radius: 6px; z-index: 100; max-height: 200px; overflow-y: auto; list-style: none; padding: 4px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.drop-item { padding: 8px 12px; cursor: pointer; display: flex; flex-direction: column; gap: 2px; border-bottom: 1px solid #e9e7e3; }
.drop-item:last-child { border-bottom: none; }
.drop-item:hover { background: #f0efee; }
.drop-main { font-size: 13px; color: #1a1a1a; }
.drop-sub { font-size: 11px; color: #aaa; }
.drop-new { color: #5f5e5a; font-size: 13px; border-top: 1px solid #e9e7e3 !important; }

.field-with-add { display: flex; gap: 6px; align-items: stretch; }
.field-with-add select, .field-with-add input { flex: 1; min-width: 0; }
.btn-add-ref { flex-shrink: 0; width: 32px; background: #fff; border: 1px solid #c8c5c0; border-radius: 6px; color: #5f5e5a; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background .15s, border-color .15s; }
.btn-add-ref:hover:not(:disabled) { background: #e9e7e3; border-color: #888780; }
.btn-add-ref:disabled { opacity: 0.35; cursor: not-allowed; }

.priest-linked-badge { display: flex; align-items: center; gap: 6px; margin-top: 6px; padding: 5px 10px; background: #f2faf4; border: 1px solid #b6ddb9; border-radius: 6px; font-size: 12px; color: #2e7d42; }
.badge-icon { font-size: 13px; color: #2e7d42; flex-shrink: 0; }
.badge-unlink { margin-left: auto; background: none; border: none; font-size: 11px; color: #888; cursor: pointer; padding: 2px 6px; border-radius: 4px; transition: background .15s, color .15s; }
.badge-unlink:hover { background: #fef2f2; color: #a00; }

.sub-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; }
.sub-block-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.sub-block-header span { font-size: 12px; font-weight: 600; color: #888780; }
.header-actions { display: flex; gap: 8px; align-items: center; }

.btn-auto-fill { background: #fef3c7; border: 1px solid #fde68a; border-radius: 6px; padding: 4px 8px; font-size: 11px; font-weight: 500; font-family: inherit; cursor: pointer; color: #92400e; transition: all 0.15s; }
.btn-auto-fill:hover:not(:disabled) { background: #fde68a; transform: scale(1.02); }
.btn-auto-fill:disabled { opacity: 0.4; cursor: not-allowed; background: #f0efee; border-color: #c8c5c0; color: #888; }

.linked-husband-badge { display: flex; align-items: center; gap: 6px; margin-top: 12px; padding: 6px 10px; background: #e0e7ff; border: 1px solid #c7d2fe; border-radius: 6px; font-size: 12px; color: #3730a3; }

.btn-remove { background: none; border: none; cursor: pointer; font-size: 16px; color: #aaa; padding: 0 4px; line-height: 1; transition: color .15s; }
.btn-remove:hover { color: #a00; }
.btn-add-block { font-size: 12px; padding: 4px 10px; background: #fff; border: 1px solid #c8c5c0; border-radius: 6px; cursor: pointer; color: #5f5e5a; font-weight: 500; font-family: inherit; transition: all .15s; }
.btn-add-block:hover { background: #e9e7e3; border-color: #888780; }

.form-footer { display: flex; gap: 10px; padding: 14px 24px; border-top: 1px solid #d5d3cf; background: #fff; flex-shrink: 0; }
.btn-submit { flex: 1; padding: 9px 20px; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; font-family: inherit; cursor: pointer; transition: background .15s; }
.btn-submit.draft-submit:not(:disabled)   { background: #f59e0b; color: #fff; }
.btn-submit.draft-submit:hover:not(:disabled) { background: #d97706; }
.btn-submit.publish-submit:not(:disabled) { background: #1a1a1a; color: #fff; }
.btn-submit.publish-submit:hover:not(:disabled) { background: #333; }
.btn-submit.edit-submit:not(:disabled)    { background: #0369a1; color: #fff; }
.btn-submit.edit-submit:hover:not(:disabled) { background: #0284c7; }
.btn-submit:disabled { background: #ccc; color: #888; cursor: not-allowed; }

/* ══════════════ МОДАЛЬНЫЕ ОКНА ══════════════ */

.modal-overlay {
  position: fixed;
  inset: 0;
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
  box-shadow: 0 20px 35px -12px rgba(0,0,0,0.25);
  animation: fadeSlideIn 0.2s ease-out;
}

.modal.modal-ref { text-align: left; }
.modal.modal-ref h4 { font-size: 16px; font-weight: 700; margin-bottom: 14px; color: #1a1a1a; }

.modal.modal-confirm { text-align: center; }
.modal.modal-confirm h4 { font-size: 1.7rem; font-weight: 600; margin-bottom: 12px; color: #222; }

.modal-icon { font-size: 52px; margin-bottom: 12px; }
.modal-text { font-size: 1rem; line-height: 1.4; color: #4b5563; margin-bottom: 28px; }

.modal-footer { display: flex; gap: 12px; justify-content: center; margin-top: 8px; }

.btn-cancel {
  background: #f1f5f9; color: #1e293b; border: none;
  padding: 8px 22px; border-radius: 40px;
  font-size: 0.95rem; font-weight: 500; font-family: inherit;
  cursor: pointer; transition: all 0.2s ease;
}
.btn-cancel:hover { background: #e2e8f0; }

.btn-action {
  background: #1a1a1a; color: #fff; border: none;
  padding: 8px 22px; border-radius: 40px;
  font-size: 0.95rem; font-weight: 500; font-family: inherit;
  cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  transition: all 0.2s ease;
}
.btn-action:hover:not(:disabled) { background: #333; transform: translateY(-1px); }
.btn-action:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-ok {
  background: #10b981; color: #fff; border: none;
  padding: 8px 28px; border-radius: 40px;
  font-size: 0.95rem; font-weight: 500; font-family: inherit;
  cursor: pointer; box-shadow: 0 2px 6px rgba(16,185,129,0.2);
  transition: all 0.2s ease;
}
.btn-ok:hover { background: #059669; transform: translateY(-1px); }

@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(-12px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════ SUGGESTIONS ══════════════ */

.suggestion-below { margin-top: 4px; padding: 6px 10px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; font-size: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.suggestion-below-text { color: #92400e; }
.suggestion-below-value { font-weight: 600; color: #b45309; }
.suggestion-below-button { background: #f59e0b; color: white; border: none; border-radius: 6px; padding: 4px 12px; font-size: 11px; cursor: pointer; transition: background 0.2s; }
.suggestion-below-button:hover { background: #d97706; }

/* ══════════════ СКАН-ПАНЕЛЬ ══════════════ */

.scan-panel { flex: 1; display: flex; flex-direction: column; background: #2c2c2a; overflow: hidden; }
.scan-viewport { flex: 1; position: relative; overflow: hidden; cursor: grab; display: flex; align-items: center; justify-content: center; user-select: none; }
.scan-viewport.grabbing { cursor: grabbing; }
.scan-inner { will-change: transform; }
.scan-inner img { display: block; max-width: none; pointer-events: none; }
.scan-empty { text-align: center; color: #888780; }
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
.scan-status { display: flex; align-items: center; gap: 4px; margin-left: 8px; padding: 4px 8px; background: rgba(34, 197, 94, 0.2); border-radius: 6px; color: #22c55e; font-size: 11px; }
.scan-status-icon { font-size: 14px; }

@media (max-width: 900px) {
  .birth-layout { flex-direction: column; }
  .form-panel { width: 100%; max-width: 100%; height: 55vh; }
  .scan-panel { height: 45vh; }
  .row.three { grid-template-columns: 1fr 1fr; }
  .suggestion-below { flex-direction: column; align-items: stretch; text-align: center; }
  .suggestion-below-button { width: 100%; }
}
@media (max-width: 600px) {
  .row.two, .row.three { grid-template-columns: 1fr; }
  .header-top { flex-wrap: wrap; }
  .status-toggle { width: 100%; }
  .toggle-btn { flex: 1; justify-content: center; }
  .record-number-wrapper { flex-direction: column; align-items: stretch; }
  .record-gender-badge { text-align: center; }
}
</style>