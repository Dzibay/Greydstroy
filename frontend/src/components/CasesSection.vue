<script setup>
import { computed } from 'vue'
import { projectsByNewest } from '../data/projects'
import ProjectCard from './ProjectCard.vue'

const recentProjects = computed(() => projectsByNewest.slice(0, 3))
</script>

<template>
  <section id="cases" class="sec sec--light">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 08</span> Крупные объекты</p>
        <h2 class="sec-title">Последние проекты <em>ООО «Грэйдстрой»</em></h2>
        <p class="sec-desc">
          Три недавних контракта из реестра — промышленные и коммерческие объекты
          с полным циклом работ.
        </p>
      </div>

      <div class="cases-grid">
        <ProjectCard
          v-for="(project, i) in recentProjects"
          :key="project.id"
          :project="project"
          :reveal-delay="i * 40"
        />
      </div>

      <div class="cases-more" v-reveal="120">
        <RouterLink to="/projects" class="btn btn--ghost">
          Крупные проекты →
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.sec-desc {
  margin-top: 16px;
  max-width: 680px;
  font-size: 15px;
  color: var(--ink-soft);
  line-height: 1.65;
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.cases-more {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

@media (max-width: 1060px) {
  .cases-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 760px) {
  .cases-grid { grid-template-columns: 1fr; }
}
</style>
