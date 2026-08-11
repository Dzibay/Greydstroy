<script setup>
const points = [
  {
    title: 'Нижегородская область',
    text: 'Самовывоз или доставка нашим транспортом, монтаж под ключ по договорённости',
  },
  {
    title: 'По всей России',
    text: 'СДЭК или Деловые линии, терминал в двух шагах от производства',
  },
  {
    title: 'Крупная отправка',
    text: 'Страхование груза обсуждается индивидуально',
  },
]

const cities = [
  { name: 'Санкт-Петербург', x: 95, y: 62, labelY: -14 },
  { name: 'Москва', x: 128, y: 128, labelY: -14 },
  { name: 'Смоленск', x: 72, y: 145, labelY: -14 },
  { name: 'Н. Новгород', x: 205, y: 140, home: true, labelY: 24 },
  { name: 'Казань', x: 268, y: 158, labelY: 24 },
  { name: 'Краснодар', x: 122, y: 262, labelY: 24 },
  { name: 'Донецк', x: 110, y: 228, labelY: -14 },
  { name: 'Луганск', x: 137, y: 218, labelY: -14 },
  { name: 'Екатеринбург', x: 352, y: 120, labelY: -14 },
  { name: 'Новосибирск', x: 462, y: 172, labelY: 24 },
  { name: 'Красноярск', x: 528, y: 130, labelY: -14 },
  { name: 'Владивосток', x: 632, y: 218, labelY: 24 },
]

const home = cities.find((c) => c.home)
</script>

<template>
  <section id="geo" class="sec sec--dark">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 10</span> География и доставка</p>
        <h2 class="sec-title">
          От Нижнего Новгорода до любой точки России — вопрос не «довезёте ли», а <em>«как быстро»</em>
        </h2>
      </div>

      <div class="geo-grid">
        <div class="geo-map card" v-reveal>
          <svg viewBox="0 0 700 320" class="geo-svg" role="img" aria-label="Схема доставки из Нижнего Новгорода по городам России">
            <g v-for="c in cities" :key="'l' + c.name">
              <line
                v-if="!c.home"
                :x1="home.x" :y1="home.y" :x2="c.x" :y2="c.y"
                class="geo-line"
              />
            </g>
            <g v-for="c in cities" :key="c.name">
              <circle v-if="c.home" :cx="c.x" :cy="c.y" r="16" class="geo-home-ring" />
              <circle :cx="c.x" :cy="c.y" :r="c.home ? 7 : 4.5" :class="c.home ? 'geo-home' : 'geo-dot'" />
              <text
                :x="c.x"
                :y="c.y + c.labelY"
                text-anchor="middle"
                :class="c.home ? 'geo-label geo-label--home' : 'geo-label'"
              >{{ c.name }}</text>
            </g>
          </svg>
          <p class="geo-map-note">СДЭК · Деловые линии · собственный транспорт по Нижегородской области</p>
        </div>

        <ul class="geo-list">
          <li v-for="(p, i) in points" :key="p.title" v-reveal="i * 100">
            <span class="geo-pin" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z" /><circle cx="12" cy="10" r="3" />
              </svg>
            </span>
            <div>
              <h3>{{ p.title }}</h3>
              <p>{{ p.text }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.geo-grid {
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 44px;
  align-items: center;
}

.geo-map { padding: 30px; }
.geo-map:hover { transform: none; }
.geo-svg { width: 100%; height: auto; }

.geo-line {
  stroke: var(--acc);
  stroke-width: 1.3;
  stroke-dasharray: 5 6;
  opacity: 0.5;
  animation: dash 1.6s linear infinite;
}
@keyframes dash {
  to { stroke-dashoffset: -22; }
}

.geo-dot { fill: var(--w-soft); }
.geo-home { fill: var(--acc); }
.geo-home-ring {
  fill: none;
  stroke: var(--acc);
  stroke-width: 1.4;
  opacity: 0.6;
  animation: ring 2.4s ease-out infinite;
  transform-origin: center;
  transform-box: fill-box;
}
@keyframes ring {
  0% { transform: scale(0.55); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

.geo-label {
  font-family: var(--font-m);
  font-size: 10.5px;
  fill: var(--w-soft);
  letter-spacing: 0.04em;
}
.geo-label--home {
  fill: var(--acc-hot);
  font-weight: 600;
  font-size: 12px;
}

.geo-map-note {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px dashed var(--line-d);
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
  text-align: center;
}

.geo-list { display: flex; flex-direction: column; gap: 26px; }
.geo-list li { display: flex; gap: 18px; align-items: flex-start; }

.geo-pin {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: var(--acc-dim);
  color: var(--acc-hot);
}
.geo-pin svg { width: 24px; height: 24px; }

.geo-list h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.geo-list p { font-size: 14px; color: var(--w-soft); }

@media (max-width: 900px) {
  .geo-grid { grid-template-columns: 1fr; }
}
</style>
