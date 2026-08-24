<script setup>
import { computed, nextTick, onUnmounted, ref, useAttrs } from 'vue'
import { company } from '../../data/company'
import { trackNow } from '../../analytics/tracker'

const props = defineProps({
  email: { type: String, default: '' },
  trackLabel: { type: String, default: 'mail' },
  subject: { type: String, default: '' },
})

defineOptions({ inheritAttrs: false })

const attrs = useAttrs()
const linkAttrs = computed(() => {
  const extra = { ...attrs }
  delete extra.href
  delete extra.onClick
  return extra
})

const to = props.email || company.email
const subject = props.subject || 'Запрос в ООО «Грэйдстрой»'
const open = ref(false)
const copied = ref(false)
const dialogEl = ref(null)

function composeUrl(provider) {
  const addr = encodeURIComponent(to)
  const su = encodeURIComponent(subject)
  if (provider === 'gmail') {
    return `https://mail.google.com/mail/?view=cm&fs=1&to=${addr}&su=${su}`
  }
  return `https://mail.yandex.ru/compose?to=${addr}&subject=${su}&subj=${su}`
}

function close() {
  open.value = false
  copied.value = false
  window.removeEventListener('keydown', onKey)
}

function onKey(e) {
  if (e.key === 'Escape') close()
}

function openPicker(e) {
  e.preventDefault()
  open.value = true
  copied.value = false
  window.addEventListener('keydown', onKey)
  nextTick(() => dialogEl.value?.querySelector('.ml-btn')?.focus())
}

function trackMail(provider, href) {
  trackNow('mail', {
    label: props.trackLabel,
    href,
    props: { provider },
  })
}

function onCompose(provider) {
  trackMail(provider, composeUrl(provider))
  setTimeout(close, 0)
}

async function copyAddress() {
  try {
    await navigator.clipboard.writeText(to)
  } catch {
    window.prompt('Скопируйте адрес:', to)
  }
  trackMail('copy', `mailto:${to}`)
  copied.value = true
  window.setTimeout(() => {
    copied.value = false
    close()
  }, 900)
}

onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <a
    v-bind="linkAttrs"
    :href="`mailto:${to}`"
    data-notrack
    @click="openPicker"
  >
    <slot>{{ to }}</slot>
  </a>

  <Teleport to="body">
    <div
      v-if="open"
      class="ml-back"
      data-notrack
      role="presentation"
      @click.self="close"
    >
      <div
        ref="dialogEl"
        class="ml-box"
        role="dialog"
        aria-modal="true"
        aria-labelledby="ml-title"
      >
        <button class="ml-x" type="button" aria-label="Закрыть" @click="close">✕</button>
        <p id="ml-title" class="ml-h">Куда открыть письмо?</p>
        <p class="ml-sub">
          Откроется новое письмо на
          <strong>{{ to }}</strong>
        </p>
        <div class="ml-actions">
          <a
            class="ml-btn ml-btn--g"
            :href="composeUrl('gmail')"
            target="_blank"
            rel="noopener noreferrer"
            @click="onCompose('gmail')"
          >
            Gmail
          </a>
          <a
            class="ml-btn ml-btn--y"
            :href="composeUrl('yandex')"
            target="_blank"
            rel="noopener noreferrer"
            @click="onCompose('yandex')"
          >
            Яндекс.Почта
          </a>
        </div>
        <button type="button" class="ml-copy" @click="copyAddress">
          {{ copied ? 'Адрес скопирован' : 'Скопировать адрес' }}
        </button>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.ml-back {
  position: fixed;
  inset: 0;
  z-index: 240;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(6, 8, 10, 0.62);
  backdrop-filter: blur(6px);
}

.ml-box {
  position: relative;
  width: min(420px, 100%);
  background: #11151a;
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 28px 24px 22px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.55);
  color: var(--white);
}

.ml-x {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  background: none;
  border: none;
  color: var(--w-faint);
  font-size: 14px;
}
.ml-x:hover { color: var(--white); }

.ml-h {
  font-family: var(--font-d);
  font-size: 17px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 8px;
  padding-right: 28px;
}

.ml-sub {
  font-size: 14px;
  color: var(--w-soft);
  line-height: 1.55;
  margin-bottom: 20px;
}
.ml-sub strong {
  color: var(--white);
  font-weight: 600;
  overflow-wrap: anywhere;
}

.ml-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.ml-btn {
  display: block;
  text-align: center;
  text-decoration: none;
  font-family: var(--font-m);
  font-size: 14px;
  font-weight: 600;
  padding: 14px 12px;
  border-radius: var(--r-sm);
  border: 1.5px solid var(--line-d);
  background: rgba(255, 255, 255, 0.04);
  color: var(--white);
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}
.ml-btn:hover { border-color: var(--acc); color: var(--acc-hot); }
.ml-btn--g:hover { border-color: #ea4335; color: #f28b82; }
.ml-btn--y:hover { border-color: #fc0; color: #ffe566; }

.ml-copy {
  display: block;
  width: 100%;
  margin-top: 12px;
  padding: 10px;
  background: none;
  border: none;
  font-size: 13px;
  color: var(--w-faint);
  text-decoration: underline;
  text-underline-offset: 3px;
}
.ml-copy:hover { color: var(--white); }

@media (max-width: 480px) {
  .ml-actions { grid-template-columns: 1fr; }
}
</style>
