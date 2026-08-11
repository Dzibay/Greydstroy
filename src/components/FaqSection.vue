<script setup>
import { ref } from 'vue'

const faq = [
  {
    q: 'Сколько это будет стоить?',
    a: 'Честно — единой цены «за деталь» не существует ни у кого в отрасли, что бы ни было написано на других сайтах. Зависит от металла, толщины, объёма и сложности чертежа. Пришлите ТЗ или опишите задачу — назовём цифру в течение рабочего дня.',
  },
  {
    q: 'Какой минимальный заказ?',
    a: 'От одной детали. Серьёзно — не нужно «натягивать» заказ до минимальной партии, чтобы с вами вообще стали разговаривать.',
  },
  {
    q: 'Какую точность реза вы обеспечиваете?',
    a: 'Под допуск вашего проекта: каждая партия проходит замер перед отгрузкой. Точные цифры по вашей детали назовём в расчёте — они зависят от металла, толщины и способа резки.',
  },
  {
    q: 'У меня нет чертежа — что делать?',
    a: 'Разработаем КМ с нуля или сделаем КМД на основе вашего КМ или АР. Это добавит времени, но не блокирует заказ.',
  },
  {
    q: 'Как происходит оплата?',
    a: 'Официально по договору: фиксируем сумму, сроки и порядок оплаты до начала работ. Закрывающие документы — в полном комплекте.',
  },
  {
    q: 'В какие регионы доставляете?',
    a: 'По всей России — СДЭК, Деловые линии, а также самовывоз и доставка своим транспортом по Нижегородской области.',
  },
  {
    q: 'Что если готовое изделие не устроит по качеству?',
    a: 'Переделаем за свой счёт. Это в договоре — не обещание «на словах».',
  },
  {
    q: 'Какой срок изготовления?',
    a: 'Зависит от объёма и загрузки производства: единичные детали — от 1 дня, серийные партии считаем индивидуально. Точный срок фиксируем в договоре вместе с ценой — и он не «плывёт» по ходу заказа.',
  },
]

const open = ref(0)

function toggle(i) {
  open.value = open.value === i ? -1 : i
}
</script>

<template>
  <section id="faq" class="sec sec--dark">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 14</span> FAQ</p>
        <h2 class="sec-title">Вопросы, которые задают <em>чаще всего</em></h2>
      </div>

      <div class="faq">
        <div
          v-for="(item, i) in faq"
          :key="i"
          class="faq-item"
          :class="{ open: open === i }"
          v-reveal="i * 50"
        >
          <button class="faq-q" @click="toggle(i)" :aria-expanded="open === i">
            <span class="faq-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="faq-title">{{ item.q }}</span>
            <span class="faq-plus" aria-hidden="true"></span>
          </button>
          <div class="faq-a">
            <div class="faq-a-in">
              <p>{{ item.a }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq { max-width: 860px; }

.faq-item {
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  margin-bottom: 10px;
  background: var(--card-d);
  transition: border-color 0.3s;
  overflow: hidden;
}
.faq-item.open { border-color: rgba(255, 90, 31, 0.5); }

.faq-q {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 20px 24px;
  background: none;
  border: none;
  color: var(--white);
  text-align: left;
}

.faq-num {
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--acc);
  flex-shrink: 0;
}
.faq-title {
  flex: 1;
  font-weight: 700;
  font-size: 15.5px;
}

.faq-plus {
  position: relative;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}
.faq-plus::before,
.faq-plus::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 14px;
  height: 2.2px;
  background: var(--acc);
  transform: translate(-50%, -50%);
  transition: transform 0.35s var(--ease);
}
.faq-plus::after { transform: translate(-50%, -50%) rotate(90deg); }
.faq-item.open .faq-plus::after { transform: translate(-50%, -50%) rotate(0deg); }

.faq-a {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.4s var(--ease);
}
.faq-item.open .faq-a { grid-template-rows: 1fr; }
.faq-a-in { overflow: hidden; }
.faq-a-in p {
  padding: 0 24px 22px 66px;
  font-size: 14.5px;
  color: var(--w-soft);
  line-height: 1.65;
}

@media (max-width: 560px) {
  .faq-a-in p { padding-left: 24px; }
}
</style>
