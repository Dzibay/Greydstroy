<script setup>
import { useRoute } from 'vue-router'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'
import CallExpertWidget from './components/CallExpertWidget.vue'

const route = useRoute()
</script>

<template>
  <SiteHeader v-if="!route.meta.bare" />
  <RouterView />
  <SiteFooter v-if="!route.meta.bare" />
  <CallExpertWidget v-if="!route.meta.bare" />
</template>
