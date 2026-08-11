export function extractDigits(value) {
  return String(value ?? '').replace(/\D/g, '')
}

/** Нормализует российский номер к 11 цифрам: 7XXXXXXXXXX */
export function normalizeRuPhone(value) {
  let digits = extractDigits(value)
  if (!digits) return ''

  // +7 в поле + вставка 89… → 789… — убираем лишнюю семёрку
  while (digits.length > 11 && digits.startsWith('78')) {
    digits = digits.slice(1)
  }

  // 8XXXXXXXXXX → 7XXXXXXXXXX
  if (digits[0] === '8') {
    digits = '7' + digits.slice(1)
  }

  if (digits[0] === '7') {
    return digits.slice(0, 11)
  }

  // 10 цифр без кода страны
  return ('7' + digits).slice(0, 11)
}

/** Форматирует номер: +7 (999) 123-45-67 */
export function formatRuPhone(value) {
  const digits = normalizeRuPhone(value)
  if (!digits) return ''
  if (digits === '7') return '+7'

  const local = digits.slice(1)
  let out = '+7'
  if (local.length > 0) out += ` (${local.slice(0, 3)}`
  if (local.length >= 3) out += ')'
  if (local.length > 3) out += ` ${local.slice(3, 6)}`
  if (local.length > 6) out += `-${local.slice(6, 8)}`
  if (local.length > 8) out += `-${local.slice(8, 10)}`
  return out
}

export function isValidRuPhone(value) {
  const digits = normalizeRuPhone(value)
  return digits.length === 11 && digits.startsWith('7')
}

function digitsBefore(str, pos) {
  return extractDigits(str.slice(0, pos)).length
}

function cursorAfterDigits(formatted, digitCount) {
  if (digitCount <= 1) return 2 // после «+7»
  let seen = 0
  for (let i = 0; i < formatted.length; i++) {
    if (/\d/.test(formatted[i])) {
      seen++
      if (seen === digitCount) return i + 1
    }
  }
  return formatted.length
}

export function applyPhoneInput(input, rawValue) {
  const start = input.selectionStart ?? 0
  const digitPos = digitsBefore(rawValue, start)
  const formatted = formatRuPhone(rawValue)
  return {
    formatted,
    cursor: cursorAfterDigits(formatted, digitPos),
  }
}

/** Вставка: полный номер (10+ цифр) заменяет поле целиком */
export function applyPhonePaste(currentValue, pastedText, selectionStart, selectionEnd) {
  const pastedDigits = extractDigits(pastedText)

  if (pastedDigits.length >= 10) {
    const formatted = formatRuPhone(pastedText)
    return { formatted, cursor: formatted.length }
  }

  const merged =
    currentValue.slice(0, selectionStart) +
    pastedText +
    currentValue.slice(selectionEnd)

  const formatted = formatRuPhone(merged)
  const digitPos = digitsBefore(merged, selectionStart + pastedText.length)
  return {
    formatted,
    cursor: cursorAfterDigits(formatted, digitPos),
  }
}
