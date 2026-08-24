<script setup>
import { projectsByNewest } from '../data/projects'
import ProjectCard from '../components/ProjectCard.vue'
</script>

<template>
  <main class="projects-list-page">
    <section id="projects-hero" class="projects-hero sec sec--dark">
      <div class="container">
        <RouterLink to="/" class="projects-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Реестр</span> Крупные объекты</p>
          <h1 class="projects-title">Металлоконструкции для крупных объектов — <em>проекты ООО «Грэйдстрой»</em></h1>
          <p class="projects-desc">
            Реестр контрактов: химия, нефтехимия, логистика, АПК и муниципальные здания.
            По каждому объекту — задача, состав работ, условия на площадке и формулировка договора.
          </p>
        </div>
      </div>
    </section>

    <section id="projects" class="sec sec--light">
      <div class="container">
        <div class="projects-grid">
          <ProjectCard
            v-for="(project, i) in projectsByNewest"
            :key="project.id"
            :project="project"
            :reveal-delay="i * 40"
          />
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.projects-hero {
  padding-top: 120px;
  padding-bottom: 64px;
}

.projects-back {
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--w-soft);
  margin-bottom: 36px;
  transition: color 0.2s;
}
.projects-back:hover { color: var(--acc-hot); }

.projects-title {
  font-family: var(--font-d);
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 900;
  line-height: 1.15;
  text-transform: uppercase;
  margin-bottom: 16px;
}
.projects-title em {
  font-style: normal;
  color: var(--acc-hot);
}

.projects-desc {
  max-width: 720px;
  font-size: 16px;
  color: var(--w-soft);
  line-height: 1.65;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

@media (max-width: 1060px) {
  .projects-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 760px) {
  .projects-grid { grid-template-columns: 1fr; }
}
</style>
