<script setup>
import { reactive, ref, nextTick } from 'vue'
import { applyPhoneInput, applyPhonePaste, isValidRuPhone } from '../../utils/phone'
import { getIds, track } from '../../analytics/tracker'
import { company } from '../../data/company'

const props = defineProps({
  extended: { type: Boolean, default: false },
  buttonText: { type: String, default: 'Рассчитать стоимость' },
  /* служебный текст (например, конфигурация калькулятора), который
     прикладывается к комментарию при отправке */
  commentPrefix: { type: String, default: '' },
})

const form = reactive({
  name: '',
  phone: '',
  comment: '',
  drawing: 'yes',
  agree: true,
  fileName: '',
  website: '',
})

const sent = ref(false)
const sending = ref(false)
const error = ref('')
const phoneRef = ref(null)
const fileRef = ref(null)
const formStarted = ref(false)

function onFormStart() {
  if (formStarted.value) return
  formStarted.value = true
  track('form_start', { label: props.buttonText })
}

function onFile(e) {
  const f = e.target.files?.[0]
  form.fileName = f ? f.name : ''
}

function setDrawing(value) {
  form.drawing = value
  if (value === 'no') {
    form.fileName = ''
    if (fileRef.value) fileRef.value.value = ''
  }
}

function setPhone(value, cursor) {
  form.phone = value
  if (phoneRef.value && cursor != null) {
    nextTick(() => {
      phoneRef.value.setSelectionRange(cursor, cursor)
    })
  }
}

function onPhoneInput(e) {
  const { formatted, cursor } = applyPhoneInput(e.target, e.target.value)
  setPhone(formatted, cursor)
}

function onPhonePaste(e) {
  e.preventDefault()
  const input = e.target
  const pasted = e.clipboardData?.getData('text') ?? ''
  const { formatted, cursor } = applyPhonePaste(
    input.value,
    pasted,
    input.selectionStart ?? 0,
    input.selectionEnd ?? 0,
  )
  setPhone(formatted, cursor)
}

function onPhoneFocus(e) {
  if (!form.phone) {
    setPhone('+7', 2)
    return
  }
  // не даём курсору встать внутрь «+7»
  if ((e.target.selectionStart ?? 0) < 2) {
    nextTick(() => e.target.setSelectionRange(2, 2))
  }
}

function onPhoneKeydown(e) {
  const pos = e.target.selectionStart ?? 0
  const end = e.target.selectionEnd ?? 0

  if (e.key === 'Backspace' && pos <= 2 && end <= 2) {
    e.preventDefault()
    return
  }
  if (e.key === 'Delete' && pos < 2) {
    e.preventDefault()
  }
}

function onPhoneBlur() {
  if (form.phone === '+7') form.phone = ''
}

async function submit() {
  if (!isValidRuPhone(form.phone)) {
    error.value = 'Укажите телефон полностью — без него мы не сможем прислать расчёт.'
    return
  }
  if (props.extended && !form.agree) {
    error.value = 'Нужно согласие на обработку данных.'
    return
  }
  error.value = ''
  sending.value = true
  try {
    if (form.website) {
      sent.value = true
      return
    }
    const file = fileRef.value?.files?.[0] ?? null
    const payload = new FormData()
    payload.append('name', form.name)
    payload.append('phone', form.phone)
    payload.append('drawing', form.drawing)
    payload.append('comment', [props.commentPrefix, form.comment].filter(Boolean).join('\n\n'))
    payload.append('file_name', form.fileName)
    payload.append('source', window.location.pathname)
    const ids = getIds()
    payload.append('visitor_id', ids.visitorId)
    payload.append('session_id', ids.sessionId)
    if (file) payload.append('file', file)

    const res = await fetch('/api/leads', {
      method: 'POST',
      body: payload,
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    sent.value = true
    track('form_submit', { label: props.buttonText })
  } catch {
    error.value = 'submit-failed'
    track('form_error', { label: props.buttonText })
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <div class="lead-form">
    <transition name="swap" mode="out-in">
      <div v-if="sent" class="lf-success" key="ok">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 6 9 17l-5-5" />
        </svg>
        <p class="lf-success-title">Заявка принята</p>
        <p class="lf-success-text">
          Технолог посмотрит задачу и ответит в течение рабочего дня —
          с цифрами, а не с «нужно уточнить».
        </p>
      </div>

      <form v-else key="form" class="lf-form" @submit.prevent="submit" novalidate @focusin="onFormStart">
        <label class="lf-hp" aria-hidden="true">
          Сайт
          <input v-model="form.website" type="text" name="website" tabindex="-1" autocomplete="off" />
        </label>
        <input
          v-if="extended"
          v-model="form.name"
          class="field"
          type="text"
          placeholder="Имя"
          autocomplete="name"
        />
        <input
          ref="phoneRef"
          :value="form.phone"
          class="field"
          type="tel"
          inputmode="tel"
          placeholder="+7 (___) ___-__-__"
          autocomplete="tel"
          @input="onPhoneInput"
          @paste="onPhonePaste"
          @focus="onPhoneFocus"
          @keydown="onPhoneKeydown"
          @blur="onPhoneBlur"
        />

        <div class="lf-toggle" role="radiogroup" aria-label="Наличие чертежа">
          <button
            type="button"
            :class="{ active: form.drawing === 'yes' }"
            @click="setDrawing('yes')"
          >Есть чертёж</button>
          <button
            type="button"
            :class="{ active: form.drawing === 'no' }"
            @click="setDrawing('no')"
          >Нет чертежа</button>
        </div>

        <transition name="lf-file-reveal">
          <label v-if="form.drawing === 'yes'" class="lf-file" key="file">
            <input
              ref="fileRef"
              type="file"
              @change="onFile"
              accept=".pdf,.dwg,.dxf,.jpg,.png,.step,.stp"
            />
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" />
            </svg>
            <span>{{ form.fileName || 'Прикрепить чертёж или эскиз' }}</span>
          </label>
        </transition>

        <template v-if="extended">
          <textarea
            v-model="form.comment"
            class="field lf-textarea"
            rows="3"
            placeholder="Комментарий (необязательно)"
          ></textarea>

          <label class="lf-agree">
            <input type="checkbox" v-model="form.agree" />
            <span>
              Согласен на
              <a href="/docs/privacy-policy.html" target="_blank" rel="noopener">обработку персональных данных</a>
            </span>
          </label>
        </template>

        <p v-if="error" class="lf-error">
          <template v-if="error === 'submit-failed'">
            Не удалось отправить заявку.
            <a :href="company.phoneHref" data-track="tel-form-error">Позвоните {{ company.phone }}</a>
          </template>
          <template v-else>{{ error }}</template>
        </p>

        <button class="btn btn--block" type="submit" data-track="lead-submit" :disabled="sending">
          {{ sending ? 'Отправляем…' : buttonText }}
        </button>
        <p class="btn-note lf-note"><slot>Отвечаем в течение рабочего дня. Ни к чему не обязывает.</slot></p>
      </form>
    </transition>
  </div>
</template>

<style scoped>
.lead-form { width: 100%; }
.lf-form { position: relative; }
.lf-hp {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.field { margin-bottom: 12px; }
.lf-textarea { resize: vertical; min-height: 76px; }

.lf-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.lf-toggle button {
  flex: 1;
  padding: 12px 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-family: var(--font-m);
  font-size: 12.5px;
  transition: all 0.25s;
}
.lf-toggle button.active {
  background: var(--acc-dim);
  border-color: var(--acc);
  color: var(--acc-hot);
}

.lf-file {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 18px;
  margin-bottom: 12px;
  border: 1.5px dashed var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 13.5px;
  cursor: pointer;
  transition: border-color 0.25s, color 0.25s;
  overflow: hidden;
}
.lf-file:hover { border-color: var(--acc); color: var(--white); }
.lf-file input { display: none; }
.lf-file svg { width: 17px; height: 17px; flex-shrink: 0; }
.lf-file span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.lf-file-reveal-enter-active,
.lf-file-reveal-leave-active {
  transition: opacity 0.25s var(--ease), transform 0.25s var(--ease), max-height 0.25s var(--ease);
  overflow: hidden;
}
.lf-file-reveal-enter-from,
.lf-file-reveal-leave-to {
  opacity: 0;
  transform: translateY(-6px);
  max-height: 0;
  margin-bottom: 0;
}
.lf-file-reveal-enter-to,
.lf-file-reveal-leave-from {
  max-height: 80px;
}

.lf-agree {
  display: flex;
  align-items: center;
  gap: 9px;
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--w-faint);
  margin-bottom: 14px;
  cursor: pointer;
}
.lf-agree input { accent-color: var(--acc); width: 15px; height: 15px; }
.lf-agree a {
  color: var(--w-soft);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.lf-agree a:hover { color: var(--white); }

.lf-error {
  font-size: 13px;
  color: var(--acc-hot);
  margin-bottom: 12px;
}
.lf-error a {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.lf-note { text-align: center; }

.lf-success {
  text-align: center;
  padding: 26px 8px;
}
.lf-success svg {
  width: 52px;
  height: 52px;
  color: var(--ok);
  margin: 0 auto 16px;
  background: rgba(53, 201, 126, 0.12);
  border-radius: 50%;
  padding: 12px;
}
.lf-success-title {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.lf-success-text { font-size: 14px; color: var(--w-soft); }

.swap-enter-active, .swap-leave-active { transition: opacity 0.3s, transform 0.3s; }
.swap-enter-from { opacity: 0; transform: translateY(10px); }
.swap-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
