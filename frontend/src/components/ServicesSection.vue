<script setup>
import { ref, computed } from 'vue'
import { mainServices } from '../data/services'

const services = mainServices

const active = ref(0)
const current = computed(() => services[active.value])

const select = (i) => {
  active.value = i
}

const onKey = (e, i) => {
  const last = services.length - 1
  let next = i
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = i === last ? 0 : i + 1
  else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = i === 0 ? last : i - 1
  else if (e.key === 'Home') next = 0
  else if (e.key === 'End') next = last
  else return
  e.preventDefault()
  select(next)
  document.getElementById(`srv-tab-${next}`)?.focus()
}
</script>

<template>
  <section id="services" class="sec sec--dark">
    <div class="container">
      <div class="srv-head" v-reveal>
        <div>
          <p class="sec-tag"><span class="idx">/ 03</span> Что мы делаем</p>
          <h2 class="sec-title">От чертежа до здания <em>под ключ</em></h2>
        </div>
        <p class="sec-sub srv-lead">
          Основа — собственный завод металлоконструкций в Дзержинске. Изготовим,
          привезём и смонтируем на объекте, зальём фундаменты — или построим здание
          целиком: один договор, один контакт, одна ответственность.
        </p>
      </div>

      <div class="srv-ex" v-reveal="80">
        <div class="srv-rail" role="tablist" aria-label="Услуги компании">
          <button
            v-for="(s, i) in services"
            :id="'srv-tab-' + i"
            :key="s.id"
            type="button"
            role="tab"
            class="srv-tab"
            :class="['srv-tab--' + s.tone, { active: active === i }]"
            :aria-selected="active === i"
            :aria-controls="'srv-panel'"
            :tabindex="active === i ? 0 : -1"
            @click="select(i)"
            @mouseenter="select(i)"
            @keydown="onKey($event, i)"
          >
            <span class="srv-tab-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="srv-tab-body">
              <span class="srv-tab-title">{{ s.title }}</span>
              <span class="srv-tab-short">{{ s.short }}</span>
              <span class="srv-tab-spec">{{ s.spec }}</span>
            </span>
            <span class="srv-tab-go" aria-hidden="true">→</span>
          </button>
        </div>

        <div
          id="srv-panel"
          class="srv-stage"
          :class="'srv-stage--' + current.tone"
          role="tabpanel"
          :aria-labelledby="'srv-tab-' + active"
        >
          <span class="srv-ghost" aria-hidden="true">{{ String(active + 1).padStart(2, '0') }}</span>
          <Transition name="srv-swap">
            <div :key="current.id" class="srv-stage-in">
              <div class="srv-stage-top">
                <span class="srv-icon" aria-hidden="true">
                  <svg v-if="current.icon === 'fab'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 26V11l8 5v-5l8 5v-5l8 5v10" /><path d="M4 26h24" /><path d="M9 21h3m4 0h3m4 0h3" />
                  </svg>
                  <svg v-else-if="current.icon === 'mount'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M7 28h12" /><path d="M13 28V9" /><path d="M4 9h24" /><path d="M13 6v3m0-3 12 3M13 6 6 9" /><path d="M24 9v6" /><path d="M21.5 15h5l-2.5 3.5z" />
                  </svg>
                  <svg v-else-if="current.icon === 'concrete'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="20" width="24" height="6" rx="1" /><path d="M9 20v-5m7 5v-5m7 5v-5" /><path d="M5 10c2-2.2 5-2.2 7 0s5 2.2 7 0 5-2.2 7 0" />
                  </svg>
                  <svg v-else-if="current.icon === 'turnkey'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 27V14l9-7 9 7v13" /><path d="M3 27h18" /><path d="M9 27v-6h6v6" /><circle cx="25" cy="11" r="3" /><path d="M25 14v8m0 0h3m-3-3.5h2" />
                  </svg>
                  <svg v-else-if="current.icon === 'design'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="5" width="24" height="22" rx="1.5" /><path d="M4 12h24M11 12v15" /><path d="M15.5 21.5 20 15l3.5 5" /><path d="M6.5 8.5h3" />
                  </svg>
                  <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 27l9-9" /><path d="M13 8l5-5 7 7-5 5z" /><path d="M16 11l-2.5 2.5" /><path d="M24 20l4 4m-4 0 4-4" stroke-dasharray="2.5 3" />
                  </svg>
                </span>
                <div class="srv-chips">
                  <span v-for="c in current.chips" :key="c" class="srv-chip">{{ c }}</span>
                </div>
              </div>

              <h3 class="srv-stage-title">
                <RouterLink :to="current.to">{{ current.title }}</RouterLink>
              </h3>
              <p class="srv-stage-text">{{ current.text }}</p>

              <ul class="srv-points">
                <li v-for="p in current.points" :key="p">{{ p }}</li>
              </ul>

              <p class="srv-fit"><span>Подходит для</span> {{ current.fit }}</p>

              <div class="srv-actions">
                <RouterLink :to="current.to" class="btn">
                  Подробнее об услуге
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M5 12h14m-6-6 6 6-6 6" />
                  </svg>
                </RouterLink>
                <RouterLink to="/kalkulyator" class="btn btn--ghost">Рассчитать</RouterLink>
              </div>
            </div>
          </Transition>
        </div>
      </div>

      <div class="srv-foot" v-reveal="140">
        <p>Шесть услуг — один подрядчик и один договор на весь цикл.</p>
        <RouterLink to="/uslugi" class="srv-all">Все услуги и технологии →</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.srv-head {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 40px 56px;
  align-items: end;
  margin-bottom: 48px;
}
.srv-lead {
  margin-top: 0;
  max-width: none;
}

.srv-ex {
  display: grid;
  grid-template-columns: minmax(280px, 0.88fr) 1.32fr;
  gap: 20px;
  align-items: stretch;
  min-height: 560px;
}

.srv-rail {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  overflow: hidden;
  background: var(--card-d);
}

.srv-tab {
  display: grid;
  grid-template-columns: 48px 1fr auto;
  align-items: center;
  gap: 10px;
  width: 100%;
  flex: 1;
  padding: 16px 20px;
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--line-d);
  border-left: 3px solid transparent;
  color: var(--w-soft);
  text-align: left;
  transition: background 0.3s, color 0.3s, border-color 0.3s, padding 0.3s var(--ease);
}
.srv-tab:last-child { border-bottom: none; }
.srv-tab:hover {
  color: var(--white);
  background: rgba(255, 255, 255, 0.03);
}
.srv-tab.active {
  color: var(--white);
  background: rgba(255, 90, 31, 0.08);
  border-left-color: var(--tone, var(--acc));
  padding-left: 24px;
}

.srv-tab--fab { --tone: #ff5a1f; }
.srv-tab--mount { --tone: #4f8dff; }
.srv-tab--concrete { --tone: #9aa7b8; }
.srv-tab--turnkey { --tone: #ffb020; }
.srv-tab--design { --tone: #38bdf8; }
.srv-tab--demolition { --tone: #ff4d6d; }

.srv-tab-num {
  font-family: var(--font-d);
  font-size: 20px;
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(255, 255, 255, 0.18);
  transition: -webkit-text-stroke-color 0.3s, color 0.3s;
}
.srv-tab.active .srv-tab-num,
.srv-tab:hover .srv-tab-num {
  -webkit-text-stroke-color: var(--tone, var(--acc));
}

.srv-tab-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}
.srv-tab-title,
.srv-tab-short {
  font-family: var(--font-d);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.01em;
  line-height: 1.25;
}
.srv-tab-short { display: none; }
.srv-tab-spec {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--w-faint);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.srv-tab.active .srv-tab-spec { color: color-mix(in srgb, var(--tone, var(--acc)) 80%, #fff); }

.srv-tab-go {
  font-size: 16px;
  color: var(--w-faint);
  opacity: 0;
  transform: translateX(-6px);
  transition: opacity 0.25s, transform 0.25s var(--ease), color 0.25s;
}
.srv-tab.active .srv-tab-go,
.srv-tab:hover .srv-tab-go {
  opacity: 1;
  transform: none;
  color: var(--tone, var(--acc));
}

.srv-stage {
  --tone: var(--acc);
  --stage-pad-y: 32px;
  --stage-pad-x: 36px;
  position: relative;
  overflow: hidden;
  min-width: 0;
  min-height: 560px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
  isolation: isolate;
}
.srv-stage--fab { --tone: #ff5a1f; }
.srv-stage--mount { --tone: #4f8dff; }
.srv-stage--concrete { --tone: #9aa7b8; }
.srv-stage--turnkey { --tone: #ffb020; }
.srv-stage--design { --tone: #38bdf8; }
.srv-stage--demolition { --tone: #ff4d6d; }

.srv-stage::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 100% 0%, color-mix(in srgb, var(--tone) 20%, transparent), transparent 52%),
    linear-gradient(var(--line-d) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-d) 1px, transparent 1px);
  background-size: auto, 56px 56px, 56px 56px;
  opacity: 0.9;
  pointer-events: none;
  z-index: 0;
}

.srv-stage-in {
  position: absolute;
  inset: var(--stage-pad-y) var(--stage-pad-x);
  z-index: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.srv-ghost {
  position: absolute;
  top: 12px;
  right: 20px;
  z-index: 1;
  font-family: var(--font-d);
  font-size: clamp(80px, 11vw, 140px);
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1.5px color-mix(in srgb, var(--tone) 28%, transparent);
  pointer-events: none;
  user-select: none;
}

.srv-stage-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 18px;
  flex-shrink: 0;
}

.srv-icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: color-mix(in srgb, var(--tone) 16%, transparent);
  color: var(--tone);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--tone) 35%, transparent);
}
.srv-icon svg { width: 32px; height: 32px; }

.srv-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}
.srv-chip {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-soft);
  border: 1px solid var(--line-d);
  border-radius: 4px;
  padding: 5px 10px;
  background: rgba(0, 0, 0, 0.2);
}

.srv-stage-title {
  font-family: var(--font-d);
  font-size: clamp(20px, 2.6vw, 28px);
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.15;
  margin-bottom: 10px;
  max-width: 18ch;
  overflow-wrap: anywhere;
}
.srv-stage-title a {
  background-image: linear-gradient(var(--tone), var(--tone));
  background-size: 0 2px;
  background-position: 0 100%;
  background-repeat: no-repeat;
  transition: background-size 0.35s var(--ease), color 0.25s;
}
.srv-stage-title a:hover {
  color: var(--tone);
  background-size: 100% 2px;
}

.srv-stage-text {
  font-size: 15.5px;
  color: var(--w-soft);
  max-width: 520px;
  margin-bottom: 14px;
}

.srv-points {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}
.srv-points li {
  position: relative;
  padding-left: 22px;
  font-size: 14.5px;
  color: var(--white);
}
.srv-points li::before {
  content: '◆';
  position: absolute;
  left: 0;
  top: 2px;
  font-size: 9px;
  color: var(--tone);
}

.srv-fit {
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--w-faint);
  margin-bottom: 18px;
}
.srv-fit span {
  color: var(--tone);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-right: 8px;
}

.srv-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: auto;
  flex-shrink: 0;
}
.srv-actions .btn svg {
  width: 18px;
  height: 18px;
}

.srv-swap-enter-active,
.srv-swap-leave-active {
  transition: opacity 0.28s var(--ease), transform 0.28s var(--ease);
}
.srv-swap-leave-active { z-index: 1; }
.srv-swap-enter-active { z-index: 2; }
.srv-swap-enter-from { opacity: 0; transform: translateY(10px); }
.srv-swap-leave-to { opacity: 0; transform: translateY(-8px); }

.srv-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 28px;
  padding-top: 22px;
  border-top: 1px dashed var(--line-d);
  font-size: 14.5px;
  color: var(--w-soft);
}
.srv-all {
  font-family: var(--font-d);
  font-size: 13.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--acc-hot);
  transition: color 0.2s, transform 0.25s var(--ease);
}
.srv-all:hover {
  color: var(--acc);
  transform: translateX(4px);
}

@media (max-width: 960px) {
  .srv-head { grid-template-columns: 1fr; gap: 16px; }
  .srv-ex { grid-template-columns: 1fr; min-height: 0; }
  .srv-rail {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    overflow: hidden;
  }
  .srv-tab {
    min-width: 0;
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
    gap: 6px;
    padding: 14px 8px;
    border-bottom: 1px solid var(--line-d);
    border-right: 1px solid var(--line-d);
    border-left: none;
    border-top: 3px solid transparent;
  }
  .srv-tab:nth-child(3n) { border-right: none; }
  .srv-tab:nth-child(n + 4) { border-bottom: none; }
  .srv-tab.active {
    padding-left: 8px;
    border-top-color: var(--tone, var(--acc));
    border-left-color: transparent;
  }
  .srv-tab-body { align-items: center; }
  .srv-tab-title { display: none; }
  .srv-tab-short { display: block; font-size: 12px; }
  .srv-tab-spec,
  .srv-tab-go { display: none; }
  .srv-stage {
    --stage-pad-y: 26px;
    --stage-pad-x: 24px;
    min-height: 520px;
  }
}

@media (max-width: 560px) {
  .srv-rail { grid-template-columns: repeat(2, 1fr); }
  .srv-tab { border-right: 1px solid var(--line-d); border-bottom: 1px solid var(--line-d); }
  .srv-tab:nth-child(2n) { border-right: none; }
  .srv-tab:nth-child(n + 5) { border-bottom: none; }
  .srv-ghost { font-size: 92px; right: 16px; top: 10px; }
  .srv-stage-title { max-width: none; }
  .srv-actions .btn { width: 100%; }
}

@media (prefers-reduced-motion: reduce) {
  .srv-swap-enter-active,
  .srv-swap-leave-active { transition: none; }
  .srv-swap-enter-from,
  .srv-swap-leave-to { transform: none; }
}
</style>
