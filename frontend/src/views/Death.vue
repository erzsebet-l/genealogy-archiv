<template>
  <div class="death-layout">

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

          <div class="status-toggle" v-if="!editingRecordId">
            <button type="button" :class="['toggle-btn', { active: formStatus === 'draft' }]" @click="switchToDraft">
              <span class="toggle-dot draft-dot"></span>
              Черновик
            </button>
            <button type="button" :class="['toggle-btn', { active: formStatus === 'published' }]" @click="switchToPublish">
              <span class="toggle-dot pub-dot"></span>
              Опубликовать
            </button>
          </div>

          <div v-if="editingRecordId" class="edit-mode-badge">
            ✎ Редактирование записи
          </div>
        </div>

        <h2 class="page-title">Запись о <em>смерти</em></h2>

        <div v-if="editingRecordId" class="edit-mode-banner">
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

        <!-- ══════════════ БЛОК: АРХИВ ══════════════ -->
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
                :class="{ auto: autoFilledFields.year, 'error-input': showFieldError('year') }"
              />
              <div v-if="autoFilledFields.year" class="auto-hint">⚡ Автозаполнено</div>
              <div v-if="showFieldError('year')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('page') }">
              <label>Номер листа <span class="req-star">*</span></label>
              <input
                type="number"
                v-model.number="formData.page"
                :class="{ 'error-input': showFieldError('page') }"
                placeholder="1"
              />
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

        <!-- ══════════════ БЛОК: МЕСТО ЖИТЕЛЬСТВА ══════════════ -->
        <section class="block">
          <h3 class="block-title">Место жительства умершего</h3>

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
                  <input type="text" v-model="provinceSearch"
                    @input="onProvinceInput"
                    @focus="provinceDropOpen = true"
                    @blur="closeProvinceDrop"
                    :placeholder="getLocationName('province')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="provinceDropOpen && filteredProvinces.length" class="drop-list">
                    <li v-for="p in filteredProvinces" :key="p.province_id"
                      @mousedown.prevent="selectProvince(p)" class="drop-item">
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
                  <input type="text" v-model="yezdSearch"
                    @input="onYezdInput"
                    @focus="yezdDropOpen = true"
                    @blur="closeYezdDrop"
                    :placeholder="getLocationName('yezd')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="yezdDropOpen && filteredYezds.length" class="drop-list">
                    <li v-for="y in filteredYezds" :key="y.yezd_id"
                      @mousedown.prevent="selectYezd(y)" class="drop-item">
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
                  <input type="text" v-model="volostSearch"
                    @input="onVolostInput"
                    @focus="volostDropOpen = true"
                    @blur="closeVolostDrop"
                    :placeholder="getLocationName('volost')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="volostDropOpen && filteredVolosts.length" class="drop-list">
                    <li v-for="v in filteredVolosts" :key="v.volost_id"
                      @mousedown.prevent="selectVolost(v)" class="drop-item">
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
                  <input type="text" v-model="villageSearch"
                    @input="onVillageInput"
                    @focus="villageDropOpen = true"
                    @blur="closeLocationDrop"
                    :placeholder="getLocationName('village')"
                    autocomplete="off" class="combo-input" />
                  <ul v-show="villageDropOpen && filteredVillages.length" class="drop-list">
                    <li v-for="v in filteredVillages" :key="v.village_id"
                      @mousedown.prevent="selectVillage(v)" class="drop-item">
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
            <div class="field">
              <label>Сословие</label>
              <div class="field-with-add">
                <select v-model="formData.estate_id">
                  <option value="">Выберите</option>
                  <option v-for="e in estates" :key="e.estate_id" :value="e.estate_id">{{ e.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('estate')" title="Добавить сословие">＋</button>
              </div>
            </div>
            <div class="field"></div>
          </div>
        </section>

        <!-- ══════════════ БЛОК: ДАТА ══════════════ -->
        <section class="block">
          <h3 class="block-title">Дата смерти</h3>
          <div class="row three">
            <div class="field" :class="{ 'field-error': showFieldError('death_month') }">
              <label>Месяц смерти <span class="req-star">*</span></label>
              <select v-model.number="formData.death_month" :class="{ 'error-input': showFieldError('death_month') }">
                <option value="">Выберите</option>
                <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
              </select>
              <div v-if="showFieldError('death_month')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('death_day') }">
              <label>Число смерти <span class="req-star">*</span></label>
              <input type="number" min="1" max="31" v-model.number="formData.death_day"
                @input="autoBurialDay" placeholder="1" :class="{ 'error-input': showFieldError('death_day') }" />
              <div v-if="showFieldError('death_day')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field">
              <label>Число погребения</label>
              <input type="number" min="1" max="31" v-model.number="formData.burial_day"
                :class="{ auto: burialAuto }" placeholder="3" />
              <span v-if="burialAuto" class="auto-hint">⚡ День смерти +2</span>
            </div>
          </div>
        </section>

        <!-- ══════════════ БЛОК: РОДСТВЕННИК ══════════════ -->
        <section class="block">
          <div class="block-title-row">
            <h3 class="block-title">Родственник</h3>
            <button type="button" class="btn-add-block" @click="addRelative">＋ добавить</button>
          </div>

          <div class="info-hint">
            <span class="hint-icon">ℹ️</span>
            <span>Выберите степень родства в поле ниже — она означает, кем <strong>умерший</strong> приходится этому родственнику</span>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('kinship_id') }">
              <label>Степень родства <span class="req-star">*</span></label>
              <div class="field-with-add">
                <select v-model="formData.kinship_id" @change="onKinshipChange">
                  <option value="">Выберите</option>
                  <option v-for="k in kinshipList" :key="k.kinship_id" :value="k.kinship_id">{{ k.name }}</option>
                </select>
                <button type="button" class="btn-add-ref" @click="openModal('kinship')" title="Добавить степень родства">＋</button>
              </div>
              <div class="kinship-hint">
                ⚡ Укажите, кем <strong>умерший</strong> приходится родственнику (например: "отец" — умерший является отцом)
              </div>
              <div v-if="showFieldError('kinship_id')" class="error-message">Обязательно для заполнения</div>
            </div>
          </div>

          <div v-for="(r, i) in relatives" :key="'rel'+i" class="sub-block">
            <div class="sub-block-header">
              <span>Родственник #{{ i + 1 }}</span>
              <button type="button" class="btn-remove" @click="relatives.splice(i, 1)">✕</button>
            </div>
            <div class="row two">
              <div class="field">
                <label>Имя</label>
                <input type="text" v-model="r.name" placeholder="Иоанн" @blur="onRelativeBlur" />
              </div>
              <div class="field">
                <label>Отчество</label>
                <input type="text" v-model="r.patronymic" placeholder="Иванович" />
              </div>
            </div>
            <div class="row two">
              <div class="field">
                <label>Фамилия</label>
                <input type="text" v-model="r.surname" placeholder="Смирнов" @blur="onRelativeBlur" />
              </div>
            </div>
          </div>
        </section>

        <!-- ══════════════ БЛОК: ОБ УМЕРШЕМ ══════════════ -->
        <section ref="deceasedBlock" class="block">
          <h3 class="block-title">Об умершем</h3>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('sex') }">
              <label>Пол <span class="req-star">*</span></label>
              <select v-model="formData.sex" @change="onSexChange" :class="{ 'error-input': showFieldError('sex') }">
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

          <!-- ── ВОЗРАСТ: 4 поля ── -->
          <div class="block">
            <div class="age-header">
              <label class="age-label">Возраст</label>
              <div class="age-fields">
                <div class="age-field">
                  <input type="number" min="0" max="150" v-model.number="ageYears" placeholder="0" />
                  <span>лет</span>
                </div>
                <div class="age-field">
                  <input type="number" min="0" max="11" v-model.number="ageMonths" placeholder="0" />
                  <span>мес</span>
                </div>
                <div class="age-field">
                  <input type="number" min="0" max="4" v-model.number="ageWeeks" placeholder="0" />
                  <span>нед</span>
                </div>
                <div class="age-field">
                  <input type="number" min="0" max="6" v-model.number="ageDays" placeholder="0" />
                  <span>дней</span>
                </div>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field" :class="{ 'field-error': showFieldError('name') }">
              <label>Имя <span class="req-star">*</span></label>
              <input type="text" v-model="formData.name" placeholder="Иоанн" :class="{ 'error-input': showFieldError('name') }" />
              <div v-if="showFieldError('name')" class="error-message">Обязательно для заполнения</div>
            </div>
            <div class="field" :class="{ 'field-error': showFieldError('surname') }">
              <label>Фамилия <span class="req-star">*</span></label>
              <input
                type="text"
                v-model="formData.surname"
                placeholder="Смирнов"
                :class="{ auto: surnameAuto, 'error-input': showFieldError('surname') }"
              />
              <div v-if="surnameAuto" class="auto-hint">⚡ От родственника (с учётом пола)</div>
              <div v-if="showFieldError('surname')" class="error-message">Обязательно для заполнения</div>
              <div v-if="showSurnameSuggestion" class="suggestion-below">
                <span class="suggestion-below-text">
                  💡 Предложена фамилия от родственника <strong>{{ selectedRelativeName || '?' }}</strong>:
                </span>
                <span class="suggestion-below-value">{{ suggestedSurname }}</span>
                <button type="button" class="suggestion-below-button" @click="acceptSurnameSuggestion">Применить</button>
              </div>
            </div>
          </div>

          <div class="row two">
            <div class="field">
              <label>Отчество</label>
              <input
                type="text"
                v-model="formData.patronymic"
                placeholder="Иванович"
                :class="{ auto: patronymicAuto }"
              />
              <div v-if="patronymicAuto" class="auto-hint">⚡ От родственника</div>
              <div v-if="showPatronymicSuggestion" class="suggestion-below">
                <span class="suggestion-below-text">
                  💡 Предложено отчество от имени родственника <strong>{{ selectedRelativeName || '?' }}</strong>:
                </span>
                <span class="suggestion-below-value">{{ suggestedPatronymic }}</span>
                <button type="button" class="suggestion-below-button" @click="acceptPatronymicSuggestion">Применить</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ══════════════ БЛОК: СВЯЩЕННОСЛУЖИТЕЛИ ══════════════ -->
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

        <!-- ══════════════ БЛОК: ДОПОЛНИТЕЛЬНЫЕ СВЕДЕНИЯ ══════════════ -->
        <section class="block">
          <h3 class="block-title">Дополнительные сведения</h3>

          <div class="field full">
            <label>Причина смерти</label>
            <input type="text" v-model="formData.cause_of_death" placeholder="Например: горячка" />
          </div>

          <div class="field full" style="margin-top:10px">
            <label>Место погребения</label>
            <input type="text" v-model="formData.burial_place" placeholder="Например: приходское кладбище" />
          </div>

          <div class="field full" style="margin-top:10px">
            <label>Примечание</label>
            <textarea v-model="formData.comment" rows="3" placeholder="Дополнительные сведения..."></textarea>
          </div>
        </section>

        <!-- ══════════════ ПОДВАЛ ФОРМЫ ══════════════ -->
        <div class="form-footer">
          <button type="submit" class="btn-submit" :disabled="loading"
            :class="formStatus === 'draft' ? 'draft-submit' : (editingRecordId ? 'edit-submit' : 'publish-submit')">
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
          <p class="scan-empty-hint">Поддерживаются JPG, PNG</p>
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

    <!-- ══════════════ МОДАЛКИ СПРАВОЧНИКОВ ══════════════ -->
    <div v-if="modal.type === 'estate'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить сословие</h4>
        <div class="field"><label>Название</label><input type="text" v-model="modal.value" @keyup.enter="saveRef" autofocus /></div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">Отмена</button>
          <button class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>
    <div v-if="modal.type === 'kinship'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить степень родства</h4>
        <div class="field"><label>Название</label><input type="text" v-model="modal.value" placeholder="Например: сын" @keyup.enter="saveRef" autofocus /></div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">Отмена</button>
          <button class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>
    <div v-if="modal.type === 'clergy'" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-ref">
        <h4>Добавить степень духовенства</h4>
        <div class="field"><label>Название</label><input type="text" v-model="modal.value" placeholder="Например: Диакон" @keyup.enter="saveRef" autofocus /></div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">Отмена</button>
          <button class="btn-action" @click="saveRef" :disabled="!modal.value.trim()">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- ══════════════ ПОДТВЕРЖДЕНИЕ ПУБЛИКАЦИИ ══════════════ -->
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
        <p class="modal-text">Черновик успешно сохранён на сервере.</p>
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
        <p class="modal-text">Запись о смерти успешно опубликована и добавлена в основную базу данных.</p>
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
        <p class="modal-text">Запись о смерти и данные персоны успешно обновлены.</p>
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
  name: 'Death',

  data() {
    return {
      loading: false,
      error: null,
      formStatus: 'published',
      burialAuto: false,
      patronymicAuto: false,
      surnameAuto: false,
      showPublishAttempt: false,
      missingFieldsList: [],
      showPublishConfirm: false,
      showDraftSuccess: false,
      showPublishSuccess: false,
      showEditSuccess: false,
      currentDraftId: null,
      editingRecordId: null,
      existingPersonId: null,

      autoFilledFields: {
        archive: false,
        number_case: false,
        year: false,
        number_record: false,
      },

      // Возраст (4 поля)
      ageYears: null,
      ageMonths: null,
      ageWeeks: null,
      ageDays: null,

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
      provinces: [],
      yezds: [],
      volosts: [],
      villages: [],
      kinshipList: [],
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
        sex: '',
        kinship_id: '',
        death_month: '',
        death_day: '',
        burial_day: '',
        province_id: '',
        yezd_id: '',
        volost_id: '',
        village_id: '',
        estate_id: '',
        name: '',
        patronymic: '',
        surname: '',
        cause_of_death: '',
        burial_place: '',
        comment: '',
        age_years: null,
        age_months: null,
        age_weeks: null,
        age_days: null
      },

      relatives: [],
      priests: [],
      months: ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
    }
  },

  computed: {
    isEditMode() {
      return !!this.editingRecordId
    },

    submitButtonLabel() {
      if (this.loading) return 'Сохранение...'
      if (this.formStatus === 'draft') return 'Сохранить черновик'
      if (this.editingRecordId) return 'Сохранить изменения'
      return 'Опубликовать запись'
    },

    archiveDropItems() {
      const q = this.archiveSearch.toLowerCase().trim()
      if (!q) return this.allArchives
      return this.allArchives.filter(a => a.name.toLowerCase().includes(q) || (a.number_case || '').toLowerCase().includes(q))
    },
    archiveExactMatch() {
      return this.allArchives.some(a => a.name.toLowerCase() === this.archiveSearch.toLowerCase().trim())
    },

    provinceExactMatch() {
      return this.provinces.some(p => p.name.toLowerCase() === this.provinceSearch.toLowerCase().trim())
    },
    yezdExactMatch() {
      return this.yezds.some(y => y.name.toLowerCase() === this.yezdSearch.toLowerCase().trim())
    },
    volostExactMatch() {
      return this.volosts.some(v => v.name.toLowerCase() === this.volostSearch.toLowerCase().trim())
    },
    villageExactMatch() {
      return this.villages.some(v => v.name.toLowerCase() === this.villageSearch.toLowerCase().trim())
    },

    filteredProvinces() { return this.filterItems(this.provinces, this.provinceSearch, 'province_id') },
    filteredYezds()     { return this.filterItems(this.yezds,     this.yezdSearch,     'yezd_id') },
    filteredVolosts()   { return this.filterItems(this.volosts,   this.volostSearch,   'volost_id') },
    filteredVillages()  { return this.filterItems(this.villages,  this.villageSearch,  'village_id') },

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
    isChild() {
      const kinship = this.kinshipList.find(k => k.kinship_id === this.formData.kinship_id)
      if (!kinship) return false
      const name = kinship.name.toLowerCase()
      return ['сын', 'дочь', 'сынъ', 'дочька', 'дочка', 'сыночек', 'доченька'].includes(name)
    },
    firstRelativeWithName() {
      return this.relatives.find(r => r.name && r.name.trim().length >= 2)
    },
    firstRelativeWithSurname() {
      return this.relatives.find(r => r.surname && r.surname.trim().length >= 2)
    },
    selectedRelativeName() {
      const rel = this.firstRelativeWithName || this.firstRelativeWithSurname
      if (rel) return `${rel.name || ''} ${rel.patronymic || ''} ${rel.surname || ''}`.trim()
      return null
    },
    suggestedPatronymic() {
      if (!this.isChild) return ''
      const rel = this.firstRelativeWithName
      if (!rel || !this.formData.sex) return ''
      return this.formPatronymic(rel.name, this.formData.sex)
    },
    showPatronymicSuggestion() {
      return this.suggestedPatronymic &&
        !this.formData.patronymic &&
        !this.patronymicAuto &&
        this.formData.sex &&
        this.isChild &&
        this.relatives.length > 0
    },
    suggestedSurname() {
      const rel = this.firstRelativeWithSurname
      if (!rel || !this.formData.sex) return ''
      return this.formSurname(rel.surname, this.formData.sex)
    },
    showSurnameSuggestion() {
      return this.suggestedSurname &&
        !this.formData.surname &&
        !this.surnameAuto &&
        this.formData.sex &&
        this.relatives.length > 0
    }
  },

  watch: {
    relatives: {
      deep: true,
      handler() { 
        // Не вызываем автоматически, только по blur
      }
    },
    'formData.sex': {
      handler() { 
        this.suggestFromRelative() 
      }
    },
    'formData.kinship_id': {
      handler() {
        this.patronymicAuto = false
        this.suggestFromRelative()
      }
    },

    // Синхронизация возраста из UI в formData
    ageYears: { 
      handler(val) { 
        this.formData.age_years = val
      } 
    },
    ageMonths: { 
      handler(val) { 
        this.formData.age_months = val
      } 
    },
    ageWeeks: { 
      handler(val) { 
        this.formData.age_weeks = val
      } 
    },
    ageDays: { 
      handler(val) { 
        this.formData.age_days = val
      } 
    },

    // Синхронизация из formData в UI
    'formData.age_years': {
      handler(val) {
        if (val !== this.ageYears) {
          this.ageYears = val
        }
      }
    },
    'formData.age_months': {
      handler(val) {
        if (val !== this.ageMonths) {
          this.ageMonths = val
        }
      }
    },
    'formData.age_weeks': {
      handler(val) {
        if (val !== this.ageWeeks) {
          this.ageWeeks = val
        }
      }
    },
    'formData.age_days': {
      handler(val) {
        if (val !== this.ageDays) {
          this.ageDays = val
        }
      }
    }
  },

  async mounted() {
    const token = localStorage.getItem('access_token')
    if (!token) {
      this.$router.push('/')
      return
    }
    this.relatives = []
    this.priests = [this.emptyPriest()]
    await this.loadReferenceData()

    // Проверка на редактирование
    const editRecordData = localStorage.getItem('edit_record')
    if (editRecordData) {
      try {
        const editData = JSON.parse(editRecordData)
        if (editData.isEditing && editData.recordId && editData.recordType === 'death') {
          await this.loadRecordForEditing(editData.recordId)
          localStorage.removeItem('edit_record')
        }
      } catch (e) {
        console.error('Ошибка загрузки данных для редактирования:', e)
      }
    }

    // Загрузка черновика
    const raw = localStorage.getItem('death_draft')
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
        localStorage.removeItem('death_draft')
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
    // ══════════════════════════════════════════════════════════════
    // ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ (как в Birth)
    // ══════════════════════════════════════════════════════════════
    filterItems(list, search, idKey) {
      const q = (search || '').toLowerCase().trim()
      if (!q) return list
      return list.filter(item => item.name.toLowerCase().includes(q))
    },

    getLocationName(type) {
      const map = {
        province: { list: this.provinces, id: this.formData.province_id, key: 'province_id', search: this.provinceSearch },
        yezd:     { list: this.yezds,     id: this.formData.yezd_id,     key: 'yezd_id',     search: this.yezdSearch },
        volost:   { list: this.volosts,   id: this.formData.volost_id,   key: 'volost_id',   search: this.volostSearch },
        village:  { list: this.villages,  id: this.formData.village_id,  key: 'village_id',  search: this.villageSearch }
      }
      const m = map[type]
      if (!m || !m.id) return 'Начните вводить...'
      const found = m.list.find(i => i[m.key] === m.id)
      if (found) return found.name
      if (m.search) return m.search
      return 'Начните вводить...'
    },

    // ── Логика территориальных единиц (как в Birth) ───────────────
    onProvinceInput() {
      this.formData.province_id = null
      this.clearLocationError()
      this.provinceDropOpen = true
    },

    async closeProvinceDrop() {
      setTimeout(async () => {
        if (this.provinceDropOpen) this.provinceDropOpen = false
        const name = this.provinceSearch.trim()
        if (name && !this.formData.province_id) {
          const existing = this.provinces.find(p => p.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.province_id = existing.province_id
            this.provinceSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/provinces/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.provinces.push(newItem)
              this.formData.province_id = newItem.province_id
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
        this.formData.province_id = newItem.province_id
        this.provinceSearch = newItem.name
        this.provinceDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания губернии:', err) }
    },

    onYezdInput() {
      this.formData.yezd_id = null
      this.clearLocationError()
      this.yezdDropOpen = true
    },

    async closeYezdDrop() {
      setTimeout(async () => {
        if (this.yezdDropOpen) this.yezdDropOpen = false
        const name = this.yezdSearch.trim()
        if (name && !this.formData.yezd_id) {
          const existing = this.yezds.find(y => y.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.yezd_id = existing.yezd_id
            this.yezdSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/yezds/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.yezds.push(newItem)
              this.formData.yezd_id = newItem.yezd_id
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
        this.formData.yezd_id = newItem.yezd_id
        this.yezdSearch = newItem.name
        this.yezdDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания уезда:', err) }
    },

    onVolostInput() {
      this.formData.volost_id = null
      this.clearLocationError()
      this.volostDropOpen = true
    },

    async closeVolostDrop() {
      setTimeout(async () => {
        if (this.volostDropOpen) this.volostDropOpen = false
        const name = this.volostSearch.trim()
        if (name && !this.formData.volost_id) {
          const existing = this.volosts.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.volost_id = existing.volost_id
            this.volostSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/volosts/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.volosts.push(newItem)
              this.formData.volost_id = newItem.volost_id
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
        this.formData.volost_id = newItem.volost_id
        this.volostSearch = newItem.name
        this.volostDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания волости:', err) }
    },

    onVillageInput() {
      this.formData.village_id = null
      this.clearLocationError()
      this.villageDropOpen = true
    },

    async closeLocationDrop() {
      setTimeout(async () => {
        if (this.villageDropOpen) this.villageDropOpen = false
        const name = this.villageSearch.trim()
        if (name && !this.formData.village_id) {
          const existing = this.villages.find(v => v.name.toLowerCase() === name.toLowerCase())
          if (existing) {
            this.formData.village_id = existing.village_id
            this.villageSearch = existing.name
          } else {
            try {
              const newItem = await api('/api/villages/', {
                method: 'POST', headers: authHeaders(true),
                body: JSON.stringify({ name })
              })
              this.villages.push(newItem)
              this.formData.village_id = newItem.village_id
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
        this.formData.village_id = newItem.village_id
        this.villageSearch = newItem.name
        this.villageDropOpen = false
        this.clearLocationError()
      } catch (err) { console.error('Ошибка создания населенного пункта:', err) }
    },

    selectProvince(p) { 
      this.formData.province_id = p.province_id
      this.provinceSearch = p.name
      this.provinceDropOpen = false
      this.clearLocationError()
    },
    selectYezd(y) { 
      this.formData.yezd_id = y.yezd_id
      this.yezdSearch = y.name
      this.yezdDropOpen = false
      this.clearLocationError()
    },
    selectVolost(v) { 
      this.formData.volost_id = v.volost_id
      this.volostSearch = v.name
      this.volostDropOpen = false
      this.clearLocationError()
    },
    selectVillage(v) { 
      this.formData.village_id = v.village_id
      this.villageSearch = v.name
      this.villageDropOpen = false
      this.clearLocationError()
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

    // ── Возраст ─────────────────────────────────────────────────────
    syncAgeToFormData() {
      this.formData.age_years = this.ageYears
      this.formData.age_months = this.ageMonths
      this.formData.age_weeks = this.ageWeeks
      this.formData.age_days = this.ageDays
    },

    parseAgeFromRecord(record) {
      if (record.age_years !== undefined && record.age_years !== null) {
        this.ageYears = record.age_years
        this.formData.age_years = record.age_years
      } else if (record.age !== undefined && record.age !== null) {
        this.ageYears = record.age
        this.formData.age_years = record.age
      } else {
        this.ageYears = null
        this.formData.age_years = null
      }
      
      if (record.age_months !== undefined && record.age_months !== null) {
        this.ageMonths = record.age_months
        this.formData.age_months = record.age_months
      } else {
        this.ageMonths = null
        this.formData.age_months = null
      }
      
      if (record.age_weeks !== undefined && record.age_weeks !== null) {
        this.ageWeeks = record.age_weeks
        this.formData.age_weeks = record.age_weeks
      } else {
        this.ageWeeks = null
        this.formData.age_weeks = null
      }
      
      if (record.age_days !== undefined && record.age_days !== null) {
        this.ageDays = record.age_days
        this.formData.age_days = record.age_days
      } else {
        this.ageDays = null
        this.formData.age_days = null
      }
    },

    // ── Остальные методы ──────────────────────────────────────────
    emptyRelative() {
      return { name: '', patronymic: '', surname: '' }
    },
    addRelative() { 
      this.relatives.push(this.emptyRelative()) 
    },
    
    onRelativeBlur() {
      this.suggestFromRelative()
    },

    emptyPriest() {
      return {
        searchText: '', dropOpen: false, dropItems: [],
        church_worker_id: null, name: '', surname: '', patronymic: '', clergy_id: ''
      }
    },
    addPriest() { this.priests.push(this.emptyPriest()) },

    onPriestSearch(i) {
      const p = this.priests[i]
      const q = (p.searchText || '').toLowerCase().trim()
      if (p.church_worker_id) this.unlinkChurchWorker(i)
      if (!q) { p.dropItems = []; p.dropOpen = false; return }
      p.dropItems = this.allChurchWorkers.filter(cw =>
        (cw.surname || '').toLowerCase().includes(q) ||
        (cw.name || '').toLowerCase().includes(q)
      ).slice(0, 10)
      p.dropOpen = true
    },
    closePriestDrop(i) {
      setTimeout(() => { this.priests[i].dropOpen = false }, 200)
    },
    selectChurchWorker(i, cw) {
      const p = this.priests[i]
      p.church_worker_id = cw.pries_id
      p.name = cw.name
      p.surname = cw.surname
      p.patronymic = cw.patronymic || ''
      p.clergy_id = cw.clergy_id ?? cw.clergy?.clergy_id ?? ''
      p.searchText = `${cw.surname} ${cw.name}${cw.patronymic ? ' ' + cw.patronymic : ''}`
      p.dropOpen = false
      p.dropItems = []
    },
    unlinkChurchWorker(i) {
      const p = this.priests[i]
      p.church_worker_id = null
      p.name = ''
      p.surname = ''
      p.patronymic = ''
      p.clergy_id = ''
    },

    switchToDraft() {
      this.formStatus = 'draft'
      this.showPublishAttempt = false
      this.missingFieldsList = []
      this.error = null
    },
    switchToPublish() { this.formStatus = 'published' },

    onKinshipChange() {
      if (!this.formData.patronymic) this.patronymicAuto = false
      this.suggestFromRelative()
    },

    suggestFromRelative() {
      if (!this.formData.surname && !this.surnameAuto && this.formData.sex) {
        const rel = this.firstRelativeWithSurname
        if (rel && rel.surname && rel.surname.trim().length >= 2) {
          const suggested = this.formSurname(rel.surname.trim(), this.formData.sex)
          if (suggested && suggested !== this.formData.surname) {
            this.formData.surname = suggested
            this.surnameAuto = true
          }
        }
      }
      if (this.isChild && !this.formData.patronymic && !this.patronymicAuto && this.formData.sex) {
        const rel = this.firstRelativeWithName
        if (rel && rel.name && rel.name.trim().length >= 2) {
          const suggested = this.formPatronymic(rel.name.trim(), this.formData.sex)
          if (suggested && suggested !== this.formData.patronymic) {
            this.formData.patronymic = suggested
            this.patronymicAuto = true
          }
        }
      }
      this.$forceUpdate()
    },

    onSexChange() {
      if (!this.formData.patronymic) this.patronymicAuto = false
      if (!this.formData.surname) this.surnameAuto = false
      
      let sexValue = this.formData.sex
      if (sexValue === 'Мужской') sexValue = 'М'
      if (sexValue === 'Женский') sexValue = 'Ж'
      if (sexValue === 'мужской') sexValue = 'М'
      if (sexValue === 'женский') sexValue = 'Ж'
      this.formData.sex = sexValue
      
      this.formData.number_record = this.formData.sex === 'М'
        ? this.numberRecordMale
        : (this.formData.sex === 'Ж' ? this.numberRecordFemale : '')
      this.suggestFromRelative()
    },

    acceptPatronymicSuggestion() {
      this.formData.patronymic = this.suggestedPatronymic
      this.patronymicAuto = true
    },
    acceptSurnameSuggestion() {
      this.formData.surname = this.suggestedSurname
      this.surnameAuto = true
    },

    async loadReferenceData() {
      this.loading = true
      try {
        const h = authHeaders()
        const [archives, estates, provinces, yezds, volosts, villages, churchWorkers, kinship, clergy] = await Promise.all([
          api('/api/archives/', { headers: h }),
          api('/api/estates/', { headers: h }),
          api('/api/provinces/', { headers: h }),
          api('/api/yezds/', { headers: h }),
          api('/api/volosts/', { headers: h }),
          api('/api/villages/', { headers: h }),
          api('/api/church-workers/', { headers: h }),
          api('/api/kinship/', { headers: h }).catch(() => []),
          api('/api/clergy/', { headers: h })
        ])
        this.allArchives = archives || []
        this.estates = estates || []
        this.provinces = provinces || []
        this.yezds = yezds || []
        this.volosts = volosts || []
        this.villages = villages || []
        this.allChurchWorkers = churchWorkers || []
        this.kinshipList = kinship || []
        this.clergyList = clergy || []
      } catch (err) {
        this.error = 'Ошибка загрузки справочников: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadRecordForEditing(recordId) {
      this.loading = true
      try {
        const headers = authHeaders()
        const record = await api(`/api/death-records/${recordId}/`, { headers })
        if (!record) throw new Error('Запись не найдена')

        this.editingRecordId = recordId
        this.formStatus = 'published'

        if (record.person) {
          this.existingPersonId = record.person
        }

        const archiveId = record.archive
        if (archiveId) {
          this.formData.archive_id = archiveId
          let foundArchive = this.allArchives.find(a => a.archive_id === archiveId)
          if (foundArchive) {
            this.archiveSearch = foundArchive.name
            this.formData.number_case = foundArchive.number_case || ''
            this.formData.year = foundArchive.year || ''
          } else {
            try {
              const archiveData = await api(`/api/archives/${archiveId}/`, { headers })
              this.archiveSearch = archiveData.name || ''
              this.formData.number_case = archiveData.number_case || ''
              this.formData.year = archiveData.year || ''
              this.allArchives.push(archiveData)
            } catch {
              this.archiveSearch = record.archive_name || ''
            }
          }
        }

        this.formData.page = record.page || ''
        this.formData.page_turn = record.page_turn || false
        this.formData.number_record = record.number_record || ''
        this.formData.sex = record.sex || ''
        this.formData.death_month = record.death_month || ''
        this.formData.death_day = record.death_day || ''
        this.formData.burial_day = record.burial_day || ''
        this.formData.cause_of_death = record.cause_of_death || ''
        this.formData.burial_place = record.burial_place || ''
        this.formData.comment = record.comment || ''

        if (record.date) {
          const dateParts = record.date.split('-')
          if (dateParts.length === 3) {
            this.formData.year = parseInt(dateParts[0])
            this.formData.death_month = parseInt(dateParts[1])
            this.formData.death_day = parseInt(dateParts[2])
          }
        }

        // Возраст
        this.parseAgeFromRecord(record)

        // Локации
        this.formData.province_id = record.province || null
        if (record.province) {
          const found = this.provinces.find(p => p.province_id === record.province)
          this.provinceSearch = found ? found.name : (record.province_name || '')
        } else {
          this.provinceSearch = ''
        }

        this.formData.yezd_id = record.yezd || null
        if (record.yezd) {
          const found = this.yezds.find(y => y.yezd_id === record.yezd)
          this.yezdSearch = found ? found.name : (record.yezd_name || '')
        } else {
          this.yezdSearch = ''
        }

        this.formData.volost_id = record.volost || null
        if (record.volost) {
          const found = this.volosts.find(v => v.volost_id === record.volost)
          this.volostSearch = found ? found.name : (record.volost_name || '')
        } else {
          this.volostSearch = ''
        }

        this.formData.village_id = record.village || null
        if (record.village) {
          const found = this.villages.find(v => v.village_id === record.village)
          this.villageSearch = found ? found.name : (record.village_name || '')
        } else {
          this.villageSearch = ''
        }

        this.formData.estate_id = record.estate || null
        this.formData.kinship_id = record.kinship || null

        if (record.person_data) {
          this.formData.name = record.person_data.name || ''
          this.formData.surname = record.person_data.surname || ''
          this.formData.patronymic = record.person_data.patronymic || ''
          this.existingPersonId = record.person_data.person_id
        } else if (record.person && typeof record.person === 'object') {
          this.formData.name = record.person.name || ''
          this.formData.surname = record.person.surname || ''
          this.formData.patronymic = record.person.patronymic || ''
          this.existingPersonId = record.person.person_id
        }

        if (record.number_record) {
          this.formData.number_record = record.number_record
          if (record.sex === 'М') this.numberRecordMale = record.number_record
          else if (record.sex === 'Ж') this.numberRecordFemale = record.number_record
        }

        if (record.relatives && record.relatives.length) {
          this.relatives = record.relatives.map(r => ({
            name: r.name || '',
            patronymic: r.patronymic || '',
            surname: r.surname || ''
          }))
        } else {
          this.relatives = []
        }

        if (record.priests && record.priests.length) {
          this.priests = record.priests.map(p => ({
            searchText: `${p.surname || ''} ${p.name || ''}`.trim(),
            dropOpen: false,
            dropItems: [],
            church_worker_id: p.church_worker?.pries_id || null,
            name: p.name || '',
            surname: p.surname || '',
            patronymic: p.patronymic || '',
            clergy_id: p.clergy?.clergy_id || null
          }))
        } else {
          this.priests = [this.emptyPriest()]
        }

        this.scanSrc = null
        const possibleExts = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
        for (const ext of possibleExts) {
          const scanUrl = `${API_BASE}/media/scans/death/${this.editingRecordId}${ext}`
          try {
            const response = await fetch(scanUrl, { method: 'HEAD' })
            if (response.ok) { this.scanSrc = scanUrl; break }
          } catch { }
        }

        this.showPublishAttempt = false
        this.missingFieldsList = []
        this.error = null
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
      }
      if (draftData.ageYears !== undefined) this.ageYears = draftData.ageYears
      if (draftData.ageMonths !== undefined) this.ageMonths = draftData.ageMonths
      if (draftData.ageWeeks !== undefined) this.ageWeeks = draftData.ageWeeks
      if (draftData.ageDays !== undefined) this.ageDays = draftData.ageDays
      if (draftData.numberRecordMale) this.numberRecordMale = draftData.numberRecordMale
      if (draftData.numberRecordFemale) this.numberRecordFemale = draftData.numberRecordFemale
      if (draftData.archiveSearch) this.archiveSearch = draftData.archiveSearch
      if (draftData.provinceSearch !== undefined) this.provinceSearch = draftData.provinceSearch || ''
      if (draftData.yezdSearch !== undefined) this.yezdSearch = draftData.yezdSearch || ''
      if (draftData.volostSearch !== undefined) this.volostSearch = draftData.volostSearch || ''
      if (draftData.villageSearch !== undefined) this.villageSearch = draftData.villageSearch || ''
      if (draftData.scanSrc) this.scanSrc = draftData.scanSrc
      if (draftData.relatives?.length) {
        this.relatives = draftData.relatives.map(r => ({ ...r }))
      }
      if (draftData.priests?.length) {
        this.priests = draftData.priests.map(p => ({
          ...this.emptyPriest(), ...p,
          dropOpen: false, dropItems: []
        }))
      }
      
      // Синхронизация возраста из черновика в formData
      if (this.ageYears !== undefined) this.formData.age_years = this.ageYears
      if (this.ageMonths !== undefined) this.formData.age_months = this.ageMonths
      if (this.ageWeeks !== undefined) this.formData.age_weeks = this.ageWeeks
      if (this.ageDays !== undefined) this.formData.age_days = this.ageDays
    },

    checkLocation() {
      return !!(
        this.formData.province_id || this.formData.yezd_id ||
        this.formData.volost_id || this.formData.village_id ||
        (this.provinceSearch && this.provinceSearch.trim()) ||
        (this.yezdSearch && this.yezdSearch.trim()) ||
        (this.volostSearch && this.volostSearch.trim()) ||
        (this.villageSearch && this.villageSearch.trim())
      )
    },

    showFieldError(fieldName) {
      if (this.formStatus !== 'published') return false
      if (!this.showPublishAttempt) return false
      if (fieldName === 'location') return !this.checkLocation()
      return this.missingFieldsList.includes(fieldName)
    },

    isFieldMissing(fieldName) {
      if (fieldName === 'location') return !this.checkLocation()
      const value = this.formData[fieldName]
      const isEmpty = value === null || value === undefined || value === '' || value === 0
      const requiredFields = ['number_case', 'year', 'page', 'number_record', 'death_month', 'death_day', 'sex', 'name', 'surname', 'kinship_id']
      if (!requiredFields.includes(fieldName)) return false
      if (fieldName === 'number_case' && this.formData.archive_id && this.archiveSearch.trim()) return false
      if (fieldName === 'year' && this.formData.archive_id && this.archiveSearch.trim()) return false
      return isEmpty
    },

    validateAllFields() {
      const requiredFields = ['number_case', 'year', 'page', 'number_record', 'death_month', 'death_day', 'sex', 'name', 'surname', 'kinship_id', 'location']
      const missing = []
      for (const field of requiredFields) {
        if (this.isFieldMissing(field)) missing.push(field)
      }
      this.missingFieldsList = missing
      this.showPublishAttempt = true
      if (missing.length > 0) {
        this.error = `Необходимо заполнить ${missing.length} обязательное(ых) поле(й)`
        setTimeout(() => {
          const firstError = document.querySelector('.field-error')
          if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }, 100)
        return false
      }
      this.error = null
      return true
    },

    onArchiveInput() {
      this.archiveDropOpen = true
      this.formData.archive_id = null
      this.formData.number_case = ''
      this.formData.year = ''
      this.autoFilledFields = { archive: false, number_case: false, year: false, number_record: false }
    },
    closeArchiveDrop() { setTimeout(() => { this.archiveDropOpen = false }, 200) },

    async selectArchive(archive) {
      this.formData.archive_id = archive.archive_id
      this.archiveSearch = archive.name
      this.formData.number_case = archive.number_case
      this.formData.year = archive.year
      this.autoFilledFields.number_case = true
      this.autoFilledFields.year = true
      this.autoFilledFields.archive = true
      this.archiveDropOpen = false
      await this.fetchLastRecords(archive.archive_id)
    },

    prepareNewArchive() {
      this.formData.archive_id = null
      this.archiveDropOpen = false
      this.formData.number_case = ''
      this.formData.year = ''
      this.autoFilledFields = { archive: false, number_case: false, year: false, number_record: false }
    },

    async fetchLastRecords(archiveId) {
      if (!archiveId) return
      try {
        const [lastMale, lastFemale] = await Promise.all([
          api(`/api/death-records/last/?archive_id=${archiveId}&sex=М`, { headers: authHeaders() }).catch(() => null),
          api(`/api/death-records/last/?archive_id=${archiveId}&sex=Ж`, { headers: authHeaders() }).catch(() => null)
        ])
        if (lastMale && lastMale.number_record) {
          this.numberRecordMale = lastMale.number_record + 1
          this.autoFilledFields.number_record = true
        }
        if (lastFemale && lastFemale.number_record) {
          this.numberRecordFemale = lastFemale.number_record + 1
          this.autoFilledFields.number_record = true
        }
      } catch (_) {}
    },

    updateNumberRecord() {
      if (this.formData.sex === 'М') this.numberRecordMale = this.formData.number_record
      else if (this.formData.sex === 'Ж') this.numberRecordFemale = this.formData.number_record
    },

    autoBurialDay() {
      const d = parseInt(this.formData.death_day)
      if (!isNaN(d) && d >= 1 && d <= 31) { this.formData.burial_day = Math.min(d + 2, 31); this.burialAuto = true }
      else { this.burialAuto = false }
    },

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
      if (specialCases[fatherName]) return sex === 'М' ? specialCases[fatherName].male : specialCases[fatherName].female
      let base = fatherName
      const lastChar = fatherName.slice(-1), lastTwoChars = fatherName.slice(-2)
      if (lastTwoChars === 'ий' || lastTwoChars === 'ый' || lastTwoChars === 'ой') base = fatherName.slice(0, -2)
      else if (lastChar === 'й' || lastChar === 'ь') base = fatherName.slice(0, -1)
      else if (lastChar === 'а' || lastChar === 'я') base = fatherName.slice(0, -1)
      const softConsonants = ['ч', 'щ', 'ж', 'ш']
      if (softConsonants.includes(base.slice(-1))) return sex === 'М' ? base + 'евич' : base + 'евна'
      const suffix = sex === 'М' ? 'ович' : 'овна'
      return base + suffix
    },

    formSurname(fatherSurname, sex) {
      if (!fatherSurname) return ''
      const immutable = ['Черных', 'Хохол', 'Дурень', 'Корень', 'Бездетко', 'Нетудыхата']
      const surnameStr = String(fatherSurname).trim()
      if (immutable.includes(surnameStr)) return surnameStr
      
      if (surnameStr.match(/(ов|ев|ин|ын)$/i)) {
        if (sex === 'Ж') {
          return surnameStr + 'а'
        }
        return surnameStr
      }
      
      if (surnameStr.match(/(ова|ева|ина|ына)$/i)) {
        return surnameStr
      }
      
      if (surnameStr.match(/(ский|цкий)$/i)) {
        if (sex === 'Ж') return surnameStr.replace(/ий$/i, 'ая')
        return surnameStr
      }
      
      if (surnameStr.match(/(ская|цкая)$/i)) {
        return surnameStr
      }
      
      if (surnameStr.match(/ой$/i)) {
        if (sex === 'Ж') return surnameStr.replace(/ой$/i, 'ая')
        return surnameStr
      }
      
      const vowels = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']
      const lastChar = surnameStr.slice(-1).toLowerCase()
      if (!vowels.includes(lastChar) && sex === 'Ж') {
        return surnameStr + 'а'
      }
      return surnameStr
    },

    openModal(type) { this.modal = { type, value: '' } },
    closeModal() { this.modal = { type: null, value: '' } },

    async saveRef() {
      if (!this.modal.value.trim()) return
      try {
        if (this.modal.type === 'estate') {
          const result = await api('/api/estates/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.estates.push(result); this.formData.estate_id = result.estate_id
        }
        if (this.modal.type === 'kinship') {
          const result = await api('/api/kinship/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.kinshipList.push(result)
        }
        if (this.modal.type === 'clergy') {
          const result = await api('/api/clergy/', { method: 'POST', headers: authHeaders(true), body: JSON.stringify({ name: this.modal.value.trim() }) })
          this.clergyList.push(result)
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
      this._onMouseUp = () => { this.isDragging = false; document.removeEventListener('mousemove', this._onMouseMove); document.removeEventListener('mouseup', this._onMouseUp) }
      document.addEventListener('mousemove', this._onMouseMove)
      document.addEventListener('mouseup', this._onMouseUp)
    },
    onWheel(e) { if (!this.scanSrc) return; const delta = e.deltaY < 0 ? 0.15 : -0.15; this.zoom = Math.min(8, Math.max(0.2, Math.round((this.zoom + delta) * 100) / 100)) },
    zoomIn() { this.zoom = Math.min(8, Math.round((this.zoom + 0.25) * 100) / 100) },
    zoomOut() { this.zoom = Math.max(0.2, Math.round((this.zoom - 0.25) * 100) / 100) },
    resetScan() { this.zoom = 1; this.panX = 0; this.panY = 0 },

    async handleSubmit() {
      if (this.formStatus === 'draft') {
        await this.saveServerDraft()
      } else {
        const isValid = this.validateAllFields()
        if (!isValid) return
        
        if (this.editingRecordId) {
          await this.saveEditedRecord()
        } else {
          this.showPublishConfirm = true
        }
      }
    },

    async confirmPublish() {
      this.showPublishConfirm = false
      await this.saveDeathRecord()
    },

    closeDraftSuccess() { this.showDraftSuccess = false; this.$router.push('/home') },
    closePublishSuccess() { this.showPublishSuccess = false; this.$router.push('/home') },
    closeEditSuccess() { this.showEditSuccess = false; this.$router.push('/home') },

    async saveServerDraft() {
      this.error = null; this.loading = true
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
          method,
          headers: authHeaders(true),
          body: JSON.stringify({ record_type: 'death', payload })
        })
        this.showDraftSuccess = true
      } catch (err) {
        this.error = 'Ошибка сохранения черновика: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.loading = false
      }
    },

    buildFullPayload() {
      return {
        formData: { ...this.formData },
        ageYears: this.ageYears,
        ageMonths: this.ageMonths,
        ageWeeks: this.ageWeeks,
        ageDays: this.ageDays,
        archiveSearch: this.archiveSearch,
        provinceSearch: this.provinceSearch,
        yezdSearch: this.yezdSearch,
        volostSearch: this.volostSearch,
        villageSearch: this.villageSearch,
        numberRecordMale: this.numberRecordMale,
        numberRecordFemale: this.numberRecordFemale,
        autoFilledFields: this.autoFilledFields,
        relatives: this.relatives.map(r => ({ ...r })),
        priests: this.priests.map(p => ({ ...p, dropOpen: false, dropItems: [] }))
      }
    },

    async saveDeathRecord() {
      this.error = null
      this.loading = true
      try {
        const H = authHeaders(true)

        let sexValue = this.formData.sex
        if (sexValue === 'Мужской') sexValue = 'М'
        if (sexValue === 'Женский') sexValue = 'Ж'
        if (sexValue === 'мужской') sexValue = 'М'
        if (sexValue === 'женский') sexValue = 'Ж'
        
        if (!sexValue || (sexValue !== 'М' && sexValue !== 'Ж')) {
          const surname = this.formData.surname || ''
          if (surname.match(/[ая]$/i)) {
            sexValue = 'Ж'
          } else if (surname) {
            sexValue = 'М'
          } else {
            this.error = 'Пожалуйста, выберите пол (Мужской или Женский)'
            this.loading = false
            return
          }
        }

        this.formData.sex = sexValue

        if (!this.formData.name || this.formData.name.trim() === '') {
          this.error = 'Укажите имя умершего'
          this.loading = false
          return
        }
        if (!this.formData.surname || this.formData.surname.trim() === '') {
          this.error = 'Укажите фамилию умершего'
          this.loading = false
          return
        }
        if (!this.formData.death_month || !this.formData.death_day) {
          this.error = 'Укажите месяц и число смерти'
          this.loading = false
          return
        }
        if (!this.formData.year) {
          this.error = 'Укажите год смерти'
          this.loading = false
          return
        }

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

        const deathDate = `${this.formData.year}-${String(this.formData.death_month).padStart(2,'0')}-${String(this.formData.death_day).padStart(2,'0')}`

        // Синхронизируем возраст перед отправкой
        this.syncAgeToFormData()

        const deathRecordData = {
          archive: Number(archiveId),
          page: this.formData.page ? Number(this.formData.page) : null,
          page_turn: this.formData.page_turn || false,
          number_record: this.formData.number_record ? Number(this.formData.number_record) : null,
          sex: sexValue,
          date: deathDate,
          province: this.formData.province_id ? Number(this.formData.province_id) : null,
          yezd: this.formData.yezd_id ? Number(this.formData.yezd_id) : null,
          volost: this.formData.volost_id ? Number(this.formData.volost_id) : null,
          village: this.formData.village_id ? Number(this.formData.village_id) : null,
          death_month: this.formData.death_month ? Number(this.formData.death_month) : null,
          death_day: this.formData.death_day ? Number(this.formData.death_day) : null,
          burial_day: this.formData.burial_day ? Number(this.formData.burial_day) : null,
          estate: this.formData.estate_id ? Number(this.formData.estate_id) : null,
          age_years: this.formData.age_years ? Number(this.formData.age_years) : null,
          age_months: this.formData.age_months ? Number(this.formData.age_months) : null,
          age_weeks: this.formData.age_weeks ? Number(this.formData.age_weeks) : null,
          age_days: this.formData.age_days ? Number(this.formData.age_days) : null,
          cause_of_death: this.formData.cause_of_death || '',
          burial_place: this.formData.burial_place || '',
          comment: this.formData.comment || '',
          kinship: this.formData.kinship_id ? Number(this.formData.kinship_id) : null,
        }

        let deathId
        if (this.editingRecordId) {
          await api(`/api/death-records/${this.editingRecordId}/`, {
            method: 'PUT', headers: H,
            body: JSON.stringify(deathRecordData)
          })
          deathId = this.editingRecordId
          
          if (this.existingPersonId) {
            await api(`/api/persons/${this.existingPersonId}/`, {
              method: 'PUT', headers: H,
              body: JSON.stringify({
                name: this.formData.name || '',
                surname: this.formData.surname || '',
                patronymic: this.formData.patronymic || '',
                sex: sexValue,
                estate: this.formData.estate_id ? Number(this.formData.estate_id) : null,
                province: this.formData.province_id ? Number(this.formData.province_id) : null,
                yezd: this.formData.yezd_id ? Number(this.formData.yezd_id) : null,
                volost: this.formData.volost_id ? Number(this.formData.volost_id) : null,
                village: this.formData.village_id ? Number(this.formData.village_id) : null,
                comment: this.formData.comment || '',
              })
            })
          }
          
          try {
            const oldPriests = await api(`/api/death-record-priests/?death=${this.editingRecordId}`, { headers: H })
            if (oldPriests && oldPriests.length) {
              for (const p of oldPriests) {
                await api(`/api/death-record-priests/${p.id}/`, { method: 'DELETE', headers: H })
              }
            }
          } catch(e) {}
          
          if (this.existingPersonId) {
            try {
              const oldRelations = await api(`/api/relationships/?whom=${this.existingPersonId}`, { headers: H })
              if (oldRelations && oldRelations.length) {
                for (const rel of oldRelations) {
                  await api(`/api/relationships/${rel.relationship_id}/`, { method: 'DELETE', headers: H })
                }
              }
            } catch(e) {}
          }
          
        } else {
          const deathRecord = await api('/api/death-records/', {
            method: 'POST', headers: H,
            body: JSON.stringify(deathRecordData)
          })
          deathId = deathRecord.death_id || deathRecord.id

          const personData = {
            name: this.formData.name || '',
            surname: this.formData.surname || '',
            patronymic: this.formData.patronymic || '',
            sex: sexValue,
            date: null,
            estate: this.formData.estate_id ? Number(this.formData.estate_id) : null,
            creed: null,
            province: this.formData.province_id ? Number(this.formData.province_id) : null,
            yezd: this.formData.yezd_id ? Number(this.formData.yezd_id) : null,
            volost: this.formData.volost_id ? Number(this.formData.volost_id) : null,
            village: this.formData.village_id ? Number(this.formData.village_id) : null,
            duplicate: 0,
            comment: this.formData.comment || '',
          }

          const deceasedPerson = await api('/api/persons/', {
            method: 'POST', headers: H,
            body: JSON.stringify(personData)
          })
          this.existingPersonId = deceasedPerson.person_id

          await api(`/api/death-records/${deathId}/`, {
            method: 'PATCH', headers: H,
            body: JSON.stringify({ person: deceasedPerson.person_id })
          })
        }

        // Создаём родственников
        for (const r of this.relatives) {
          if (!r.name && !r.surname) continue
          
          let relativeSex = ''
          if (r.surname && r.surname.match(/[ая]$/i)) {
            relativeSex = 'Ж'
          } else if (r.surname) {
            relativeSex = 'М'
          }
          
          const relPerson = await api('/api/persons/', {
            method: 'POST', headers: H,
            body: JSON.stringify({
              name: r.name || '',
              surname: r.surname || '',
              patronymic: r.patronymic || '',
              sex: relativeSex,
              date: null,
              estate: null,
              creed: null,
              province: null,
              yezd: null,
              volost: null,
              village: null,
              duplicate: 0,
              comment: `Родственник из записи о смерти #${deathId}`
            })
          })
          
          if (this.formData.kinship_id) {
            await api('/api/relationships/', {
              method: 'POST', headers: H,
              body: JSON.stringify({
                who: this.existingPersonId,
                whom: relPerson.person_id,
                kinship: Number(this.formData.kinship_id),
              })
            }).catch(err => console.error('Ошибка создания родства:', err))
          }
        }

        for (const p of this.priests) {
          if (!p.name || !p.name.trim()) continue

          const priestData = {
            death: deathId,
            name: p.name || '',
            surname: p.surname || '',
            patronymic: p.patronymic || '',
            clergy: p.clergy_id ? Number(p.clergy_id) : null,
            church_worker: p.church_worker_id ? Number(p.church_worker_id) : null,
          }

          try {
            await api('/api/death-record-priests/', {
              method: 'POST', headers: H,
              body: JSON.stringify(priestData)
            })
          } catch (err) {
            console.error('Ошибка сохранения священника:', err)
          }
        }

        if (this.scanFile) {
          try {
            const fd = new FormData()
            fd.append('scan', this.scanFile)
            await fetch(`${API_BASE}/api/death-records/${deathId}/upload_scan/`, {
              method: 'POST',
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
              body: fd,
            })
          } catch (scanErr) { 
            console.error('Ошибка загрузки скана:', scanErr) 
          }
        }

        if (this.currentDraftId) {
          await fetch(`${API_BASE}/api/drafts/${this.currentDraftId}/`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          }).catch(() => {})
        }

        localStorage.removeItem('death_draft')
        
        if (this.editingRecordId) {
          this.showEditSuccess = true
        } else {
          this.showPublishSuccess = true
        }

      } catch (err) {
        console.error('Ошибка сохранения:', err)
        this.error = 'Ошибка сохранения: ' + err.message
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        this.loading = false
      }
    },

    async saveEditedRecord() {
      await this.saveDeathRecord()
    }
  }
}
</script>

<style scoped>
/* Стили для блока возраста */
.age-header {
  margin-bottom: 12px;
}
.age-label {
  font-size: 12px;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
  display: block;
}
.age-fields {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.age-field {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  padding: 4px 8px;
}
.age-field input {
  width: 60px;
  border: none;
  padding: 6px 0;
  text-align: center;
  font-size: 13px;
  -moz-appearance: textfield;
}
.age-field input::-webkit-outer-spin-button,
.age-field input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.age-field input:focus {
  outline: none;
}
.age-field span {
  font-size: 12px;
  color: #888;
  min-width: 32px;
}

@media (max-width: 600px) {
  .age-fields {
    flex-direction: column;
    gap: 8px;
  }
  .age-field {
    justify-content: space-between;
  }
  .age-field input {
    width: 80px;
  }
}

/* Остальные стили (сохраняем из оригинального Death) */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.death-layout {
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
.pub-dot { background: #22c55e; }

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
.req-star { color: #dc2626; font-size: 14px; }
.error-banner { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 6px 10px; border-radius: 6px; font-size: 12px; margin-top: 6px; }

.kinship-hint {
  font-size: 10px;
  color: #888;
  margin-top: 4px;
}

.info-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #e8f4ea;
  border: 1px solid #b6ddb9;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 12px;
  color: #2e7d42;
}
.hint-icon { font-size: 16px; }

.form-body { flex: 1; overflow-y: auto; padding: 16px 24px; }
.form-body::-webkit-scrollbar { width: 6px; }
.form-body::-webkit-scrollbar-track { background: #f0efee; }
.form-body::-webkit-scrollbar-thumb { background: #c8c5c0; border-radius: 3px; }

.block { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid #e9e7e3; }
.block:last-of-type { border-bottom: none; margin-bottom: 0; }
.block-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #888780; margin: 0 0 16px; }
.block-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.block-title-row .block-title { margin-bottom: 0; }

.location-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 14px; margin-bottom: 16px; }
.location-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.location-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #5f5e5a; }
.location-hint { font-size: 11px; color: #aaa; transition: color .2s; }
.location-hint.hint-error { color: #a00; font-weight: 600; }

.field { display: flex; flex-direction: column; gap: 4px; margin-bottom: 0; }
.field label { font-size: 12px; font-weight: 600; color: #444; }

.field input, .field select, .field textarea {
  padding: 8px 10px;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
  color: #1a1a1a;
  background: #fff;
  transition: border-color .15s, box-shadow .15s;
  width: 100%;
}
.field input:focus, .field select:focus, .field textarea:focus {
  outline: none;
  border-color: #888780;
  box-shadow: 0 0 0 3px rgba(136,135,128,0.12);
}
.field textarea { resize: vertical; min-height: 60px; }

.field input.auto, .field select.auto, .combo-input.auto {
  background: #fffbeb !important;
  border-color: #fde68a !important;
}
.auto-hint { font-size: 11px; color: #b45309; margin-top: 2px; }

.field-error { position: relative; }
.error-input { border-color: #dc2626 !important; background-color: #fef2f2 !important; }
.error-input:focus { border-color: #dc2626 !important; box-shadow: 0 0 0 3px rgba(220,38,38,0.1) !important; }
.error-message { font-size: 11px; color: #dc2626; margin-top: 2px; font-weight: 500; }

.row { display: grid; gap: 12px; margin-bottom: 12px; }
.row.two { grid-template-columns: 1fr 1fr; }
.row.three { grid-template-columns: 1fr 1fr 1fr; }
.full { margin-bottom: 12px; }

.checkbox-field { justify-content: flex-end; }
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #444;
  cursor: pointer;
  font-weight: 400 !important;
  padding: 8px 0;
}
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; }

.record-number-wrapper { display: flex; align-items: center; gap: 8px; }
.record-gender-badge {
  display: inline-block;
  padding: 4px 10px;
  background: #f0efee;
  border: 1px solid #d5d3cf;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #5f5e5a;
  white-space: nowrap;
  min-width: 90px;
  text-align: center;
}
.record-number-wrapper input { flex: 1; min-width: 0; }

.combobox-wrap { position: relative; }
.combo-input { width: 100%; }
.drop-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  z-index: 100;
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 4px 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.drop-item {
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-bottom: 1px solid #e9e7e3;
}
.drop-item:last-child { border-bottom: none; }
.drop-item:hover { background: #f0efee; }
.drop-main { font-size: 13px; color: #1a1a1a; }
.drop-sub { font-size: 11px; color: #aaa; }
.drop-new { color: #5f5e5a; font-size: 13px; border-top: 1px solid #e9e7e3 !important; }

.field-with-add { display: flex; gap: 6px; align-items: stretch; }
.field-with-add select, .field-with-add input { flex: 1; min-width: 0; }
.btn-add-ref {
  flex-shrink: 0;
  width: 32px;
  background: #fff;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  color: #5f5e5a;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .15s, border-color .15s;
}
.btn-add-ref:hover:not(:disabled) { background: #e9e7e3; border-color: #888780; }
.btn-add-ref:disabled { opacity: 0.35; cursor: not-allowed; }

.input-linked { background: #f2faf4; border-color: #b6ddb9; }
.readonly-input { background: #f0efee !important; color: #888 !important; cursor: default; }
.priest-linked-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  padding: 6px 10px;
  background: #f2faf4;
  border: 1px solid #b6ddb9;
  border-radius: 6px;
  font-size: 12px;
  color: #2e7d42;
}
.badge-icon { font-size: 13px; color: #2e7d42; flex-shrink: 0; }
.badge-unlink {
  margin-left: auto;
  background: none;
  border: none;
  font-size: 11px;
  color: #888;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  transition: background .15s, color .15s;
}
.badge-unlink:hover { background: #fef2f2; color: #a00; }

.sub-block { background: #f0efee; border: 1px solid #d5d3cf; border-radius: 8px; padding: 14px; margin-bottom: 12px; }
.sub-block-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.sub-block-header span { font-size: 12px; font-weight: 600; color: #888780; }
.btn-remove { background: none; border: none; cursor: pointer; font-size: 16px; color: #aaa; padding: 0 4px; line-height: 1; transition: color .15s; }
.btn-remove:hover { color: #a00; }
.btn-add-block {
  font-size: 12px;
  padding: 4px 12px;
  background: #fff;
  border: 1px solid #c8c5c0;
  border-radius: 6px;
  cursor: pointer;
  color: #5f5e5a;
  font-weight: 500;
  font-family: inherit;
  transition: all .15s;
}
.btn-add-block:hover { background: #e9e7e3; border-color: #888780; }

.suggestion-below {
  margin-top: 6px;
  padding: 8px 10px;
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}
.suggestion-below-text { color: #92400e; }
.suggestion-below-value { font-weight: 600; color: #b45309; }
.suggestion-below-button {
  background: #f59e0b;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 11px;
  cursor: pointer;
  transition: background 0.2s;
}
.suggestion-below-button:hover { background: #d97706; }

.form-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #d5d3cf;
  background: #fff;
  flex-shrink: 0;
}
.btn-submit {
  flex: 1;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background .15s;
}
.btn-submit.draft-submit:not(:disabled) { background: #f59e0b; color: #fff; }
.btn-submit.draft-submit:hover:not(:disabled) { background: #d97706; }
.btn-submit.publish-submit:not(:disabled) { background: #1a1a1a; color: #fff; }
.btn-submit.publish-submit:hover:not(:disabled) { background: #333; }
.btn-submit.edit-submit:not(:disabled) { background: #0369a1; color: #fff; }
.btn-submit.edit-submit:hover:not(:disabled) { background: #0284c7; }
.btn-submit:disabled { background: #ccc; color: #888; cursor: not-allowed; }

.scan-panel { flex: 1; display: flex; flex-direction: column; background: #2c2c2a; overflow: hidden; }
.scan-viewport {
  flex: 1;
  position: relative;
  overflow: hidden;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
}
.scan-viewport.grabbing { cursor: grabbing; }
.scan-inner { will-change: transform; }
.scan-inner img { display: block; max-width: none; pointer-events: none; }
.scan-empty { text-align: center; color: #888780; }
.scan-empty-icon { font-size: 48px; margin-bottom: 12px; opacity: 0.4; }
.scan-empty p { font-size: 14px; margin: 0 0 4px; }
.scan-empty-hint { font-size: 12px; color: #5f5e5a; }
.scan-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: rgba(0,0,0,0.5);
}
.scan-btn {
  width: 30px;
  height: 30px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 6px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .15s;
}
.scan-btn:hover:not(:disabled) { background: rgba(255,255,255,0.2); }
.scan-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.zoom-display { color: #aaa; font-size: 12px; min-width: 46px; text-align: center; }
.scan-upload-btn {
  margin-left: auto;
  padding: 6px 14px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 6px;
  color: #fff;
  font-size: 12px;
  cursor: pointer;
  transition: background .15s;
  font-family: inherit;
}
.scan-upload-btn:hover { background: rgba(255,255,255,0.2); }
.scan-status {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  padding: 4px 8px;
  background: rgba(34,197,94,0.2);
  border-radius: 6px;
  color: #22c55e;
  font-size: 11px;
}
.scan-status-icon { font-size: 14px; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
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
.modal.modal-ref h4 { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1a1a1a; }
.modal.modal-confirm { text-align: center; }
.modal.modal-confirm h4 { font-size: 1.7rem; font-weight: 600; margin-bottom: 12px; color: #222; }
.modal-icon { font-size: 52px; margin-bottom: 12px; }
.modal-text { font-size: 1rem; line-height: 1.4; color: #4b5563; margin-bottom: 24px; }
.modal-footer { display: flex; gap: 12px; justify-content: center; margin-top: 8px; }
.btn-cancel { background: #f1f5f9; color: #1e293b; border: none; padding: 8px 22px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; transition: all 0.2s; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-action { background: #1a1a1a; color: #fff; border: none; padding: 8px 22px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.15); transition: all 0.2s; }
.btn-action:hover:not(:disabled) { background: #333; transform: translateY(-1px); }
.btn-action:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-ok { background: #10b981; color: #fff; border: none; padding: 8px 28px; border-radius: 40px; font-size: 0.95rem; font-weight: 500; font-family: inherit; cursor: pointer; box-shadow: 0 2px 6px rgba(16,185,129,0.2); transition: all 0.2s; }
.btn-ok:hover { background: #059669; transform: translateY(-1px); }

@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(-12px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 900px) {
  .death-layout { flex-direction: column; }
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