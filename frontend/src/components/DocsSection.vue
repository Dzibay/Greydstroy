<script setup>
const docs = [
  {
    title: 'Лицензии компании',
    text: 'Пришлём копии по первому запросу, не через неделю «уточню у бухгалтерии»',
    icon: 'license',
  },
  {
    title: 'Паспорт на изделие',
    text: 'Сертификат качества на каждое изделие — пригодится на приёмке объекта или входном контроле у вас на производстве',
    icon: 'passport',
  },
  {
    title: 'Официальная оплата по договору',
    text: 'Сумма, сроки и порядок оплаты фиксируем в договоре до запуска в производство — с полным пакетом закрывающих документов',
    icon: 'payment',
  },
  {
    title: 'Гарантия на детали',
    text: 'Если брак наш — переделаем бесплатно, без лишней переписки',
    icon: 'shield',
  },
]
</script>

<template>
  <section class="sec sec--dark sec--deep">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 09</span> Документы и оплата</p>
        <h2 class="sec-title">Документы, которые не придётся <em>выпрашивать</em></h2>
      </div>

      <div class="docs-grid">
        <article v-for="(d, i) in docs" :key="d.title" class="docs-item" v-reveal="i * 90">
          <span class="docs-icon" aria-hidden="true">
            <svg v-if="d.icon === 'license'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 3h12l6 6v20H8z" /><path d="M20 3v6h6" /><path d="M12 15h8m-8 5h8m-8-10h3" />
            </svg>
            <svg v-else-if="d.icon === 'passport'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="6" y="4" width="20" height="24" rx="2" /><circle cx="16" cy="13" r="4" />
              <path d="M11 22h10" />
            </svg>
            <svg v-else-if="d.icon === 'payment'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="8" width="26" height="17" rx="2.5" /><path d="M3 14h26" /><path d="M8 20h6" />
            </svg>
            <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 3 6 7v8c0 7 4.5 11.5 10 14 5.5-2.5 10-7 10-14V7z" /><path d="m11.5 16 3 3 6-6" />
            </svg>
          </span>
          <h3>{{ d.title }}</h3>
          <p>{{ d.text }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.docs-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  overflow: hidden;
}

.docs-item {
  padding: 36px 30px;
  background: var(--card-d);
  transition: background 0.3s;
  position: relative;
}
.docs-item + .docs-item { border-left: 1px solid var(--line-d); }
.docs-item:hover { background: var(--bg2); }
.docs-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--acc);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s var(--ease);
}
.docs-item:hover::before { transform: scaleX(1); }

.docs-icon {
  display: inline-grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 13px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  margin-bottom: 22px;
}
.docs-icon svg { width: 28px; height: 28px; }

.docs-item h3 {
  font-family: var(--font-d);
  font-size: 14.5px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.3;
  margin-bottom: 12px;
}
.docs-item p { font-size: 13.5px; color: var(--w-soft); }

@media (max-width: 980px) {
  .docs-grid { grid-template-columns: 1fr 1fr; }
  .docs-item:nth-child(3) { border-left: none; }
  .docs-item:nth-child(n + 3) { border-top: 1px solid var(--line-d); }
}
@media (max-width: 560px) {
  .docs-grid { grid-template-columns: 1fr; }
  .docs-item { border-left: none !important; }
  .docs-item + .docs-item { border-top: 1px solid var(--line-d); }
}
</style>
