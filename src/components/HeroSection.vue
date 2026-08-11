<script setup>
import LeadForm from './ui/LeadForm.vue'

const marquee = [
  'Лазерная резка',
  'Плазменная резка',
  'Гибка на листогибе',
  'Сварка и металлоконструкции',
  'КМ / КМД с нуля',
  'От 1 детали до серии',
]
</script>

<template>
  <section id="top" class="hero">
    <div class="hero-bg">
      <img src="/img/hero-laser.png" alt="Лазерная резка металла" fetchpriority="high" />
    </div>
    <div class="hero-grid-lines" aria-hidden="true"></div>

    <div class="container hero-in">
      <div class="hero-left">
        <p class="hero-kicker" v-reveal>
          <span class="dot"></span>
          Металлообработка · Дзержинск → вся Россия
        </p>

        <h1 class="hero-title" v-reveal="80">
          Деталь встанет в узел <em>с первого раза</em> — или переделаем её за свой счёт
        </h1>

        <p class="hero-sub" v-reveal="160">
          Лазерная и плазменная резка, гибка на листогибе, сварка — от одной детали
          до серийной партии. Расчёт стоимости и сроков — в течение рабочего дня,
          отгрузка по всей России.
        </p>

        <ul class="hero-trust" v-reveal="240">
          <li>Своё производство</li>
          <li>Паспорт на каждое изделие</li>
          <li>Расчёт за 1 рабочий день</li>
        </ul>

        <div class="hero-cta" v-reveal="320">
          <a href="#cta" class="btn">Рассчитать стоимость и сроки</a>
          <p class="btn-note">Отвечаем в течение рабочего дня.<br />Ни к чему не обязывает.</p>
        </div>
      </div>

      <div class="hero-form" v-reveal="300">
        <div class="hero-form-head">
          <span class="hf-num">01</span>
          <p>Быстрый расчёт<br /><small>займёт 20 секунд</small></p>
        </div>
        <LeadForm button-text="Рассчитать стоимость" />
      </div>
    </div>

    <div class="hero-marquee" aria-hidden="true">
      <div class="hm-track">
        <template v-for="n in 2" :key="n">
          <span v-for="item in marquee" :key="item + n">{{ item }}<i>◆</i></span>
        </template>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 140px 0 90px;
  overflow: hidden;
  background: var(--bg0);
}

.hero-bg {
  position: absolute;
  inset: 0;
}
.hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 65% center;
}
.hero-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(11, 14, 17, 0.96) 0%, rgba(11, 14, 17, 0.82) 42%, rgba(11, 14, 17, 0.35) 100%),
    linear-gradient(0deg, rgba(11, 14, 17, 0.95) 0%, transparent 34%);
}

.hero-grid-lines {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: linear-gradient(180deg, transparent, #000 30%, #000 70%, transparent);
}

.hero-in {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.35fr 0.75fr;
  gap: 64px;
  align-items: center;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--w-soft);
  border: 1px solid var(--line-d);
  padding: 8px 16px;
  border-radius: 40px;
  margin-bottom: 30px;
  background: rgba(11, 14, 17, 0.5);
}
.hero-kicker .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--acc);
  box-shadow: 0 0 12px var(--acc);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  50% { opacity: 0.4; }
}

.hero-title {
  font-family: var(--font-d);
  font-size: clamp(30px, 4.6vw, 58px);
  font-weight: 900;
  line-height: 1.08;
  text-transform: uppercase;
  letter-spacing: -0.015em;
  margin-bottom: 28px;
}
.hero-title em {
  font-style: normal;
  color: var(--acc);
  text-shadow: 0 0 44px rgba(255, 90, 31, 0.45);
}

.hero-sub {
  font-size: clamp(15px, 1.5vw, 18px);
  color: var(--w-soft);
  max-width: 560px;
  margin-bottom: 30px;
}

.hero-trust {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 38px;
}
.hero-trust li {
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--white);
  border: 1px solid var(--line-d);
  background: rgba(255, 255, 255, 0.05);
  padding: 8px 15px;
  border-radius: 6px;
  backdrop-filter: blur(6px);
}
.hero-trust li::before {
  content: '▸ ';
  color: var(--acc);
}

.hero-cta {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.hero-cta .btn-note { margin-top: 0; }

.hero-form {
  background: rgba(17, 21, 26, 0.86);
  backdrop-filter: blur(18px);
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 30px 28px;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.5);
}
.hero-form-head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 22px;
}
.hf-num {
  font-family: var(--font-d);
  font-size: 30px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.5px var(--acc);
}
.hero-form-head p {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.3;
}
.hero-form-head small {
  font-family: var(--font-m);
  font-size: 10.5px;
  font-weight: 400;
  color: var(--w-faint);
  text-transform: none;
  letter-spacing: 0.06em;
}

.hero-marquee {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 3;
  border-top: 1px solid var(--line-d);
  background: rgba(11, 14, 17, 0.72);
  backdrop-filter: blur(10px);
  overflow: hidden;
  padding: 15px 0;
}
.hm-track {
  display: flex;
  gap: 44px;
  width: max-content;
  animation: marquee 26s linear infinite;
}
.hm-track span {
  display: flex;
  align-items: center;
  gap: 44px;
  font-family: var(--font-m);
  font-size: 13px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--w-soft);
  white-space: nowrap;
}
.hm-track i {
  font-style: normal;
  color: var(--acc);
  font-size: 9px;
}
@keyframes marquee {
  to { transform: translateX(-50%); }
}

@media (max-width: 980px) {
  .hero { padding: 120px 0 110px; }
  .hero-in { grid-template-columns: 1fr; gap: 44px; }
  .hero-bg img { object-position: 70% center; }
  .hero-form { max-width: 460px; }
}
</style>
