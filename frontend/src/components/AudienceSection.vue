<script setup>
import { ref, computed } from 'vue'

const audiences = [
  {
    id: 'builders',
    short: 'Застройщикам',
    title: 'Застройщикам и подрядчикам',
    lead: 'У вас есть дата сдачи объекта, и металлоконструкции — не единственная головная боль. Возьмём эту часть на себя: каркас, монтаж, фундаменты — или здание целиком по одному договору.',
    points: [
      'Изготовим каркас в своём цехе и привезём с маркировкой',
      'Смонтируем своими бригадами по Нижегородской области',
      'Зальём фундаменты под колонны — анкера из того же цеха',
    ],
    links: [
      { to: '/metallokonstruktsii/izgotovlenie', label: 'Изготовление' },
      { to: '/metallokonstruktsii/montazh', label: 'Монтаж' },
      { to: '/uslugi/stroitelstvo-pod-klyuch', label: 'Под ключ' },
    ],
    cta: 'Обсудить объект',
    icon: 'building',
  },
  {
    id: 'plants',
    short: 'Производствам',
    title: 'Производствам',
    lead: 'Свой лазер, плазма или листогиб загружены на две недели вперёд? Возьмём часть партии на аутсорс — без потери в качестве и без объяснений вашему клиенту, почему сроки сдвинулись.',
    points: [
      'Резка, гибка и сварка на одной площадке — одна накладная',
      'Закладные, площадки, узлы под ваше оборудование',
      'Демонтаж и усиление — в том числе в действующем цехе',
    ],
    links: [
      { to: '/metallokonstruktsii/izgotovlenie', label: 'Изготовление' },
      { to: '/uslugi', label: 'Резка и гибка' },
      { to: '/uslugi/demontazh-metallokonstruktsij', label: 'Демонтаж' },
    ],
    cta: 'Обсудить заказ',
    icon: 'factory',
  },
  {
    id: 'private',
    short: 'Частным лицам',
    title: 'Частным лицам',
    lead: 'Лестница, навес или ограждение, которые не выглядят так, будто их сварил сосед по гаражу. По эскизу, фото или на глаз — чертёж снимем сами.',
    points: [
      'Лестницы и площадки по размерам проёма',
      'Навесы для авто и входных групп',
      'Считаем по эскизу — КМД разработаем, если его нет',
    ],
    links: [
      { to: '/metallokonstruktsii/lestnitsy', label: 'Лестницы' },
      { to: '/metallokonstruktsii/navesy', label: 'Навесы' },
      { to: '/uslugi/proektirovanie-metallokonstruktsij', label: 'Проект' },
    ],
    cta: 'Обсудить проект',
    icon: 'person',
  },
]

const active = ref(0)
const current = computed(() => audiences[active.value])

const select = (i) => {
  active.value = i
}

const onKey = (e, i) => {
  const last = audiences.length - 1
  let next = i
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = i === last ? 0 : i + 1
  else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = i === 0 ? last : i - 1
  else if (e.key === 'Home') next = 0
  else if (e.key === 'End') next = last
  else return
  e.preventDefault()
  select(next)
  document.getElementById(`aud-tab-${next}`)?.focus()
}
</script>

<template>
  <section id="audience" class="sec sec--dark">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 07</span> Для кого мы работаем</p>
        <h2 class="sec-title">Три типа клиентов. <em>Возможно, один — это вы</em></h2>
      </div>

      <div class="aud" v-reveal="80">
        <div class="aud-rail" role="tablist" aria-label="Тип клиента">
          <button
            v-for="(a, i) in audiences"
            :id="'aud-tab-' + i"
            :key="a.id"
            type="button"
            role="tab"
            class="aud-tab"
            :class="{ active: active === i }"
            :aria-selected="active === i"
            :aria-controls="'aud-panel'"
            :tabindex="active === i ? 0 : -1"
            @click="select(i)"
            @keydown="onKey($event, i)"
          >
            <span class="aud-tab-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="aud-tab-label">{{ a.short }}</span>
          </button>
        </div>

        <div
          id="aud-panel"
          class="aud-panel"
          role="tabpanel"
          :aria-labelledby="'aud-tab-' + active"
        >
          <Transition name="aud-swap">
            <div :key="current.id" class="aud-panel-in">
              <span class="aud-icon" aria-hidden="true">
                <svg v-if="current.icon === 'building'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 28V10l9-6v24M14 28V14l13 5v9" /><path d="M3 28h26" />
                  <path d="M9 12h1m-1 5h1m-1 5h1m9 1h1m4 2h1" />
                </svg>
                <svg v-else-if="current.icon === 'factory'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 28V13l8 5v-5l8 5v-5l8 5v10z" /><path d="M2 28h28" /><path d="M6 13V5h4v10" />
                  <path d="M12 23h2m4 0h2m4 0h2" />
                </svg>
                <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="16" cy="10" r="5" /><path d="M6 28c0-5.5 4.5-9 10-9s10 3.5 10 9" />
                </svg>
              </span>

              <div class="aud-body">
                <h3>{{ current.title }}</h3>
                <p>{{ current.lead }}</p>
                <ul>
                  <li v-for="p in current.points" :key="p">{{ p }}</li>
                </ul>
                <div class="aud-actions">
                  <a href="#cta" class="btn">{{ current.cta }}</a>
                  <div class="aud-links">
                    <RouterLink v-for="l in current.links" :key="l.to" :to="l.to">{{ l.label }} →</RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.aud {
  display: grid;
  gap: 0;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  overflow: hidden;
  background: var(--card-d);
}

.aud-rail {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-bottom: 1px solid var(--line-d);
}

.aud-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  min-height: 72px;
  padding: 18px 16px;
  background: transparent;
  border: none;
  border-right: 1px solid var(--line-d);
  border-bottom: 3px solid transparent;
  color: var(--w-soft);
  cursor: pointer;
  transition: color 0.25s, background 0.25s, border-color 0.25s;
}
.aud-tab:last-child { border-right: none; }
.aud-tab:hover { color: var(--white); background: rgba(255, 255, 255, 0.03); }
.aud-tab.active {
  color: var(--white);
  background: rgba(255, 90, 31, 0.08);
  border-bottom-color: var(--acc);
}

.aud-tab-num {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(255, 255, 255, 0.22);
}
.aud-tab.active .aud-tab-num,
.aud-tab:hover .aud-tab-num { -webkit-text-stroke-color: var(--acc); }

.aud-tab-label {
  font-family: var(--font-d);
  font-size: 13.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.aud-panel {
  position: relative;
  min-height: 340px;
  overflow: hidden;
}

.aud-panel-in {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 28px 32px;
  align-items: start;
  padding: 36px 40px 34px;
}

.aud-icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--acc-dim);
  color: var(--acc-hot);
}
.aud-icon svg { width: 32px; height: 32px; }

.aud-body h3 {
  font-family: var(--font-d);
  font-size: clamp(18px, 2.2vw, 24px);
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.2;
  margin-bottom: 12px;
}
.aud-body p {
  font-size: 15.5px;
  color: var(--w-soft);
  max-width: 640px;
  margin-bottom: 18px;
}
.aud-body ul {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 26px;
}
.aud-body li {
  position: relative;
  padding-left: 22px;
  font-size: 14.5px;
  color: var(--white);
}
.aud-body li::before {
  content: '◆';
  position: absolute;
  left: 0;
  top: 2px;
  font-size: 9px;
  color: var(--acc);
}

.aud-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px 28px;
}
.aud-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 22px;
}
.aud-links a {
  font-size: 14px;
  font-weight: 700;
  color: var(--w-soft);
  transition: color 0.2s;
}
.aud-links a:hover { color: var(--acc-hot); }

.aud-swap-enter-active,
.aud-swap-leave-active {
  transition: opacity 0.25s var(--ease), transform 0.25s var(--ease);
}
.aud-swap-leave-active { position: absolute; inset: 0; }
.aud-swap-enter-from { opacity: 0; transform: translateY(8px); }
.aud-swap-leave-to { opacity: 0; transform: translateY(-6px); }

@media (max-width: 720px) {
  .aud-tab { flex-direction: column; gap: 6px; min-height: 64px; padding: 14px 8px; }
  .aud-tab-label { font-size: 11.5px; text-align: center; }
  .aud-panel { min-height: 0; }
  .aud-panel-in { grid-template-columns: 1fr; padding: 26px 22px 28px; gap: 18px; }
}
@media (prefers-reduced-motion: reduce) {
  .aud-swap-enter-active,
  .aud-swap-leave-active { transition: none; }
  .aud-swap-enter-from,
  .aud-swap-leave-to { transform: none; }
}
</style>
