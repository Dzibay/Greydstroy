<script setup>
import CompanyLogo from './ui/CompanyLogo.vue'
</script>

<template>
  <footer class="ftr">
    <div class="container ftr-in">
      <div class="ftr-brand">
        <RouterLink to="/" class="logo">
          <CompanyLogo variant="light" />
        </RouterLink>
        <p class="ftr-desc">
          Изготовление металлоконструкций: резка, гибка, сварка.
          Дзержинск, Нижегородская область — отгрузка по всей России.
        </p>
      </div>

      <nav class="ftr-nav" aria-label="Разделы сайта">
        <p class="ftr-h">Разделы</p>
        <RouterLink to="/metallokonstruktsii">Металлоконструкции</RouterLink>
        <RouterLink to="/uslugi">Услуги</RouterLink>
        <RouterLink to="/projects">Объекты</RouterLink>
        <RouterLink to="/dostavka">Доставка</RouterLink>
        <RouterLink to="/rekvizity">Реквизиты</RouterLink>
        <RouterLink to="/kontakty">Контакты</RouterLink>
      </nav>

      <div class="ftr-contacts">
        <p class="ftr-h">Контакты</p>
        <a href="tel:+79056646665" class="ftr-phone" data-track="tel-footer">+7 (905) 664-66-65</a>
        <a href="mailto:greydstroy@yandex.ru" data-track="mail-footer">greydstroy@yandex.ru</a>
        <p class="ftr-addr">Нижегородская область, г. Дзержинск<br />дорога Заревская объездная, д. 9В</p>
      </div>

      <div class="ftr-cta">
        <p class="ftr-h">Расчёт заказа</p>
        <p class="ftr-cta-text">Пришлите чертёж или опишите задачу — ответим в течение рабочего дня.</p>
        <RouterLink to="/kalkulyator" class="btn" data-track="calc-footer">Рассчитать стоимость</RouterLink>
      </div>
    </div>

    <div class="container ftr-bottom">
      <p>© {{ new Date().getFullYear() }} ООО «Грэйдстрой» · Все права защищены</p>
      <a href="/docs/privacy-policy.html" target="_blank" rel="noopener">Политика обработки персональных данных</a>
    </div>
  </footer>
</template>

<style scoped>
.ftr {
  background: #07090b;
  border-top: 1px solid var(--line-d);
  padding: 72px 0 0;
}

.ftr-in {
  display: grid;
  grid-template-columns: 1.3fr 0.8fr 1fr 1.1fr;
  gap: 44px;
  padding-bottom: 56px;
}

.logo { display: inline-flex; align-items: center; margin-bottom: 20px; }

.ftr-desc { font-size: 13.5px; color: var(--w-faint); max-width: 300px; line-height: 1.7; }

.ftr-h {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 18px;
}

.ftr-nav { display: flex; flex-direction: column; }
.ftr-nav a {
  font-size: 14px;
  color: var(--w-soft);
  padding: 5px 0;
  transition: color 0.2s;
}
.ftr-nav a:hover { color: var(--white); }

.ftr-contacts { display: flex; flex-direction: column; gap: 8px; }
.ftr-contacts a { color: var(--w-soft); font-size: 14px; transition: color 0.2s; }
.ftr-contacts a:hover { color: var(--white); }
.ftr-phone {
  font-family: var(--font-m);
  font-size: clamp(13px, 1.1vw + 0.55rem, 17px) !important;
  font-weight: 600;
  color: var(--white) !important;
  white-space: nowrap;
}
.ftr-phone:hover { color: var(--acc-hot) !important; }
.ftr-addr { font-size: 13px; color: var(--w-faint); line-height: 1.7; margin-top: 6px; }

.ftr-cta-text { font-size: 13.5px; color: var(--w-faint); margin-bottom: 18px; line-height: 1.7; }

.ftr-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  border-top: 1px solid var(--line-d);
  padding-top: 24px;
  padding-bottom: 28px;
  font-family: var(--font-m);
  font-size: 11.5px;
  color: var(--w-faint);
}
.ftr-bottom a { color: var(--w-faint); text-decoration: underline; }
.ftr-bottom a:hover { color: var(--white); }

@media (max-width: 960px) {
  .ftr-in { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .ftr-in { grid-template-columns: 1fr; gap: 36px; }
}
</style>
