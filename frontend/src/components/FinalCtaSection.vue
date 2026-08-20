<script setup>
import LeadForm from './ui/LeadForm.vue'

defineProps({
  sectionId: { type: String, default: 'cta' },
})
</script>

<template>
  <section :id="sectionId" class="sec cta">
    <div class="container">
      <div class="cta-grid">
        <div>
          <div class="sec-head cta-head" v-reveal>
            <p class="sec-tag"><span class="idx">/ 15</span> Расчёт заказа</p>
            <h2 class="sec-title">Посчитаем стоимость и сроки <em>под ваш объект</em></h2>
          </div>
          <div class="cta-text" v-reveal="100">
            <p>
              Есть дата сдачи объекта? Отсчитайте от неё в обратную сторону.
              Металлоконструкции — не то, из-за чего должен сдвинуться весь график.
            </p>
            <p>Расчёт бесплатный и ни к чему не обязывает. Отвечаем в течение рабочего дня.</p>
          </div>
          <ul class="cta-points" v-reveal="180">
            <li>Расчёт в течение рабочего дня</li>
            <li>Гарантия: брак по нашим деталям — переделаем бесплатно</li>
            <li>От 1 детали до серийной партии</li>
          </ul>
        </div>

        <div class="cta-form" v-reveal="200">
          <LeadForm extended button-text="Отправить заявку на расчёт">
            Пока не готовы звонить? Оставьте телефон — пришлём ориентир по ценам
            и чек-лист подготовки ТЗ. Без звонков с нашей стороны, обещаем.
          </LeadForm>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta {
  background:
    radial-gradient(900px 500px at 78% 30%, rgba(255, 90, 31, 0.16), transparent 65%),
    var(--bg0);
  color: var(--white);
  --fg: var(--white);
  --fg-soft: var(--w-soft);
  --fg-faint: var(--w-faint);
  --line: var(--line-d);
}
.cta::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--line-d) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-d) 1px, transparent 1px);
  background-size: 72px 72px;
  opacity: 0.3;
}

.cta-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 72px;
  align-items: center;
}

.cta-head { margin-bottom: 26px; }

.cta-text p {
  font-size: 16px;
  color: var(--w-soft);
  margin-bottom: 16px;
  max-width: 520px;
}

.cta-points {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 13px;
}
.cta-points li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 15px;
}
.cta-points li::before {
  content: '✓';
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
  border-radius: 7px;
  background: rgba(255, 90, 31, 0.2);
  color: var(--acc-hot);
  font-size: 12px;
  flex-shrink: 0;
}

.cta-form {
  background: rgba(17, 21, 26, 0.9);
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 34px 30px;
  box-shadow: 0 40px 90px rgba(0, 0, 0, 0.55);
}

@media (max-width: 920px) {
  .cta-grid { grid-template-columns: 1fr; gap: 44px; }
}
</style>
