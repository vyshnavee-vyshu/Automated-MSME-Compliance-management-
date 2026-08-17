import { useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, CalendarDays } from 'lucide-react'
import StatusBadge from './StatusBadge'
import EmptyState from './EmptyState'
import { formatDate } from '../utils/formatters'
import {
  getMonthGrid,
  getWeekGrid,
  getWeekdayLabels,
  isSameDay,
  isSameMonth,
  formatMonthLabel,
  formatWeekRangeLabel,
} from '../utils/calendarUtils'

const VIEWS = ['Month', 'Week', 'List']

export default function Calendar({ events }) {
  const [view, setView] = useState('Month')
  const [referenceDate, setReferenceDate] = useState(new Date())

  const eventsByDay = useMemo(() => {
    const map = new Map()
    events.forEach((event) => {
      if (!event.due_date) return
      const key = new Date(event.due_date).toDateString()
      if (!map.has(key)) map.set(key, [])
      map.get(key).push(event)
    })
    return map
  }, [events])

  const getEventsForDay = (day) => eventsByDay.get(day.toDateString()) || []

  const goToPrevious = () => {
    const next = new Date(referenceDate)
    if (view === 'Week') next.setDate(next.getDate() - 7)
    else next.setMonth(next.getMonth() - 1)
    setReferenceDate(next)
  }

  const goToNext = () => {
    const next = new Date(referenceDate)
    if (view === 'Week') next.setDate(next.getDate() + 7)
    else next.setMonth(next.getMonth() + 1)
    setReferenceDate(next)
  }

  const goToToday = () => setReferenceDate(new Date())

  const monthDays = useMemo(
    () => getMonthGrid(referenceDate.getFullYear(), referenceDate.getMonth()),
    [referenceDate],
  )
  const weekDays = useMemo(() => getWeekGrid(referenceDate), [referenceDate])
  const today = new Date()

  return (
    <div className="card overflow-hidden">
      <div className="flex flex-col gap-4 border-b border-navy-100 px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div className="flex items-center gap-3">
          {view !== 'List' && (
            <div className="flex items-center gap-1">
              <button
                onClick={goToPrevious}
                aria-label="Previous"
                className="rounded-md p-1.5 text-navy-500 hover:bg-navy-50"
              >
                <ChevronLeft size={17} />
              </button>
              <button
                onClick={goToNext}
                aria-label="Next"
                className="rounded-md p-1.5 text-navy-500 hover:bg-navy-50"
              >
                <ChevronRight size={17} />
              </button>
            </div>
          )}
          <h2 className="text-[15px] font-semibold text-navy-900">
            {view === 'Month' && formatMonthLabel(referenceDate)}
            {view === 'Week' && formatWeekRangeLabel(weekDays)}
            {view === 'List' && 'Upcoming Compliance Events'}
          </h2>
          {view !== 'List' && (
            <button
              onClick={goToToday}
              className="rounded-md border border-navy-200 px-2.5 py-1 text-xs font-medium text-navy-600 hover:bg-navy-50"
            >
              Today
            </button>
          )}
        </div>

        <div className="flex gap-1 rounded-md border border-navy-100 bg-navy-50/60 p-1">
          {VIEWS.map((label) => (
            <button
              key={label}
              onClick={() => setView(label)}
              className={`rounded px-3 py-1.5 text-xs font-medium transition-colors ${
                view === label ? 'bg-white text-navy-900 shadow-subtle' : 'text-navy-500 hover:text-navy-800'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="p-5 sm:p-6">
        {events.length === 0 ? (
          <EmptyState icon={CalendarDays} title="No compliance events available." />
        ) : (
          <>
            {view === 'Month' && (
              <MonthGrid
                days={monthDays}
                referenceDate={referenceDate}
                today={today}
                getEventsForDay={getEventsForDay}
              />
            )}
            {view === 'Week' && (
              <WeekGrid days={weekDays} today={today} getEventsForDay={getEventsForDay} />
            )}
            {view === 'List' && <EventList events={events} />}
          </>
        )}
      </div>
    </div>
  )
}

function MonthGrid({ days, referenceDate, today, getEventsForDay }) {
  return (
    <div>
      <div className="grid grid-cols-7 gap-px overflow-hidden rounded-md border border-navy-100 bg-navy-100">
        {getWeekdayLabels().map((label) => (
          <div key={label} className="bg-navy-50 py-2 text-center text-xs font-medium text-navy-500">
            {label}
          </div>
        ))}
        {days.map((day) => {
          const dayEvents = getEventsForDay(day)
          const inMonth = isSameMonth(day, referenceDate)
          const isToday = isSameDay(day, today)
          return (
            <div
              key={day.toISOString()}
              className={`min-h-[92px] bg-white p-2 ${inMonth ? '' : 'bg-navy-50/40'}`}
            >
              <span
                className={`inline-flex h-6 w-6 items-center justify-center rounded-full text-xs ${
                  isToday
                    ? 'bg-navy-900 font-semibold text-white'
                    : inMonth
                    ? 'text-navy-700'
                    : 'text-navy-300'
                }`}
              >
                {day.getDate()}
              </span>
              <div className="mt-1 space-y-1">
                {dayEvents.slice(0, 2).map((event, i) => (
                  <div
                    key={i}
                    className="truncate rounded bg-navy-50 px-1.5 py-0.5 text-[11px] font-medium text-navy-700"
                    title={event.compliance_name}
                  >
                    {event.compliance_name}
                  </div>
                ))}
                {dayEvents.length > 2 && (
                  <div className="text-[11px] text-navy-400">+{dayEvents.length - 2} more</div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function WeekGrid({ days, today, getEventsForDay }) {
  return (
    <div className="grid grid-cols-1 divide-y divide-navy-100 rounded-md border border-navy-100 sm:grid-cols-7 sm:divide-x sm:divide-y-0">
      {days.map((day) => {
        const dayEvents = getEventsForDay(day)
        const isToday = isSameDay(day, today)
        return (
          <div key={day.toISOString()} className="min-h-[140px] p-3">
            <p className={`text-xs font-medium ${isToday ? 'text-navy-900' : 'text-navy-400'}`}>
              {day.toLocaleDateString('en-IN', { weekday: 'short' })}
            </p>
            <p className={`mt-0.5 text-sm ${isToday ? 'font-semibold text-navy-900' : 'text-navy-600'}`}>
              {day.getDate()}
            </p>
            <div className="mt-2 space-y-1.5">
              {dayEvents.map((event, i) => (
                <div key={i} className="rounded bg-navy-50 px-2 py-1 text-[11px] font-medium text-navy-700">
                  {event.compliance_name}
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

function EventList({ events }) {
  return (
    <div className="divide-y divide-navy-100 rounded-md border border-navy-100">
      {events.map((event, index) => (
        <div key={index} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3.5">
          <div>
            <p className="text-sm font-medium text-navy-900">{event.compliance_name}</p>
            <p className="mt-0.5 text-xs text-navy-400">
              {event.category} &middot; Due {formatDate(event.due_date)}
            </p>
          </div>
          <StatusBadge status={event.status} />
        </div>
      ))}
    </div>
  )
}
