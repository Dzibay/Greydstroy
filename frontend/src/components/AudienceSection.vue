<script setup>
const audiences = [
  {
    title: 'Застройщикам и подрядчикам',
    text: 'У вас есть дата сдачи объекта, и металлоконструкции — не единственная головная боль. Возьмём эту часть на себя, вплоть до монтажа в Нижегородской области. Разработаем КМД под ваш КМ или АР.',
    cta: 'Обсудить объект',
    icon: 'building',
  },
  {
    title: 'Производствам',
    text: 'Свой лазер, плазма или листогиб загружены на две недели вперёд? Возьмём часть партии на аутсорс — без потери в качестве и без объяснений вашему клиенту, почему сроки сдвинулись.',
    cta: 'Обсудить заказ',
    icon: 'factory',
  },
  {
    title: 'Частным лицам',
    text: 'Лестница или ограждение, которые не выглядят так, будто их сварил сосед по гаражу. По эскизу или на глаз, без чертежа.',
    cta: 'Обсудить проект',
    icon: 'person',
  },
]
</script>

<template>
  <section id="audience" class="sec sec--dark">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 07</span> Для кого мы работаем</p>
        <h2 class="sec-title">Три типа клиентов. <em>Возможно, один — это вы</em></h2>
      </div>

      <div class="aud-grid">
        <article v-for="(a, i) in audiences" :key="a.title" class="card aud-card" v-reveal="i * 110">
          <span class="aud-icon" aria-hidden="true">
            <svg v-if="a.icon === 'building'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 28V10l9-6v24M14 28V14l13 5v9" /><path d="M3 28h26" />
              <path d="M9 12h1m-1 5h1m-1 5h1m9 1h1m4 2h1" />
            </svg>
            <svg v-else-if="a.icon === 'factory'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 28V13l8 5v-5l8 5v-5l8 5v10z" /><path d="M2 28h28" /><path d="M6 13V5h4v10" />
              <path d="M12 23h2m4 0h2m4 0h2" />
            </svg>
            <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="16" cy="10" r="5" /><path d="M6 28c0-5.5 4.5-9 10-9s10 3.5 10 9" />
            </svg>
          </span>
          <h3>{{ a.title }}</h3>
          <p>{{ a.text }}</p>
          <a href="#cta" class="aud-link">
            {{ a.cta }}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14m-6-6 6 6-6 6" />
            </svg>
          </a>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.aud-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.aud-card {
  display: flex;
  flex-direction: column;
  padding: 34px 30px;
}

.aud-icon {
  width: 60px;
  height: 60px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  margin-bottom: 24px;
  transition: background 0.3s, color 0.3s;
}
.aud-icon svg { width: 32px; height: 32px; }
.aud-card:hover .aud-icon { background: var(--acc); color: #fff; }

.aud-card h3 {
  font-family: var(--font-d);
  font-size: 17px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.25;
  margin-bottom: 14px;
}
.aud-card p {
  font-size: 14.5px;
  color: var(--w-soft);
  flex: 1;
  margin-bottom: 24px;
}

.aud-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  font-size: 14.5px;
  color: var(--acc-hot);
  transition: gap 0.25s var(--ease);
}
.aud-link:hover { gap: 16px; }
.aud-link svg { width: 18px; height: 18px; }

@media (max-width: 900px) {
  .aud-grid { grid-template-columns: 1fr; }
}
</style>
