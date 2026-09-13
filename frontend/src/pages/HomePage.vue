<script setup>
import HeroSection from '../components/HeroSection.vue'
import QuickCallBanner from '../components/QuickCallBanner.vue'
import PainsSection from '../components/PainsSection.vue'
import ServicesSection from '../components/ServicesSection.vue'
import ProcessSection from '../components/ProcessSection.vue'
import CompareSection from '../components/CompareSection.vue'
import PrecisionSection from '../components/PrecisionSection.vue'
import AudienceSection from '../components/AudienceSection.vue'
import CasesSection from '../components/CasesSection.vue'
import DocsSection from '../components/DocsSection.vue'
import GeoSection from '../components/GeoSection.vue'
import DraftSection from '../components/DraftSection.vue'
import TeamSection from '../components/TeamSection.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import { homeGallery } from '../data/shopPhotos'
</script>

<template>
  <main>
    <HeroSection />
    <div class="qcb-standalone">
      <QuickCallBanner />
    </div>
    <PainsSection />
    <ServicesSection />
    <ProcessSection />
    <CompareSection />
    <PrecisionSection />
    <ShopGallery
      :items="homeGallery"
      tag="/ 07"
      kicker="Цех и объекты"
      title="Железо"
      title-em="с площадки"
      lead="Каркас, раскрой, колонны после грунта, навес в монтаже — не сток из фотобанка."
    />
    <AudienceSection />
    <CasesSection />
    <DocsSection />
    <GeoSection />
    <DraftSection />
    <TeamSection />
    <FaqSection />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
/* Hide standalone banner when it fits inside the hero */
@media (min-width: 1100px) and (min-height: 820px) {
  .qcb-standalone { display: none; }
}
</style>
