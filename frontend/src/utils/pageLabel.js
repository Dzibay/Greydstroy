import { uslugi } from '../data/uslugi'
import { laserLandings, laserLandingPath } from '../data/lazernayaRezka'
import { metalworkLandings, metalworkLandingPath } from '../data/metallokonstruktsii'
import { projects } from '../data/projects'

const PATH_NAMES = {
  '/': 'Главная',
  '/kalkulyator': 'Калькулятор',
  '/uslugi': 'Услуги',
  '/metallokonstruktsii': 'Металлоконструкции',
  '/projects': 'Объекты',
  '/kontakty': 'Контакты',
  '/dostavka': 'Доставка',
  '/rekvizity': 'Реквизиты',
}

for (const u of uslugi) {
  PATH_NAMES[`/uslugi/${u.slug}`] = u.label
}
for (const p of laserLandings) {
  PATH_NAMES[laserLandingPath(p.slug)] = `Лазер · ${p.navLabel}`
}
for (const p of metalworkLandings) {
  PATH_NAMES[metalworkLandingPath(p.slug)] = p.navLabel
}
for (const p of projects) {
  PATH_NAMES[`/projects/${p.id}`] = p.title
}

function humanize(slug) {
  return String(slug || '')
    .split('/')
    .filter(Boolean)
    .pop()
    ?.replace(/-/g, ' ') || ''
}

/** Короткое русское имя страницы для админки и заявок. */
export function pageLabel(path) {
  if (!path) return '—'
  const clean = String(path).split('?')[0] || '/'
  if (PATH_NAMES[clean]) return PATH_NAMES[clean]
  if (clean.startsWith('/uslugi/')) return `Услуга · ${humanize(clean.slice(8))}`
  if (clean.startsWith('/metallokonstruktsii/')) return humanize(clean.slice(21)) || 'Металлоконструкции'
  if (clean.startsWith('/projects/')) return `Объект · ${humanize(clean.slice(10))}`
  return clean
}

export function pagePath(path) {
  if (!path) return ''
  return String(path).split('?')[0] || ''
}
