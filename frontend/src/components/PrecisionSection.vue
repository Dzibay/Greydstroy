<script setup>
import StatCounter from './ui/StatCounter.vue'

const points = [
  'Почему деталь после лазерной резки идёт сразу в сборку, а не на верстак «подровнять»',
  'Деталь №1 и деталь №100 из одной партии — один и тот же угол, до градуса. Спросите, как',
  'Толщина металла, на которой лазеру уже невыгодно, плазме — самое то, а толще — газ',
  'Что именно замеряется в каждой партии перед отгрузкой — и почему не «на глаз»',
]

const stats = [
  { value: 10, suffix: '+', label: 'единиц оборудования' },
  { value: 1500, suffix: '+', label: 'выполненных проектов' },
  { value: 3000, unit: 'м²', label: 'площадь производства' },
  { value: 50, suffix: '+', label: 'сотрудников в штате' },
]
</script>

<template>
  <section id="precision" class="sec sec--light">
    <div class="container">
      <div class="prc-grid">
        <div>
          <div class="sec-head prc-head" v-reveal>
            <p class="sec-tag"><span class="idx">/ 06</span> Точность и оборудование</p>
            <h2 class="sec-title">
              Сотые доли миллиметра — не наша заслуга, а <em>ваше требование</em>, которое мы выполняем
            </h2>
          </div>
          <p class="prc-lead" v-reveal="80">
            Марка станка сама по себе ничего не говорит о результате.
            Важнее то, что происходит с деталью на практике.
          </p>
          <ul class="prc-list">
            <li v-for="(point, i) in points" :key="i" v-reveal="120 + i * 80">
              <span class="q" aria-hidden="true">?</span>
              {{ point }}
            </li>
          </ul>
        </div>

        <figure class="prc-media" v-reveal="200">
          <img src="/img/press-brake.jpg" alt="Листогибочный пресс с ЧПУ гнёт деталь" loading="lazy" />
          <figcaption>
            <span class="cap-line"></span>
            Листогибочный пресс с ЧПУ · рабочая зона 3000 × 1500 мм
          </figcaption>
        </figure>
      </div>
    </div>

    <div class="prc-stats">
      <div class="container prc-stats-in">
        <div v-for="(stat, i) in stats" :key="stat.label" class="stat" v-reveal="i * 90">
          <p class="stat-value">
            <StatCounter :value="stat.value" :suffix="stat.suffix" />
            <span v-if="stat.unit" class="stat-unit">{{ stat.unit }}</span>
          </p>
          <p class="stat-label">{{ stat.label }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.prc-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 64px;
  align-items: center;
  margin-bottom: 96px;
}

.prc-head { margin-bottom: 24px; }

.prc-lead {
  font-size: 16.5px;
  color: var(--ink-soft);
  margin-bottom: 30px;
  max-width: 540px;
}

.prc-list { max-width: 560px; }
.prc-list li {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 16px 0;
  border-bottom: 1px dashed var(--line-l);
  font-size: 15px;
  font-weight: 500;
  color: var(--ink-soft);
}
.prc-list .q {
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  display: grid;
  place-items: center;
  border-radius: 7px;
  background: var(--acc-dim);
  color: var(--acc);
  font-family: var(--font-d);
  font-weight: 900;
  font-size: 13px;
  margin-top: 1px;
}

.prc-media {
  position: relative;
}
.prc-media img {
  border-radius: var(--r);
  width: 100%;
  aspect-ratio: 4 / 3.4;
  object-fit: cover;
  box-shadow: 24px 24px 0 -1px transparent, 0 30px 60px rgba(18, 22, 27, 0.22);
}
.prc-media::before {
  content: '';
  position: absolute;
  top: 22px;
  left: 22px;
  right: -22px;
  bottom: -22px;
  border: 1.5px solid var(--acc);
  border-radius: var(--r);
  z-index: -1;
  opacity: 0.55;
}
.prc-media figcaption {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 18px;
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-faint);
}
.cap-line { width: 30px; height: 2px; background: var(--acc); flex-shrink: 0; }

.prc-stats {
  background: var(--bg0);
  padding: 58px 0;
  position: relative;
}
.prc-stats::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: linear-gradient(90deg, var(--line-d) 1px, transparent 1px);
  background-size: 72px 100%;
  opacity: 0.5;
}
.prc-stats-in {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}
.stat { text-align: center; }
.stat-value {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.12em;
  white-space: nowrap;
  font-family: var(--font-d);
  font-size: clamp(30px, 3.5vw, 48px);
  font-weight: 900;
  color: var(--acc);
  line-height: 1.1;
  text-shadow: 0 0 44px rgba(255, 90, 31, 0.3);
}
.stat-unit {
  font-size: 0.5em;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.stat-label {
  margin-top: 8px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-soft);
}

/* секция светлая, но низ — тёмная лента статистики: убираем нижний паддинг */
.sec { padding-bottom: 0; }

@media (max-width: 960px) {
  .prc-grid { grid-template-columns: 1fr; gap: 48px; margin-bottom: 72px; }
  .prc-stats-in { grid-template-columns: 1fr 1fr; }
}
</style>
