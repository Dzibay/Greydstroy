<script setup>
import { ref, computed } from 'vue'
import ProjectMedia from './ProjectMedia.vue'

const props = defineProps({
  title: { type: String, required: true },
  images: { type: Array, default: () => [] },
})

const selected = ref(0)

const mainImages = computed(() => {
  if (!props.images.length) return []
  const idx = Math.min(selected.value, props.images.length - 1)
  return [props.images[idx]]
})
</script>

<template>
  <div class="project-gallery" v-reveal>
    <figure class="project-gallery-main">
      <ProjectMedia
        :title="title"
        :images="mainImages"
        variant="hero"
        :alt="title"
      />
    </figure>
    <div v-if="images.length > 1" class="project-gallery-thumbs">
      <button
        v-for="(src, i) in images"
        :key="src"
        type="button"
        class="project-gallery-thumb"
        :class="{ active: i === selected }"
        @click="selected = i"
      >
        <img :src="src" :alt="`${title} — фото ${i + 1}`" loading="lazy" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.project-gallery {
  display: grid;
  gap: 16px;
}

.project-gallery-main {
  margin: 0;
}

.project-gallery-thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.project-gallery-thumb {
  border: 2px solid transparent;
  border-radius: var(--r-sm);
  overflow: hidden;
  padding: 0;
  background: none;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s;
}
.project-gallery-thumb:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--acc) 40%, transparent);
}
.project-gallery-thumb.active {
  border-color: var(--acc);
}

.project-gallery-thumb img {
  width: 100%;
  height: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  display: block;
}
</style>
