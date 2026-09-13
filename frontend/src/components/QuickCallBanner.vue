<script setup>
import { company } from '../data/company'
import MailLink from './ui/MailLink.vue'

defineProps({
  /** When true — compact block for embedding under hero content */
  embedded: { type: Boolean, default: false },
})
</script>

<template>
  <section
    :id="embedded ? undefined : 'quick-call'"
    class="qcb-wrap"
    :class="{ 'qcb-wrap--embedded': embedded }"
    aria-label="Быстрая связь"
  >
    <div :class="embedded ? undefined : 'container'">
      <div class="qcb" v-reveal>
        <div class="qcb-left">
          <p class="qcb-kicker">Звоните прямо сейчас!</p>
          <p class="qcb-text">
            По телефону назовём примерные сроки и стоимость производства,
            а после точечно посчитаем КП
          </p>
        </div>

        <div class="qcb-contact">
          <a :href="company.phoneHref" class="qcb-phone" data-track="tel-banner">{{ company.phone }}</a>
          <span class="qcb-mail-wrap">
            <MailLink track-label="mail-banner-addr">{{ company.email }}</MailLink>
          </span>
        </div>

        <div class="qcb-mail-cta">
          <MailLink track-label="mail-banner">
            <span class="qcb-mail-ico" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M3.5 7.2h17c.8 0 1.5.7 1.5 1.5v9.6c0 .8-.7 1.5-1.5 1.5h-17c-.8 0-1.5-.7-1.5-1.5V8.7c0-.8.7-1.5 1.5-1.5Z"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <path
                  d="m3.8 8.6 8.2 6 8.2-6"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
            <span class="qcb-mail-label">Написать письмо</span>
          </MailLink>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.qcb-wrap {
  background: var(--bg1);
  padding: 34px 0;
  border-bottom: 1px solid var(--line-d);
}

.qcb-wrap--embedded {
  background: transparent;
  padding: 0;
  border: none;
  margin-top: 36px;
  width: 100%;
}

.qcb {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  flex-wrap: wrap;
  border: 1.5px solid color-mix(in srgb, var(--acc) 45%, transparent);
  background:
    repeating-linear-gradient(-45deg, transparent 0 18px, rgba(255, 90, 31, 0.04) 18px 36px),
    var(--card-d);
  border-radius: var(--r);
  padding: 26px 34px;
}

.qcb-wrap--embedded .qcb {
  background:
    repeating-linear-gradient(-45deg, transparent 0 18px, rgba(255, 90, 31, 0.05) 18px 36px),
    rgba(17, 21, 26, 0.86);
  backdrop-filter: blur(14px);
}

.qcb-kicker {
  font-family: var(--font-m);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc-hot);
  margin-bottom: 8px;
}

.qcb-text {
  font-size: 14.5px;
  color: var(--w-soft);
  max-width: 420px;
  line-height: 1.55;
}

.qcb-contact {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.qcb-phone {
  font-family: var(--font-m);
  font-size: clamp(22px, 2.6vw, 30px);
  font-weight: 600;
  color: var(--white);
  white-space: nowrap;
  transition: color 0.2s;
}
.qcb-phone:hover { color: var(--acc-hot); }

.qcb-mail-wrap :deep(a) {
  font-family: var(--font-m);
  font-size: 13px;
  color: var(--w-soft);
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s;
  word-break: break-all;
}
.qcb-mail-wrap :deep(a:hover) { color: var(--acc-hot); }

.qcb-mail-cta :deep(a) {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 22px 14px 16px;
  background: var(--acc);
  color: #fff;
  text-decoration: none;
  font-family: var(--font-m);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
  box-shadow: 0 12px 28px rgba(255, 90, 31, 0.35);
  transition: background 0.25s, transform 0.25s, box-shadow 0.25s;
  white-space: nowrap;
}
.qcb-mail-cta :deep(a:hover) {
  background: var(--acc-hot);
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(255, 90, 31, 0.45);
}

.qcb-mail-ico {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.16);
  flex-shrink: 0;
}
.qcb-mail-ico svg {
  width: 18px;
  height: 18px;
}
.qcb-mail-label {
  padding-right: 4px;
}

@media (max-width: 900px) {
  .qcb {
    flex-direction: column;
    align-items: flex-start;
    gap: 18px;
    padding: 24px 24px;
  }
}
</style>
