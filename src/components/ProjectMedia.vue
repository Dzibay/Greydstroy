<script setup>
defineProps({
  title: { type: String, required: true },
  images: { type: Array, default: () => [] },
  variant: { type: String, default: 'card' }, // card | hero | thumb
  alt: { type: String, default: '' },
})

const emit = defineEmits(['error'])
</script>

<template>
  <div
    class="project-media"
    :class="[`project-media--${variant}`, { 'project-media--empty': !images?.length }]"
  >
    <img
      v-if="images?.length"
      :src="images[0]"
      :alt="alt || title"
      loading="lazy"
      decoding="async"
      @error="emit('error')"
    />
    <div v-else class="project-media-placeholder" aria-hidden="true">
      <div class="project-media-placeholder-icon">
        <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M6 38V18l18-10 18 10v20H6Z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
          />
          <path
            d="M18 38V26h12v12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
          />
          <path d="M6 18l18 10 18-10" stroke="currentColor" stroke-width="2" />
        </svg>
      </div>
      <p class="project-media-placeholder-title">{{ title }}</p>
      <p class="project-media-placeholder-note">Фотография объекта скоро появится</p>
    </div>
  </div>
</template>

<style scoped>
.project-media {
  position: relative;
  overflow: hidden;
  background: var(--bg2, #171d24);
}

.project-media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s var(--ease, cubic-bezier(0.22, 1, 0.36, 1));
}

.project-media--card {
  min-height: 180px;
  aspect-ratio: 16 / 10;
}
.project-media--hero {
  min-height: 320px;
  border-radius: var(--r);
  aspect-ratio: 16 / 7;
}
.project-media--thumb {
  min-height: 140px;
  aspect-ratio: 4 / 3;
  border-radius: var(--r-sm);
}

.project-media--empty {
  background:
    linear-gradient(145deg, #1a2028 0%, #12161b 55%, #1e2630 100%);
}

.project-media-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 24px;
  text-align: center;
}

.project-media-placeholder-icon {
  width: 52px;
  height: 52px;
  color: color-mix(in srgb, var(--acc, #ff5a1f) 70%, #fff);
  opacity: 0.85;
}
.project-media-placeholder-icon svg {
  width: 100%;
  height: 100%;
}

.project-media-placeholder-title {
  font-family: var(--font-d);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.35;
  color: color-mix(in srgb, var(--white, #f2f4f6) 85%, transparent);
  max-width: 280px;
}

.project-media-placeholder-note {
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--w-faint, #67717d);
  letter-spacing: 0.04em;
}

/* light section placeholder */
:global(.sec--light) .project-media--empty {
  background:
    linear-gradient(145deg, #eceae5 0%, #e2dfe8 50%, #f3f1ec 100%);
}
:global(.sec--light) .project-media-placeholder-title {
  color: var(--ink-soft, #49525c);
}
:global(.sec--light) .project-media-placeholder-note {
  color: var(--ink-faint, #8b939d);
}
:global(.sec--light) .project-media-placeholder-icon {
  color: color-mix(in srgb, var(--acc, #ff5a1f) 55%, var(--ink, #12161b));
}
</style>
