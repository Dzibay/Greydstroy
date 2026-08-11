<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectById } from '../data/projects'
import ProjectGallery from '../components/ProjectGallery.vue'

const route = useRoute()
const project = computed(() => getProjectById(route.params.id))

const period = computed(() => {
  if (!project.value) return ''
  return `${project.value.dateStart} — ${project.value.dateEnd}`
})
</script>

<template>
  <main v-if="project" class="project-page">
    <section class="project-hero sec sec--dark">
      <div class="container">
        <RouterLink to="/projects" class="project-back" v-reveal>
          ← Все объекты
        </RouterLink>

        <div class="project-hero-grid">
          <div class="project-hero-text" v-reveal="60">
            <p class="sec-tag">
              <span class="idx">Объект</span>
              <span v-if="project.status === 'ongoing'" class="project-badge">В работе</span>
            </p>
            <h1 class="project-title">{{ project.title }}</h1>
            <p class="project-client">{{ project.client }}</p>
          </div>

          <div class="project-stats card" v-reveal="120">
            <div class="stat-row">
              <span class="stat-label">Период</span>
              <span class="stat-value">{{ period }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Стоимость</span>
              <span class="stat-value stat-value--acc">{{ project.cost }} ₽</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Локация</span>
              <span class="stat-value">{{ project.location }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Формат</span>
              <span class="stat-value">{{ project.scope }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="sec sec--light project-body">
      <div class="container project-content">
        <ProjectGallery
          :title="project.title"
          :images="project.images"
        />

        <article class="card project-detail" v-reveal="80">
          <h2>Предмет договора</h2>
          <p>{{ project.subject }}</p>

          <template v-if="project.workItems?.length">
            <h3>Выполненные виды работ</h3>
            <ul class="work-list">
              <li v-for="(item, i) in project.workItems" :key="i">{{ item }}</li>
            </ul>
          </template>
        </article>

        <div class="project-cta" v-reveal="120">
          <p>Нужен расчёт на аналогичный объект?</p>
          <RouterLink to="/#cta" class="btn">Рассчитать заказ</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.project-hero { padding-top: 120px; padding-bottom: 80px; }

.project-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--w-soft);
  margin-bottom: 36px;
  transition: color 0.2s;
}
.project-back:hover { color: var(--acc-hot); }

.project-hero-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 32px;
  align-items: start;
}

.project-badge {
  margin-left: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  font-family: var(--font-m);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.project-title {
  font-family: var(--font-d);
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 900;
  line-height: 1.15;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.project-client {
  font-size: 16px;
  color: var(--w-soft);
  max-width: 640px;
}

.project-stats {
  padding: 28px 30px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.stat-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line-d);
}
.stat-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.stat-label {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-faint);
}

.stat-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--white);
  line-height: 1.45;
}
.stat-value--acc {
  font-family: var(--font-m);
  color: var(--acc-hot);
}

.project-content {
  display: grid;
  gap: 28px;
}

.project-detail {
  padding: 36px 40px;
}
.project-detail h2 {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 16px;
}
.project-detail h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin: 28px 0 14px;
}
.project-detail p {
  font-size: 16px;
  color: var(--ink-soft);
  line-height: 1.7;
}

.work-list {
  display: grid;
  gap: 10px;
}
.work-list li {
  position: relative;
  padding-left: 22px;
  font-size: 15px;
  color: var(--ink-soft);
  line-height: 1.55;
}
.work-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 9px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--acc);
}

.project-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  padding: 28px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
}
.project-cta p {
  font-size: 16px;
  font-weight: 600;
  color: var(--ink);
}

@media (max-width: 900px) {
  .project-hero-grid { grid-template-columns: 1fr; }
  .project-detail { padding: 28px 24px; }
}
</style>
