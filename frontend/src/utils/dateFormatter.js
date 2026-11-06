/**
 * Centralized Indonesian Date and Time Formatter (WIB - Western Indonesian Time)
 * Completely lossless and free of UTC offset shift issues.
 */

export const parseLocalDate = (dateVal) => {
  if (!dateVal) return null
  if (dateVal instanceof Date) return dateVal

  if (typeof dateVal === 'string') {
    // If it has timezone indicator (e.g. Z or +07:00), parse standard
    if (dateVal.includes('Z') || dateVal.includes('+')) {
      return new Date(dateVal)
    }
    // Pure local datetime string (YYYY-MM-DDTHH:mm:ss or YYYY-MM-DD HH:mm:ss)
    // Replace '-' with '/' and 'T' with ' ' for cross-browser local time parsing
    const clean = dateVal.slice(0, 19).replace(/-/g, '/').replace('T', ' ')
    return new Date(clean)
  }

  return new Date(dateVal)
}

export const formatIndonesianDate = (dateVal) => {
  if (!dateVal) return '-'
  const d = parseLocalDate(dateVal)
  if (!d || isNaN(d.getTime())) return '-'

  return new Intl.DateTimeFormat('id-ID', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(d)
}

export const formatIndonesianDateTime = (dateVal, withWib = true) => {
  if (!dateVal) return '-'
  const d = parseLocalDate(dateVal)
  if (!d || isNaN(d.getTime())) return '-'

  const formatted = new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(d)

  // Replace dot with colon (e.g. 18.30 -> 18:30)
  const normalized = formatted.replace(/\./g, ':')
  return withWib ? `${normalized} WIB` : normalized
}

export const formatIndonesianClock = (dateVal = new Date()) => {
  const d = dateVal instanceof Date ? dateVal : parseLocalDate(dateVal)
  if (!d || isNaN(d.getTime())) return ''

  const timeStr = new Intl.DateTimeFormat('id-ID', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(d).replace(/\./g, ':')

  return `${timeStr} WIB`
}

/**
 * Converts stored datetime string to HTML <input type="datetime-local"> value (YYYY-MM-DDTHH:mm)
 * 100% lossless without UTC conversion.
 */
export const toDateTimeLocalValue = (dateVal) => {
  if (!dateVal) return ''
  if (typeof dateVal === 'string' && dateVal.includes('T')) {
    return dateVal.slice(0, 16)
  }
  const d = parseLocalDate(dateVal)
  if (!d || isNaN(d.getTime())) return ''

  const pad = (n) => String(n).padStart(2, '0')
  const year = d.getFullYear()
  const month = pad(d.getMonth() + 1)
  const day = pad(d.getDate())
  const hours = pad(d.getHours())
  const minutes = pad(d.getMinutes())

  return `${year}-${month}-${day}T${hours}:${minutes}`
}

/**
 * Converts HTML <input type="datetime-local"> (YYYY-MM-DDTHH:mm) to API payload string (YYYY-MM-DDTHH:mm:00)
 * directly preserving the local time selected by user without UTC shift.
 */
export const fromDateTimeLocalValue = (localStr) => {
  if (!localStr) return null
  const clean = localStr.trim()
  if (!clean) return null
  if (clean.length === 16) {
    return `${clean}:00`
  }
  return clean
}
