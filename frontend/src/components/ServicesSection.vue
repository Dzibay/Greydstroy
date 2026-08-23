<script setup>
import { ref, computed } from 'vue'

const services = [
  {
    slug: 'lazernaya-rezka',
    title: 'Лазерная резка',
    short: 'Лазер',
    text: 'Сложный контур сегодня — деталь для сборки без доработки напильником.',
    spec: 'до 16 мм · чистая кромка · ЧПУ',
    chips: ['до 16 мм', 'ЧПУ', 'DXF / DWG'],
    points: [
      'Чистая кромка — сразу в сборку или на покраску',
      'Отверстия, пазы и маркировка за один установ',
    ],
    fit: 'Детали под сборку · серия · сложный контур',
    icon: 'laser',
    tone: 'laser',
  },
  {
    slug: 'plazmennaya-rezka',
    title: 'Плазменная резка',
    short: 'Плазма',
    text: 'Толстый металл и большие объёмы — кромка под сварку без «доп. зачистки».',
    spec: 'до 25 мм · чёрный металл',
    chips: ['до 25 мм', 'чёрный металл', 'крупный формат'],
    points: [
      'Выгоднее лазера на толщинах от 16 мм',
      'Фланцы, косынки, закладные, основания',
    ],
    fit: 'Толстый лист · закладные · крупный раскрой',
    icon: 'plasma',
    tone: 'plasma',
  },
  {
    slug: 'gazovaya-rezka',
    title: 'Газовая резка',
    short: 'Газ',
    text: 'Сверхтолстая чёрная сталь — плиты, закладные и основания до 70 мм.',
    spec: 'до 70 мм · чёрная сталь',
    chips: ['до 70 мм', 'чёрная сталь', 'плиты'],
    points: [
      'Там, где лазер и плазма уже не берут',
      'Кромка под сварку металлоконструкций',
    ],
    fit: 'Плиты и основания · толстые фланцы',
    icon: 'gas',
    tone: 'gas',
  },
  {
    slug: 'gibka-metalla',
    title: 'Гибка на листогибе',
    short: 'Гибка',
    text: 'Деталь №50 гнётся под тем же углом, что и деталь №1 — на том же участке, сразу после резки.',
    spec: 'ЧПУ · до 6 мм · до 3000 мм',
    chips: ['до 6 мм', 'до 3000 мм', 'ЧПУ'],
    points: [
      'Повторяемый угол без подгонки на объекте',
      'Короба, кожухи, лотки и нестандартный профиль',
    ],
    fit: 'Короба · лотки · панели · профиль',
    icon: 'bend',
    tone: 'bend',
  },
  {
    slug: 'svarka',
    title: 'Сварка',
    short: 'Сварка',
    text: 'От одного шва до объекта под ключ. В Нижегородской области — с монтажом.',
    spec: 'MIG/MAG · TIG · РДС',
    chips: ['MIG/MAG', 'TIG', 'РДС'],
    points: [
      'Паспорт на изделие — швы проверяются до отгрузки',
      'Резка, гибка и сборка на одной площадке',
    ],
    fit: 'Каркасы · ёмкости · узлы · под ключ',
    icon: 'weld',
    tone: 'weld',
  },
]

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
          <h2 class="sec-title">Один подрядчик <em>вместо трёх</em></h2>
        </div>
        <p class="sec-sub srv-lead">
          Пока деталь пересылают между цехом резки, гибочным участком и сварочным постом —
          время теряется на каждой пересылке. У нас всё на одной площадке:
          один договор, один контакт, одна ответственность.
        </p>
      </div>

      <div class="srv-ex" v-reveal="80">
        <div class="srv-rail" role="tablist" aria-label="Участки производства">
          <button
            v-for="(s, i) in services"
            :id="'srv-tab-' + i"
            :key="s.slug"
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
          <Transition name="srv-swap" mode="out-in">
            <div :key="current.slug" class="srv-stage-in">
              <span class="srv-ghost" aria-hidden="true">{{ String(active + 1).padStart(2, '0') }}</span>

              <div class="srv-stage-top">
                <span class="srv-icon" aria-hidden="true">
                  <svg v-if="current.icon === 'laser'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 3h8l-2 6h-4l-2-6z" /><path d="M14 9v4h4V9" /><path d="M16 13v6" />
                    <path d="m16 19-6 8m6-8 6 8m-6-8v9" stroke-dasharray="2.5 3" />
                  </svg>
                  <svg v-else-if="current.icon === 'plasma'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 3h10l-3 7h-4l-3-7z" /><path d="M16 10v5" />
                    <path d="M16 15c-2 3-5 4-5 8m5-8c2 3 5 4 5 8m-5-8v10" stroke-dasharray="3 2.5" />
                    <path d="M6 29h20" />
                  </svg>
                  <svg v-else-if="current.icon === 'gas'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 28V14" /><path d="M12 28h8" />
                    <path d="M16 14c-3-4-1-8 0-10 1 2 3 6 0 10z" />
                    <path d="M13 18h6" stroke-dasharray="2 2.5" />
                  </svg>
                  <svg v-else-if="current.icon === 'bend'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 24 16 12l12 12" /><path d="M16 12V4" /><path d="M9 4h14" />
                    <circle cx="16" cy="24" r="2.6" />
                  </svg>
                  <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 20 14 11l7 7-9 9z" /><path d="m14 11 5-5 3-1 4 4-1 3-4 4" />
                    <path d="m22 18 5 5" stroke-dasharray="2.5 3" /><circle cx="9" cy="24" r="1" fill="currentColor" />
                  </svg>
                </span>
                <div class="srv-chips">
                  <span v-for="c in current.chips" :key="c" class="srv-chip">{{ c }}</span>
                </div>
              </div>

              <h3 class="srv-stage-title">
                <RouterLink :to="`/uslugi/${current.slug}`">{{ current.title }}</RouterLink>
              </h3>
              <p class="srv-stage-text">{{ current.text }}</p>

              <ul class="srv-points">
                <li v-for="p in current.points" :key="p">{{ p }}</li>
              </ul>

              <p class="srv-fit"><span>Подходит для</span> {{ current.fit }}</p>

              <div class="srv-actions">
                <RouterLink :to="`/uslugi/${current.slug}`" class="btn">
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
        <p>Пять участков — один договор и один контакт.</p>
        <RouterLink to="/uslugi" class="srv-all">Все услуги и подбор технологии →</RouterLink>
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
  min-height: 440px;
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
  padding: 18px 20px;
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

.srv-tab--laser { --tone: #ff5a1f; }
.srv-tab--plasma { --tone: #4f8dff; }
.srv-tab--gas { --tone: #3dd68c; }
.srv-tab--bend { --tone: #ffb020; }
.srv-tab--weld { --tone: #ff7d3f; }

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
  font-size: 13.5px;
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
  position: relative;
  overflow: hidden;
  min-height: 440px;
  padding: 36px 38px 34px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
  isolation: isolate;
}
.srv-stage--laser { --tone: #ff5a1f; }
.srv-stage--plasma { --tone: #4f8dff; }
.srv-stage--gas { --tone: #3dd68c; }
.srv-stage--bend { --tone: #ffb020; }
.srv-stage--weld { --tone: #ff7d3f; }

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
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 368px;
}

.srv-ghost {
  position: absolute;
  top: -18px;
  right: -8px;
  font-family: var(--font-d);
  font-size: clamp(96px, 14vw, 168px);
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
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 28px;
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
  font-size: clamp(22px, 3vw, 32px);
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.15;
  margin-bottom: 14px;
  max-width: 18ch;
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
  font-size: 16px;
  color: var(--w-soft);
  max-width: 520px;
  margin-bottom: 22px;
}

.srv-points {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 22px;
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
  margin-bottom: 28px;
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
}
.srv-actions .btn svg {
  width: 18px;
  height: 18px;
}

.srv-swap-enter-active,
.srv-swap-leave-active {
  transition: opacity 0.28s var(--ease), transform 0.28s var(--ease);
}
.srv-swap-enter-from { opacity: 0; transform: translateY(14px); }
.srv-swap-leave-to { opacity: 0; transform: translateY(-10px); }

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
    grid-template-columns: repeat(5, 1fr);
    overflow: hidden;
  }
  .srv-tab {
    min-width: 0;
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
    gap: 6px;
    padding: 14px 8px;
    border-bottom: none;
    border-right: 1px solid var(--line-d);
    border-left: none;
    border-top: 3px solid transparent;
  }
  .srv-tab:last-child { border-right: none; }
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
  .srv-stage { min-height: 0; padding: 28px 24px; }
  .srv-stage-in { min-height: 0; }
}

@media (max-width: 560px) {
  .srv-rail { grid-template-columns: repeat(6, 1fr); }
  .srv-tab { grid-column: span 2; border-bottom: 1px solid var(--line-d); }
  .srv-tab:nth-child(3) { border-right: none; }
  .srv-tab:nth-child(4) { grid-column: 1 / span 3; border-bottom: none; }
  .srv-tab:nth-child(5) { grid-column: 4 / span 3; border-bottom: none; border-right: none; }
  .srv-ghost { font-size: 92px; right: -4px; }
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
