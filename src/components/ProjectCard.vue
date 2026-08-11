<script setup>
import ProjectMedia from './ProjectMedia.vue'

defineProps({
  project: { type: Object, required: true },
  revealDelay: { type: Number, default: 0 },
})

function formatPeriod(p) {
  return `${p.dateStart} — ${p.dateEnd}`
}
</script>

<template>
  <RouterLink
    :to="`/projects/${project.id}`"
    class="card case-card"
    v-reveal="revealDelay"
  >
    <div class="case-photo-wrap">
      <ProjectMedia
        :title="project.title"
        :images="project.images"
        variant="card"
        :alt="project.title"
      />
      <span v-if="project.status === 'ongoing'" class="case-status">В работе</span>
    </div>
    <div class="case-body">
      <p class="case-meta">
        {{ project.location }} · {{ formatPeriod(project) }}
      </p>
      <h3>{{ project.title }}</h3>
      <p class="case-client">{{ project.client }}</p>
      <p class="case-cost">{{ project.cost }} ₽</p>
      <span class="case-link">Подробнее о проекте →</span>
    </div>
  </RouterLink>
</template>

<style scoped>
.case-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease);
}
.case-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(18, 22, 27, 0.12);
}
.case-card:hover :deep(.project-media img) {
  transform: scale(1.04);
}

.case-photo-wrap {
  position: relative;
}

.case-status {
  position: absolute;
  top: 14px;
  right: 14px;
  z-index: 2;
  padding: 5px 12px;
  border-radius: 999px;
  background: var(--acc);
  color: #fff;
  font-family: var(--font-m);
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.case-body { padding: 24px 26px 28px; }

.case-meta {
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 10px;
  line-height: 1.4;
}
.case-body h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
  line-height: 1.35;
}
.case-client {
  font-size: 13px;
  color: var(--ink-faint);
  margin-bottom: 12px;
  line-height: 1.45;
}
.case-cost {
  font-family: var(--font-m);
  font-size: 14px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 16px;
}
.case-link {
  font-size: 13px;
  font-weight: 700;
  color: var(--acc);
  transition: color 0.2s;
}
.case-card:hover .case-link { color: var(--acc-hot); }
</style>
