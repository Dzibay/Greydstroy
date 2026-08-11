<script setup>
const pains = [
  'Подрядчик обещал «к пятнице». Наступила пятница, потом ещё одна — деталь так и не пришла',
  'Замерили — допуск оказался «плюс-минус на глаз». В узел не встало',
  'Отправили аванс. Трубку взяли последний раз в тот же день',
  'На приёмке объекта попросили сертификат на металл — а у подрядчика «его вообще нет, никто раньше не спрашивал»',
  'Чертёж доделывали сами, потому что «мы просто режем то, что дали»',
]
</script>

<template>
  <section class="sec sec--light">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 02</span> Знакомо?</p>
        <h2 class="sec-title">Пять сценариев, которые вы <em>уже видели</em></h2>
      </div>

      <ol class="pains">
        <li v-for="(pain, i) in pains" :key="i" v-reveal="i * 70">
          <span class="p-num">{{ String(i + 1).padStart(2, '0') }}</span>
          <span class="p-x" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round">
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </span>
          <p>{{ pain }}</p>
        </li>
      </ol>

      <p class="pains-outro" v-reveal>
        Ничего из этого — не совпадение. Это следствие того, как устроен процесс
        у конкретного исполнителя. <strong>Наш устроен иначе — дальше по пунктам.</strong>
      </p>
    </div>
  </section>
</template>

<style scoped>
.pains {
  max-width: 860px;
  counter-reset: pain;
}
.pains li {
  display: flex;
  align-items: flex-start;
  gap: 22px;
  padding: 26px 26px 26px 0;
  border-bottom: 1px solid var(--line-l);
  transition: padding-left 0.3s var(--ease), background 0.3s;
}
.pains li:first-child { border-top: 1px solid var(--line-l); }
.pains li:hover {
  padding-left: 14px;
  background: rgba(255, 90, 31, 0.04);
}

.p-num {
  font-family: var(--font-d);
  font-size: 26px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.3px rgba(18, 22, 27, 0.28);
  line-height: 1.2;
  flex-shrink: 0;
  width: 52px;
}
.pains li:hover .p-num { -webkit-text-stroke-color: var(--acc); }

.p-x {
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: rgba(224, 92, 74, 0.12);
  color: var(--bad);
  margin-top: 1px;
}
.p-x svg { width: 16px; height: 16px; }

.pains li p {
  font-size: clamp(15px, 1.5vw, 17.5px);
  font-weight: 500;
  color: var(--ink-soft);
  padding-top: 4px;
}

.pains-outro {
  margin-top: 38px;
  max-width: 720px;
  font-size: clamp(15px, 1.5vw, 17.5px);
  font-style: italic;
  color: var(--ink-soft);
  border-left: 3px solid var(--acc);
  padding-left: 22px;
}
.pains-outro strong { color: var(--ink); }
</style>
