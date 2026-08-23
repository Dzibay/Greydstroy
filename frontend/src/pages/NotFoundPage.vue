<template>
  <main>
    <section class="nf sec sec--dark">
      <div class="nf-bg" aria-hidden="true">404</div>
      <div class="container nf-in">
        <h1 class="nf-title">Страницы нет</h1>
        <RouterLink to="/" class="btn">На главную</RouterLink>
      </div>
    </section>
  </main>
</template>

<style scoped>
.nf {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 100px 0 72px;
  overflow: hidden;
}

.nf-bg {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-family: var(--font-d);
  font-size: clamp(180px, 48vw, 480px);
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1.5px rgba(255, 90, 31, 0.28);
  pointer-events: none;
  user-select: none;
}

.nf-in {
  position: relative;
  z-index: 1;
  text-align: center;
}

.nf-title {
  font-family: var(--font-d);
  font-size: clamp(22px, 3vw, 32px);
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 28px;
}

@media (max-width: 560px) {
  .nf-bg { -webkit-text-stroke-width: 1px; }
}
</style>
