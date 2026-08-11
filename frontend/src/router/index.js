import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import ProjectsListPage from '../pages/ProjectsListPage.vue'
import ProjectPage from '../pages/ProjectPage.vue'
import { getProjectById } from '../data/projects'

// Скрытый путь админки: не упоминается в навигации, sitemap и robots.
export const ADMIN_PATH = '/gs-panel-x7k2m9'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/projects', name: 'projects', component: ProjectsListPage },
    {
      path: '/projects/:id',
      name: 'project',
      component: ProjectPage,
      props: true,
      beforeEnter: (to) => {
        if (!getProjectById(to.params.id)) return { name: 'home' }
      },
    },
    {
      path: ADMIN_PATH,
      name: 'admin',
      component: () => import('../pages/AdminLeadsPage.vue'),
      meta: { bare: true },
    },
  ],
  scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  },
})

export default router
