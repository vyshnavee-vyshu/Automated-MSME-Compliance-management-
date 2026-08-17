const STATUS_STYLES = {
  Completed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Upcoming: 'bg-blue-50 text-blue-700 border-blue-200',
  'Due Soon': 'bg-amber-50 text-amber-700 border-amber-200',
  Overdue: 'bg-red-50 text-red-700 border-red-200',
  Critical: 'bg-red-50 text-red-700 border-red-200',
  High: 'bg-amber-50 text-amber-700 border-amber-200',
  Medium: 'bg-blue-50 text-blue-700 border-blue-200',
  Low: 'bg-emerald-50 text-emerald-700 border-emerald-200',
}

export default function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || 'bg-navy-50 text-navy-600 border-navy-200'
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${style}`}
    >
      {status}
    </span>
  )
}
