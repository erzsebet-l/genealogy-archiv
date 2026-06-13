<template>
  <div class="marriage-layout">

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

          <div class="status-toggle" v-if="!isEditMode">
            <button type="button" :class="['toggle-btn', { active: formStatus === 'draft' }]" @click="switchToDraft">
              <span class="toggle-dot draft-dot"></span>
              Черновик
            </button>
            <button type="button" :class="['toggle-btn', { active: formStatus === 'published' }]" @click="switchToPublish">
              <span class="toggle-dot pub-dot"></span>
              Опубликовать
            </button>
          </div>

          <div v-if="isEditMode" class="edit-mode-badge">✏️ Редактирование записи</div>
        </div>

        <h2 class="page-title">Запись о <em>браке</em></h2>

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
                <li v-for="a in archiveDropItems" :key="a.archive_id"
                  @mousedown.prevent="selectArchive(a)" class="drop-item">
                  <span class="drop-main">{{ a.name }}</span>
                  <span class="drop-sub">{{ a.number_case }} · {{ a.year }}</span>
                </li>
                <li v-if="archiveSearch.trim() && !archiveExactMatch"
                  @mousedown.prevent="prepareNewArchive" class="drop-item drop-new">
                  ＋ Создать «{{ archiveSearch.trim() }}»
                </li>
              </ul>
            </div>
            <div v-if="autoFilledFields.archive" class="auto-hint">⚡ Автозаполнено</div>
          </div>

          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('number_case') }">
              <label>Номер дела <span class="req-star">*</span></label>
              <input type="text" v-model="formData.number_case" placeholder="Ф.160 Оп.1"
                :class="{ 'error-input': showFieldError('number_case'), auto: autoFilledFields.number_case }" />
              <div v-if="autoFilledFields.number_case" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('number_case')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('year') }">
              <label>Год <span class="req-star">*</span></label>
              <input type="number" v-model.number="formData.year" placeholder="1850" min="1000" max="2000"
                :class="{ auto: autoFilledFields.year }" />
              <div v-if="autoFilledFields.year" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('year')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('page') }">
              <label>Номер листа <span class="req-star">*</span></label>
              <input type="number" v-model.number="formData.page"
                :class="{ auto: autoFilledFields.page, 'error-input': showFieldError('page') }" placeholder="1" />
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
            <div class="field" :class="{ 'field-error': showFieldError('number_record') }">
              <label>Номер записи <span class="req-star">*</span></label>
              <div class="record-number-wrapper">
                <input type="number" v-model.number="formData.number_record"
                  :class="{ auto: autoFilledFields.number_record, 'error-input': showFieldError('number_record') }"
                  placeholder="1" />
              </div>
              <div v-if="autoFilledFields.number_record" class="auto-hint">⚡ +1 от предыдущей записи</div>
              <div v-if="showFieldError('number_record')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ДАТА ───────────── -->
        <section class="block">
          <h3 class="block-title">Дата бракосочетания</h3>
          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('marriage_month') }">
              <label>Месяц <span class="req-star">*</span></label>
              <select v-model.number="formData.marriage_month"
                :class="{ auto: autoFilledFields.marriage_month, 'error-input': showFieldError('marriage_month') }">
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
              <div v-if="autoFilledFields.marriage_month" class="auto-hint">⚡ Автозаполнено из предыдущей записи</div>
              <div v-if="showFieldError('marriage_month')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('marriage_day') }">
              <label>Число <span class="req-star">*</span></label>
              <input type="number" min="1" max="31" v-model.number="formData.marriage_day" placeholder="1"
                :class="{ 'error-input': showFieldError('marriage_day') }" />
              <div v-if="showFieldError('marriage_day')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ЖЕНИХ ───────────── -->
        <section class="block">
          <h3 class="block-title">Жених</h3>

          <div class="location-block">
            <div class="location-header">
              <span class="location-label">Место жительства</span>
              <span class="location-hint" :class="{ 'hint-error': showFieldError('husband_location') }">
                {{ showFieldError('husband_location') ? '⚠ Заполните хотя бы одно поле' : 'Заполните хотя бы одно поле' }}
              </span>
            </div>
            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="husbandProvinceSearch" @input="onHusbandProvinceInput"
                    @focus="husbandProvinceDropOpen = true" @blur="onHusbandProvinceBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="husbandProvinceDropOpen && filteredHusbandProvinces.length" class="drop-list">
                    <li v-for="p in filteredHusbandProvinces" :key="p.province_id"
                      @mousedown.prevent="selectHusbandProvince(p)" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                    <li v-if="husbandProvinceSearch.trim() && !husbandProvinceExactMatch"
                      @mousedown.prevent="createNewHusbandProvince" class="drop-item drop-new">
                      ＋ Создать «{{ husbandProvinceSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="husbandYezdSearch" @input="onHusbandYezdInput"
                    @focus="husbandYezdDropOpen = true" @blur="onHusbandYezdBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="husbandYezdDropOpen && filteredHusbandYezds.length" class="drop-list">
                    <li v-for="y in filteredHusbandYezds" :key="y.yezd_id"
                      @mousedown.prevent="selectHusbandYezd(y)" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                    <li v-if="husbandYezdSearch.trim() && !husbandYezdExactMatch"
                      @mousedown.prevent="createNewHusbandYezd" class="drop-item drop-new">
                      ＋ Создать «{{ husbandYezdSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="husbandVolostSearch" @input="onHusbandVolostInput"
                    @focus="husbandVolostDropOpen = true" @blur="onHusbandVolostBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="husbandVolostDropOpen && filteredHusbandVolosts.length" class="drop-list">
                    <li v-for="v in filteredHusbandVolosts" :key="v.volost_id"
                      @mousedown.prevent="selectHusbandVolost(v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="husbandVolostSearch.trim() && !husbandVolostExactMatch"
                      @mousedown.prevent="createNewHusbandVolost" class="drop-item drop-new">
                      ＋ Создать «{{ husbandVolostSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Село / Населённый пункт</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="husbandVillageSearch" @input="onHusbandVillageInput"
                    @focus="husbandVillageDropOpen = true" @blur="onHusbandVillageBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="husbandVillageDropOpen && filteredHusbandVillages.length" class="drop-list">
                    <li v-for="v in filteredHusbandVillages" :key="v.village_id"
                      @mousedown.prevent="selectHusbandVillage(v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="husbandVillageSearch.trim() && !husbandVillageExactMatch"
                      @mousedown.prevent="createNewHusbandVillage" class="drop-item drop-new">
                      ＋ Создать «{{ husbandVillageSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('husband_estate_id') }">
              <label>Сословие <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select v-model="formData.husband_estate_id" :class="{ 'error-input': showFieldError('husband_estate_id') }">
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('estate')" title="Добавить">＋</button>
              </div>
              <div v-if="showFieldError('husband_estate_id')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('creed_id') }">
              <label>Вероисповедание <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select v-model="formData.creed_id" :class="{ 'error-input': showFieldError('creed_id') }">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('religion')" title="Добавить">＋</button>
              </div>
              <div v-if="showFieldError('creed_id')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>

          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('husband_name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input type="text" v-model="formData.husband_name" placeholder="Иван"
                :class="{ 'error-input': showFieldError('husband_name') }" />
              <div v-if="showFieldError('husband_name')" class="error-message">Обязательно</div>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.husband_patronymic" placeholder="Иванович" />
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('husband_surname') }">
              <label>Фамилия <span class="req-star">*</span></label>
              <input type="text" v-model="formData.husband_surname" placeholder="Смирнов"
                :class="{ 'error-input': showFieldError('husband_surname') }" />
              <div v-if="showFieldError('husband_surname')" class="error-message">Обязательно</div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('husband_age') }">
              <label>Возраст жениха <span class="req-star">*</span></label>
              <div class="age-spinner">
                <button type="button" class="age-btn" @click="formData.husband_age = Math.max(0, (formData.husband_age || 0) - 1)">−</button>
                <input type="number" v-model.number="formData.husband_age" min="0" max="120" placeholder="—" class="age-input"
                  :class="{ 'error-input': showFieldError('husband_age') }" />
                <button type="button" class="age-btn" @click="formData.husband_age = Math.min(120, (formData.husband_age || 0) + 1)">+</button>
              </div>
              <div v-if="showFieldError('husband_age')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Брак жениха (по счёту)</label>
              <div class="age-spinner">
                <button type="button" class="age-btn" @click="formData.husband_number_marriage = Math.max(1, (formData.husband_number_marriage || 1) - 1)">−</button>
                <input type="number" v-model.number="formData.husband_number_marriage" min="1" max="10" placeholder="1" class="age-input" />
                <button type="button" class="age-btn" @click="formData.husband_number_marriage = Math.min(10, (formData.husband_number_marriage || 1) + 1)">+</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: НЕВЕСТА ───────────── -->
        <section class="block">
          <h3 class="block-title">Невеста</h3>

          <div class="location-block">
            <div class="location-header">
              <span class="location-label">Место жительства</span>
              <span class="location-hint" :class="{ 'hint-error': showFieldError('wife_location') }">
                {{ showFieldError('wife_location') ? '⚠ Заполните хотя бы одно поле' : 'Заполните хотя бы одно поле' }}
              </span>
            </div>
            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="wifeProvinceSearch" @input="onWifeProvinceInput"
                    @focus="wifeProvinceDropOpen = true" @blur="onWifeProvinceBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="wifeProvinceDropOpen && filteredWifeProvinces.length" class="drop-list">
                    <li v-for="p in filteredWifeProvinces" :key="p.province_id"
                      @mousedown.prevent="selectWifeProvince(p)" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                    <li v-if="wifeProvinceSearch.trim() && !wifeProvinceExactMatch"
                      @mousedown.prevent="createNewWifeProvince" class="drop-item drop-new">
                      ＋ Создать «{{ wifeProvinceSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="wifeYezdSearch" @input="onWifeYezdInput"
                    @focus="wifeYezdDropOpen = true" @blur="onWifeYezdBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="wifeYezdDropOpen && filteredWifeYezds.length" class="drop-list">
                    <li v-for="y in filteredWifeYezds" :key="y.yezd_id"
                      @mousedown.prevent="selectWifeYezd(y)" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                    <li v-if="wifeYezdSearch.trim() && !wifeYezdExactMatch"
                      @mousedown.prevent="createNewWifeYezd" class="drop-item drop-new">
                      ＋ Создать «{{ wifeYezdSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="wifeVolostSearch" @input="onWifeVolostInput"
                    @focus="wifeVolostDropOpen = true" @blur="onWifeVolostBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="wifeVolostDropOpen && filteredWifeVolosts.length" class="drop-list">
                    <li v-for="v in filteredWifeVolosts" :key="v.volost_id"
                      @mousedown.prevent="selectWifeVolost(v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="wifeVolostSearch.trim() && !wifeVolostExactMatch"
                      @mousedown.prevent="createNewWifeVolost" class="drop-item drop-new">
                      ＋ Создать «{{ wifeVolostSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Село / Населённый пункт</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="wifeVillageSearch" @input="onWifeVillageInput"
                    @focus="wifeVillageDropOpen = true" @blur="onWifeVillageBlur"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="wifeVillageDropOpen && filteredWifeVillages.length" class="drop-list">
                    <li v-for="v in filteredWifeVillages" :key="v.village_id"
                      @mousedown.prevent="selectWifeVillage(v)" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                    <li v-if="wifeVillageSearch.trim() && !wifeVillageExactMatch"
                      @mousedown.prevent="createNewWifeVillage" class="drop-item drop-new">
                      ＋ Создать «{{ wifeVillageSearch.trim() }}»
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('wife_estate_id') }">
              <label>Сословие <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select v-model="formData.wife_estate_id" :class="{ 'error-input': showFieldError('wife_estate_id') }">
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('estate')">＋</button>
              </div>
              <div v-if="showFieldError('wife_estate_id')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('wife_creed_id') }">
              <label>Вероисповедание <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select v-model="formData.wife_creed_id" :class="{ 'error-input': showFieldError('wife_creed_id') }">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('religion')">＋</button>
              </div>
              <div v-if="showFieldError('wife_creed_id')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>

          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('wife_name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input type="text" v-model="formData.wife_name" placeholder="Мария"
                :class="{ 'error-input': showFieldError('wife_name') }" />
              <div v-if="showFieldError('wife_name')" class="error-message">Обязательно</div>
            </div>
            <div class="field">
              <label>Отчество</label>
              <input type="text" v-model="formData.wife_patronymic" placeholder="Петровна" />
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('wife_surname') }">
              <label>Фамилия <span class="req-star">*</span></label>
              <input type="text" v-model="formData.wife_surname" placeholder="Смирнова"
                :class="{ 'error-input': showFieldError('wife_surname') }" />
              <div v-if="showFieldError('wife_surname')" class="error-message">Обязательно</div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('wife_age') }">
              <label>Возраст невесты <span class="req-star">*</span></label>
              <div class="age-spinner">
                <button type="button" class="age-btn" @click="formData.wife_age = Math.max(0, (formData.wife_age || 0) - 1)">−</button>
                <input type="number" v-model.number="formData.wife_age" min="0" max="120" placeholder="—" class="age-input"
                  :class="{ 'error-input': showFieldError('wife_age') }" />
                <button type="button" class="age-btn" @click="formData.wife_age = Math.min(120, (formData.wife_age || 0) + 1)">+</button>
              </div>
              <div v-if="showFieldError('wife_age')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Брак невесты (по счёту)</label>
              <div class="age-spinner">
                <button type="button" class="age-btn" @click="formData.wife_number_marriage = Math.max(1, (formData.wife_number_marriage || 1) - 1)">−</button>
                <input type="number" v-model.number="formData.wife_number_marriage" min="1" max="10" placeholder="1" class="age-input" />
                <button type="button" class="age-btn" @click="formData.wife_number_marriage = Math.min(10, (formData.wife_number_marriage || 1) + 1)">+</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ───────────── БЛОК: ПОРУЧИТЕЛИ (МУЖЧИНЫ) ───────────── -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Поручители (мужчины)</h3>
            <button type="button" class="btn-add-block" @click="addMaleGuarantor">＋ добавить</button>
          </div>

          <div v-for="(g, i) in maleGuarantors" :key="'mg'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Поручитель #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="maleGuarantors.splice(i, 1)" v-if="maleGuarantors.length > 1">✕</button>
            </div>

            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.provinceSearch"
                    @input="g.provinceDropOpen = true; g.province_id = ''"
                    @focus="g.provinceDropOpen = true" @blur="closeGodDrop(g, 'provinceDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.provinceDropOpen && filterItems(provinces, g.provinceSearch, 'province_id').length" class="drop-list">
                    <li v-for="p in filterItems(provinces, g.provinceSearch, 'province_id')" :key="p.province_id"
                      @mousedown.prevent="g.province_id = p.province_id; g.provinceSearch = p.name; g.provinceDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.yezdSearch"
                    @input="g.yezdDropOpen = true; g.yezd_id = ''"
                    @focus="g.yezdDropOpen = true" @blur="closeGodDrop(g, 'yezdDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.yezdDropOpen && filterItems(yezds, g.yezdSearch, 'yezd_id').length" class="drop-list">
                    <li v-for="y in filterItems(yezds, g.yezdSearch, 'yezd_id')" :key="y.yezd_id"
                      @mousedown.prevent="g.yezd_id = y.yezd_id; g.yezdSearch = y.name; g.yezdDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.volostSearch"
                    @input="g.volostDropOpen = true; g.volost_id = ''"
                    @focus="g.volostDropOpen = true" @blur="closeGodDrop(g, 'volostDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.volostDropOpen && filterItems(volosts, g.volostSearch, 'volost_id').length" class="drop-list">
                    <li v-for="v in filterItems(volosts, g.volostSearch, 'volost_id')" :key="v.volost_id"
                      @mousedown.prevent="g.volost_id = v.volost_id; g.volostSearch = v.name; g.volostDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Село</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.villageSearch"
                    @input="g.villageDropOpen = true; g.village_id = ''"
                    @focus="g.villageDropOpen = true" @blur="closeGodDrop(g, 'villageDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.villageDropOpen && filterItems(villages, g.villageSearch, 'village_id').length" class="drop-list">
                    <li v-for="v in filterItems(villages, g.villageSearch, 'village_id')" :key="v.village_id"
                      @mousedown.prevent="g.village_id = v.village_id; g.villageSearch = v.name; g.villageDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Сословие</label>
                <div class="field-with-add">
                  <select v-model="g.estate_id">
                    <option value="">Выберите</option>
                    <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                  </select>
                  <button type="button" class="btn-add-ref" @click="openModal('estate')">＋</button>
                </div>
              </div>
              <div class="field">
                <label>Вероисповедание</label>
                <select v-model="g.creed_id">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
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

        <!-- ───────────── БЛОК: ПОРУЧИТЕЛЬНИЦЫ (ЖЕНЩИНЫ) ───────────── -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Поручительницы (женщины)</h3>
            <button type="button" class="btn-add-block" @click="addFemaleGuarantor">＋ добавить</button>
          </div>

          <div v-for="(g, i) in femaleGuarantors" :key="'fg'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Поручительница #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="femaleGuarantors.splice(i, 1)" v-if="femaleGuarantors.length > 1">✕</button>
            </div>

            <div class="row two">
              <div class="field">
                <label>Губерния</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.provinceSearch"
                    @input="g.provinceDropOpen = true; g.province_id = ''"
                    @focus="g.provinceDropOpen = true" @blur="closeGodDrop(g, 'provinceDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.provinceDropOpen && filterItems(provinces, g.provinceSearch, 'province_id').length" class="drop-list">
                    <li v-for="p in filterItems(provinces, g.provinceSearch, 'province_id')" :key="p.province_id"
                      @mousedown.prevent="g.province_id = p.province_id; g.provinceSearch = p.name; g.provinceDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ p.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Уезд</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.yezdSearch"
                    @input="g.yezdDropOpen = true; g.yezd_id = ''"
                    @focus="g.yezdDropOpen = true" @blur="closeGodDrop(g, 'yezdDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.yezdDropOpen && filterItems(yezds, g.yezdSearch, 'yezd_id').length" class="drop-list">
                    <li v-for="y in filterItems(yezds, g.yezdSearch, 'yezd_id')" :key="y.yezd_id"
                      @mousedown.prevent="g.yezd_id = y.yezd_id; g.yezdSearch = y.name; g.yezdDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ y.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Волость</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.volostSearch"
                    @input="g.volostDropOpen = true; g.volost_id = ''"
                    @focus="g.volostDropOpen = true" @blur="closeGodDrop(g, 'volostDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.volostDropOpen && filterItems(volosts, g.volostSearch, 'volost_id').length" class="drop-list">
                    <li v-for="v in filterItems(volosts, g.volostSearch, 'volost_id')" :key="v.volost_id"
                      @mousedown.prevent="g.volost_id = v.volost_id; g.volostSearch = v.name; g.volostDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field">
                <label>Село</label>
                <div class="combobox-wrap">
                  <input type="text" v-model="g.villageSearch"
                    @input="g.villageDropOpen = true; g.village_id = ''"
                    @focus="g.villageDropOpen = true" @blur="closeGodDrop(g, 'villageDropOpen')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="g.villageDropOpen && filterItems(villages, g.villageSearch, 'village_id').length" class="drop-list">
                    <li v-for="v in filterItems(villages, g.villageSearch, 'village_id')" :key="v.village_id"
                      @mousedown.prevent="g.village_id = v.village_id; g.villageSearch = v.name; g.villageDropOpen = false" class="drop-item">
                      <span class="drop-main">{{ v.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Сословие</label>
                <div class="field-with-add">
                  <select v-model="g.estate_id">
                    <option value="">Выберите</option>
                    <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                  </select>
                  <button type="button" class="btn-add-ref" @click="openModal('estate')">＋</button>
                </div>
              </div>
              <div class="field">
                <label>Вероисповедание</label>
                <select v-model="g.creed_id">
                  <option value="">Выберите</option>
                  <option v-for="r in religions" :key="r.creed_id" :value="r.creed_id">{{ r.name }}</option>
                </select>
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
                <input type="text" v-model="p.searchText" @input="onPriestSearch(i)"
                  @focus="p.dropOpen = true" @blur="closePriestDrop(i)"
                  placeholder="Фамилия или имя — начните вводить..."
                  autocomplete="off" class="combo-input" :class="{ 'input-linked': p.church_worker_id }" />
                <ul v-show="p.dropOpen && p.dropItems.length > 0" class="drop-list">
                  <li v-for="cw in p.dropItems" :key="cw.pries_id"
                    @mousedown.prevent="selectChurchWorker(i, cw)" class="drop-item">
                    <span class="drop-main">{{ cw.surname }} {{ cw.name }}</span>
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
                <label>Имя <span class="req-star">*</span></label>
                <input type="text" v-model="p.name" placeholder="Имя"
                  :readonly="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }" />
              </div>
              <div class="field">
                <label>Фамилия <span class="req-star">*</span></label>
                <input type="text" v-model="p.surname" placeholder="Фамилия"
                  :readonly="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }" />
              </div>
            </div>

            <div class="field full">
              <label>Степень духовенства</label>
              <div class="field-with-add">
                <select v-model="p.clergy_id" :disabled="!!p.church_worker_id" :class="{ 'readonly-input': !!p.church_worker_id }">
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
          <button type="submit" class="btn-submit" :disabled="loading"
            :class="formStatus === 'draft' ? 'draft-submit' : (isEditMode ? 'edit-submit' : 'publish-submit')">
            {{ submitButtonLabel }}
          </button>
        </div>

      </form>
    </div>

    <!-- ══════════════ ПРАВАЯ ПАНЕЛЬ — СКАН ══════════════ -->
    <div class="scan-panel">
      <div class="scan-viewport" ref="scanViewport"
        @mousedown="startDrag" @wheel.prevent="onWheel"
        :class="{ grabbing: isDragging }">
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

    <!-- ══════════════ МОДАЛЬНЫЕ ОКНА ══════════════ -->
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

    <div v-if="modal.type === 'wife_status'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить статус</h4>
        <div class="field">
          <label>Название</label>
          <input type="text" v-model="modal.value" placeholder="Например: девица" @keyup.enter="saveRef" autofocus />
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

    <!-- Подтверждение публикации -->
    <div v-if="showPublishConfirm" class="modal-overlay" @click.self="showPublishConfirm = false">
      <div class="modal modal-confirm">
        <div class="modal-icon">📢</div>
        <h4>Опубликовать запись?</h4>
        <p class="modal-text">Запись будет сохранена в основную базу данных. Убедитесь, что все данные проверены.</p>
        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="showPublishConfirm = false">Отмена</button>
          <button type="button" class="btn-action" @click="confirmPublish" :disabled="loading">
            {{ loading ? 'Публикация...' : 'Да, опубликовать' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Успех: черновик -->
    <div v-if="showDraftSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Черновик сохранён</h4>
        <p class="modal-text">Черновик успешно сохранён.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="showDraftSuccess = false; $router.push('/home')">OK</button>
        </div>
      </div>
    </div>

    <!-- Успех: публикация -->
    <div v-if="showPublishSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Запись опубликована</h4>
        <p class="modal-text">Запись о браке успешно опубликована и добавлена в основную базу данных.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="showPublishSuccess = false; $router.push('/home')">OK</button>
        </div>
      </div>
    </div>

    <!-- Успех: редактирование -->
    <div v-if="showEditSuccess" class="modal-overlay">
      <div class="modal modal-confirm">
        <div class="modal-icon">✅</div>
        <h4>Изменения сохранены</h4>
        <p class="modal-text">Запись о браке и данные персон успешно обновлены.</p>
        <div class="modal-footer">
          <button type="button" class="btn-ok" @click="showEditSuccess = false; $router.push('/home')">OK</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { api, authHeaders, API_BASE } from '@/utils/api.js'

export default {
  name: 'Marriage',

  data() {
    return {
      loading: false,
      error: null,
      formStatus: 'published',
      showPublishConfirm: false,
      showDraftSuccess: false,
      showPublishSuccess: false,
      showEditSuccess: false,
      showPublishAttempt: false,
      missingFieldsList: [],
      currentDraftId: null,
      editingRecordId: null,
      existingPersonIds: {
        husband: null,
        wife: null
      },

      autoFilledFields: {
        archive: false,
        number_case: false,
        year: false,
        page: false,
        number_record: false,
        marriage_month: false,
      },

      archiveSearch: '',
      archiveDropOpen: false,
      allArchives: [],

      // Жених: поля для поиска/создания территорий
      husbandProvinceSearch: '',
      husbandProvinceDropOpen: false,
      husbandYezdSearch: '',
      husbandYezdDropOpen: false,
      husbandVolostSearch: '',
      husbandVolostDropOpen: false,
      husbandVillageSearch: '',
      husbandVillageDropOpen: false,

      // Невеста: поля для поиска/создания территорий
      wifeProvinceSearch: '',
      wifeProvinceDropOpen: false,
      wifeYezdSearch: '',
      wifeYezdDropOpen: false,
      wifeVolostSearch: '',
      wifeVolostDropOpen: false,
      wifeVillageSearch: '',
      wifeVillageDropOpen: false,

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

      formData: {
        archive_id: null,
        number_case: '',
        year: '',
        page: '',
        page_turn: false,
        number_record: '',
        marriage_month: '',
        marriage_day: '',
        husband_name: '',
        husband_patronymic: '',
        husband_surname: '',
        husband_estate_id: '',
        husband_province_id: '',
        husband_yezd_id: '',
        husband_volost_id: '',
        husband_village_id: '',
        husband_age: '',
        husband_number_marriage: 1,
        wife_name: '',
        wife_patronymic: '',
        wife_surname: '',
        wife_estate_id: '',
        wife_creed_id: '',
        wife_province_id: '',
        wife_yezd_id: '',
        wife_volost_id: '',
        wife_village_id: '',
        wife_age: '',
        wife_number_marriage: 1,
        wife_status: '',
        creed_id: '',
        comment: '',
      },

      maleGuarantors: [],
      femaleGuarantors: [],
      priests: [],

      months: [
        'Январь','Февраль','Март','Апрель','Май','Июнь',
        'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'
      ]
    }
  },

  computed: {
    isEditMode() { return !!this.editingRecordId },

    submitButtonLabel() {
      if (this.loading) return 'Сохранение...'
      if (this.formStatus === 'draft') return 'Сохранить черновик'
      if (this.isEditMode) return 'Сохранить изменения'
      return 'Опубликовать запись'
    },

    archiveDropItems() {
      const q = this.archiveSearch.toLowerCase().trim()
      if (!q) return this.allArchives
      return this.allArchives.filter(a =>
        a.name.toLowerCase().includes(q) ||
        (a.number_case || '').toLowerCase().includes(q)
      )
    },

    archiveExactMatch() {
      return this.allArchives.some(a => a.name.toLowerCase() === this.archiveSearch.toLowerCase().trim())
    },

    // Жених: computed для фильтрации
    filteredHusbandProvinces() {
      return this.filterItems(this.provinces, this.husbandProvinceSearch, 'province_id')
    },
    husbandProvinceExactMatch() {
      return this.provinces.some(p => p.name.toLowerCase() === this.husbandProvinceSearch.toLowerCase().trim())
    },
    filteredHusbandYezds() {
      return this.filterItems(this.yezds, this.husbandYezdSearch, 'yezd_id')
    },
    husbandYezdExactMatch() {
      return this.yezds.some(y => y.name.toLowerCase() === this.husbandYezdSearch.toLowerCase().trim())
    },
    filteredHusbandVolosts() {
      return this.filterItems(this.volosts, this.husbandVolostSearch, 'volost_id')
    },
    husbandVolostExactMatch() {
      return this.volosts.some(v => v.name.toLowerCase() === this.husbandVolostSearch.toLowerCase().trim())
    },
    filteredHusbandVillages() {
      return this.filterItems(this.villages, this.husbandVillageSearch, 'village_id')
    },
    husbandVillageExactMatch() {
      return this.villages.some(v => v.name.toLowerCase() === this.husbandVillageSearch.toLowerCase().trim())
    },

    // Невеста: computed для фильтрации
    filteredWifeProvinces() {
      return this.filterItems(this.provinces, this.wifeProvinceSearch, 'province_id')
    },
    wifeProvinceExactMatch() {
      return this.provinces.some(p => p.name.toLowerCase() === this.wifeProvinceSearch.toLowerCase().trim())
    },
    filteredWifeYezds() {
      return this.filterItems(this.yezds, this.wifeYezdSearch, 'yezd_id')
    },
    wifeYezdExactMatch() {
      return this.yezds.some(y => y.name.toLowerCase() === this.wifeYezdSearch.toLowerCase().trim())
    },
    filteredWifeVolosts() {
      return this.filterItems(this.volosts, this.wifeVolostSearch, 'volost_id')
    },
    wifeVolostExactMatch() {
      return this.volosts.some(v => v.name.toLowerCase() === this.wifeVolostSearch.toLowerCase().trim())
    },
    filteredWifeVillages() {
      return this.filterItems(this.villages, this.wifeVillageSearch, 'village_id')
    },
    wifeVillageExactMatch() {
      return this.villages.some(v => v.name.toLowerCase() === this.wifeVillageSearch.toLowerCase().trim())
    },

    scanTransformStyle() {
      return {
        position: 'absolute',
        transformOrigin: 'center center',
        transform: `translate(${this.panX}px, ${this.panY}px) scale(${this.zoom})`,
        transition: this.isDragging ? 'none' : 'transform 0.08s ease'
      }
    },
  },

  async mounted() {
    this.maleGuarantors   = [this.emptyGuarantor()]
    this.femaleGuarantors = [this.emptyGuarantor()]
    this.priests          = [this.emptyPriest()]

    await this.loadReferenceData()

    const editRecordData = localStorage.getItem('edit_record')
    if (editRecordData) {
      try {
        const editData = JSON.parse(editRecordData)
        if (editData.isEditing && editData.recordId && editData.recordType === 'marriage') {
          await this.loadRecordForEditing(editData.recordId)
          localStorage.removeItem('edit_record')
        }
      } catch (e) { console.error('Ошибка загрузки данных редактирования:', e) }
    }

    const raw = localStorage.getItem('marriage_draft')
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
        localStorage.removeItem('marriage_draft')
      } catch (e) {
        console.error('Ошибка загрузки черновика:', e)
      }
    }
  },

  beforeUnmount() {
    document.removeEventListener('mousemove', this._onMouseMove)
    document.removeEventListener('mouseup', this._onMouseUp)
  },

  methods: {
    emptyGuarantor() {
      return {
        name: '', patronymic: '', surname: '',
        estate_id: '', creed_id: '',
        village_id: '', province_id: '', yezd_id: '', volost_id: '',
        provinceSearch: '', yezdSearch: '', volostSearch: '', villageSearch: '',
        provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false,
        guarantor_id: null,
      }
    },

    emptyPriest() {
      return {
        searchText: '', dropOpen: false, dropItems: [],
        church_worker_id: null, name: '', surname: '', clergy_id: '',
        priest_record_id: null,
      }
    },

    filterItems(list, search, idKey) {
      const q = (search || '').toLowerCase().trim()
      if (!q) return list
      return list.filter(item => item.name.toLowerCase().includes(q))
    },

    loadDraftData(draftData) {
      if (draftData.formData) {
        Object.assign(this.formData, draftData.formData)
      }
      if (draftData.archiveSearch) this.archiveSearch = draftData.archiveSearch
      if (draftData.husbandProvinceSearch !== undefined) this.husbandProvinceSearch = draftData.husbandProvinceSearch || ''
      if (draftData.husbandYezdSearch !== undefined) this.husbandYezdSearch = draftData.husbandYezdSearch || ''
      if (draftData.husbandVolostSearch !== undefined) this.husbandVolostSearch = draftData.husbandVolostSearch || ''
      if (draftData.husbandVillageSearch !== undefined) this.husbandVillageSearch = draftData.husbandVillageSearch || ''
      if (draftData.wifeProvinceSearch !== undefined) this.wifeProvinceSearch = draftData.wifeProvinceSearch || ''
      if (draftData.wifeYezdSearch !== undefined) this.wifeYezdSearch = draftData.wifeYezdSearch || ''
      if (draftData.wifeVolostSearch !== undefined) this.wifeVolostSearch = draftData.wifeVolostSearch || ''
      if (draftData.wifeVillageSearch !== undefined) this.wifeVillageSearch = draftData.wifeVillageSearch || ''
      if (draftData.scanSrc) this.scanSrc = draftData.scanSrc
      if (draftData.maleGuarantors?.length) {
        this.maleGuarantors = draftData.maleGuarantors.map(g => ({
          ...this.emptyGuarantor(), ...g,
          provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false
        }))
      }
      if (draftData.femaleGuarantors?.length) {
        this.femaleGuarantors = draftData.femaleGuarantors.map(g => ({
          ...this.emptyGuarantor(), ...g,
          provinceDropOpen: false, yezdDropOpen: false, volostDropOpen: false, villageDropOpen: false
        }))
      }
      if (draftData.priests?.length) {
        this.priests = draftData.priests.map(p => ({
          ...this.emptyPriest(), ...p,
          dropOpen: false, dropItems: []
        }))
      }
    },

    async loadReferenceData() {
      this.loading = true
      try {
        const h = authHeaders()
        const [archives, estates, religions, villages, provinces, yezds, volosts, churchWorkers, motherStatuses, clergyList] =
          await Promise.all([
            api('/api/archives/', { headers: h }),
            api('/api/estates/', { headers: h }),
            api('/api/religions/', { headers: h }),
            api('/api/villages/', { headers: h }),
            api('/api/provinces/', { headers: h }),
            api('/api/yezds/', { headers: h }),
            api('/api/volosts/', { headers: h }),
            api('/api/church-workers/', { headers: h }),
            api('/api/status-choices/', { headers: h }),
            api('/api/clergy/', { headers: h }),
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

    // ══════════════════════════════════════════════════════════════
    // АРХИВ
    // ══════════════════════════════════════════════════════════════
    onArchiveInput() {
      this.archiveDropOpen = true
      this.formData.archive_id = null
      this.formData.number_case = ''
      this.formData.year = ''
      this.formData.number_record = ''
      this.autoFilledFields = { 
        archive: false, 
        number_case: false, 
        year: false, 
        page: false, 
        number_record: false, 
        marriage_month: false 
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
      this.autoFilledFields.year        = true
      this.autoFilledFields.archive     = true
      this.archiveDropOpen              = false

      try {
        const lastRecord = await api(`/api/marriage-records/last/?archive_id=${archive.archive_id}`, { headers: authHeaders() }).catch(() => null)
        if (lastRecord && lastRecord.number_record) {
          this.formData.number_record = lastRecord.number_record + 1
          this.autoFilledFields.number_record = true
        }
        if (lastRecord && lastRecord.marriage_month) {
          this.formData.marriage_month = lastRecord.marriage_month
          this.autoFilledFields.marriage_month = true
        }
        if (lastRecord && lastRecord.marriage_day) {
          this.formData.marriage_day = lastRecord.marriage_day
        }
      } catch (_) {}
    },

    prepareNewArchive() {
      this.formData.archive_id  = null
      this.archiveDropOpen      = false
      this.formData.number_case = ''
      this.formData.year        = ''
      this.autoFilledFields.number_case = false
      this.autoFilledFields.year        = false
      this.autoFilledFields.archive     = false
    },

    // ══════════════════════════════════════════════════════════════
    // ТЕРРИТОРИАЛЬНЫЕ ЕДИНИЦЫ — ЖЕНИХ
    // ══════════════════════════════════════════════════════════════
    onHusbandProvinceInput() {
      this.formData.husband_province_id = null
      this.husbandProvinceDropOpen = true
      this.clearHusbandLocationError()
    },

    async onHusbandProvinceBlur() {
      setTimeout(async () => {
        this.husbandProvinceDropOpen = false
        const name = this.husbandProvinceSearch.trim()
        if (name && !this.formData.husband_province_id) {
          const existing = this.provinces.find(p => p.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.husband_province_id = existing.province_id
            this.husbandProvinceSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/provinces/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.provinces.push(newItem)
              this.formData.husband_province_id = newItem.province_id
              this.husbandProvinceSearch = newItem.name
            } catch (err) { console.error('Ошибка создания губернии:', err) }
          }
          this.clearHusbandLocationError()
        }
      }, 200)
    },

    selectHusbandProvince(item) {
      this.formData.husband_province_id = item.province_id
      this.husbandProvinceSearch = item.name
      this.husbandProvinceDropOpen = false
      this.clearHusbandLocationError()
    },

    async createNewHusbandProvince() {
      const name = this.husbandProvinceSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/provinces/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.provinces.push(newItem)
        this.formData.husband_province_id = newItem.province_id
        this.husbandProvinceSearch = newItem.name
        this.husbandProvinceDropOpen = false
        this.clearHusbandLocationError()
      } catch (err) { console.error('Ошибка создания губернии:', err) }
    },

    onHusbandYezdInput() {
      this.formData.husband_yezd_id = null
      this.husbandYezdDropOpen = true
      this.clearHusbandLocationError()
    },

    async onHusbandYezdBlur() {
      setTimeout(async () => {
        this.husbandYezdDropOpen = false
        const name = this.husbandYezdSearch.trim()
        if (name && !this.formData.husband_yezd_id) {
          const existing = this.yezds.find(y => y.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.husband_yezd_id = existing.yezd_id
            this.husbandYezdSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/yezds/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.yezds.push(newItem)
              this.formData.husband_yezd_id = newItem.yezd_id
              this.husbandYezdSearch = newItem.name
            } catch (err) { console.error('Ошибка создания уезда:', err) }
          }
          this.clearHusbandLocationError()
        }
      }, 200)
    },

    selectHusbandYezd(item) {
      this.formData.husband_yezd_id = item.yezd_id
      this.husbandYezdSearch = item.name
      this.husbandYezdDropOpen = false
      this.clearHusbandLocationError()
    },

    async createNewHusbandYezd() {
      const name = this.husbandYezdSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/yezds/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.yezds.push(newItem)
        this.formData.husband_yezd_id = newItem.yezd_id
        this.husbandYezdSearch = newItem.name
        this.husbandYezdDropOpen = false
        this.clearHusbandLocationError()
      } catch (err) { console.error('Ошибка создания уезда:', err) }
    },

    onHusbandVolostInput() {
      this.formData.husband_volost_id = null
      this.husbandVolostDropOpen = true
      this.clearHusbandLocationError()
    },

    async onHusbandVolostBlur() {
      setTimeout(async () => {
        this.husbandVolostDropOpen = false
        const name = this.husbandVolostSearch.trim()
        if (name && !this.formData.husband_volost_id) {
          const existing = this.volosts.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.husband_volost_id = existing.volost_id
            this.husbandVolostSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/volosts/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.volosts.push(newItem)
              this.formData.husband_volost_id = newItem.volost_id
              this.husbandVolostSearch = newItem.name
            } catch (err) { console.error('Ошибка создания волости:', err) }
          }
          this.clearHusbandLocationError()
        }
      }, 200)
    },

    selectHusbandVolost(item) {
      this.formData.husband_volost_id = item.volost_id
      this.husbandVolostSearch = item.name
      this.husbandVolostDropOpen = false
      this.clearHusbandLocationError()
    },

    async createNewHusbandVolost() {
      const name = this.husbandVolostSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/volosts/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.volosts.push(newItem)
        this.formData.husband_volost_id = newItem.volost_id
        this.husbandVolostSearch = newItem.name
        this.husbandVolostDropOpen = false
        this.clearHusbandLocationError()
      } catch (err) { console.error('Ошибка создания волости:', err) }
    },

    onHusbandVillageInput() {
      this.formData.husband_village_id = null
      this.husbandVillageDropOpen = true
      this.clearHusbandLocationError()
    },

    async onHusbandVillageBlur() {
      setTimeout(async () => {
        this.husbandVillageDropOpen = false
        const name = this.husbandVillageSearch.trim()
        if (name && !this.formData.husband_village_id) {
          const existing = this.villages.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.husband_village_id = existing.village_id
            this.husbandVillageSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/villages/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.villages.push(newItem)
              this.formData.husband_village_id = newItem.village_id
              this.husbandVillageSearch = newItem.name
            } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
          }
          this.clearHusbandLocationError()
        }
      }, 200)
    },

    selectHusbandVillage(item) {
      this.formData.husband_village_id = item.village_id
      this.husbandVillageSearch = item.name
      this.husbandVillageDropOpen = false
      this.clearHusbandLocationError()
    },

    async createNewHusbandVillage() {
      const name = this.husbandVillageSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/villages/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.villages.push(newItem)
        this.formData.husband_village_id = newItem.village_id
        this.husbandVillageSearch = newItem.name
        this.husbandVillageDropOpen = false
        this.clearHusbandLocationError()
      } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
    },

    clearHusbandLocationError() {
      if (this.missingFieldsList.includes('husband_location')) {
        const index = this.missingFieldsList.indexOf('husband_location')
        this.missingFieldsList.splice(index, 1)
      }
    },

    // ══════════════════════════════════════════════════════════════
    // ТЕРРИТОРИАЛЬНЫЕ ЕДИНИЦЫ — НЕВЕСТА
    // ══════════════════════════════════════════════════════════════
    onWifeProvinceInput() {
      this.formData.wife_province_id = null
      this.wifeProvinceDropOpen = true
      this.clearWifeLocationError()
    },

    async onWifeProvinceBlur() {
      setTimeout(async () => {
        this.wifeProvinceDropOpen = false
        const name = this.wifeProvinceSearch.trim()
        if (name && !this.formData.wife_province_id) {
          const existing = this.provinces.find(p => p.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.wife_province_id = existing.province_id
            this.wifeProvinceSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/provinces/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.provinces.push(newItem)
              this.formData.wife_province_id = newItem.province_id
              this.wifeProvinceSearch = newItem.name
            } catch (err) { console.error('Ошибка создания губернии:', err) }
          }
          this.clearWifeLocationError()
        }
      }, 200)
    },

    selectWifeProvince(item) {
      this.formData.wife_province_id = item.province_id
      this.wifeProvinceSearch = item.name
      this.wifeProvinceDropOpen = false
      this.clearWifeLocationError()
    },

    async createNewWifeProvince() {
      const name = this.wifeProvinceSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/provinces/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.provinces.push(newItem)
        this.formData.wife_province_id = newItem.province_id
        this.wifeProvinceSearch = newItem.name
        this.wifeProvinceDropOpen = false
        this.clearWifeLocationError()
      } catch (err) { console.error('Ошибка создания губернии:', err) }
    },

    onWifeYezdInput() {
      this.formData.wife_yezd_id = null
      this.wifeYezdDropOpen = true
      this.clearWifeLocationError()
    },

    async onWifeYezdBlur() {
      setTimeout(async () => {
        this.wifeYezdDropOpen = false
        const name = this.wifeYezdSearch.trim()
        if (name && !this.formData.wife_yezd_id) {
          const existing = this.yezds.find(y => y.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.wife_yezd_id = existing.yezd_id
            this.wifeYezdSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/yezds/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.yezds.push(newItem)
              this.formData.wife_yezd_id = newItem.yezd_id
              this.wifeYezdSearch = newItem.name
            } catch (err) { console.error('Ошибка создания уезда:', err) }
          }
          this.clearWifeLocationError()
        }
      }, 200)
    },

    selectWifeYezd(item) {
      this.formData.wife_yezd_id = item.yezd_id
      this.wifeYezdSearch = item.name
      this.wifeYezdDropOpen = false
      this.clearWifeLocationError()
    },

    async createNewWifeYezd() {
      const name = this.wifeYezdSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/yezds/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.yezds.push(newItem)
        this.formData.wife_yezd_id = newItem.yezd_id
        this.wifeYezdSearch = newItem.name
        this.wifeYezdDropOpen = false
        this.clearWifeLocationError()
      } catch (err) { console.error('Ошибка создания уезда:', err) }
    },

    onWifeVolostInput() {
      this.formData.wife_volost_id = null
      this.wifeVolostDropOpen = true
      this.clearWifeLocationError()
    },

    async onWifeVolostBlur() {
      setTimeout(async () => {
        this.wifeVolostDropOpen = false
        const name = this.wifeVolostSearch.trim()
        if (name && !this.formData.wife_volost_id) {
          const existing = this.volosts.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.wife_volost_id = existing.volost_id
            this.wifeVolostSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/volosts/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.volosts.push(newItem)
              this.formData.wife_volost_id = newItem.volost_id
              this.wifeVolostSearch = newItem.name
            } catch (err) { console.error('Ошибка создания волости:', err) }
          }
          this.clearWifeLocationError()
        }
      }, 200)
    },

    selectWifeVolost(item) {
      this.formData.wife_volost_id = item.volost_id
      this.wifeVolostSearch = item.name
      this.wifeVolostDropOpen = false
      this.clearWifeLocationError()
    },

    async createNewWifeVolost() {
      const name = this.wifeVolostSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/volosts/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.volosts.push(newItem)
        this.formData.wife_volost_id = newItem.volost_id
        this.wifeVolostSearch = newItem.name
        this.wifeVolostDropOpen = false
        this.clearWifeLocationError()
      } catch (err) { console.error('Ошибка создания волости:', err) }
    },

    onWifeVillageInput() {
      this.formData.wife_village_id = null
      this.wifeVillageDropOpen = true
      this.clearWifeLocationError()
    },

    async onWifeVillageBlur() {
      setTimeout(async () => {
        this.wifeVillageDropOpen = false
        const name = this.wifeVillageSearch.trim()
        if (name && !this.formData.wife_village_id) {
          const existing = this.villages.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.wife_village_id = existing.village_id
            this.wifeVillageSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/villages/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
              this.villages.push(newItem)
              this.formData.wife_village_id = newItem.village_id
              this.wifeVillageSearch = newItem.name
            } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
          }
          this.clearWifeLocationError()
        }
      }, 200)
    },

    selectWifeVillage(item) {
      this.formData.wife_village_id = item.village_id
      this.wifeVillageSearch = item.name
      this.wifeVillageDropOpen = false
      this.clearWifeLocationError()
    },

    async createNewWifeVillage() {
      const name = this.wifeVillageSearch.trim()
      if (!name) return
      try {
        const newItem = await api('/api/villages/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name }) })
        this.villages.push(newItem)
        this.formData.wife_village_id = newItem.village_id
        this.wifeVillageSearch = newItem.name
        this.wifeVillageDropOpen = false
        this.clearWifeLocationError()
      } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
    },

    clearWifeLocationError() {
      if (this.missingFieldsList.includes('wife_location')) {
        const index = this.missingFieldsList.indexOf('wife_location')
        this.missingFieldsList.splice(index, 1)
      }
    },

    // ══════════════════════════════════════════════════════════════
    // ПОРУЧИТЕЛИ (без авто-заполнения)
    // ══════════════════════════════════════════════════════════════
    addMaleGuarantor()   { this.maleGuarantors.push(this.emptyGuarantor()) },
    addFemaleGuarantor() { this.femaleGuarantors.push(this.emptyGuarantor()) },
    addPriest()          { this.priests.push(this.emptyPriest()) },

    closeGodDrop(g, field) {
      setTimeout(() => { g[field] = false }, 200)
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
      p.searchText       = `${cw.surname} ${cw.name}`
      p.dropOpen         = false
      p.dropItems        = []
    },

    unlinkChurchWorker(i) {
      const p = this.priests[i]
      p.church_worker_id = null
      p.name = ''
      p.surname = ''
      p.clergy_id = ''
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
        }
        if (type === 'religion') {
          result = await api('/api/religions/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.religions.push(result)
        }
        if (type === 'wife_status') {
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
      } catch (err) { alert('Ошибка сохранения: ' + err.message) }
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
      this._onMouseMove = (ev) => { this.panX = ev.clientX - this._dragStartX; this.panY = ev.clientY - this._dragStartY }
      this._onMouseUp   = ()   => { this.isDragging = false; document.removeEventListener('mousemove', this._onMouseMove); document.removeEventListener('mouseup', this._onMouseUp) }
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

    checkHusbandLocation() {
      return !!(this.formData.husband_province_id || this.formData.husband_yezd_id || this.formData.husband_volost_id || this.formData.husband_village_id || this.husbandProvinceSearch.trim() || this.husbandYezdSearch.trim() || this.husbandVolostSearch.trim() || this.husbandVillageSearch.trim())
    },

    checkWifeLocation() {
      return !!(this.formData.wife_province_id || this.formData.wife_yezd_id || this.formData.wife_volost_id || this.formData.wife_village_id || this.wifeProvinceSearch.trim() || this.wifeYezdSearch.trim() || this.wifeVolostSearch.trim() || this.wifeVillageSearch.trim())
    },

    showFieldError(fieldName) {
      if (this.formStatus !== 'published') return false
      if (!this.showPublishAttempt) return false
      return this.missingFieldsList.includes(fieldName)
    },

    validateAllFields() {
      const required = [
        'number_case', 'year', 'page', 'number_record', 
        'marriage_month', 'marriage_day', 
        'husband_name', 'husband_surname', 'husband_age', 'husband_estate_id',
        'wife_name', 'wife_surname', 'wife_age', 'wife_estate_id', 'wife_creed_id',
        'creed_id'
      ]
      const missing = []
      for (const f of required) {
        const v = this.formData[f]
        if (v === null || v === undefined || v === '' || v === 0) {
          if (f === 'number_case' && this.formData.archive_id) continue
          if (f === 'year' && this.formData.archive_id) continue
          missing.push(f)
        }
      }
      if (!this.checkHusbandLocation()) missing.push('husband_location')
      if (!this.checkWifeLocation()) missing.push('wife_location')
      this.missingFieldsList = missing
      this.showPublishAttempt = true
      if (missing.length > 0) {
        this.error = `Необходимо заполнить ${missing.length} обязательное(ых) поле(й)`
        setTimeout(() => { const el = document.querySelector('.field-error'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' }) }, 100)
      } else {
        this.error = null
      }
      return missing.length === 0
    },

    switchToDraft()   { this.formStatus = 'draft'; this.showPublishAttempt = false; this.missingFieldsList = []; this.error = null },
    switchToPublish() { this.formStatus = 'published' },

    async handleSubmit() {
      if (this.formStatus === 'draft') { await this.saveServerDraft(); return }
      const isValid = this.validateAllFields()
      if (!isValid) return
      if (this.isEditMode) { await this.saveEditedRecord() }
      else { this.showPublishConfirm = true }
    },

    async confirmPublish() {
      this.showPublishConfirm = false
      await this.saveMarriageRecord()
    },

    async saveServerDraft() {
      this.error = null; this.loading = true
      try {
        const payload = {
          formData: { ...this.formData },
          archiveSearch: this.archiveSearch,
          husbandProvinceSearch: this.husbandProvinceSearch,
          husbandYezdSearch: this.husbandYezdSearch,
          husbandVolostSearch: this.husbandVolostSearch,
          husbandVillageSearch: this.husbandVillageSearch,
          wifeProvinceSearch: this.wifeProvinceSearch,
          wifeYezdSearch: this.wifeYezdSearch,
          wifeVolostSearch: this.wifeVolostSearch,
          wifeVillageSearch: this.wifeVillageSearch,
          maleGuarantors: this.maleGuarantors.map(g => ({ ...g, dropOpen: false, dropItems: [] })),
          femaleGuarantors: this.femaleGuarantors.map(g => ({ ...g, dropOpen: false, dropItems: [] })),
          priests: this.priests.map(p => ({ ...p, dropOpen: false, dropItems: [] }))
        }
        if (this.scanSrc) payload.scanSrc = this.scanSrc
        let url = '/api/drafts/'; let method = 'POST'
        if (this.currentDraftId) { url = `/api/drafts/${this.currentDraftId}/`; method = 'PUT' }
        const result = await api(url, { method, headers: authHeaders(true), body: JSON.stringify({ record_type: 'marriage', payload }) })
        if (result && result.draft_id) this.currentDraftId = result.draft_id
        this.showDraftSuccess = true
      } catch (err) { this.error = 'Ошибка сохранения черновика: ' + err.message; window.scrollTo({ top: 0, behavior: 'smooth' }) }
      finally { this.loading = false }
    },

    _uploadScan(recordType, recordId, file) {
      const fd = new FormData(); fd.append('scan', file)
      return fetch(`${API_BASE}/api/${recordType}-records/${recordId}/upload_scan/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        body: fd,
      })
    },

    async saveMarriageRecord() {
      this.error = null; this.loading = true
      try {
        const H = authHeaders(true)
        const marriageDate = this.formatDateForApi(this.formData.year, this.formData.marriage_month, this.formData.marriage_day)

        let archiveId = this.formData.archive_id
        if (!archiveId && this.archiveSearch.trim()) {
          const newArchive = await api('/api/archives/', { method: 'POST', headers: H, body: JSON.stringify({ name: this.archiveSearch.trim(), number_case: this.formData.number_case, year: this.formData.year }) })
          archiveId = newArchive.archive_id
        }
        if (!archiveId) throw new Error('Необходимо указать архив')

        let husbandPersonId = null
        if (this.formData.husband_name && this.formData.husband_surname) {
          const husbandPerson = await api('/api/persons/', { method: 'POST', headers: H, body: JSON.stringify({
            name: this.formData.husband_name,
            surname: this.formData.husband_surname,
            patronymic: this.formData.husband_patronymic || '',
            sex: 'М',
            estate: this.formData.husband_estate_id ? Number(this.formData.husband_estate_id) : null,
            creed: this.formData.creed_id ? Number(this.formData.creed_id) : null,
            province: this.formData.husband_province_id ? Number(this.formData.husband_province_id) : null,
            yezd: this.formData.husband_yezd_id ? Number(this.formData.husband_yezd_id) : null,
            volost: this.formData.husband_volost_id ? Number(this.formData.husband_volost_id) : null,
            village: this.formData.husband_village_id ? Number(this.formData.husband_village_id) : null,
            duplicate: 0,
            comment: `Жених из записи о браке #${this.formData.number_record}`
          }) })
          husbandPersonId = husbandPerson.person_id
        }

        let wifePersonId = null
        if (this.formData.wife_name) {
          const wifePerson = await api('/api/persons/', { method: 'POST', headers: H, body: JSON.stringify({
            name: this.formData.wife_name,
            surname: this.formData.wife_surname || 'Неизвестно',
            patronymic: this.formData.wife_patronymic || '',
            sex: 'Ж',
            estate: this.formData.wife_estate_id ? Number(this.formData.wife_estate_id) : null,
            creed: this.formData.wife_creed_id ? Number(this.formData.wife_creed_id) : this.formData.creed_id ? Number(this.formData.creed_id) : null,
            province: this.formData.wife_province_id ? Number(this.formData.wife_province_id) : null,
            yezd: this.formData.wife_yezd_id ? Number(this.formData.wife_yezd_id) : null,
            volost: this.formData.wife_volost_id ? Number(this.formData.wife_volost_id) : null,
            village: this.formData.wife_village_id ? Number(this.formData.wife_village_id) : null,
            duplicate: 0,
            comment: `Невеста из записи о браке #${this.formData.number_record}, статус: ${this.formData.wife_status}`
          }) })
          wifePersonId = wifePerson.person_id
          
          if (this.formData.wife_status && marriageDate) {
            const statusObj = this.motherStatuses.find(s => s.name === this.formData.wife_status)
            if (statusObj) {
              await api('/api/statuses/', {
                method: 'POST',
                headers: H,
                body: JSON.stringify({
                  person: wifePersonId,
                  status_choice: statusObj.status_choice_id,
                  date_start: marriageDate,
                })
              }).catch(err => console.warn('Статус не сохранен:', err))
            }
          }
        }

        const marriage = await api('/api/marriage-records/', { method: 'POST', headers: H, body: JSON.stringify({
          archive: Number(archiveId),
          page: this.formData.page ? String(this.formData.page) : '',
          page_turn: this.formData.page_turn || false,
          number_record: this.formData.number_record ? String(this.formData.number_record) : '',
          date: marriageDate,
          comment: this.formData.comment || '',
        }) })

        if (husbandPersonId) {
          await api('/api/husbands/', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({
              person: husbandPersonId,
              marriage: marriage.marriage_id,
              number_marriage: this.formData.husband_number_marriage || 1,
              age: this.formData.husband_age || null
            })
          })
        }

        if (wifePersonId) {
          await api('/api/wives/', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({
              person: wifePersonId,
              marriage: marriage.marriage_id,
              number_marriage: this.formData.wife_number_marriage || 1,
              age: this.formData.wife_age || null
            })
          })
        }

        if (this.scanFile) {
          try { await this._uploadScan('marriage', marriage.marriage_id, this.scanFile) }
          catch (e) { console.error('Ошибка загрузки скана:', e) }
        }

        for (const g of this.maleGuarantors) {
          if (!g.name || !g.name.trim()) continue
          
          const guarantorPerson = await api('/api/persons/', { method: 'POST', headers: H, body: JSON.stringify({
            name: g.name.trim(),
            surname: g.surname || 'Неизвестно',
            patronymic: g.patronymic || '',
            sex: 'М',
            estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
            creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
            province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
            yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
            volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
            village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
            duplicate: 0,
            comment: `Поручитель в браке #${this.formData.number_record}`
          }) })
          
          await api('/api/male-guarantors/', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({
              person: guarantorPerson.person_id,
              marriage: marriage.marriage_id
            })
          }).catch(err => console.error('Ошибка создания поручителя:', err))
        }

        for (const g of this.femaleGuarantors) {
          if (!g.name || !g.name.trim()) continue
          
          const guarantorPerson = await api('/api/persons/', { method: 'POST', headers: H, body: JSON.stringify({
            name: g.name.trim(),
            surname: g.surname || 'Неизвестно',
            patronymic: g.patronymic || '',
            sex: 'Ж',
            estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
            creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
            province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
            yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
            volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
            village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
            duplicate: 0,
            comment: `Поручительница в браке #${this.formData.number_record}`
          }) })
          
          await api('/api/female-guarantors/', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({
              person: guarantorPerson.person_id,
              marriage: marriage.marriage_id
            })
          }).catch(err => console.error('Ошибка создания поручительницы:', err))
        }

        for (const p of this.priests) {
          if (!p.name || !p.name.trim()) continue

          let churchWorkerId = null
          
          if (!p.church_worker_id) {
            const priestPerson = await api('/api/persons/', { method: 'POST', headers: H, body: JSON.stringify({
              name: p.name.trim(),
              surname: p.surname || 'Неизвестно',
              sex: 'М',
              creed: this.formData.creed_id ? Number(this.formData.creed_id) : null,
              duplicate: 0,
              comment: `Священнослужитель в браке #${this.formData.number_record}`
            }) })
          } else {
            churchWorkerId = p.church_worker_id
          }

          await api('/api/marriage-record-priests/', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({
              marriage: marriage.marriage_id,
              name: p.name.trim(),
              surname: p.surname || 'Неизвестно',
              clergy: p.clergy_id && p.clergy_id !== '' ? Number(p.clergy_id) : null,
              church_worker: churchWorkerId
            })
          }).catch(err => console.error('Ошибка сохранения священника:', err))
        }

        if (this.currentDraftId) {
          try {
            await fetch(`${API_BASE}/api/drafts/${this.currentDraftId}/`, {
              method: 'DELETE',
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            })
          } catch (e) { console.error(e) }
        }

        this.showPublishSuccess = true
        
      } catch (err) {
        console.error('Ошибка при сохранении:', err)
        this.error = 'Ошибка при сохранении: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally { this.loading = false }
    },

    async saveEditedRecord() {
      this.error = null; this.loading = true
      try {
        const H = authHeaders(true)
        
        if (!this.existingPersonIds.husband && !this.existingPersonIds.wife) {
          console.warn('Нет ID персон для обновления, но продолжаем с остальными данными')
        }
        
        if (this.existingPersonIds.husband && this.existingPersonIds.husband > 0) {
          try {
            await api(`/api/persons/${this.existingPersonIds.husband}/`, { 
              method: 'PATCH', 
              headers: H, 
              body: JSON.stringify({
                name: this.formData.husband_name,
                surname: this.formData.husband_surname,
                patronymic: this.formData.husband_patronymic || '',
                estate: this.formData.husband_estate_id ? Number(this.formData.husband_estate_id) : null,
                creed: this.formData.creed_id ? Number(this.formData.creed_id) : null,
                province: this.formData.husband_province_id ? Number(this.formData.husband_province_id) : null,
                yezd: this.formData.husband_yezd_id ? Number(this.formData.husband_yezd_id) : null,
                volost: this.formData.husband_volost_id ? Number(this.formData.husband_volost_id) : null,
                village: this.formData.husband_village_id ? Number(this.formData.husband_village_id) : null,
              })
            })
            
            const husbands = await api(`/api/husbands/?person=${this.existingPersonIds.husband}&marriage=${this.editingRecordId}`, { headers: H })
            if (husbands && husbands.length > 0) {
              await api(`/api/husbands/${husbands[0].man_id}/`, { 
                method: 'PATCH', 
                headers: H, 
                body: JSON.stringify({
                  age: this.formData.husband_age || null,
                  number_marriage: this.formData.husband_number_marriage || 1,
                })
              })
            }
          } catch (err) {
            console.error('Ошибка обновления жениха:', err)
          }
        }
        
        if (this.existingPersonIds.wife && this.existingPersonIds.wife > 0) {
          try {
            await api(`/api/persons/${this.existingPersonIds.wife}/`, { 
              method: 'PATCH', 
              headers: H, 
              body: JSON.stringify({
                name: this.formData.wife_name,
                surname: this.formData.wife_surname || 'Неизвестно',
                patronymic: this.formData.wife_patronymic || '',
                estate: this.formData.wife_estate_id ? Number(this.formData.wife_estate_id) : null,
                creed: this.formData.wife_creed_id ? Number(this.formData.wife_creed_id) : this.formData.creed_id ? Number(this.formData.creed_id) : null,
                province: this.formData.wife_province_id ? Number(this.formData.wife_province_id) : null,
                yezd: this.formData.wife_yezd_id ? Number(this.formData.wife_yezd_id) : null,
                volost: this.formData.wife_volost_id ? Number(this.formData.wife_volost_id) : null,
                village: this.formData.wife_village_id ? Number(this.formData.wife_village_id) : null,
              })
            })
            
            const wives = await api(`/api/wives/?person=${this.existingPersonIds.wife}&marriage=${this.editingRecordId}`, { headers: H })
            if (wives && wives.length > 0) {
              await api(`/api/wives/${wives[0].wife_id}/`, { 
                method: 'PATCH', 
                headers: H, 
                body: JSON.stringify({
                  age: this.formData.wife_age || null,
                  number_marriage: this.formData.wife_number_marriage || 1,
                })
              })
            }
            
            if (this.formData.wife_status) {
              const statusObj = this.motherStatuses.find(s => s.name === this.formData.wife_status)
              if (statusObj) {
                const marriageDate = this.formatDateForApi(this.formData.year, this.formData.marriage_month, this.formData.marriage_day)
                const existingStatuses = await api(`/api/statuses/?person=${this.existingPersonIds.wife}`, { headers: H }).catch(() => [])
                if (existingStatuses && existingStatuses.length > 0) {
                  await api(`/api/statuses/${existingStatuses[0].status_id}/`, {
                    method: 'PATCH',
                    headers: H,
                    body: JSON.stringify({
                      status_choice: statusObj.status_choice_id,
                      date_start: marriageDate,
                    })
                  }).catch(err => console.warn('Не удалось обновить статус:', err))
                } else if (marriageDate) {
                  await api('/api/statuses/', {
                    method: 'POST',
                    headers: H,
                    body: JSON.stringify({
                      person: this.existingPersonIds.wife,
                      status_choice: statusObj.status_choice_id,
                      date_start: marriageDate,
                    })
                  }).catch(err => console.warn('Не удалось создать статус:', err))
                }
              }
            }
          } catch (err) {
            console.error('Ошибка обновления невесты:', err)
          }
        }
        
        // ОБНОВЛЯЕМ ПОРУЧИТЕЛЕЙ (МУЖЧИНЫ)
        try {
          const existingMaleGuarantors = await api(`/api/male-guarantors/?marriage=${this.editingRecordId}`, { headers: H }).catch(() => [])
          
          for (const g of existingMaleGuarantors) {
            await api(`/api/male-guarantors/${g.guarantors_id}/`, { method: 'DELETE', headers: H }).catch(err => console.warn('Ошибка удаления поручителя:', err))
          }
          
          for (const g of this.maleGuarantors) {
            if (!g.name || !g.name.trim()) continue
            
            let guarantorPersonId = g.guarantor_id
            
            if (guarantorPersonId) {
              await api(`/api/persons/${guarantorPersonId}/`, {
                method: 'PATCH',
                headers: H,
                body: JSON.stringify({
                  name: g.name.trim(),
                  surname: g.surname || 'Неизвестно',
                  patronymic: g.patronymic || '',
                  sex: 'М',
                  estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
                  creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
                  province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
                  yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
                  volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
                  village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
                })
              })
            } else {
              const newPerson = await api('/api/persons/', {
                method: 'POST',
                headers: H,
                body: JSON.stringify({
                  name: g.name.trim(),
                  surname: g.surname || 'Неизвестно',
                  patronymic: g.patronymic || '',
                  sex: 'М',
                  estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
                  creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
                  province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
                  yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
                  volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
                  village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
                  duplicate: 0,
                  comment: `Поручитель в браке #${this.formData.number_record}`
                })
              })
              guarantorPersonId = newPerson.person_id
            }
            
            await api('/api/male-guarantors/', {
              method: 'POST',
              headers: H,
              body: JSON.stringify({
                person: guarantorPersonId,
                marriage: this.editingRecordId
              })
            }).catch(err => console.error('Ошибка создания поручителя:', err))
          }
        } catch (err) {
          console.error('Ошибка при обновлении поручителей-мужчин:', err)
        }
        
        // ОБНОВЛЯЕМ ПОРУЧИТЕЛЬНИЦ (ЖЕНЩИНЫ)
        try {
          const existingFemaleGuarantors = await api(`/api/female-guarantors/?marriage=${this.editingRecordId}`, { headers: H }).catch(() => [])
          
          for (const g of existingFemaleGuarantors) {
            await api(`/api/female-guarantors/${g.guarantors_id}/`, { method: 'DELETE', headers: H }).catch(err => console.warn('Ошибка удаления поручительницы:', err))
          }
          
          for (const g of this.femaleGuarantors) {
            if (!g.name || !g.name.trim()) continue
            
            let guarantorPersonId = g.guarantor_id
            
            if (guarantorPersonId) {
              await api(`/api/persons/${guarantorPersonId}/`, {
                method: 'PATCH',
                headers: H,
                body: JSON.stringify({
                  name: g.name.trim(),
                  surname: g.surname || 'Неизвестно',
                  patronymic: g.patronymic || '',
                  sex: 'Ж',
                  estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
                  creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
                  province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
                  yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
                  volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
                  village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
                })
              })
            } else {
              const newPerson = await api('/api/persons/', {
                method: 'POST',
                headers: H,
                body: JSON.stringify({
                  name: g.name.trim(),
                  surname: g.surname || 'Неизвестно',
                  patronymic: g.patronymic || '',
                  sex: 'Ж',
                  estate: g.estate_id && g.estate_id !== '' ? Number(g.estate_id) : null,
                  creed: g.creed_id && g.creed_id !== '' ? Number(g.creed_id) : null,
                  province: g.province_id && g.province_id !== '' ? Number(g.province_id) : null,
                  yezd: g.yezd_id && g.yezd_id !== '' ? Number(g.yezd_id) : null,
                  volost: g.volost_id && g.volost_id !== '' ? Number(g.volost_id) : null,
                  village: g.village_id && g.village_id !== '' ? Number(g.village_id) : null,
                  duplicate: 0,
                  comment: `Поручительница в браке #${this.formData.number_record}`
                })
              })
              guarantorPersonId = newPerson.person_id
            }
            
            await api('/api/female-guarantors/', {
              method: 'POST',
              headers: H,
              body: JSON.stringify({
                person: guarantorPersonId,
                marriage: this.editingRecordId
              })
            }).catch(err => console.error('Ошибка создания поручительницы:', err))
          }
        } catch (err) {
          console.error('Ошибка при обновлении поручительниц-женщин:', err)
        }
        
        // ОБНОВЛЯЕМ СВЯЩЕННИКОВ
        try {
          const existingPriests = await api(`/api/marriage-record-priests/?marriage=${this.editingRecordId}`, { headers: H }).catch(() => [])
          
          for (const p of existingPriests) {
            await api(`/api/marriage-record-priests/${p.id}/`, { method: 'DELETE', headers: H }).catch(err => console.warn('Ошибка удаления священника:', err))
          }
          
          for (const p of this.priests) {
            if (!p.name || !p.name.trim()) continue
            
            await api('/api/marriage-record-priests/', {
              method: 'POST',
              headers: H,
              body: JSON.stringify({
                marriage: this.editingRecordId,
                name: p.name.trim(),
                surname: p.surname || 'Неизвестно',
                clergy: p.clergy_id && p.clergy_id !== '' ? Number(p.clergy_id) : null,
                church_worker: p.church_worker_id || null
              })
            }).catch(err => console.error('Ошибка сохранения священника:', err))
          }
        } catch (err) {
          console.error('Ошибка при обновлении священников:', err)
        }
        
        // Обновляем саму запись о браке
        const marriageDate = this.formatDateForApi(this.formData.year, this.formData.marriage_month, this.formData.marriage_day)
        await api(`/api/marriage-records/${this.editingRecordId}/`, { 
          method: 'PATCH', 
          headers: H, 
          body: JSON.stringify({
            page: this.formData.page ? String(this.formData.page) : '',
            page_turn: this.formData.page_turn || false,
            number_record: this.formData.number_record ? String(this.formData.number_record) : '',
            date: marriageDate,
            comment: this.formData.comment || '',
          }) 
        })

        if (this.scanFile) {
          try { await this._uploadScan('marriage', this.editingRecordId, this.scanFile) }
          catch (e) { console.error(e) }
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

    async loadRecordForEditing(recordId) {
      this.loading = true
      try {
        const record = await api(`/api/marriage-records/${recordId}/`, { headers: authHeaders() })
        if (!record) throw new Error('Запись не найдена')
        this.editingRecordId = recordId

        if (record.marriage_month) {
          this.formData.marriage_month = record.marriage_month
        }
        if (record.marriage_day) {
          this.formData.marriage_day = record.marriage_day
        }
        
        if (record.date) {
          const dateParts = record.date.split('-')
          if (dateParts.length === 3) {
            this.formData.year = parseInt(dateParts[0])
            this.formData.marriage_month = parseInt(dateParts[1])
            this.formData.marriage_day = parseInt(dateParts[2])
          }
        }

        this.existingPersonIds.husband = null
        this.existingPersonIds.wife = null

        const [husbands, wives, maleGuarantorsData, femaleGuarantorsData, priestsData] = await Promise.all([
          api(`/api/husbands/?marriage=${recordId}`, { headers: authHeaders() }).catch(() => []),
          api(`/api/wives/?marriage=${recordId}`, { headers: authHeaders() }).catch(() => []),
          api(`/api/male-guarantors/?marriage=${recordId}`, { headers: authHeaders() }).catch(() => []),
          api(`/api/female-guarantors/?marriage=${recordId}`, { headers: authHeaders() }).catch(() => []),
          api(`/api/marriage-record-priests/?marriage=${recordId}`, { headers: authHeaders() }).catch(() => [])
        ])

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

        const findName = (list, id, key) => {
          if (!id) return ''
          const found = list.find(i => i[key] === id)
          return found ? found.name : ''
        }

        if (husbands && husbands.length > 0 && husbands[0].person) {
          this.existingPersonIds.husband = husbands[0].person
          const husbandPerson = await api(`/api/persons/${husbands[0].person}/`, { headers: authHeaders() }).catch(() => null)
          if (husbandPerson) {
            this.formData.husband_name = husbandPerson.name || ''
            this.formData.husband_surname = husbandPerson.surname || ''
            this.formData.husband_patronymic = husbandPerson.patronymic || ''
            this.formData.husband_age = husbands[0].age || ''
            this.formData.husband_number_marriage = husbands[0].number_marriage || 1
            this.formData.husband_estate_id = husbandPerson.estate || ''
            this.formData.creed_id = husbandPerson.creed || ''
            
            this.formData.husband_province_id = husbandPerson.province || ''
            this.husbandProvinceSearch = findName(this.provinces, this.formData.husband_province_id, 'province_id')
            this.formData.husband_yezd_id = husbandPerson.yezd || ''
            this.husbandYezdSearch = findName(this.yezds, this.formData.husband_yezd_id, 'yezd_id')
            this.formData.husband_volost_id = husbandPerson.volost || ''
            this.husbandVolostSearch = findName(this.volosts, this.formData.husband_volost_id, 'volost_id')
            this.formData.husband_village_id = husbandPerson.village || ''
            this.husbandVillageSearch = findName(this.villages, this.formData.husband_village_id, 'village_id')
          }
        }

        if (wives && wives.length > 0 && wives[0].person) {
          this.existingPersonIds.wife = wives[0].person
          const wifePerson = await api(`/api/persons/${wives[0].person}/`, { headers: authHeaders() }).catch(() => null)
          if (wifePerson) {
            this.formData.wife_name = wifePerson.name || ''
            this.formData.wife_surname = wifePerson.surname || ''
            this.formData.wife_patronymic = wifePerson.patronymic || ''
            this.formData.wife_age = wives[0].age || ''
            this.formData.wife_number_marriage = wives[0].number_marriage || 1
            this.formData.wife_estate_id = wifePerson.estate || ''
            this.formData.wife_creed_id = wifePerson.creed || ''
            
            this.formData.wife_province_id = wifePerson.province || ''
            this.wifeProvinceSearch = findName(this.provinces, this.formData.wife_province_id, 'province_id')
            this.formData.wife_yezd_id = wifePerson.yezd || ''
            this.wifeYezdSearch = findName(this.yezds, this.formData.wife_yezd_id, 'yezd_id')
            this.formData.wife_volost_id = wifePerson.volost || ''
            this.wifeVolostSearch = findName(this.volosts, this.formData.wife_volost_id, 'volost_id')
            this.formData.wife_village_id = wifePerson.village || ''
            this.wifeVillageSearch = findName(this.villages, this.formData.wife_village_id, 'village_id')
            
            try {
              const statuses = await api(`/api/statuses/?person=${wives[0].person}`, { headers: authHeaders() }).catch(() => [])
              if (statuses && statuses.length > 0 && statuses[0].status_choice) {
                let statusId = statuses[0].status_choice
                if (typeof statuses[0].status_choice === 'object') {
                  statusId = statuses[0].status_choice.status_choice_id || statuses[0].status_choice.id
                }
                const statusObj = this.motherStatuses.find(s => 
                  s.status_choice_id === statusId || s.id === statusId
                )
                if (statusObj) this.formData.wife_status = statusObj.name
              }
            } catch (err) {
              console.warn('Не удалось загрузить статус невесты:', err)
            }
          }
        }

        if (record.archive) {
          this.formData.archive_id = record.archive
          const archive = this.allArchives.find(a => a.archive_id === record.archive)
          if (archive) {
            this.archiveSearch = archive.name
            this.formData.number_case = archive.number_case || ''
            this.formData.year = archive.year || ''
          }
        }

        this.formData.page = record.page || ''
        this.formData.page_turn = record.page_turn || false
        this.formData.number_record = record.number_record || ''
        this.formData.comment = record.comment || ''

        const scanExtensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
        for (const ext of scanExtensions) {
          const scanUrl = `${API_BASE}/media/scans/marriage/${recordId}${ext}`
          try {
            const response = await fetch(scanUrl, { headers: authHeaders() })
            if (response.ok) {
              this.scanSrc = scanUrl
              break
            }
          } catch (e) {}
        }

        if (maleGuarantorsData && maleGuarantorsData.length > 0) {
          this.maleGuarantors = []
          for (const mg of maleGuarantorsData) {
            if (mg.person) {
              const guarantorPerson = await api(`/api/persons/${mg.person}/`, { headers: authHeaders() }).catch(() => null)
              if (guarantorPerson) {
                const guarantor = this.emptyGuarantor()
                guarantor.guarantor_id = mg.person
                guarantor.name = guarantorPerson.name || ''
                guarantor.patronymic = guarantorPerson.patronymic || ''
                guarantor.surname = guarantorPerson.surname || ''
                guarantor.estate_id = guarantorPerson.estate || ''
                guarantor.creed_id = guarantorPerson.creed || ''
                
                guarantor.province_id = guarantorPerson.province || ''
                guarantor.provinceSearch = findName(this.provinces, guarantor.province_id, 'province_id')
                guarantor.yezd_id = guarantorPerson.yezd || ''
                guarantor.yezdSearch = findName(this.yezds, guarantor.yezd_id, 'yezd_id')
                guarantor.volost_id = guarantorPerson.volost || ''
                guarantor.volostSearch = findName(this.volosts, guarantor.volost_id, 'volost_id')
                guarantor.village_id = guarantorPerson.village || ''
                guarantor.villageSearch = findName(this.villages, guarantor.village_id, 'village_id')
                
                this.maleGuarantors.push(guarantor)
              }
            }
          }
        }
        
        if (maleGuarantorsData.length === 0) {
          this.maleGuarantors = [this.emptyGuarantor()]
        }

        if (femaleGuarantorsData && femaleGuarantorsData.length > 0) {
          this.femaleGuarantors = []
          for (const fg of femaleGuarantorsData) {
            if (fg.person) {
              const guarantorPerson = await api(`/api/persons/${fg.person}/`, { headers: authHeaders() }).catch(() => null)
              if (guarantorPerson) {
                const guarantor = this.emptyGuarantor()
                guarantor.guarantor_id = fg.person
                guarantor.name = guarantorPerson.name || ''
                guarantor.patronymic = guarantorPerson.patronymic || ''
                guarantor.surname = guarantorPerson.surname || ''
                guarantor.estate_id = guarantorPerson.estate || ''
                guarantor.creed_id = guarantorPerson.creed || ''
                
                guarantor.province_id = guarantorPerson.province || ''
                guarantor.provinceSearch = findName(this.provinces, guarantor.province_id, 'province_id')
                guarantor.yezd_id = guarantorPerson.yezd || ''
                guarantor.yezdSearch = findName(this.yezds, guarantor.yezd_id, 'yezd_id')
                guarantor.volost_id = guarantorPerson.volost || ''
                guarantor.volostSearch = findName(this.volosts, guarantor.volost_id, 'volost_id')
                guarantor.village_id = guarantorPerson.village || ''
                guarantor.villageSearch = findName(this.villages, guarantor.village_id, 'village_id')
                
                this.femaleGuarantors.push(guarantor)
              }
            }
          }
        }
        
        if (femaleGuarantorsData.length === 0) {
          this.femaleGuarantors = [this.emptyGuarantor()]
        }

        if (priestsData && priestsData.length > 0) {
          this.priests = priestsData.map(p => ({
            ...this.emptyPriest(),
            priest_record_id: p.id,
            name: p.name || '',
            surname: p.surname || '',
            clergy_id: p.clergy || '',
            church_worker_id: p.church_worker || null,
            searchText: `${p.surname || ''} ${p.name || ''}`.trim()
          }))
        }
        
        if (priestsData.length === 0) {
          this.priests = [this.emptyPriest()]
        }

        this.formStatus = 'published'
        this.showPublishAttempt = false
        this.missingFieldsList = []
        this.error = null
        this.$forceUpdate()
      } catch (err) {
        console.error('Ошибка загрузки записи:', err)
        this.error = 'Не удалось загрузить данные для редактирования: ' + err.message
      } finally { 
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.marriage-layout {
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
.error-input:focus { border-color: #dc2626 !important; box-shadow: 0 0 0 3px rgba(220,38,38,0.1) !important; }
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

.age-spinner { display: flex; align-items: center; gap: 0; border: 1px solid #c8c5c0; border-radius: 6px; overflow: hidden; }
.age-btn {
  width: 36px; height: 34px; background: #f0efee; border: none; border-right: 1px solid #c8c5c0;
  font-size: 18px; font-weight: 400; color: #444; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: background .15s; flex-shrink: 0; line-height: 1;
}
.age-btn:last-child { border-right: none; border-left: 1px solid #c8c5c0; }
.age-btn:hover { background: #e0dfdd; }
.age-btn:active { background: #d0cfcc; }
.age-input {
  flex: 1; border: none !important; border-radius: 0 !important; text-align: center;
  padding: 7px 4px !important; font-size: 13px; min-width: 0;
  box-shadow: none !important;
}
.age-input:focus { outline: none; box-shadow: none !important; border: none !important; }

.row { display: grid; gap: 10px; margin-bottom: 10px; }
.row.two   { grid-template-columns: 1fr 1fr; }
.row.three { grid-template-columns: 1fr 1fr 1fr; }
.full { margin-bottom: 10px; }

.checkbox-field { justify-content: flex-end; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #444; cursor: pointer; font-weight: 400 !important; padding: 7px 0; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; }

.record-number-wrapper { display: flex; align-items: center; gap: 8px; }
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
.badge-icon { font-size: 13px; flex-shrink: 0; }
.badge-unlink { margin-left: auto; background: none; border: none; font-size: 11px; color: #888; cursor: pointer; padding: 2px 6px; border-radius: 4px; transition: background .15s, color .15s; }
.badge-unlink:hover { background: #fef2f2; color: #a00; }

.sub-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; }
.sub-block-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.sub-block-header span { font-size: 12px; font-weight: 600; color: #888780; }
.header-actions { display: flex; gap: 8px; align-items: center; }

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

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(3px); }
.modal { background: #fff; border-radius: 20px; max-width: 460px; width: 90%; padding: 24px 28px; box-shadow: 0 20px 35px -12px rgba(0,0,0,0.25); animation: fadeSlideIn 0.2s ease-out; }
.modal.modal-ref { text-align: left; }
.modal.modal-ref h4 { font-size: 16px; font-weight: 700; margin-bottom: 14px; color: #1a1a1a; }
.modal.modal-confirm { text-align: center; }
.modal.modal-confirm h4 { font-size: 1.7rem; font-weight: 600; margin-bottom: 12px; color: #222; }
.modal-icon { font-size: 52px; margin-bottom: 12px; }
.modal-text { font-size: 1rem; line-height: 1.4; color: #4b5563; margin-bottom: 28px; }
.modal-footer { display: flex; gap: 12px; justify-content: center; margin-top: 8px; }
.btn-cancel { background: #f1f5f9; color: #1e293b; border: none; padding: 8px 22px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; transition: all 0.2s ease; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-action { background: #1a1a1a; color: #fff; border: none; padding: 8px 22px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.15); transition: all 0.2s ease; }
.btn-action:hover:not(:disabled) { background: #333; transform: translateY(-1px); }
.btn-action:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-ok { background: #10b981; color: #fff; border: none; padding: 8px 28px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; box-shadow: 0 2px 6px rgba(16,185,129,0.2); transition: all 0.2s ease; }
.btn-ok:hover { background: #059669; transform: translateY(-1px); }
@keyframes fadeSlideIn { from { opacity: 0; transform: translateY(-12px); } to { opacity: 1; transform: translateY(0); } }

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
.scan-status { display: flex; align-items: center; gap: 4px; margin-left: 8px; padding: 4px 8px; background: rgba(34,197,94,0.2); border-radius: 6px; color: #22c55e; font-size: 11px; }

@media (max-width: 900px) {
  .marriage-layout { flex-direction: column; }
  .form-panel { width: 100%; max-width: 100%; height: 55vh; }
  .scan-panel { height: 45vh; }
  .row.three { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .row.two, .row.three { grid-template-columns: 1fr; }
  .header-top { flex-wrap: wrap; }
  .status-toggle { width: 100%; }
  .toggle-btn { flex: 1; justify-content: center; }
  .age-spinner { max-width: 160px; }
}
</style>