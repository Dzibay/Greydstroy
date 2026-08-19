import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import ProjectsListPage from '../pages/ProjectsListPage.vue'
import UslugiPage from '../pages/UslugiPage.vue'
import ProjectPage from '../pages/ProjectPage.vue'
import ContactsPage from '../pages/ContactsPage.vue'
import DeliveryPage from '../pages/DeliveryPage.vue'
import RequisitesPage from '../pages/RequisitesPage.vue'
import { getProjectById } from '../data/projects'
import { applyPageMeta } from '../utils/meta'

// Скрытый путь админки: не упоминается в навигации, sitemap и robots.
export const ADMIN_PATH = '/gs-panel-x7k2m9'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    {
      path: '/uslugi',
      name: 'uslugi',
      component: UslugiPage,
      meta: {
        title: 'Услуги резки, гибки и сварки металла — Грэйдстрой | Дзержинск',
        description:
          'Услуги металлообработки для изготовления металлоконструкций: лазерная резка до 20 мм, плазменная до 50 мм, гибка на ЧПУ-листогибе до 3000 мм, сварка MIG/TIG. Расчёт за 1 рабочий день, отгрузка по всей России.',
      },
    },
    {
      path: '/projects',
      name: 'projects',
      component: ProjectsListPage,
      meta: {
        title: 'Металлоконструкции для крупных объектов — проекты Грэйдстрой | Дзержинск',
        description:
          'Реализованные и текущие контракты ООО «Грэйдстрой»: металлоконструкции для промышленных комплексов, складов, муниципальных объектов. Изготовление, резка, гибка, сварка.',
      },
    },
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
      path: '/kontakty',
      name: 'contacts',
      component: ContactsPage,
      meta: {
        title: 'Контакты — Грэйдстрой | Металлоконструкции в Дзержинске',
        description:
          'Контакты ООО «Грэйдстрой»: +7 (905) 664-66-65, greydstroy@yandex.ru. Производство металлоконструкций: г. Дзержинск, дорога Заревская объездная, д. 9В. Расчёт заказа за 1 рабочий день.',
      },
    },
    {
      path: '/dostavka',
      name: 'delivery',
      component: DeliveryPage,
      meta: {
        title: 'Доставка металлоконструкций по России — Грэйдстрой',
        description:
          'Доставка металлоконструкций и металлоизделий: самовывоз из Дзержинска, свой транспорт по Нижегородской области, СДЭК и Деловые линии по всей России.',
      },
    },
    {
      path: '/rekvizity',
      name: 'requisites',
      component: RequisitesPage,
      meta: {
        title: 'Реквизиты ООО «Грэйдстрой» — ИНН 5249127903',
        description:
          'Реквизиты ООО «Грэйдстрой»: ИНН 5249127903, КПП 524901001, ОГРН 1135249003504. Юридический адрес, банковские реквизиты, телефон и e-mail для документов.',
      },
    },
    {
      path: ADMIN_PATH,
      name: 'admin',
      component: () => import('../pages/AdminLeadsPage.vue'),
      meta: { bare: true, noindex: true, title: 'Панель заявок' },
    },
  ],
  scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  },
})

router.afterEach((to) => {
  applyPageMeta(to)
})

export default router
