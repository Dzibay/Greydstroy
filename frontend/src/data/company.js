export const company = {
  legalName: 'Общество с ограниченной ответственностью «Грэйдстрой»',
  shortName: 'ООО «ГРЭЙДСТРОЙ»',
  brand: 'Грэйдстрой',
  inn: '5249127903',
  kpp: '524901001',
  ogrn: '1135249003504',
  legalAddress: '606000, Нижегородская область, г. Дзержинск, дорога Заревская объездная, д. 9В',
  postalAddress: '606000, Нижегородская область, г. Дзержинск, дорога Заревская объездная, д. 9В',
  phone: '+7 (905) 664-66-65',
  phoneHref: 'tel:+79056646665',
  email: 'greydstroy@yandex.ru',
  bank: {
    name: 'ПАО «НБД-БАНК», г. Нижний Новгород',
    bik: '042202705',
    account: '40702810701040028918',
    corrAccount: '30101810400000000705',
  },
  schedule: 'Пн–Пт, 08:00–17:00 (МСК)',
}

export const requisiteGroups = [
  {
    title: 'Общие сведения',
    rows: [
      { label: 'Полное наименование', value: company.legalName },
      { label: 'Сокращённое наименование', value: company.shortName },
      { label: 'ИНН', value: company.inn, mono: true, copy: true },
      { label: 'КПП', value: company.kpp, mono: true, copy: true },
      { label: 'ОГРН', value: company.ogrn, mono: true, copy: true },
    ],
  },
  {
    title: 'Адреса и связь',
    rows: [
      { label: 'Юридический адрес', value: company.legalAddress },
      { label: 'Почтовый адрес', value: company.postalAddress },
      { label: 'Телефон', value: company.phone, mono: true, href: company.phoneHref },
      { label: 'Электронная почта', value: company.email, href: `mailto:${company.email}` },
    ],
  },
  {
    title: 'Банковские реквизиты',
    rows: [
      { label: 'Банк', value: company.bank.name },
      { label: 'БИК', value: company.bank.bik, mono: true, copy: true },
      { label: 'Расчётный счёт', value: company.bank.account, mono: true, copy: true },
      { label: 'Корреспондентский счёт', value: company.bank.corrAccount, mono: true, copy: true },
    ],
  },
]
