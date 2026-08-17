const WEEKDAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export function getWeekdayLabels() {
  return WEEKDAY_LABELS
}

/**
 * Builds a 6x7 grid of dates for the given month, including
 * leading/trailing days from adjacent months for alignment.
 */
export function getMonthGrid(year, month) {
  const firstOfMonth = new Date(year, month, 1)
  const startOffset = firstOfMonth.getDay()
  const gridStart = new Date(year, month, 1 - startOffset)

  const days = []
  for (let i = 0; i < 42; i += 1) {
    const date = new Date(gridStart)
    date.setDate(gridStart.getDate() + i)
    days.push(date)
  }
  return days
}

export function getWeekGrid(referenceDate) {
  const startOffset = referenceDate.getDay()
  const weekStart = new Date(referenceDate)
  weekStart.setDate(referenceDate.getDate() - startOffset)

  const days = []
  for (let i = 0; i < 7; i += 1) {
    const date = new Date(weekStart)
    date.setDate(weekStart.getDate() + i)
    days.push(date)
  }
  return days
}

export function isSameDay(a, b) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  )
}

export function isSameMonth(a, b) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth()
}

export function formatMonthLabel(date) {
  return date.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })
}

export function formatWeekRangeLabel(days) {
  if (days.length === 0) return ''
  const start = days[0]
  const end = days[days.length - 1]
  const startLabel = start.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
  const endLabel = end.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
  return `${startLabel} - ${endLabel}`
}
