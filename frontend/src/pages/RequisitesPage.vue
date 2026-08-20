<script setup>
import { ref } from 'vue'
import { company, requisiteGroups } from '../data/company'

const copied = ref(false)

const fullText = [
  company.legalName,
  `ИНН ${company.inn} / КПП ${company.kpp}`,
  `ОГРН ${company.ogrn}`,
  `Юридический адрес: ${company.legalAddress}`,
  `Почтовый адрес: ${company.postalAddress}`,
  `Телефон: ${company.phone}`,
  `E-mail: ${company.email}`,
  `Р/с ${company.bank.account}`,
  company.bank.name,
  `БИК ${company.bank.bik}`,
  `К/с ${company.bank.corrAccount}`,
].join('\n')

async function copyAll() {
  try {
    await navigator.clipboard.writeText(fullText)
    copied.value = true
    setTimeout(() => (copied.value = false), 2200)
  } catch {
    /* клипборд недоступен — кнопка просто не сработает */
  }
}
</script>

<template>
  <main>
    <section id="requisites-hero" class="sec sec--dark page-hero">
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Документы</span> Реквизиты</p>
          <h1 class="page-title">Реквизиты <em>ООО «Грэйдстрой»</em></h1>
          <p class="page-desc">
            Карточка предприятия для договора, счёта и бухгалтерии.
            Можно скопировать всё одной кнопкой.
          </p>
        </div>
        <button type="button" class="btn req-copy" @click="copyAll" v-reveal="100">
          {{ copied ? 'Скопировано ✓' : 'Скопировать реквизиты' }}
        </button>
      </div>
    </section>

    <section id="requisites" class="sec sec--light req-body">
      <div class="container">
        <div class="req-grid">
          <section
            v-for="(group, gi) in requisiteGroups"
            :key="group.title"
            :id="group.id"
            class="card req-card"
            v-reveal="gi * 90"
          >
            <h2>{{ group.title }}</h2>
            <dl>
              <div v-for="row in group.rows" :key="row.label" class="req-row">
                <dt>{{ row.label }}</dt>
                <dd :class="{ mono: row.mono }">
                  <a v-if="row.href" :href="row.href">{{ row.value }}</a>
                  <template v-else>{{ row.value }}</template>
                </dd>
              </div>
            </dl>
          </section>
        </div>

        <div class="req-cta" v-reveal="120">
          <p>Нужен счёт или договор? Пришлите заявку — подготовим документы вместе с расчётом.</p>
          <RouterLink to="/kalkulyator" class="btn">Рассчитать заказ</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-hero { padding-bottom: 80px; }
.req-copy { margin-top: -20px; }

.req-body { padding-top: 72px; }

.req-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}
.req-card:last-child { grid-column: 1 / -1; }
.req-card:hover { transform: none; }

.req-card h2 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--line-l);
}

.req-row {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 16px;
  padding: 11px 0;
  border-bottom: 1px dashed var(--line-l);
}
.req-row:last-child { border-bottom: none; }

.req-row dt {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-faint);
  padding-top: 3px;
}
.req-row dd {
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.55;
}
.req-row dd.mono { font-family: var(--font-m); letter-spacing: 0.03em; }
.req-row dd a { color: var(--acc); }
.req-row dd a:hover { color: var(--acc-hot); }

.req-cta {
  margin-top: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding: 28px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
}
.req-cta p { font-size: 16px; font-weight: 600; color: var(--ink); max-width: 560px; }

@media (max-width: 900px) {
  .req-grid { grid-template-columns: 1fr; }
  .req-row { grid-template-columns: 1fr; gap: 4px; }
}
</style>
